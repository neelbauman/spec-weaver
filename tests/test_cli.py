from unittest.mock import patch
from typer.testing import CliRunner
from spec_weaver.cli import app

runner = CliRunner()

@patch("spec_weaver.cli.get_tags")
@patch("spec_weaver.cli.get_specs")
def test_audit_perfect_match(mock_get_specs, mock_get_tags, tmp_path):
    # 仕様とテストが完全に一致する状態
    mock_get_specs.return_value = {"SPEC-001", "SPEC-002"}
    mock_get_tags.return_value = {"SPEC-001", "SPEC-002"}

    # 実行
    result = runner.invoke(app, ["audit", str(tmp_path), "--repo-root", str(tmp_path)])

    # 終了コード0（成功）で、成功メッセージが含まれているか
    assert result.exit_code == 0
    assert "完璧です！" in result.stdout

@patch("spec_weaver.cli.get_tags")
@patch("spec_weaver.cli.get_specs")
def test_audit_with_errors(mock_get_specs, mock_get_tags, tmp_path):
    # 乖離がある状態
    mock_get_specs.return_value = {"SPEC-001", "SPEC-002"} # SPEC-002 がテスト漏れ
    mock_get_tags.return_value = {"SPEC-001", "SPEC-003"}  # SPEC-003 が孤児タグ

    result = runner.invoke(app, ["audit", str(tmp_path), "--repo-root", str(tmp_path)])

    # 終了コード1（失敗）で、それぞれの警告が出力されているか
    assert result.exit_code == 1
    assert "テストが実装されていない仕様" in result.stdout
    assert "SPEC-002" in result.stdout
    assert "仕様書に存在しない孤児タグ" in result.stdout
    assert "@SPEC-003" in result.stdout
