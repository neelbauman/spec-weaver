# src/spec_weaver/doorstop.py

import os
from pathlib import Path
from typing import Any, Set, Dict, Optional

import doorstop

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

def is_suspect(item: Any) -> bool:
    """
    指定されたDoorstopアイテムがSuspect状態（上位要件の変更に伴うレビュー待ち）か判定します。
    """
    try:
        # アイテム自体がsuspectフラグを持っている場合
        if getattr(item, "suspect", False):
            return True
        # リンク先のいずれかがsuspect状態の場合
        for link in getattr(item, "links", []):
            if getattr(link, "suspect", False):
                return True
        return False
    except Exception:
        return False

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
