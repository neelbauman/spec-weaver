import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from spec_weaver.services.status_service import StatusService, StatusReport

@pytest.fixture
def mock_repo_root():
    return Path("/mock/repo")

@pytest.fixture
def mock_feature_dir():
    return Path("/mock/repo/features")

@pytest.fixture
def status_service():
    return StatusService()

def _make_mock_item(uid: str, active: bool = True, custom_status: str | None = None):
    item = MagicMock()
    item.uid = uid
    item.header = uid
    item.active = active
    item.get.return_value = custom_status
    return item

@patch("spec_weaver.services.status_service.get_item_map")
@patch("spec_weaver.services.status_service.get_all_prefixes")
@patch("spec_weaver.services.status_service.get_spec_fingerprints")
@patch("spec_weaver.services.status_service.get_tag_map")
@patch("spec_weaver.services.status_service.AuditService")
@patch("spec_weaver.services.status_service.compute_review_state")
@patch("spec_weaver.services.status_service.check_behave_steps")
def test_get_status_report_success(
    mock_check_behave_steps,
    mock_compute_review_state,
    mock_audit_service_cls,
    mock_get_tag_map,
    mock_get_spec_fingerprints,
    mock_get_all_prefixes,
    mock_get_item_map,
    status_service,
    mock_repo_root,
    mock_feature_dir
):
    # Setup mocks
    mock_get_all_prefixes.return_value = {"REQ", "SPEC"}
    mock_item_req = _make_mock_item("REQ-001", custom_status="draft")
    mock_item_spec = _make_mock_item("SPEC-001", custom_status="implemented")
    mock_get_item_map.return_value = {
        "REQ-001": mock_item_req,
        "SPEC-001": mock_item_spec
    }

    mock_get_spec_fingerprints.return_value = {}
    mock_get_tag_map.return_value = {
        "SPEC-001": [{"file": "login.feature"}]
    }

    mock_review_state = MagicMock()
    mock_review_state.get_status.return_value = "✅ reviewed"
    mock_compute_review_state.return_value = mock_review_state

    mock_check_behave_steps.return_value = (["unused1"], ["undefined1"])

    with patch("spec_weaver.services.status_service._get_custom_attribute") as mock_get_custom:
        def mock_custom_attr(item, key, default):
            if key == "status":
                return item.get()
            return default
        mock_get_custom.side_effect = mock_custom_attr

        # Run
        report = status_service.get_status_report(mock_repo_root, mock_feature_dir)

        # Assert
        assert isinstance(report, StatusReport)
        assert report.total_items_shown == 2
        assert len(report.grouped_items["REQ"]) == 1
        assert len(report.grouped_items["SPEC"]) == 1
        assert report.grouped_items["REQ"][0].uid == "REQ-001"
        assert report.grouped_items["REQ"][0].raw_status == "draft"
        assert len(report.feature_files) == 1
        assert report.feature_files[0].file_path == "login.feature"
        assert report.feature_files[0].related_specs == ["SPEC-001"]
        assert report.unused_step_defs_count == 1
        assert report.undefined_steps_count == 1


@patch("spec_weaver.services.status_service.get_item_map")
@patch("spec_weaver.services.status_service.get_all_prefixes")
@patch("spec_weaver.services.status_service.get_spec_fingerprints")
@patch("spec_weaver.services.status_service.get_tag_map")
@patch("spec_weaver.services.status_service.AuditService")
@patch("spec_weaver.services.status_service.compute_review_state")
def test_get_status_report_with_filter(
    mock_compute_review_state,
    mock_audit_service_cls,
    mock_get_tag_map,
    mock_get_spec_fingerprints,
    mock_get_all_prefixes,
    mock_get_item_map,
    status_service,
    mock_repo_root,
    mock_feature_dir
):
    mock_get_all_prefixes.return_value = {"REQ"}
    mock_item_req1 = _make_mock_item("REQ-001", custom_status="draft")
    mock_item_req2 = _make_mock_item("REQ-002", custom_status="implemented")
    mock_get_item_map.return_value = {
        "REQ-001": mock_item_req1,
        "REQ-002": mock_item_req2
    }

    mock_get_spec_fingerprints.return_value = {}
    mock_get_tag_map.return_value = {}
    mock_compute_review_state.return_value = MagicMock()

    with patch("spec_weaver.services.status_service._get_custom_attribute") as mock_get_custom:
        def mock_custom_attr(item, key, default):
            if key == "status":
                return item.get()
            return default
        mock_get_custom.side_effect = mock_custom_attr

        # Run with filter
        report = status_service.get_status_report(mock_repo_root, mock_feature_dir, filter_status="implemented")

        # Assert
        assert report.total_items_shown == 1
        assert len(report.grouped_items["REQ"]) == 1
        assert report.grouped_items["REQ"][0].uid == "REQ-002"
        # feature_files are not populated when filtering
        assert len(report.feature_files) == 0
