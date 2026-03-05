# src/spec_weaver/doorstop.py
# implements: TRC-002

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Set, Dict, List, Optional

import doorstop

# get_ref_files は impl_scanner に実装し、ここから re-export する
from spec_weaver.adapters.impl_scanner import get_ref_files as get_ref_files  # noqa: F401


# ---------------------------------------------------------------------------
# 複数ルート対応
# ---------------------------------------------------------------------------


class MultiTree:
    """複数のルートドキュメントツリーを束ねるコンテナ。

    doorstop.Tree は単一ルートを前提としているため、複数ルートが存在する
    プロジェクトでは DoorstopError が発生する。本クラスはルートごとに
    独立した Tree を保持し、ドキュメント列挙・アイテム検索を統合する。
    """

    def __init__(self, trees: List) -> None:
        self._trees = trees

    @property
    def trees(self) -> List:
        return self._trees

    def __iter__(self):
        for tree in self._trees:
            yield from tree

    def find_item(self, item_id: str) -> Any:
        """複数ツリーをまたいでアイテムを検索する。"""
        for tree in self._trees:
            try:
                item = tree.find_item(item_id)
                if item:
                    return item
            except Exception:
                pass
        return None


def _build_all_trees(repo_root: Path) -> List:
    """複数ルートドキュメントに対応したツリービルダー。

    doorstop.build() はルートが1つしかないことを前提とし、複数ルートが
    存在すると DoorstopError("multiple root documents") を送出する。
    本関数はルートごとに Tree を独立して構築し、List[Tree] として返す。
    単一ルートの場合は [Tree] を返す（既存動作と同一）。

    Args:
        repo_root: Doorstop ドキュメントを探索するリポジトリルートパス。

    Returns:
        Tree オブジェクトのリスト（ルートドキュメントごとに1つ）。
    """
    from doorstop.core.builder import _document_from_path
    from doorstop.common import DoorstopError

    documents: list = []
    root_str = str(repo_root)
    skip_file_name = ".doorstop.skip-all"
    exclude_dirnames = {".git", ".tox", ".venv", "venv"}

    if not os.path.isfile(os.path.join(root_str, skip_file_name)):
        _document_from_path(root_str, root_str, documents)

    if not os.path.isfile(os.path.join(root_str, skip_file_name)):
        for dirpath, dirnames, _ in os.walk(root_str, topdown=True):
            whitelist: list = []
            for dirname in dirnames:
                if dirname in exclude_dirnames:
                    continue
                path = os.path.join(dirpath, dirname)
                if os.path.isfile(os.path.join(path, skip_file_name)):
                    continue
                whitelist.append(dirname)
                _document_from_path(path, root_str, documents)
            dirnames[:] = whitelist

    if not documents:
        return [doorstop.Tree(document=None, root=root_str)]

    root_docs = [doc for doc in documents if doc.parent is None]
    if not root_docs:
        raise DoorstopError("no root document")

    if len(root_docs) == 1:
        return [doorstop.Tree.from_list(documents, root=root_str)]

    # 複数ルート: ルートごとにサブツリーを構築
    trees = []
    for root_doc in root_docs:
        placed = {root_doc.prefix.lower()}
        subtree_docs = [root_doc]

        changed = True
        while changed:
            changed = False
            for doc in documents:
                if doc.parent is None:
                    continue
                if doc.prefix.lower() in placed:
                    continue
                if doc.parent.lower() in placed:
                    subtree_docs.append(doc)
                    placed.add(doc.prefix.lower())
                    changed = True

        trees.append(doorstop.Tree.from_list(subtree_docs, root=root_str))

    return trees


# ---------------------------------------------------------------------------
# バリデーション警告
# ---------------------------------------------------------------------------


@dataclass
class ItemWarnings:
    """Doorstop バリデーション警告"""

    has_suspect_links: bool = False
    has_unreviewed_changes: bool = False
    suspect_link_targets: list[str] = field(default_factory=list)
    has_suspect_children: bool = False
    suspect_children: list[str] = field(default_factory=list)
    broken_links: list[str] = field(default_factory=list)

    @property
    def has_any_warning(self) -> bool:
        return (
            self.has_suspect_links
            or self.has_unreviewed_changes
            or self.has_suspect_children
            or bool(self.broken_links)
        )


