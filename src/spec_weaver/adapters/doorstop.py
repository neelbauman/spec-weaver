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

    @property
    def has_any_warning(self) -> bool:
        return self.has_suspect_links or self.has_unreviewed_changes


def get_item_warnings(item: Any) -> ItemWarnings:
    """item.cleared / item.reviewed を使って警告を検出する。

    - cleared == False → 上位リンク先が変更されている (suspect link)
    - reviewed == False → アイテム自身に未レビュー変更がある
    """
    w = ItemWarnings()
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
    try:
        if not item.reviewed:
            w.has_unreviewed_changes = True
    except Exception:
        pass
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

    item.clear() を呼び出して、親アイテムのスタンプを更新します。
    suspect リンクが存在し解除された場合は True、それ以外は False を返します。
    複数ルートが存在する場合も全ツリーを対象に検索します。
    """
    multi_tree = get_doorstop_tree(repo_root)
    item = multi_tree.find_item(item_id)
    if not item:
        return False
    if not item.cleared:
        item.clear()
        item.save()
        return True
    return False
