from collections import defaultdict
from typing import Dict, List, Optional, Set, Any
from pathlib import Path


class ReviewState:
    def __init__(self):
        # uid/path -> set of uids/paths that caused it to be suspect
        self.suspect_causes: Dict[str, Set[str]] = defaultdict(set)
        # uid/path that are directly unreviewed
        self.unreviewed_nodes: Set[str] = set()
        # uid/path -> set of parent uids/paths
        self.parents: Dict[str, Set[str]] = defaultdict(set)

    def get_status(self, node_id: str) -> str:
        is_unreviewed = node_id in self.unreviewed_nodes
        causes = self.suspect_causes.get(node_id, set())
        is_suspect = bool(causes)

        # QA-001: Check if any related items are unreviewed
        has_unreviewed_related = False
        
        # 1. Check direct parents (for Doorstop native suspect)
        for p in self.parents.get(node_id, set()):
            if p in self.unreviewed_nodes:
                has_unreviewed_related = True
                break
        
        # 2. Check causes that are themselves node IDs
        if not has_unreviewed_related:
            for cause in causes:
                if cause in self.unreviewed_nodes:
                    has_unreviewed_related = True
                    break
        
        statuses = []
        if is_unreviewed:
            statuses.append("📋 unreviewed")

        if is_suspect:
            if has_unreviewed_related:
                statuses.append("⚠️ suspect-with-unreviewed")
            else:
                statuses.append("⚠️ suspect-with-reviewed")

        if not statuses:
            return "✅ reviewed"

        return " / ".join(statuses)


def compute_review_state(
    all_items: dict,
    gherkin_fingerprints: dict,
    tag_map: dict,
    feature_file_states: Optional[Dict[str, bool]] = None,
) -> ReviewState:
    """
    レビュー状態を計算して ReviewState を返します。

    Args:
        all_items: Doorstop アイテム辞書 {uid_str: item}
        gherkin_fingerprints: {spec_id: 計算済みハッシュ}（SPEC suspect 判定に使用）
        tag_map: {spec_id: [ScenarioInfo, ...]}
        feature_file_states: {file_path: is_unreviewed} .feature ファイル単位のレビュー状態。
            None の場合は feature file の unreviewed 判定をスキップする。
    """
    state = ReviewState()

    children: Dict[str, Set[str]] = defaultdict(set)

    # Doorstop アイテム間のリンク
    for uid, item in all_items.items():
        uid_str = str(uid)
        for link in getattr(item, "links", []):
            parent_uid = str(link)
            if parent_uid in all_items:
                state.parents[uid_str].add(parent_uid)
                children[parent_uid].add(uid_str)

    # feature ファイルと SPEC の親子関係 (SPEC -> Feature)
    for tag, scenarios in tag_map.items():
        if tag in all_items:
            for s in scenarios:
                fpath = s["file"]
                state.parents[fpath].add(tag)
                children[tag].add(fpath)

    # Doorstop アイテムの unreviewed / native suspect 検出
    for uid, item in all_items.items():
        uid_str = str(uid)
        try:
            if not getattr(item, "reviewed", True):
                state.unreviewed_nodes.add(uid_str)
        except Exception:
            pass

        try:
            if not getattr(item, "cleared", True):
                state.suspect_causes[uid_str].add("Doorstop native suspect link")
        except Exception:
            pass

    # feature ファイルの unreviewed 判定と suspect 判定
    if feature_file_states is not None:
        for fpath, data in feature_file_states.items():
            # 古い形式 (bool) の場合は後方互換性のためフォールバック
            if isinstance(data, bool):
                if data:
                    state.unreviewed_nodes.add(fpath)
                continue

            stored_fps = data.get("stored", {})
            actual_file = data.get("actual_file")

            if stored_fps.get("") != actual_file or actual_file is None:
                state.unreviewed_nodes.add(fpath)

            for tag, stored_stamp in stored_fps.items():
                if not tag:
                    continue
                if tag in all_items:
                    actual_stamp = all_items[tag].stamp() if hasattr(all_items[tag], "stamp") else None
                    if actual_stamp and stored_stamp != actual_stamp:
                        state.suspect_causes[fpath].add(tag)

    # SPEC の suspect 判定（gherkin_fingerprints と現在の Gherkin ハッシュの比較）
    for tag, actual_fps in gherkin_fingerprints.items():
        if tag in all_items:
            item = all_items[tag]
            expected_fps = getattr(item, "gherkin_fingerprints", None)
            if expected_fps is None and hasattr(item, "get"):
                expected_fps = item.get("gherkin_fingerprints")

            if expected_fps is not None:
                # Strip newlines from expected fingerprints
                stripped_expected_fps = []
                for d in expected_fps:
                    stripped_expected_fps.append({k: v.strip() for k, v in d.items()})
                
                if actual_fps != stripped_expected_fps:
                    # QA-001: どのファイルが変更されたかを原因として記録する
                    actual_dict = {list(d.keys())[0]: list(d.values())[0] for d in actual_fps}
                    expected_dict = {list(d.keys())[0]: list(d.values())[0] for d in stripped_expected_fps}
                    
                    changed_files = set()
                    for f, h in actual_dict.items():
                        if expected_dict.get(f) != h:
                            changed_files.add(f)
                    for f in expected_dict:
                        if f not in actual_dict:
                            changed_files.add(f)
                    
                    if changed_files:
                        state.suspect_causes[tag].update(changed_files)
                    else:
                        state.suspect_causes[tag].add("gherkin_fingerprints mismatch")
            else:
                # 従来の test_fingerprint 判定 (フォールバック)
                expected_fp = getattr(item, "test_fingerprint", None)
                if expected_fp is None and hasattr(item, "get"):
                    expected_fp = item.get("test_fingerprint")
                
                if expected_fp and isinstance(expected_fp, str):
                    expected_fp = expected_fp.strip()
                    import hashlib
                    combined = "".join(list(d.values())[0] for d in actual_fps)
                    actual_fp_single = hashlib.sha256(combined.encode("utf-8")).hexdigest()
                    
                    if actual_fp_single != expected_fp:
                        state.suspect_causes[tag].add("test_fingerprint mismatch")

    return state

