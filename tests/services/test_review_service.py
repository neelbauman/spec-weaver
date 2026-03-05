from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from spec_weaver.services.review_service import ReviewService


@pytest.fixture
def review_service():
    return ReviewService()


@pytest.fixture
def mock_repo_root():
    return Path("/mock/repo")


@patch("spec_weaver.services.review_service.get_item_map")
@patch("spec_weaver.services.review_service.get_doorstop_tree")
def test_run_review_doorstop_item_success(
    mock_get_doorstop_tree,
    mock_get_item_map,
    review_service,
    mock_repo_root,
):
    mock_item = MagicMock()
    mock_get_item_map.return_value = {"SPEC-001": mock_item}
    mock_multi_tree = MagicMock()
    mock_multi_tree.find_item.return_value = mock_item
    mock_get_doorstop_tree.return_value = mock_multi_tree

    result = review_service.run_review("SPEC-001", mock_repo_root)

    assert result.is_success is True
    assert result.target_type == "doorstop"
    assert result.item_id == "SPEC-001"
    mock_item.review.assert_called_once()
    mock_item.save.assert_called_once()


@patch("spec_weaver.services.review_service.get_item_map")
@patch("spec_weaver.services.review_service.get_doorstop_tree")
def test_run_review_doorstop_item_failure(
    mock_get_doorstop_tree,
    mock_get_item_map,
    review_service,
    mock_repo_root,
):
    mock_item = MagicMock()
    mock_item.review.side_effect = Exception("review failed")
    mock_get_item_map.return_value = {"SPEC-001": mock_item}
    mock_multi_tree = MagicMock()
    mock_multi_tree.find_item.return_value = mock_item
    mock_get_doorstop_tree.return_value = mock_multi_tree

    result = review_service.run_review("SPEC-001", mock_repo_root)

    assert result.is_success is False
    assert result.target_type == "doorstop"
    assert "review failed" in result.error_message


@patch("spec_weaver.services.review_service.get_item_map")
def test_run_review_item_not_found(
    mock_get_item_map,
    review_service,
    mock_repo_root,
):
    mock_get_item_map.return_value = {}

    result = review_service.run_review("NONEXISTENT-999", mock_repo_root)

    assert result.is_success is False
    assert result.target_type == "doorstop"
    assert "見つかりません" in result.error_message
