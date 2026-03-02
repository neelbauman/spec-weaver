from collections import defaultdict
from typing import Dict, List, Set, Any
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

def compute_review_state(all_items: dict, gherkin_fingerprints: dict, tag_map: dict) -> ReviewState:
    state = ReviewState()
    
    parents = defaultdict(set)
    children = defaultdict(set)
    
    # Links between Doorstop items
    for uid, item in all_items.items():
        uid_str = str(uid)
        for link in getattr(item, "links", []):
            parent_uid = str(link)
            if parent_uid in all_items:
                parents[uid_str].add(parent_uid)
                children[parent_uid].add(uid_str)
                
    # Links between feature files and SPECs
    for tag, scenarios in tag_map.items():
        if tag in all_items:
            for s in scenarios:
                fpath = s["file"]
                # Feature tests the tag (child -> parent)
                parents[fpath].add(tag)
                children[tag].add(fpath)
                
    # Identify unreviewed nodes
    for uid, item in all_items.items():
        uid_str = str(uid)
        try:
            if not getattr(item, "reviewed", True):
                state.unreviewed_nodes.add(uid_str)
        except Exception:
            pass

        try:
            if not getattr(item, "cleared", True):
                # Native Doorstop suspect. We don't necessarily know WHICH parent, 
                # but we know it's suspect. Add a generic cause or infer from links.
                state.suspect_causes[uid_str].add("Doorstop native suspect link")
        except Exception:
            pass
            
    # Identify unreviewed feature files
    for tag, actual_fp in gherkin_fingerprints.items():
        if tag in all_items:
            item = all_items[tag]
            # Use getattr with fallback, or parse custom attributes (simulating _get_custom_attribute)
            expected_fp = getattr(item, "test_fingerprint", None)
            if expected_fp is None and hasattr(item, "get"):
                expected_fp = item.get("test_fingerprint")

            if expected_fp and isinstance(expected_fp, str):
                expected_fp = expected_fp.strip()
            
            if actual_fp and actual_fp != expected_fp:
                # Which feature files contain this tag?
                for s in tag_map.get(tag, []):
                    fpath = s["file"]
                    state.unreviewed_nodes.add(fpath)
                    
    # Propagate suspect status (Upstream)
    for start_node in state.unreviewed_nodes:
        queue = list(parents[start_node])
        visited = set()
        while queue:
            curr = queue.pop(0)
            if curr not in visited:
                visited.add(curr)
                if curr != start_node:
                    state.suspect_causes[curr].add(start_node)
                    queue.extend(parents[curr])
                
    # Propagate suspect status (Downstream)
    for start_node in state.unreviewed_nodes:
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
