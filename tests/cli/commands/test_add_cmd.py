from unittest.mock import patch

from typer.testing import CliRunner

from spec_weaver.cli.main import app
from spec_weaver.services.bdd_service import ImportResult

runner = CliRunner()


@patch("spec_weaver.services.bdd_service._create_bdd_item")
def test_add_cmd_import_feature(mock_create, tmp_path):
    """既存 .feature ファイルを BDD アイテムに取り込む。"""
    mock_create.return_value = "BDD-001"

    feature = tmp_path / "audit.feature"
    feature.write_text(
        "@QA-001\nFeature: 監査コマンド\n  Scenario: テスト\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["add", str(feature)])

    assert result.exit_code == 0
    assert "BDD-001" in result.output


@patch("spec_weaver.services.bdd_service._create_bdd_item")
def test_add_cmd_create_new(mock_create, tmp_path):
    """--slug で新規 BDD アイテムを作成する。"""
    mock_create.return_value = "BDD-002"

    result = runner.invoke(
        app, ["add", "--slug", "monitoring", "--link", "QA-003"]
    )

    assert result.exit_code == 0
    assert "BDD-002" in result.output


def test_add_cmd_no_args():
    """引数なしの場合はエラー。"""
    result = runner.invoke(app, ["add"])

    assert result.exit_code == 1
    assert "指定してください" in result.output


@patch("spec_weaver.services.bdd_service._create_bdd_item")
def test_add_cmd_file_not_found(mock_create):
    """存在しないファイルを指定するとエラー。"""
    result = runner.invoke(app, ["add", "/nonexistent/file.feature"])

    assert result.exit_code == 1
    assert "見つかりません" in result.output
    mock_create.assert_not_called()
