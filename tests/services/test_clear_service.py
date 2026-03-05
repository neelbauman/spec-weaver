from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from spec_weaver.services.clear_service import ClearService


@pytest.fixture
def mock_repo_root():
    return Path("/mock/repo")


@pytest.fixture
def mock_feature_dir():
    return Path("/mock/repo/features")


@pytest.fixture
def clear_service():
    return ClearService()


@patch("spec_weaver.services.clear_service.compute_review_state")
@patch("spec_weaver.services.clear_service.AuditService")
@patch("spec_weaver.services.clear_service.get_tag_map")
@patch("spec_weaver.services.clear_service.get_spec_fingerprints")
@patch("spec_weaver.services.clear_service.get_item_map")
@patch("spec_weaver.services.clear_service.get_all_prefixes")
def test_run_clear_item_unreviewed_blocks(
    mock_get_all_prefixes,
    mock_get_item_map,
    mock_get_spec_fingerprints,
    mock_get_tag_map,
    mock_audit_service_cls,
    mock_compute_review_state,
    clear_service,
    mock_repo_root,
    mock_feature_dir,
):
    mock_get_all_prefixes.return_value = {"SPEC"}
    mock_get_item_map.return_value = {"SPEC-001": MagicMock()}
    mock_get_spec_fingerprints.return_value = {}

    mock_review_state = MagicMock()
    mock_review_state.unreviewed_nodes = {"SPEC-001"}
    mock_review_state.get_status.return_value = "❌ unreviewed"
    mock_compute_review_state.return_value = mock_review_state

    result = clear_service.run_clear("SPEC-001", mock_feature_dir, mock_repo_root)

    assert result.is_success is False
    assert "SPEC-001" in result.skipped_unreviewed
    assert "は未レビューです" in result.error_message


@patch("spec_weaver.services.clear_service.compute_review_state")
@patch("spec_weaver.services.clear_service.AuditService")
@patch("spec_weaver.services.clear_service.get_tag_map")
@patch("spec_weaver.services.clear_service.get_spec_fingerprints")
@patch("spec_weaver.services.clear_service.get_item_map")
@patch("spec_weaver.services.clear_service.get_all_prefixes")
def test_run_clear_item_suspect_unreviewed_blocks(
    mock_get_all_prefixes,
    mock_get_item_map,
    mock_get_spec_fingerprints,
    mock_get_tag_map,
    mock_audit_service_cls,
    mock_compute_review_state,
    clear_service,
    mock_repo_root,
    mock_feature_dir,
):
    mock_get_all_prefixes.return_value = {"SPEC"}
    mock_get_item_map.return_value = {"SPEC-001": MagicMock()}
    mock_get_spec_fingerprints.return_value = {}

    mock_review_state = MagicMock()
    mock_review_state.unreviewed_nodes = set()
    mock_review_state.get_status.return_value = "⚠️ suspect-with-unreviewed"
    mock_compute_review_state.return_value = mock_review_state

    result = clear_service.run_clear("SPEC-001", mock_feature_dir, mock_repo_root)

    assert result.is_success is False
    assert "SPEC-001" in result.skipped_suspect_unreviewed
    assert "上位アイテムが未レビューです" in result.error_message


@patch("spec_weaver.services.clear_service.compute_review_state")
@patch("spec_weaver.services.clear_service.AuditService")
@patch("spec_weaver.services.clear_service.get_tag_map")
@patch("spec_weaver.services.clear_service.get_spec_fingerprints")
@patch("spec_weaver.services.clear_service.get_item_map")
@patch("spec_weaver.services.clear_service.get_all_prefixes")
def test_run_clear_not_found(
    mock_get_all_prefixes,
    mock_get_item_map,
    mock_get_spec_fingerprints,
    mock_get_tag_map,
    mock_audit_service_cls,
    mock_compute_review_state,
    clear_service,
    mock_repo_root,
    mock_feature_dir,
):
    mock_get_all_prefixes.return_value = {"SPEC"}
    mock_get_item_map.return_value = {"SPEC-001": MagicMock()}

    result = clear_service.run_clear("SPEC-999", mock_feature_dir, mock_repo_root)

    assert result.is_success is False
    assert "見つかりません" in result.error_message
