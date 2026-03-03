import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from spec_weaver.services.clear_service import ClearService, ClearResult

@pytest.fixture
def mock_repo_root():
    return Path("/mock/repo")

@pytest.fixture
def mock_feature_dir():
    return Path("/mock/repo/features")

@pytest.fixture
def clear_service():
    return ClearService()

@patch("spec_weaver.services.clear_service.get_tags")
@patch("spec_weaver.services.clear_service.compute_review_state")
@patch("spec_weaver.services.clear_service.AuditService")
@patch("spec_weaver.services.clear_service.get_tag_map")
@patch("spec_weaver.services.clear_service.get_spec_fingerprints")
@patch("spec_weaver.services.clear_service.get_item_map")
@patch("spec_weaver.services.clear_service.get_all_prefixes")
def test_run_clear_feature_file_success(
    mock_get_all_prefixes,
    mock_get_item_map,
    mock_get_spec_fingerprints,
    mock_get_tag_map,
    mock_audit_service_cls,
    mock_compute_review_state,
    mock_get_tags,
    clear_service,
    mock_repo_root,
    mock_feature_dir
):
    mock_get_all_prefixes.return_value = {"SPEC"}
    mock_get_item_map.return_value = {"SPEC-001": MagicMock()}
    mock_get_spec_fingerprints.return_value = {"SPEC-001": ["hash"]}
    
    mock_review_state = MagicMock()
    mock_review_state.unreviewed_nodes = set()
    mock_review_state.get_status.return_value = "✅ reviewed"
    mock_compute_review_state.return_value = mock_review_state

    mock_get_tags.return_value = {"SPEC-001"}

    # Mock Path to say it's a file and exists
    with patch("spec_weaver.services.clear_service.Path") as mock_path_cls:
        mock_path_obj = MagicMock()
        mock_path_obj.suffix = ".feature"
        mock_path_obj.exists.return_value = True
        mock_path_cls.return_value = mock_path_obj
        
        with patch("spec_weaver.services.clear_service.update_item_attribute") as mock_update:
            with patch("spec_weaver.services.clear_service.clear_doorstop_suspects") as mock_doorstop_clear:
                
                mock_doorstop_clear.return_value = True

                result = clear_service.run_clear("dummy.feature", mock_feature_dir, mock_repo_root)

                assert result.is_success is True
                assert "SPEC-001" in result.updated_items
                mock_update.assert_called_once_with(mock_repo_root, "SPEC-001", "gherkin_fingerprints", ["hash"])
                mock_doorstop_clear.assert_called_once_with(mock_repo_root, "SPEC-001")


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
    mock_feature_dir
):
    mock_get_all_prefixes.return_value = {"SPEC"}
    mock_get_item_map.return_value = {"SPEC-001": MagicMock()}
    mock_get_spec_fingerprints.return_value = {}
    
    mock_review_state = MagicMock()
    mock_review_state.unreviewed_nodes = {"SPEC-001"}
    mock_review_state.get_status.return_value = "❌ unreviewed"
    mock_compute_review_state.return_value = mock_review_state

    # Not a .feature file, acts as item ID
    with patch("spec_weaver.services.clear_service.Path") as mock_path_cls:
        mock_path_obj = MagicMock()
        mock_path_obj.suffix = ""
        mock_path_cls.return_value = mock_path_obj
        
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
    mock_feature_dir
):
    mock_get_all_prefixes.return_value = {"SPEC"}
    mock_get_item_map.return_value = {"SPEC-001": MagicMock()}
    mock_get_spec_fingerprints.return_value = {}
    
    mock_review_state = MagicMock()
    mock_review_state.unreviewed_nodes = set()
    mock_review_state.get_status.return_value = "⚠️ suspect-with-unreviewed"
    mock_compute_review_state.return_value = mock_review_state

    # Not a .feature file, acts as item ID
    with patch("spec_weaver.services.clear_service.Path") as mock_path_cls:
        mock_path_obj = MagicMock()
        mock_path_obj.suffix = ""
        mock_path_cls.return_value = mock_path_obj
        
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
    mock_feature_dir
):
    mock_get_all_prefixes.return_value = {"SPEC"}
    mock_get_item_map.return_value = {"SPEC-001": MagicMock()}

    # Not a .feature file, acts as item ID
    with patch("spec_weaver.services.clear_service.Path") as mock_path_cls:
        mock_path_obj = MagicMock()
        mock_path_obj.suffix = ""
        mock_path_cls.return_value = mock_path_obj
        
        result = clear_service.run_clear("SPEC-999", mock_feature_dir, mock_repo_root)

        assert result.is_success is False
        assert "見つかりません" in result.error_message
