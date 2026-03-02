from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Set, Optional, Dict

from spec_weaver.doorstop import (
    get_item_map, get_all_prefixes, 
    update_item_attribute, clear_doorstop_suspects
)
# ※delete_item_attributeは元のcli.pyで使われていましたがimport漏れがあったためここで追加します
from spec_weaver.doorstop import delete_item_attribute 
from spec_weaver.gherkin import get_tags, get_spec_fingerprints, get_tag_map
from spec_weaver.review_state import compute_review_state
from spec_weaver.services.audit_service import AuditService

@dataclass
class ClearResult:
    is_success: bool
    updated_items: List[str] = field(default_factory=list)
    skipped_unreviewed: List[str] = field(default_factory=list)
    skipped_suspect_unreviewed: List[str] = field(default_factory=list)
    error_message: Optional[str] = None

class ClearService:
    def run_clear(
        self,
        item_id_or_path: str,
        feature_dir: Path,
        repo_root: Path
    ) -> ClearResult:
        item_path = Path(item_id_or_path)
        all_prefixes = get_all_prefixes(repo_root)
        raw_items = get_item_map(repo_root)
        all_items_str = {str(uid): it for uid, it in raw_items.items()}
        
        # 状態計算の準備
        gherkin_fingerprints = get_spec_fingerprints(feature_dir, repo_root, all_prefixes)
        tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
        feature_file_states = AuditService()._compute_feature_file_states(feature_dir, repo_root)
        
        review_state = compute_review_state(
            all_items_str, gherkin_fingerprints, tag_map, feature_file_states
        )

        result = ClearResult(is_success=True)
        target_tags: Set[str] = set()

        # 1. .featureファイルが指定された場合
        if item_path.suffix == ".feature" and item_path.exists():
            target_tags = get_tags(item_path, repo_root, all_prefixes)
            if not target_tags:
                result.is_success = False
                result.error_message = f"{item_id_or_path} に紐づく仕様IDが見つかりませんでした。"
                return result
        # 2. アイテムIDが指定された場合
        else:
            if item_id_or_path not in raw_items:
                result.is_success = False
                result.error_message = f"アイテム {item_id_or_path} が見つかりません。"
                return result
            target_tags = {item_id_or_path}

        # 更新処理
        for tag in sorted(target_tags):
            status = review_state.get_status(tag)
            
            # ブロック条件 (QA-001)
            if tag in review_state.unreviewed_nodes:
                result.skipped_unreviewed.append(tag)
                # 単一アイテム指定の場合は即時エラーとする
                if len(target_tags) == 1:
                    result.is_success = False
                    result.error_message = f"{tag} は未レビューです。先にレビューしてください。"
                continue
            
            if "suspect-with-unreviewed" in status:
                result.skipped_suspect_unreviewed.append(tag)
                if len(target_tags) == 1:
                    result.is_success = False
                    result.error_message = f"{tag} は上位アイテムが未レビューです。先に上位アイテムをレビューしてください。"
                continue

            # YAML更新
            actual_fps = gherkin_fingerprints.get(tag)
            if actual_fps:
                update_item_attribute(repo_root, tag, "gherkin_fingerprints", actual_fps)
                try:
                    delete_item_attribute(repo_root, tag, "test_fingerprint")
                except Exception:
                    pass
                result.updated_items.append(tag)
            
            # Doorstopネイティブのsuspect解除
            try:
                if clear_doorstop_suspects(repo_root, tag) and tag not in result.updated_items:
                    result.updated_items.append(tag)
            except Exception:
                pass

        if len(target_tags) == 1 and not result.updated_items and result.is_success:
            # 更新すべきGherkinシナリオもsuspectリンクもなかった場合
            pass # エラーにはしないが更新もなし

        return result
