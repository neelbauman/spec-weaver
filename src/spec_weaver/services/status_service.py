from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from spec_weaver.adapters.behave import check_behave_steps
from spec_weaver.adapters.doorstop import (
    _build_child_index,
    _get_custom_attribute,
    get_all_prefixes,
    get_doorstop_tree,
    get_item_map,
)
from spec_weaver.adapters.gherkin import get_spec_fingerprints, get_tag_map
from spec_weaver.core.review_state import ReviewState, compute_review_state
from spec_weaver.services.audit_service import (
    AuditService,  # feature_file_states取得などを再利用
)
from spec_weaver.utils.formatters import get_uid_prefix


@dataclass
class ItemStatusDTO:
    uid: str
    title: str
    active: bool
    raw_status: Optional[str]
    item_obj: Any  # フォーマッタに渡すための元のオブジェクト参照

@dataclass
class FeatureStatusDTO:
    file_path: str
    scenario_count: int
    related_specs: List[str]
    status: str

@dataclass
class StatusReport:
    # { "REQ": [ItemStatusDTO, ...], "SPEC": [...] } のようなグループ化データ
    grouped_items: Dict[str, List[ItemStatusDTO]]
    feature_files: List[FeatureStatusDTO]
    unused_step_defs_count: int
    undefined_steps_count: int
    total_items_shown: int
    review_state: ReviewState

class StatusService:
    def get_status_report(
        self,
        repo_root: Path,
        feature_dir: Path,
        filter_status: Optional[str] = None
    ) -> StatusReport:
        # 1. Doorstopデータの取得
        raw_items = get_item_map(repo_root=repo_root)
        all_items_str = {str(uid): item for uid, item in raw_items.items()}
        all_prefixes = get_all_prefixes(repo_root)

        # 2. レビュー状態の計算
        try:
            gherkin_fingerprints = get_spec_fingerprints(feature_dir, repo_root, all_prefixes)
        except Exception:
            gherkin_fingerprints = {}
        try:
            tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
        except Exception:
            tag_map = {}

        # TODO: _compute_feature_file_states は共通UtilityかGherkinモジュールに完全に移すのが理想ですが、
        # 今回は一旦 AuditService から流用する想定とします。
        feature_file_states = AuditService()._compute_feature_file_states(feature_dir, repo_root)
        multi_tree = get_doorstop_tree(repo_root)
        child_index = _build_child_index(multi_tree)
        review_state = compute_review_state(
            all_items_str, gherkin_fingerprints, tag_map, feature_file_states,
            multi_tree=multi_tree, child_index=child_index,
        )

        # 3. アイテムのグループ化とフィルタリング
        grouped_items: Dict[str, List[ItemStatusDTO]] = {p: [] for p in all_prefixes}
        total_shown = 0

        for uid, item in all_items_str.items():
            raw_status = _get_custom_attribute(item, "status", None)
            
            # フィルタリング
            if filter_status and str(raw_status or "") != filter_status:
                continue

            prefix = get_uid_prefix(uid)
            dto = ItemStatusDTO(
                uid=uid,
                title=(item.header or "").strip(),
                active=item.active,
                raw_status=str(raw_status) if raw_status else None,
                item_obj=item
            )
            
            if prefix in grouped_items:
                grouped_items[prefix].append(dto)
            else:
                grouped_items.setdefault("OTHER", []).append(dto)
                
            total_shown += 1

        # 4. Featureファイルの集計 (filter指定がない場合のみ)
        feature_files: List[FeatureStatusDTO] = []
        if not filter_status:
            f_map: Dict[str, Dict] = {}
            for uid, scenarios in tag_map.items():
                for sc in scenarios:
                    fpath = sc["file"]
                    if fpath not in f_map:
                        f_map[fpath] = {"scenarios": 0, "specs": set()}
                    f_map[fpath]["scenarios"] += 1
                    f_map[fpath]["specs"].add(uid)

            for fpath in sorted(f_map.keys()):
                info = f_map[fpath]
                feature_files.append(FeatureStatusDTO(
                    file_path=fpath,
                    scenario_count=info["scenarios"],
                    related_specs=sorted(info["specs"]),
                    status=review_state.get_status(fpath)
                ))

        # 5. ステップの整合性チェック (概要のみ)
        unused_defs_cnt, undefined_steps_cnt = 0, 0
        try:
            unused_defs, undefined_steps = check_behave_steps(feature_dir)
            unused_defs_cnt = len(unused_defs)
            undefined_steps_cnt = len(undefined_steps)
        except Exception:
            pass

        return StatusReport(
            grouped_items=grouped_items,
            feature_files=feature_files,
            unused_step_defs_count=unused_defs_cnt,
            undefined_steps_count=undefined_steps_cnt,
            total_items_shown=total_shown,
            review_state=review_state
        )
