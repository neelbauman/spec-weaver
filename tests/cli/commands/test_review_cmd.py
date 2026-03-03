"""review コマンドと clear コマンドのユニットテスト。"""

import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from spec_weaver.cli.main import app
from spec_weaver.adapters.gherkin import read_stored_fingerprints, _FINGERPRINT_PREFIX
from spec_weaver.services.review_service import ReviewResult
from spec_weaver.services.clear_service import ClearResult

runner = CliRunner()


# ---------------------------------------------------------------------------
# review コマンド
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.commands.review_cmd.ReviewService")
@patch("spec_weaver.cli.commands.review_cmd._audit_cmd")
def test_review_feature_success(mock_audit, mock_service_class, tmp_path):
    """review コマンドが正常終了する。"""
    mock_service = mock_service_class.return_value
    mock_service.run_review.return_value = ReviewResult(
        is_success=True, target_type="feature", fingerprint="dummy_fp"
    )
    
    feature_file = tmp_path / "test.feature"
    feature_file.write_text("Feature: test", encoding="utf-8")

    result = runner.invoke(app, ["review", str(feature_file)])

    assert result.exit_code == 0
    assert "フィンガープリントを書き込みました" in result.output
    mock_audit.assert_called_once()


@patch("spec_weaver.cli.commands.review_cmd.ReviewService")
def test_review_nonexistent_file_returns_exit_1(mock_service_class):
    """.feature ファイルが存在しない場合は終了コード 1 を返す。"""
    mock_service = mock_service_class.return_value
    mock_service.run_review.return_value = ReviewResult(
        is_success=False, target_type="unknown", error_message="Not found"
    )
    
    result = runner.invoke(app, ["review", "nonexistent.feature"])
    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# clear コマンド
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.commands.clear_cmd.ClearService")
def test_clear_feature_file_success(mock_service_class, tmp_path):
    """.feature ファイルを指定した場合の正常系。"""
    mock_service = mock_service_class.return_value
    mock_service.run_clear.return_value = ClearResult(
        is_success=True, updated_items=["SPEC-001", "SPEC-002"]
    )
    
    feature_file = tmp_path / "test.feature"
    feature_file.write_text("Feature: test", encoding="utf-8")

    result = runner.invoke(app, ["clear", str(feature_file), "--repo-root", str(tmp_path)])

    assert result.exit_code == 0
    assert "SPEC-001" in result.output
    assert "SPEC-002" in result.output


@patch("spec_weaver.cli.commands.clear_cmd.ClearService")
def test_clear_single_item_success(mock_service_class, tmp_path):
    """アイテムIDを指定した場合の正常系。"""
    mock_service = mock_service_class.return_value
    mock_service.run_clear.return_value = ClearResult(
        is_success=True, updated_items=["SPEC-001"]
    )

    result = runner.invoke(app, [
        "clear", "SPEC-001",
        "--repo-root", str(tmp_path),
    ])

    assert result.exit_code == 0
    assert "SPEC-001" in result.output


@patch("spec_weaver.cli.commands.clear_cmd.ClearService")
def test_clear_error_returns_exit_1(mock_service_class, tmp_path):
    """エラーが発生した場合は終了コード 1 を返す。"""
    mock_service = mock_service_class.return_value
    mock_service.run_clear.return_value = ClearResult(
        is_success=False, error_message="Some error"
    )

    result = runner.invoke(app, [
        "clear", "SPEC-999",
        "--repo-root", str(tmp_path),
    ])

    assert result.exit_code == 1
    assert "Some error" in result.output
