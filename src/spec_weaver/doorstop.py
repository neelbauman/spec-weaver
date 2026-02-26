# src/spec_weaver/doorstop.py

import os
from pathlib import Path
from typing import Any, Set, Dict

import doorstop

def get_specs(repo_root: Path, prefix: str = "SPEC") -> Set[str]:
    """監査用：アクティブな仕様IDの集合を取得します。"""
    item_map = get_item_map(repo_root)
    return set(item_map.keys())

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
                    item_map[item.uid] = item
                            
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
                    all_items[item.uid] = item
        return all_items
    finally:
        os.chdir(original_cwd)
