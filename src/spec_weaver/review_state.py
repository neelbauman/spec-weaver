from collections import defaultdict
from typing import Dict, List, Optional, Set, Any
from pathlib import Path


class ReviewState:
    def __init__(self):
        # uid/path -> set of uids/paths that caused it to be suspect
        self.suspect_causes: Dict[str, Set[str]] = defaultdict(set)
        # uid/path that are directly unreviewed
        self.unreviewed_nodes: Set[str] = set()

    def get_status(self, node_id: str) -> str:
        statuses = []
        if node_id in self.unreviewed_nodes:
            statuses.append("📋 unreviewed")
        if self.suspect_causes.get(node_id):
            statuses.append("⚠️ suspect")

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

    parents: Dict[str, Set[str]] = defaultdict(set)
    children: Dict[str, Set[str]] = defaultdict(set)

    # Doorstop アイテム間のリンク
    for uid, item in all_items.items():
        uid_str = str(uid)
        for link in getattr(item, "links", []):
            parent_uid = str(link)
            if parent_uid in all_items:
                parents[uid_str].add(parent_uid)
                children[parent_uid].add(uid_str)

    # feature ファイルと SPEC の親子関係
    for tag, scenarios in tag_map.items():
        if tag in all_items:
            for s in scenarios:
                fpath = s["file"]
                parents[fpath].add(tag)
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

    # feature ファイルの unreviewed 判定（ファイル先頭コメントのハッシュ比較）
    if feature_file_states is not None:
        for fpath, is_unreviewed in feature_file_states.items():
            if is_unreviewed:
                state.unreviewed_nodes.add(fpath)

    # SPEC の suspect 判定（test_fingerprint と現在の Gherkin ハッシュの比較）
    for tag, actual_fp in gherkin_fingerprints.items():
        if tag in all_items:
            item = all_items[tag]
            expected_fp = getattr(item, "test_fingerprint", None)
            if expected_fp is None and hasattr(item, "get"):
                expected_fp = item.get("test_fingerprint")
            if expected_fp and isinstance(expected_fp, str):
                expected_fp = expected_fp.strip()

            if actual_fp and expected_fp and actual_fp != expected_fp:
                state.suspect_causes[tag].add("test_fingerprint mismatch")

    # suspect 伝播（上位方向）
    for start_node in list(state.unreviewed_nodes) + list(state.suspect_causes.keys()):
        queue = list(parents[start_node])
        visited: Set[str] = set()
        while queue:
            curr = queue.pop(0)
            if curr not in visited:
                visited.add(curr)
                if curr != start_node:
                    state.suspect_causes[curr].add(start_node)
                    queue.extend(parents[curr])

    # suspect 伝播（下位方向）
    for start_node in list(state.unreviewed_nodes) + list(state.suspect_causes.keys()):
        queue = list(children[start_node])
        visited = set()
        while queue:
            curr = queue.pop(0)
            if curr not in visited:
                visited.add(curr)
                if curr != start_node:
                    state.suspect_causes[curr].add(start_node)
                    queue.extend(children[curr])

    return state
