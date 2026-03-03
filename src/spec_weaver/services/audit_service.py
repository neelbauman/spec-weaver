from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Set, Dict, List, Tuple
from datetime import date as _date

from spec_weaver.core.review_state import compute_review_state, ReviewState
from spec_weaver.adapters.behave import check_behave_steps
from spec_weaver.adapters.doorstop import (
    get_item_map, get_specs, get_all_prefixes, 
    _get_custom_attribute, _get_git_file_date
)
from spec_weaver.adapters.gherkin import (
    get_tag_map, get_tags, get_spec_fingerprints, 
    compute_feature_file_hash, read_stored_fingerprints
)
from spec_weaver.adapters.impl_scanner import ImplScanner, get_ref_files

@dataclass
class AuditReport:
    """
    監査(audit)コマンドのビジネスロジック実行結果を格納するデータクラス。
    UI（表示形式）には一切依存せず、純粋なドメインの状態を表現する。
    """
    is_success: bool
    specs_count: int
    inactive_testable: Set[str]
    untested_specs: Set[str]
    orphaned_tags: Set[str]
    suspect_specs: Dict[str, Set[str]]
    suspect_features: Dict[str, Set[str]]
    unreviewed_specs: Set[str]
    unreviewed_features: Set[str]
    stale_items: List[Tuple[str, str, int]]  # (uid, updated_at_str, delta_days)
    unused_step_defs: Set[str]
    undefined_steps: Set[str]
    review_state_parents: Dict[str, Set[str]] = field(default_factory=dict)
    broken_refs: List[Tuple[str, str]] = field(default_factory=list)
    ref_only: List[Tuple[str, str]] = field(default_factory=list)
    annotation_only: List[Tuple[str, str]] = field(default_factory=list)


