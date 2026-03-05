from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from spec_weaver.adapters.doorstop import (
    get_doorstop_tree,
    get_item_map,
)


@dataclass
class ReviewResult:
    is_success: bool
    target_type: str  # "doorstop" | "unknown"
    item_id: Optional[str] = None
    error_message: Optional[str] = None


class ReviewService:
    def run_review(self, item_id: str, repo_root: Path) -> ReviewResult:
        """単一 Doorstop アイテムをレビュー済みにする。

        Args:
            item_id: レビューする Doorstop アイテム ID。
            repo_root: リポジトリルートパス。

        Returns:
            ReviewResult。
        """
        item_map = get_item_map(repo_root)
        if item_id not in item_map:
            return ReviewResult(
                is_success=False,
                target_type="doorstop",
                error_message=f"アイテムが見つかりません: {item_id}",
            )

        try:
            multi_tree = get_doorstop_tree(repo_root)
            item = multi_tree.find_item(item_id)
            if item is None:
                return ReviewResult(
                    is_success=False,
                    target_type="doorstop",
                    error_message=f"アイテムが見つかりません: {item_id}",
                )
            item.review()
            item.save()
            return ReviewResult(is_success=True, target_type="doorstop", item_id=item_id)
        except Exception as e:
            return ReviewResult(
                is_success=False,
                target_type="doorstop",
                error_message=f"レビュー処理に失敗しました: {e}",
            )

    def run_review_all_items(self, repo_root: Path) -> Tuple[List[str], List[Tuple[str, str]]]:
        """全アクティブ Doorstop アイテムをレビューする（エディタなし）。

        Returns:
            (reviewed_items, failed_items) のタプル。
            failed_items は (uid_str, error_message) のリスト。
        """
        item_map = get_item_map(repo_root)
        multi_tree = get_doorstop_tree(repo_root)
        reviewed: List[str] = []
        failed: List[Tuple[str, str]] = []

        for uid_str in sorted(item_map.keys()):
            try:
                doorstop_item = multi_tree.find_item(uid_str)
                if doorstop_item is None:
                    failed.append((uid_str, "アイテムが見つかりません"))
                    continue
                try:
                    doorstop_item.clear()
                except Exception:
                    pass
                doorstop_item.review()
                doorstop_item.save()
                reviewed.append(uid_str)
            except Exception as e:
                failed.append((uid_str, str(e)))

        return reviewed, failed
