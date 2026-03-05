
from spec_weaver.core.review_state import ReviewState, compute_review_state


def test_review_state_reviewed():
    state = ReviewState()
    # No unreviewed, no suspect
    assert state.get_status("SPEC-001") == "✅ reviewed"

def test_review_state_unreviewed():
    state = ReviewState()
    state.unreviewed_nodes.add("SPEC-001")
    assert state.get_status("SPEC-001") == "📋 unreviewed"

def test_review_state_suspect_with_reviewed_parent():
    state = ReviewState()
    # Parent is reviewed
    state.parents["SPEC-002"].add("REQ-001")
    state.suspect_causes["SPEC-002"].add("Doorstop native suspect link")
    
    assert state.get_status("SPEC-002") == "⚠️ suspect-with-reviewed"

def test_review_state_suspect_with_unreviewed_parent():
    state = ReviewState()
    # Parent is unreviewed
    state.parents["SPEC-002"].add("REQ-001")
    state.unreviewed_nodes.add("REQ-001")
    state.suspect_causes["SPEC-002"].add("Doorstop native suspect link")
    
    assert state.get_status("SPEC-002") == "⚠️ suspect-with-unreviewed"

def test_review_state_unreviewed_and_suspect():
    state = ReviewState()
    state.unreviewed_nodes.add("SPEC-001")
    state.suspect_causes["SPEC-001"].add("gherkin_fingerprints mismatch")
    
    # By default, suspect-with-reviewed if no related item is unreviewed
    assert state.get_status("SPEC-001") == "📋 unreviewed / ⚠️ suspect-with-reviewed"

def test_compute_review_state_basic():
    class MockItem:
        def __init__(self, uid, reviewed=True, cleared=True, links=None):
            self.uid = uid
            self.reviewed = reviewed
            self.cleared = cleared
            self.links = links or []

    all_items = {
        "REQ-001": MockItem("REQ-001", reviewed=False),
        "SPEC-001": MockItem("SPEC-001", links=["REQ-001"], cleared=False),
    }
    
    state = compute_review_state(all_items, {}, {})
    
    assert "REQ-001" in state.unreviewed_nodes
    assert "SPEC-001" in state.suspect_causes
    assert state.get_status("SPEC-001") == "⚠️ suspect-with-unreviewed"
    assert state.get_status("REQ-001") == "📋 unreviewed"

def test_compute_review_state_gherkin_mismatch():
    class MockItem:
        def __init__(self, uid, gherkin_fingerprints=None):
            self.uid = uid
            self.reviewed = True
            self.cleared = True
            self.links = []
            self.gherkin_fingerprints = gherkin_fingerprints

    # Expected fingerprints in YAML
    item = MockItem("SPEC-001", gherkin_fingerprints=[{"feat.feature": "hash1"}])
    all_items = {"SPEC-001": item}
    
    # Actual fingerprints (mismatch)
    actual_fps = {"SPEC-001": [{"feat.feature": "hash2"}]}
    
    # Feature file is unreviewed
    feature_file_states = {"feat.feature": True}
    
    state = compute_review_state(all_items, actual_fps, {}, feature_file_states)
    
    assert "feat.feature" in state.unreviewed_nodes
    assert "feat.feature" in state.suspect_causes["SPEC-001"]
    assert state.get_status("SPEC-001") == "⚠️ suspect-with-unreviewed"
