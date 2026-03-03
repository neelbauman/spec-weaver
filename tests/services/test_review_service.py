import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import subprocess

from spec_weaver.services.review_service import ReviewService, ReviewResult

@pytest.fixture
def review_service():
    return ReviewService()

@pytest.fixture
def mock_repo_root():
    return Path("/mock/repo")

@pytest.fixture
def mock_feature_dir():
    return Path("/mock/repo/features")

@patch("spec_weaver.services.review_service.get_item_map")
@patch("spec_weaver.services.review_service.get_all_prefixes")
@patch("spec_weaver.services.review_service.get_tag_map")
@patch("spec_weaver.services.review_service.compute_feature_file_hash")
@patch("spec_weaver.services.review_service.write_feature_fingerprints")
def test_run_review_feature_file(
    mock_write_feature_fingerprints,
    mock_compute_feature_file_hash,
    mock_get_tag_map,
    mock_get_all_prefixes,
    mock_get_item_map,
    review_service,
    mock_repo_root,
    mock_feature_dir
):
    target_path = "login.feature"
    mock_compute_feature_file_hash.return_value = "new_hash"
    mock_get_all_prefixes.return_value = {"SPEC"}
    
    # Mock tags to simulate "login.feature" having "SPEC-001"
    mock_get_tag_map.return_value = {
        "SPEC-001": [{"file": "login.feature"}]
    }
    
    mock_item = MagicMock()
    mock_item.stamp.return_value = "item_hash"
    mock_get_item_map.return_value = {"SPEC-001": mock_item}

    with patch("spec_weaver.services.review_service.Path") as mock_path_cls:
        mock_path_obj = MagicMock()
        mock_path_obj.exists.return_value = True
        mock_path_obj.suffix = ".feature"
        # Mock resolve to match equality check
        mock_path_obj.resolve.return_value = "resolved_login.feature"
        mock_path_cls.return_value = mock_path_obj
        
        # We need to intercept Path(s["file"]).resolve() inside the loop as well
        with patch("spec_weaver.services.review_service.Path", return_value=mock_path_obj):
            result = review_service.run_review(target_path, mock_feature_dir, mock_repo_root)

            assert result.is_success is True
            assert result.target_type == "feature"
            assert result.fingerprint == "new_hash"
            assert result.linked_items == {"SPEC-001": "item_hash"}
            mock_write_feature_fingerprints.assert_called_once_with(mock_path_obj, "new_hash", {"SPEC-001": "item_hash"})

@patch("spec_weaver.services.review_service.get_item_map")
@patch("spec_weaver.services.review_service.subprocess.run")
def test_run_review_doorstop_item_success(
    mock_subprocess_run,
    mock_get_item_map,
    review_service,
    mock_repo_root,
    mock_feature_dir
):
    mock_get_item_map.return_value = {"SPEC-001": MagicMock()}

    with patch("spec_weaver.services.review_service.Path") as mock_path_cls:
        mock_path_obj = MagicMock()
        mock_path_obj.exists.return_value = False
        mock_path_obj.suffix = ""
        mock_path_cls.return_value = mock_path_obj
        
        result = review_service.run_review("SPEC-001", mock_feature_dir, mock_repo_root)

        assert result.is_success is True
        assert result.target_type == "doorstop"
        assert result.item_id == "SPEC-001"
        mock_subprocess_run.assert_called_once_with(
            ["doorstop", "review", "-i", "SPEC-001", "-f", "-j", str(mock_repo_root)],
            check=True, capture_output=True
        )

@patch("spec_weaver.services.review_service.get_item_map")
@patch("spec_weaver.services.review_service.subprocess.run")
def test_run_review_doorstop_item_failure(
    mock_subprocess_run,
    mock_get_item_map,
    review_service,
    mock_repo_root,
    mock_feature_dir
):
    mock_get_item_map.return_value = {"SPEC-001": MagicMock()}
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd=[], stderr=b"doorstop error"
    )

    with patch("spec_weaver.services.review_service.Path") as mock_path_cls:
        mock_path_obj = MagicMock()
        mock_path_obj.exists.return_value = False
        mock_path_obj.suffix = ""
        mock_path_cls.return_value = mock_path_obj
        
        result = review_service.run_review("SPEC-001", mock_feature_dir, mock_repo_root)

        assert result.is_success is False
        assert result.target_type == "doorstop"
        assert "doorstop error" in result.error_message

def test_run_review_unknown_target(
    review_service,
    mock_repo_root,
    mock_feature_dir
):
    with patch("spec_weaver.services.review_service.Path") as mock_path_cls:
        mock_path_obj = MagicMock()
        mock_path_obj.exists.return_value = False
        mock_path_obj.suffix = ""
        mock_path_cls.return_value = mock_path_obj
        
        with patch("spec_weaver.services.review_service.get_item_map", return_value={}):
            result = review_service.run_review("unknown-target", mock_feature_dir, mock_repo_root)

            assert result.is_success is False
            assert result.target_type == "unknown"
            assert "ターゲットが見つかりません" in result.error_message
