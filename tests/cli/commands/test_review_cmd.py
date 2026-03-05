"""review コマンドと clear コマンドのユニットテスト。"""

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from spec_weaver.cli.main import app
from spec_weaver.services.clear_service import ClearResult
from spec_weaver.services.review_service import ReviewResult

runner = CliRunner()


# ---------------------------------------------------------------------------
# review コマンド
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.commands.review_cmd.StatusService")
@patch("spec_weaver.cli.commands.review_cmd._audit_cmd")
@patch("spec_weaver.cli.commands.review_cmd.ReviewService")
@patch("spec_weaver.cli.commands.review_cmd.get_item_map")
def test_review_item_success_no_edit(mock_get_item_map, mock_service_class, mock_audit, mock_status_service, tmp_path):
    """--no-edit でアイテムを正常にレビューできる。"""
    mock_status_report = MagicMock()
    mock_status_report.review_state.get_status.return_value = "unreviewed"
    mock_status_service.return_value.get_status_report.return_value = mock_status_report

    mock_item = MagicMock()
    mock_item.path = str(tmp_path / "specs" / "QA-001.yml")
    mock_get_item_map.return_value = {"QA-001": mock_item}

    mock_service = mock_service_class.return_value
    mock_service.run_review.return_value = ReviewResult(
        is_success=True, target_type="doorstop", item_id="QA-001"
    )

    result = runner.invoke(app, ["review", "QA-001", "--no-edit", "--repo-root", str(tmp_path)])

    assert result.exit_code == 0
    assert "QA-001" in result.output
    mock_audit.assert_called_once()


@patch("spec_weaver.cli.commands.review_cmd.get_item_map")
def test_review_item_not_found(mock_get_item_map, tmp_path):
    """存在しないアイテムIDを指定するとエラーになる。"""
    mock_get_item_map.return_value = {}

    result = runner.invoke(app, ["review", "NONEXISTENT-999", "--no-edit", "--repo-root", str(tmp_path)])

    assert result.exit_code == 1
    assert "見つかりません" in result.output


def test_review_no_args(tmp_path):
    """引数も --all も指定しないとエラーになる。"""
    result = runner.invoke(app, ["review", "--repo-root", str(tmp_path)])
    assert result.exit_code == 1


def test_review_all_and_id_conflict(tmp_path):
    """--all と対象IDを同時に指定するとエラーになる。"""
    result = runner.invoke(app, ["review", "--all", "QA-001", "--repo-root", str(tmp_path)])
    assert result.exit_code == 1


@patch("spec_weaver.cli.commands.review_cmd._audit_cmd")
@patch("spec_weaver.cli.commands.review_cmd.ReviewService")
def test_review_all_success(mock_service_class, mock_audit, tmp_path):
    """--all で全アイテムを一括レビューできる。"""
    mock_service = mock_service_class.return_value
    mock_service.run_review_all_items.return_value = (["SPEC-001", "SPEC-002"], [])

    result = runner.invoke(app, ["review", "--all", "--repo-root", str(tmp_path)])

    assert result.exit_code == 0
    assert "2" in result.output
    mock_audit.assert_called_once()


# ---------------------------------------------------------------------------
# clear コマンド
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.commands.clear_cmd.ClearService")
@patch("spec_weaver.cli.commands.clear_cmd.get_item_map")
def test_clear_single_item_success_no_edit(mock_get_item_map, mock_service_class, tmp_path):
    """--no-edit でアイテムIDを指定した場合の正常系。"""
    mock_item = MagicMock()
    mock_item.path = str(tmp_path / "specs" / "SPEC-001.yml")
    mock_get_item_map.return_value = {"SPEC-001": mock_item}

    mock_service = mock_service_class.return_value
    mock_service.run_clear.return_value = ClearResult(
        is_success=True, updated_items=["SPEC-001"]
    )

    result = runner.invoke(app, [
        "clear", "SPEC-001", "--no-edit",
        "--repo-root", str(tmp_path),
    ])

    assert result.exit_code == 0
    assert "SPEC-001" in result.output


@patch("spec_weaver.cli.commands.clear_cmd.get_item_map")
def test_clear_item_not_found(mock_get_item_map, tmp_path):
    """存在しないアイテムIDを指定するとエラーになる。"""
    mock_get_item_map.return_value = {}

    result = runner.invoke(app, [
        "clear", "SPEC-999", "--no-edit",
        "--repo-root", str(tmp_path),
    ])

    assert result.exit_code == 1
    assert "見つかりません" in result.output


@patch("spec_weaver.cli.commands.clear_cmd.StatusService")
@patch("spec_weaver.cli.commands.clear_cmd.ClearService")
@patch("spec_weaver.cli.commands.clear_cmd.get_item_map")
def test_clear_service_error(mock_get_item_map, mock_service_class, mock_status_service, tmp_path):
    """サービスがエラーを返した場合は終了コード 1 を返す。"""
    mock_status_report = MagicMock()
    mock_status_report.review_state.get_status.return_value = "suspect"
    mock_status_service.return_value.get_status_report.return_value = mock_status_report

    mock_item = MagicMock()
    mock_item.path = str(tmp_path / "specs" / "SPEC-001.yml")
    mock_get_item_map.return_value = {"SPEC-001": mock_item}

    mock_service = mock_service_class.return_value
    mock_service.run_clear.return_value = ClearResult(
        is_success=False, error_message="Some error"
    )

    result = runner.invoke(app, [
        "clear", "SPEC-001", "--no-edit",
        "--repo-root", str(tmp_path),
    ])

    assert result.exit_code == 1
    assert "Some error" in result.output


def test_clear_all_and_id_conflict(tmp_path):
    """--all と対象IDを同時に指定するとエラーになる。"""
    result = runner.invoke(app, ["clear", "--all", "SPEC-001", "--repo-root", str(tmp_path)])
    assert result.exit_code == 1
