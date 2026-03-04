from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict

from spec_weaver.adapters.doorstop import get_item_map, get_all_prefixes, get_doorstop_tree
from spec_weaver.adapters.gherkin import get_tag_map, compute_feature_file_hash, write_feature_fingerprints

@dataclass
class ReviewResult:
    is_success: bool
    target_type: str  # "feature" | "doorstop"
    fingerprint: Optional[str] = None
    linked_items: Dict[str, str] | None = None
    item_id: Optional[str] = None
    error_message: Optional[str] = None

class ReviewService:
    def run_review(
        self,
        target_path: str,
        feature_dir: Path,
        repo_root: Path
    ) -> ReviewResult:
        target = Path(target_path)
        
        # 1. .feature ファイルの場合
        if target.exists() and target.suffix == ".feature":
            fp = compute_feature_file_hash(target)
            all_prefixes = get_all_prefixes(repo_root)
            tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
            raw_items = get_item_map(repo_root)
            
            linked_tags = set()
            for tag, scenarios in tag_map.items():
                for s in scenarios:
                    if Path(s["file"]).resolve() == target.resolve():
                        linked_tags.add(tag)
                        break
                        
            item_fps = {}
            for tag in linked_tags:
                if tag in raw_items:
                    item = raw_items[tag]
                    item_fps[tag] = item.stamp() if hasattr(item, "stamp") else ""

            write_feature_fingerprints(target, fp, item_fps)
            
            return ReviewResult(
                is_success=True, target_type="feature",
                fingerprint=fp, linked_items=item_fps
            )

        # 2. Doorstop アイテム (.yml または ID) の場合
        item_id = target.stem if target.exists() and target.suffix == ".yml" else target_path

        item_map = get_item_map(repo_root)
        if item_id in item_map:
            try:
                multi_tree = get_doorstop_tree(repo_root)
                item = multi_tree.find_item(item_id)
                if item is None:
                    return ReviewResult(
                        is_success=False, target_type="doorstop",
                        error_message=f"アイテムが見つかりません: {item_id}"
                    )
                item.review()
                item.save()
                return ReviewResult(is_success=True, target_type="doorstop", item_id=item_id)
            except Exception as e:
                return ReviewResult(
                    is_success=False, target_type="doorstop",
                    error_message=f"レビュー処理に失敗しました: {e}"
                )

        # 3. どちらでもない場合
        msg = f"ターゲットが見つかりません: {target_path}" if not target.exists() else f"未対応のファイル形式です: {target_path}"
        return ReviewResult(is_success=False, target_type="unknown", error_message=msg)
