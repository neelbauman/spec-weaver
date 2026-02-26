# src/spec_weaver/doorstop.py

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Set, Dict, Optional

import doorstop


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

def get_item_map(repo_root: Path) -> Dict[str, Any]:
    """
    DoorstopのTreeから、すべてのドキュメントのアクティブなアイテムを取得します。
    """
    original_cwd = os.getcwd()
    os.chdir(repo_root)
    
    try:
        tree = doorstop.build()
        item_map: Dict[str, Any] = {}

        for doc in tree:
            # prefixでのフィルタリングを削除し、全ドキュメントを対象にする
            for item in doc:
                if item.active:
                    item_map[str(item.uid)] = item

        return item_map
    finally:
        os.chdir(original_cwd)

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
        if mode == "first":
            cmd = ["git", "log", "--follow", "--format=%aI", "--diff-filter=A", "--", file_path]
        else:
            cmd = ["git", "log", "-1", "--format=%aI", "--", file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            line = result.stdout.strip().splitlines()[0]
            return line[:10]  # YYYY-MM-DD
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def is_suspect(item: Any) -> bool:
    """後方互換ラッパー: いずれかの警告がある場合 True を返す。"""
    return get_item_warnings(item).has_any_warning

def get_doorstop_tree(repo_root: Path):
    """Doorstopのツリーオブジェクトをそのまま返す（ドキュメント階層の走査用）。"""
    original_cwd = os.getcwd()
    os.chdir(repo_root)
    try:
        return doorstop.build()
    finally:
        os.chdir(original_cwd)


def get_all_prefixes(repo_root: Path) -> Set[str]:
    """Doorstopのツリーからすべてのドキュメントプレフィックスを取得します。"""
    tree = get_doorstop_tree(repo_root)
    return {str(doc.prefix) for doc in tree}


def get_all_items(repo_root: Path) -> Dict[str, Any]:
    """
    リポジトリ内の全ドキュメントから全アイテムを取得し、
    親子関係（リンク）を含めたマップを作成します。
    """
    original_cwd = os.getcwd()
    os.chdir(repo_root)
    try:
        tree = doorstop.build()
        all_items: Dict[str, Any] = {}
        for doc in tree:
            for item in doc:
                if item.active:
                    all_items[str(item.uid)] = item
        return all_items
    finally:
        os.chdir(original_cwd)
