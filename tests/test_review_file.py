
import pytest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from spec_weaver.cli import app
from pathlib import Path

runner = CliRunner()

@patch("spec_weaver.cli.get_all_prefixes")
@patch("spec_weaver.cli.get_tags")
@patch("spec_weaver.cli.get_spec_fingerprints")
@patch("spec_weaver.cli.update_item_attribute")
def test_review_feature_file(
    mock_update, mock_get_fp, mock_get_tags, mock_get_prefixes, tmp_path
):
    # Setup
    feature_file = tmp_path / "test.feature"
    feature_file.write_text("Feature: test")
    
    mock_get_prefixes.return_value = {"SPEC"}
    mock_get_tags.return_value = {"SPEC-001", "SPEC-002"}
    mock_get_fp.return_value = {
        "SPEC-001": "hash1",
        "SPEC-002": "hash2",
        "SPEC-003": "hash3",
    }
    
    # Execute
    result = runner.invoke(app, ["review", str(feature_file), "--repo-root", str(tmp_path)])
    
    # Verify
    assert result.exit_code == 0
    assert "SPEC-001 のフィンガープリントを更新しました" in result.stdout
    assert "SPEC-002 のフィンガープリントを更新しました" in result.stdout
    assert "SPEC-003" not in result.stdout
    
    assert mock_update.call_count == 2
    mock_update.assert_any_call(Path(str(tmp_path)), "SPEC-001", "test_fingerprint", "hash1")
    mock_update.assert_any_call(Path(str(tmp_path)), "SPEC-002", "test_fingerprint", "hash2")

@patch("spec_weaver.cli.get_all_prefixes")
@patch("spec_weaver.cli.get_spec_fingerprints")
@patch("spec_weaver.cli.update_item_attribute")
def test_review_single_item(
    mock_update, mock_get_fp, mock_get_prefixes, tmp_path
):
    # Setup
    mock_get_prefixes.return_value = {"SPEC"}
    mock_get_fp.return_value = {
        "SPEC-001": "hash1",
    }
    
    # Execute (non-existent file, so it's treated as item ID)
    result = runner.invoke(app, ["review", "SPEC-001", "--repo-root", str(tmp_path)])
    
    # Verify
    assert result.exit_code == 0
    assert "SPEC-001 のフィンガープリントを更新しました" in result.stdout
    mock_update.assert_called_once_with(Path(str(tmp_path)), "SPEC-001", "test_fingerprint", "hash1")
