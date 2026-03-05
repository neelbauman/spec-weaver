from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from spec_weaver.adapters.doorstop import (
    _build_child_index,
    get_all_prefixes,
    get_doorstop_tree,
    get_item_map,
)
from spec_weaver.adapters.gherkin import get_spec_fingerprints, get_tag_map
from spec_weaver.adapters.impl_scanner import ImplScanner, get_ref_files
from spec_weaver.core.review_state import ReviewState, compute_review_state
from spec_weaver.services.audit_service import AuditService


@dataclass
class TraceData:
    """Traceコマンドの描画に必要な全ての状態を保持するデータクラス"""
    all_items_str: Dict[str, any]
    child_map: Dict[str, List[str]]
    tag_map: Dict[str, List[any]]
    review_state: Optional[ReviewState]
    impl_map: Optional[Dict[str, List[Dict[str, str]]]] # uid -> [{"path": str, "source": str, "exists": bool}]

class TraceService:
    def prepare_trace_data(
        self,
        repo_root: Path,
        feature_dir: Optional[Path],
        show_impl: bool,
        extensions: Optional[list[str]]
    ) -> TraceData:
        # 1. Doorstopデータの読み込み
        try:
            raw_items = get_item_map(repo_root)
        except Exception:
            raw_items = {}

        if not raw_items:
            # Doorstopのツリーが見つからない場合、テストの期待するエラーメッセージを投げる
            raise RuntimeError("No Doorstop tree found")
            
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
                multi_tree = get_doorstop_tree(repo_root)
                ci = _build_child_index(multi_tree)
                review_state = compute_review_state(
                    raw_items, gherkin_fingerprints, tag_map, feature_file_states,
                    multi_tree=multi_tree, child_index=ci,
                )
            except Exception:
                pass
        else:
            # feature_dirがなくてもDoorstopネイティブのsuspectを見るため計算は試みる
            try:
                multi_tree = get_doorstop_tree(repo_root)
                ci = _build_child_index(multi_tree)
                review_state = compute_review_state(
                    raw_items, {}, {}, {},
                    multi_tree=multi_tree, child_index=ci,
                )
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
                
                all_paths = refs | annotations
                if not all_paths:
                    continue
                
                impl_list = []
                for p in sorted(list(all_paths)):
                    source = "both"
                    if p in refs and p not in annotations:
                        source = "ref"
                    elif p in annotations and p not in refs:
                        source = "annotation"
                    
                    exists = (repo_root / p).exists()
                    impl_list.append({"path": p, "source": source, "exists": exists})
                
                impl_map[uid] = impl_list

        return TraceData(
            all_items_str=all_items_str,
            child_map=child_map,
            tag_map=tag_map,
            review_state=review_state,
            impl_map=impl_map
        )
