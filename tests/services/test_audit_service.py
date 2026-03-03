import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from datetime import date

from spec_weaver.services.audit_service import AuditService, AuditReport

@pytest.fixture
def mock_repo_root():
    return Path("/mock/repo")

@pytest.fixture
def mock_feature_dir():
    return Path("/mock/repo/features")

@pytest.fixture
def audit_service():
    return AuditService()

def _make_mock_item(uid: str, active: bool = True, testable: bool = True, custom_attrs: dict | None = None):
    item = MagicMock()
    item.uid = uid
    item.active = active
    if custom_attrs is None:
        custom_attrs = {}
    
    def _get(key, default=None):
        if key == "testable":
            return testable
        return custom_attrs.get(key, default)

    item.get.side_effect = _get
    return item

@patch("spec_weaver.services.audit_service.get_specs")
@patch("spec_weaver.services.audit_service.get_all_prefixes")
@patch("spec_weaver.services.audit_service.get_item_map")
@patch("spec_weaver.services.audit_service.get_tags")
@patch("spec_weaver.services.audit_service.get_tag_map")
@patch("spec_weaver.services.audit_service.get_spec_fingerprints")
@patch("spec_weaver.services.audit_service.compute_review_state")
@patch("spec_weaver.services.audit_service.check_behave_steps")
def test_run_audit_success_no_issues(
    mock_check_behave_steps,
    mock_compute_review_state,
    mock_get_spec_fingerprints,
    mock_get_tag_map,
    mock_get_tags,
    mock_get_item_map,
    mock_get_all_prefixes,
    mock_get_specs,
    audit_service,
    mock_repo_root,
    mock_feature_dir
):
    mock_get_specs.return_value = {"SPEC-001"}
    mock_get_all_prefixes.return_value = {"SPEC"}
    
    mock_item = _make_mock_item("SPEC-001", active=True, testable=True)
    mock_get_item_map.return_value = {"SPEC-001": mock_item}
    
    mock_get_tags.return_value = {"SPEC-001"}
    mock_get_tag_map.return_value = {"SPEC-001": [{"file": "login.feature"}]}
    mock_get_spec_fingerprints.return_value = {}

    mock_review_state = MagicMock()
    mock_review_state.unreviewed_nodes = set()
    mock_review_state.get_status.return_value = "✅ reviewed"
    mock_review_state.suspect_causes = {}
    mock_review_state.parents = {}
    mock_compute_review_state.return_value = mock_review_state

    mock_check_behave_steps.return_value = (set(), set())

    # We mock _compute_feature_file_states to avoid filesystem hits
    with patch.object(AuditService, "_compute_feature_file_states", return_value={}):
        report = audit_service.run_audit(
            feature_dir=mock_feature_dir,
            repo_root=mock_repo_root,
            check_impl=False
        )

        assert report.is_success is True
        assert report.specs_count == 1
        assert not report.inactive_testable
        assert not report.untested_specs
        assert not report.orphaned_tags
        assert not report.suspect_specs
        assert not report.suspect_features
        assert not report.unreviewed_specs
        assert not report.unreviewed_features
        assert not report.stale_items
        assert not report.broken_refs


@patch("spec_weaver.services.audit_service.get_specs")
@patch("spec_weaver.services.audit_service.get_all_prefixes")
@patch("spec_weaver.services.audit_service.get_item_map")
@patch("spec_weaver.services.audit_service.get_tags")
@patch("spec_weaver.services.audit_service.get_tag_map")
@patch("spec_weaver.services.audit_service.get_spec_fingerprints")
@patch("spec_weaver.services.audit_service.compute_review_state")
@patch("spec_weaver.services.audit_service.check_behave_steps")
def test_run_audit_with_issues(
    mock_check_behave_steps,
    mock_compute_review_state,
    mock_get_spec_fingerprints,
    mock_get_tag_map,
    mock_get_tags,
    mock_get_item_map,
    mock_get_all_prefixes,
    mock_get_specs,
    audit_service,
    mock_repo_root,
    mock_feature_dir
):
    mock_get_specs.return_value = {"SPEC-001"}
    mock_get_all_prefixes.return_value = {"SPEC"}
    
    mock_item = _make_mock_item("SPEC-001", active=True, testable=True)
    mock_get_item_map.return_value = {"SPEC-001": mock_item}
    
    # Missing tag SPEC-001 -> untested, extra tag SPEC-002 -> orphaned
    mock_get_tags.return_value = {"SPEC-002"}
    mock_get_tag_map.return_value = {"SPEC-002": [{"file": "login.feature"}]}
    mock_get_spec_fingerprints.return_value = {}

    mock_review_state = MagicMock()
    # SPEC-001 is unreviewed
    mock_review_state.unreviewed_nodes = {"SPEC-001", "login.feature"}
    mock_review_state.get_status.return_value = "❌ unreviewed"
    mock_review_state.suspect_causes = {}
    mock_review_state.parents = {}
    mock_compute_review_state.return_value = mock_review_state

    mock_check_behave_steps.return_value = ({"unused"}, {"undefined"})

    with patch.object(AuditService, "_compute_feature_file_states", return_value={}):
        report = audit_service.run_audit(
            feature_dir=mock_feature_dir,
            repo_root=mock_repo_root,
            check_impl=False
        )

        assert report.is_success is False
        assert "SPEC-001" in report.untested_specs
        assert "SPEC-002" in report.orphaned_tags
        assert "SPEC-001" in report.unreviewed_specs
        assert "login.feature" in report.unreviewed_features
        assert "undefined" in report.undefined_steps
        assert "unused" in report.unused_step_defs
