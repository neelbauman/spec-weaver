from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from spec_weaver.adapters.doorstop import (
    _build_child_index,
    clear_children_stamps,
    get_all_prefixes,
    get_doorstop_tree,
    get_item_map,
)
from spec_weaver.adapters.gherkin import get_tag_map
from spec_weaver.adapters.impl_scanner import ImplScanner


class SyncService:
    """
    AST解析結果やアノテーションスキャン結果をDoorstopアイテムに同期し、
    CLIフレンドリー（grep等で検索可能）な状態にするサービス。
    """

    def sync_all(
        self,
        repo_root: Path,
        feature_dir: Optional[Path] = None,
        extensions: Optional[List[str]] = None,
        sync_children: bool = False,
    ) -> Tuple[int, int]:
        """
        ASTやスキャナから得られた紐づけ情報をDoorstop YAMLに書き込む。
        戻り値: (更新されたアイテム数, エラー数)
        """
        updated_count = 0
        error_count = 0

        try:
            raw_items = get_item_map(repo_root, include_inactive=True)
        except Exception:
            return 0, 1

        if not raw_items:
            return 0, 0

        # 1. feature_files の算出
        new_feature_files: Dict[str, Set[str]] = {}
        if feature_dir and feature_dir.exists():
            try:
                prefixes = get_all_prefixes(repo_root)
                tag_map = get_tag_map(feature_dir, repo_root, prefixes)
                for uid, scenarios in tag_map.items():
                    files = set()
                    for sc in scenarios:
                        path_str = sc["file"]
                        if path_str.startswith("./"):
                            path_str = path_str[2:]
                        files.add(path_str)
                    new_feature_files[uid] = files
            except Exception as e:
                # Gherkinパースエラーなどはスキップして他を進めるか、エラーとしてカウント
                error_count += 1

        # 2. scanned_impl_files の算出
        new_impl_files: Dict[str, Set[str]] = {}
        try:
            scanner = ImplScanner()
            annotation_map = scanner.scan(repo_root, extensions=extensions)
            for uid, files in annotation_map.items():
                new_impl_files[uid] = set(files)
        except Exception:
            error_count += 1

        # 3. 各アイテムの更新
        for uid, item in raw_items.items():
            changed = False

            # feature_files の更新
            current_ff = set(item.get("feature_files") or [])
            target_ff = new_feature_files.get(uid, set())
            if current_ff != target_ff:
                if target_ff:
                    item.set("feature_files", sorted(list(target_ff)))
                else:
                    if "feature_files" in item.data:
                        del item.data["feature_files"]
                changed = True

            # scanned_impl_files の更新
            current_si = set(item.get("scanned_impl_files") or [])
            target_si = new_impl_files.get(uid, set())
            if current_si != target_si:
                if target_si:
                    item.set("scanned_impl_files", sorted(list(target_si)))
                else:
                    if "scanned_impl_files" in item.data:
                        del item.data["scanned_impl_files"]
                changed = True

            if changed:
                try:
                    item.save()
                    updated_count += 1
                except Exception:
                    error_count += 1

        # 4. child_stamps の同期 (オプション)
        if sync_children:
            try:
                multi_tree = get_doorstop_tree(repo_root)
                child_index = _build_child_index(multi_tree)
                for uid, item in raw_items.items():
                    if clear_children_stamps(item, child_index):
                        updated_count += 1
            except Exception:
                error_count += 1

        return updated_count, error_count
