from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, List, Set

from spec_weaver.core.review_state import compute_review_state, ReviewState
from spec_weaver.adopters.doorstop import get_item_map, get_all_prefixes
from spec_weaver.adopters.gherkin import get_tag_map, get_spec_fingerprints
from spec_weaver.adopters.impl_scanner import ImplScanner, get_ref_files
from spec_weaver.services.audit_service import AuditService

@dataclass
class TraceData:
    """Traceコマンドの描画に必要な全ての状態を保持するデータクラス"""
    all_items_str: Dict[str, any]
    child_map: Dict[str, List[str]]
    tag_map: Dict[str, List[any]]
    review_state: Optional[ReviewState]
    impl_map: Optional[Dict[str, Set[str]]]

class TraceService:
    def prepare_trace_data(
        self,
        repo_root: Path,
        feature_dir: Optional[Path],
        show_impl: bool,
        extensions: Optional[list[str]]
    ) -> TraceData:
        # 1. Doorstopデータの読み込み
        raw_items = get_item_map(repo_root)
        all_items_str = {str(uid): item for uid, item in raw_items.items()}

        # 2. child_map 構築（parent_uid → [child_uid, ...]）
        child_map: Dict[str, List[str]] = {}
        for uid, item in all_items_str.items():
            for link in item.links:
                parent_uid = str(link)
                child_map.setdefault(parent_uid, []).append(uid)

        # 3. Gherkin関連のパースとレビュー状態の計算
        tag_map = {}
        review_state = None
        if feature_dir is not None:
            all_prefixes = get_all_prefixes(repo_root)
            tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
            try:
                gherkin_fingerprints = get_spec_fingerprints(feature_dir, repo_root, all_prefixes)
                feature_file_states = AuditService()._compute_feature_file_states(feature_dir, repo_root)
                review_state = compute_review_state(raw_items, gherkin_fingerprints, tag_map, feature_file_states)
            except Exception:
                pass
        else:
            # feature_dirがなくてもDoorstopネイティブのsuspectを見るため計算は試みる
            try:
                review_state = compute_review_state(raw_items, {}, {}, {})
            except Exception:
                pass

        # 4. 実装ファイルマップの構築
        impl_map = None
        if show_impl:
            impl_map = {}
            scanner = ImplScanner()
            annotation_map = scanner.scan(repo_root, extensions=extensions)
            for uid, item in all_items_str.items():
                refs = set(get_ref_files(item))
                annotations = annotation_map.get(uid, set())
                merged = refs | annotations
                if merged:
                    impl_map[uid] = merged

        return TraceData(
            all_items_str=all_items_str,
            child_map=child_map,
            tag_map=tag_map,
            review_state=review_state,
            impl_map=impl_map
        )
