from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from spec_weaver.adapters.doorstop import (
    _build_child_index,
    clear_doorstop_suspects,
    delete_item_attribute,
    get_all_prefixes,
    get_doorstop_tree,
    get_item_map,
    update_item_attribute,
)
from spec_weaver.adapters.gherkin import (
    get_spec_fingerprints,
    get_tag_map,
)
from spec_weaver.core.review_state import compute_review_state
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
        item_id: str,
        feature_dir: Path,
        repo_root: Path,
    ) -> ClearResult:
        """単一アイテムの gherkin_fingerprints を更新する。

        Args:
            item_id: 更新する Doorstop アイテム ID。
            feature_dir: .feature ファイルを含むディレクトリ。
            repo_root: リポジトリルートパス。

        Returns:
            ClearResult。
        """
        all_prefixes = get_all_prefixes(repo_root)
        raw_items = get_item_map(repo_root)
        all_items_str = {str(uid): it for uid, it in raw_items.items()}

        if item_id not in raw_items:
            return ClearResult(
                is_success=False,
                error_message=f"アイテム {item_id} が見つかりません。",
            )

        gherkin_fingerprints = get_spec_fingerprints(feature_dir, repo_root, all_prefixes)
        tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
        feature_file_states = AuditService()._compute_feature_file_states(feature_dir, repo_root)

        multi_tree = get_doorstop_tree(repo_root)
        child_index = _build_child_index(multi_tree)
        review_state = compute_review_state(
            all_items_str, gherkin_fingerprints, tag_map, feature_file_states,
            multi_tree=multi_tree, child_index=child_index,
        )

        result = ClearResult(is_success=True)

        # ブロック条件: 未レビュー
        if item_id in review_state.unreviewed_nodes:
            result.skipped_unreviewed.append(item_id)
            result.is_success = False
            result.error_message = f"{item_id} は未レビューです。先にレビューしてください。"
            return result

        # ブロック条件: 上位アイテムが未レビュー
        status = review_state.get_status(item_id)
        if "suspect-with-unreviewed" in status:
            result.skipped_suspect_unreviewed.append(item_id)
            result.is_success = False
            result.error_message = f"{item_id} は上位アイテムが未レビューです。先に上位アイテムをレビューしてください。"
            return result

        # gherkin_fingerprints 更新
        actual_fps = gherkin_fingerprints.get(item_id)
        if actual_fps:
            update_item_attribute(repo_root, item_id, "gherkin_fingerprints", actual_fps)
            try:
                delete_item_attribute(repo_root, item_id, "test_fingerprint")
            except Exception:
                pass
            result.updated_items.append(item_id)

        # Doorstop ネイティブ suspect 解除
        try:
            if clear_doorstop_suspects(repo_root, item_id) and item_id not in result.updated_items:
                result.updated_items.append(item_id)
        except Exception:
            pass

        if not result.updated_items:
            result.is_success = False
            result.error_message = f"警告: {item_id} に紐づく Gherkin シナリオまたは Suspect リンクが見つかりません。"

        return result

    def run_clear_all_items(
        self,
        feature_dir: Path,
        repo_root: Path,
    ) -> ClearResult:
        """全アクティブ Doorstop アイテムの gherkin_fingerprints を一括更新する（エディタなし）。

        未レビューのアイテムはスキップして警告を記録する。

        Args:
            feature_dir: .feature ファイルを含むディレクトリ。
            repo_root: リポジトリルートパス。

        Returns:
            ClearResult。
        """
        all_prefixes = get_all_prefixes(repo_root)
        raw_items = get_item_map(repo_root)
        all_items_str = {str(uid): it for uid, it in raw_items.items()}

        if feature_dir.exists():
            gherkin_fingerprints = get_spec_fingerprints(feature_dir, repo_root, all_prefixes)
            tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
            feature_file_states = AuditService()._compute_feature_file_states(feature_dir, repo_root)
        else:
            gherkin_fingerprints = {}
            tag_map = {}
            feature_file_states = {}

        multi_tree = get_doorstop_tree(repo_root)
        child_index = _build_child_index(multi_tree)
        review_state = compute_review_state(
            all_items_str, gherkin_fingerprints, tag_map, feature_file_states,
            multi_tree=multi_tree, child_index=child_index,
        )

        result = ClearResult(is_success=True)

        for uid_str in sorted(all_items_str.keys()):
            if uid_str in review_state.unreviewed_nodes:
                result.skipped_unreviewed.append(uid_str)
                continue

            actual_fps = gherkin_fingerprints.get(uid_str)
            if actual_fps:
                update_item_attribute(repo_root, uid_str, "gherkin_fingerprints", actual_fps)
                try:
                    delete_item_attribute(repo_root, uid_str, "test_fingerprint")
                except Exception:
                    pass
                result.updated_items.append(uid_str)

            try:
                if clear_doorstop_suspects(repo_root, uid_str) and uid_str not in result.updated_items:
                    result.updated_items.append(uid_str)
            except Exception:
                pass

        return result