def get_item_warnings(
    item: Any, multi_tree: Optional["MultiTree"] = None, child_index: Optional[Dict[str, List[Any]]] = None
) -> ItemWarnings:
    w = ItemWarnings()
    try:
        if not getattr(item, "reviewed", True):
            w.has_unreviewed_changes = True
    except Exception:
        pass

    if multi_tree is not None:
        suspects, broken = check_suspect_cross_root(multi_tree, item)
        if suspects:
            w.has_suspect_links = True
            w.suspect_link_targets = suspects
        if broken:
            w.broken_links = broken
    else:
        try:
            if not item.cleared:
                w.has_suspect_links = True
                try:
                    for uid, parent in item._get_parent_uid_and_item():
                        if uid.stamp != parent.stamp():
                            w.suspect_link_targets.append(str(uid))
                except Exception:
                    w.suspect_link_targets = [str(l) for l in getattr(item, "links", [])]
        except Exception:
            pass

    if child_index is not None:
        suspect_children = check_children_suspect(item, child_index)
        if suspect_children:
            w.has_suspect_children = True
            w.suspect_children = suspect_children

    return w


def get_specs(repo_root: Path, prefix: Optional[str] = "SPEC") -> Set[str]:
    """監査用：アクティブな仕様IDの集合を取得します。"""
    item_map = get_item_map(repo_root)
    specs = set()
    for uid, item in item_map.items():
        uid_str = str(uid)
        is_testable = _get_custom_attribute(item, "testable", True)
        if is_testable:
            if prefix is None or uid_str.startswith(prefix):
                specs.add(uid_str)
    return specs


def get_item_map(repo_root: Path, include_inactive: bool = False) -> Dict[str, Any]:
    """
    DoorstopのTreeから、すべてのドキュメントのアイテムを取得します。
    複数ルートドキュメントが存在する場合も全アイテムを返します。

    Args:
        include_inactive: True の場合、active=false のアイテムも含めて返す。
    """
    trees = _build_all_trees(repo_root)
    item_map: Dict[str, Any] = {}

    for tree in trees:
        for doc in tree:
            for item in doc:
                if item.active or include_inactive:
                    item_map[str(item.uid)] = item

    return item_map


def _get_custom_attribute(item: Any, key: str, default: Any = None) -> Any:
    """
    DoorstopのItemは内部的に __getattr__ や get メソッドで
    YAMLのカスタム属性を扱えるようになっています。
    """
    try:
        # Doorstop Itemは .get('key') または .key で属性にアクセス可能
        value = item.get(key)
        return value if value is not None else default
    except AttributeError:
        return getattr(item, key, default)


def _get_git_file_date(file_path: str, mode: str = "latest") -> str | None:
    """Git履歴からファイルの日付を YYYY-MM-DD で取得する。

    mode="latest": 最終コミット日（updated_at 用）
    mode="first":  初回コミット日（created_at 用）
    Git 外や未コミットファイルでは None を返す。
    """
    try:
        cwd = os.path.dirname(os.path.abspath(file_path))
        if mode == "first":
            cmd = [
                "git",
                "log",
                "--follow",
                "--format=%aI",
                "--diff-filter=A",
                "--",
                file_path,
            ]
        else:
            cmd = ["git", "log", "-1", "--format=%aI", "--", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5, cwd=cwd)
        if result.returncode == 0 and result.stdout.strip():
            line = result.stdout.strip().splitlines()[0]
            return line[:10]  # YYYY-MM-DD
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def is_suspect(item: Any) -> bool:
    """後方互換ラッパー: いずれかの警告がある場合 True を返す。"""
    return get_item_warnings(item).has_any_warning


def get_doorstop_tree(repo_root: Path) -> "MultiTree":
    """Doorstopのツリーをドキュメント階層の走査用に返す。

    複数ルートが存在する場合は MultiTree を返す。
    MultiTree はイテレーション・find_item の両方において
    単一の doorstop.Tree と同様に扱える。
    """
    trees = _build_all_trees(repo_root)
    return MultiTree(trees)


def get_all_prefixes(repo_root: Path) -> Set[str]:
    """Doorstopのツリーからすべてのドキュメントプレフィックスを取得します。
    複数ルートドキュメントが存在する場合も全プレフィックスを返します。
    """
    trees = _build_all_trees(repo_root)
    prefixes: Set[str] = set()
    for tree in trees:
        for doc in tree:
            prefixes.add(str(doc.prefix))
    return prefixes


def get_all_items(repo_root: Path) -> Dict[str, Any]:
    """
    リポジトリ内の全ドキュメントから全アイテムを取得し、
    親子関係（リンク）を含めたマップを作成します。
    複数ルートドキュメントが存在する場合も全アイテムを返します。
    """
    trees = _build_all_trees(repo_root)
    all_items: Dict[str, Any] = {}
    for tree in trees:
        for doc in tree:
            for item in doc:
                if item.active:
                    all_items[str(item.uid)] = item
    return all_items