class AuditService:
    """
    Doorstopの仕様データとGherkinのテストデータを突き合わせ、
    乖離や不整合を監査(Audit)するビジネスロジックを提供するサービス。
    """

    def run_audit(
        self,
        feature_dir: Path,
        repo_root: Path,
        prefix: Optional[str] = None,
        stale_days: int = 90,
        check_impl: bool = False,
        extensions: Optional[str] = None,
    ) -> AuditReport:
        # 1. Doorstopデータの読み込み
        specs_in_db = get_specs(repo_root=repo_root, prefix=prefix)
        all_prefixes = get_all_prefixes(repo_root=repo_root)
        
        all_items_with_inactive = get_item_map(repo_root=repo_root, include_inactive=True)
        inactive_testable: Set[str] = set()
        for uid, item in all_items_with_inactive.items():
            if item.active:
                continue
            if prefix and not uid.startswith(prefix):
                continue
            if _get_custom_attribute(item, "testable", True):
                inactive_testable.add(uid)

        # 2. Gherkin解析
        search_prefixes = {prefix} if prefix else all_prefixes
        tags_in_code = get_tags(features_dir=feature_dir, repo_root=repo_root, prefixes=search_prefixes)

        # 3. レビュー状態・Suspectの確認
        raw_items = get_item_map(repo_root=repo_root)
        try:
            gherkin_fingerprints = get_spec_fingerprints(feature_dir, repo_root, search_prefixes)
            tag_map = get_tag_map(feature_dir, repo_root, search_prefixes)
        except Exception:
            gherkin_fingerprints, tag_map = {}, {}

        feature_file_states = self._compute_feature_file_states(feature_dir, repo_root)
        review_state = compute_review_state(raw_items, gherkin_fingerprints, tag_map, feature_file_states)

        suspect_specs, suspect_features = {}, {}
        unreviewed_specs, unreviewed_features = set(), set()
        
        for uid in raw_items.keys():
            if prefix and not uid.startswith(prefix):
                continue
            status = review_state.get_status(uid)
            if uid in review_state.unreviewed_nodes:
                unreviewed_specs.add(uid)
            if "suspect" in status:
                suspect_specs[uid] = review_state.suspect_causes.get(uid, set())

        feature_to_specs: Dict[str, Set[str]] = {}
        for tag, scenarios in tag_map.items():
            if prefix and not str(tag).startswith(prefix):
                continue
            for s in scenarios:
                feature_to_specs.setdefault(s["file"], set()).add(str(tag))

        for fpath in feature_to_specs.keys():
            fstatus = review_state.get_status(fpath)
            if fpath in review_state.unreviewed_nodes:
                unreviewed_features.add(fpath)
            if "suspect" in fstatus:
                suspect_features[fpath] = review_state.suspect_causes.get(fpath, set())

        # 4. 未テスト/孤児タグの計算
        untested_specs = specs_in_db - tags_in_code
        orphaned_tags = tags_in_code - specs_in_db

        # 5. Staleチェック
        stale_items = []
        if stale_days > 0:
            today = _date.today()
            for uid, item in raw_items.items():
                if prefix and not uid.startswith(prefix):
                    continue
                if str(_get_custom_attribute(item, "status", None) or "") == "deprecated":
                    continue
                
                updated_at_val = None
                if getattr(item, "path", None):
                    updated_at_val = _get_git_file_date(str(item.path), mode="latest")
                if not updated_at_val:
                    updated_at_val = _get_custom_attribute(item, "updated_at", None)
                if not updated_at_val:
                    continue

                try:
                    delta = (today - _date.fromisoformat(str(updated_at_val))).days
                    if delta > stale_days:
                        stale_items.append((str(uid), str(updated_at_val), delta))
                except ValueError:
                    pass

        # 6. 実装ファイルリンクの検証
        broken_refs, ref_only, annotation_only = [], [], []
        if check_impl:
            ext_list = [e.strip() for e in extensions.split(",")] if extensions else None
            broken_refs, ref_only, annotation_only = self._run_impl_link_check(raw_items, repo_root, ext_list, prefix)

        # 7. Behaveステップ検証
        unused_defs, undefined_steps = check_behave_steps(feature_dir)

        # 8. 全体成功判定
        is_success = not (untested_specs or orphaned_tags or suspect_specs or 
                          suspect_features or unreviewed_specs or unreviewed_features or 
                          broken_refs or undefined_steps)

        return AuditReport(
            is_success=is_success,
            specs_count=len(specs_in_db),
            inactive_testable=inactive_testable,
            untested_specs=untested_specs,
            orphaned_tags=orphaned_tags,
            suspect_specs=suspect_specs,
            suspect_features=suspect_features,
            unreviewed_specs=unreviewed_specs,
            unreviewed_features=unreviewed_features,
            stale_items=stale_items,
            unused_step_defs=unused_defs,
            undefined_steps=undefined_steps,
            review_state_parents=review_state.parents,
            broken_refs=broken_refs,
            ref_only=ref_only,
            annotation_only=annotation_only,
        )

    def _compute_feature_file_states(self, feature_dir: Path, repo_root: Path) -> dict:
        """Gherkinファイルの状態計算（元CLIのヘルパーを移譲）"""
        states = {}
        if not feature_dir.is_dir():
            return states
        for f in feature_dir.rglob("*.feature"):
            rel = "./" + str(f.relative_to(repo_root)) if str(f).startswith(str(repo_root)) else str(f)
            try:
                states[rel] = {
                    "stored": read_stored_fingerprints(f), 
                    "actual_file": compute_feature_file_hash(f)
                }
            except Exception:
                states[rel] = {"stored": {}, "actual_file": None}
        return states

    def _run_impl_link_check(self, raw_items: dict, repo_root: Path, extensions: Optional[list[str]], prefix: Optional[str]):
        """実装ファイルリンクの検証ロジック"""
        scanner = ImplScanner()
        annotation_map = scanner.scan(repo_root, extensions=extensions)
        ref_map = {str(uid): get_ref_files(it) for uid, it in raw_items.items() if (not prefix or str(uid).startswith(prefix)) and get_ref_files(it)}
        
        all_spec_ids = set(ref_map.keys()) | set(annotation_map.keys())
        if prefix:
            all_spec_ids = {sid for sid in all_spec_ids if sid.startswith(prefix)}

        broken, r_only, a_only = [], [], []
        for spec_id in all_spec_ids:
            refs = set(ref_map.get(spec_id, []))
            annotations = annotation_map.get(spec_id, set())

            for p in refs:
                if not (repo_root / p).exists():
                    broken.append((spec_id, p))
                elif p not in annotations:
                    r_only.append((spec_id, p))
            for p in (annotations - refs):
                a_only.append((spec_id, p))

        return broken, r_only, a_only