def update_item_attribute(repo_root: Path, item_id: str, key: str, value: Any) -> None:
    """指定したアイテムのカスタム属性を更新し、YAMLに保存します。
    複数ルートが存在する場合も全ツリーを対象に検索します。
    """
    multi_tree = get_doorstop_tree(repo_root)
    item = multi_tree.find_item(item_id)
    if not item:
        raise ValueError(f"Item not found: {item_id}")
    item.set(key, value)
    item.save()


def delete_item_attribute(repo_root: Path, item_id: str, key: str) -> None:
    """指定したアイテムのカスタム属性を削除し、YAMLに保存します。
    複数ルートが存在する場合も全ツリーを対象に検索します。
    """
    multi_tree = get_doorstop_tree(repo_root)
    item = multi_tree.find_item(item_id)
    if not item:
        raise ValueError(f"Item not found: {item_id}")
    if key in item.data:
        del item.data[key]
        item.save()


def clear_doorstop_suspects(repo_root: Path, item_id: str) -> bool:
    """Doorstop ネイティブの suspect リンクを解除します。

    クロスルート対応: item.clear() は同一ツリー内しか検索できないため、
    MultiTree を使って全ツリーからリンク先アイテムを解決してスタンプを更新します。
    suspect リンクが存在し解除された場合は True、それ以外は False を返します。
    """
    multi_tree = get_doorstop_tree(repo_root)
    item = multi_tree.find_item(item_id)
    if not item:
        return False

    # item.cleared / item.clear() は self.tree.find_item() しか使わないため
    # クロスルートリンクを解決できない。直接スタンプを操作する。
    suspect_uids = [uid for uid in item.links if not bool(uid.stamp)]
    if not suspect_uids:
        return False

    for uid in suspect_uids:
        linked = multi_tree.find_item(str(uid))
        if linked:
            uid.stamp = linked.stamp()

    item.save()
    return True

# ---------------------------------------------------------------------------
# Cross-root & Children suspects
# ---------------------------------------------------------------------------

def _build_child_index(multi_tree: "MultiTree") -> Dict[str, List[Any]]:
    index: Dict[str, List[Any]] = {}
    for doc in multi_tree:
        for item in doc:
            if not getattr(item, "active", True):
                continue
            for link_uid in getattr(item, "links", []):
                parent_id = str(link_uid)
                if parent_id not in index:
                    index[parent_id] = []
                index[parent_id].append(item)
    return index

def check_suspect_cross_root(
    multi_tree: "MultiTree", item: Any
) -> tuple[list[str], list[str]]:
    suspect_targets: list[str] = []
    broken_links: list[str] = []
    for link_uid in getattr(item, "links", []):
        parent_id = str(link_uid)
        parent = multi_tree.find_item(parent_id)
        if parent is None:
            broken_links.append(parent_id)
            continue
        if link_uid.stamp != parent.stamp():
            suspect_targets.append(parent_id)
    return suspect_targets, broken_links

def check_children_suspect(
    item: Any, child_index: Dict[str, List[Any]]
) -> list[str]:
    item_id = str(item.uid)
    children = child_index.get(item_id, [])
    if not children:
        return []

    stored_stamps = _get_custom_attribute(item, "child_stamps", {}) or {}
    suspect_children: list[str] = []
    for child in children:
        child_id = str(child.uid)
        stored = stored_stamps.get(child_id)
        if stored is None:
            continue
        current_stamp = child.stamp()
        if str(stored) != str(current_stamp):
            suspect_children.append(child_id)
    return suspect_children

def clear_suspect_cross_root(multi_tree: "MultiTree", item: Any, targets: Optional[Set[str]] = None) -> bool:
    updated = False
    for link_uid in getattr(item, "links", []):
        parent_id = str(link_uid)
        if targets is not None and parent_id not in targets:
            continue
        parent = multi_tree.find_item(parent_id)
        if parent is None:
            continue
        p_stamp = parent.stamp()
        if link_uid.stamp != p_stamp:
            link_uid.stamp = p_stamp
            updated = True
    if updated:
        item.save()
    return updated

def clear_children_stamps(parent: Any, child_index: Dict[str, List[Any]]) -> bool:
    parent_id = str(parent.uid)
    children = child_index.get(parent_id, [])
    if not children:
        return False
    
    stored_stamps = _get_custom_attribute(parent, "child_stamps", {}) or {}
    updated = False
    for child in children:
        child_id = str(child.uid)
        c_stamp = child.stamp()
        if stored_stamps.get(child_id) != str(c_stamp):
            stored_stamps[child_id] = str(c_stamp)
            updated = True
            
    if updated:
        parent.set("child_stamps", stored_stamps)
        parent.save()
    return updated
