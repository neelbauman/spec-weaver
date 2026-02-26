from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from spec_weaver.cli import app

runner = CliRunner()


def _make_mock_item(uid: str, suspect: bool = False, status: str | None = None):
    """テスト用のDoorstopアイテムモックを生成する。"""
    item = MagicMock()
    item.uid = uid
    item.suspect = suspect
    item.links = []
    item.header = uid
    # get() で status を返す
    def _get(key, default=None):
        if key == "status":
            return status
        if key == "testable":
            return default
        return default
    item.get.side_effect = _get
    return item


@patch("spec_weaver.cli.get_item_map")
@patch("spec_weaver.cli.get_tags")
@patch("spec_weaver.cli.get_specs")
def test_audit_perfect_match(mock_get_specs, mock_get_tags, mock_get_item_map, tmp_path):
    # 仕様とテストが完全に一致する状態
    mock_get_specs.return_value = {"SPEC-001", "SPEC-002"}
    mock_get_tags.return_value = {"SPEC-001", "SPEC-002"}
    mock_get_item_map.return_value = {
        "SPEC-001": _make_mock_item("SPEC-001"),
        "SPEC-002": _make_mock_item("SPEC-002"),
    }

    # 実行
    result = runner.invoke(app, ["audit", str(tmp_path), "--repo-root", str(tmp_path)])

    # 終了コード0（成功）で、成功メッセージが含まれているか
    assert result.exit_code == 0
    assert "完璧です！" in result.stdout


@patch("spec_weaver.cli.get_item_map")
@patch("spec_weaver.cli.get_tags")
@patch("spec_weaver.cli.get_specs")
def test_audit_with_errors(mock_get_specs, mock_get_tags, mock_get_item_map, tmp_path):
    # 乖離がある状態
    mock_get_specs.return_value = {"SPEC-001", "SPEC-002"}  # SPEC-002 がテスト漏れ
    mock_get_tags.return_value = {"SPEC-001", "SPEC-003"}   # SPEC-003 が孤児タグ
    mock_get_item_map.return_value = {
        "SPEC-001": _make_mock_item("SPEC-001"),
        "SPEC-002": _make_mock_item("SPEC-002"),
    }

    result = runner.invoke(app, ["audit", str(tmp_path), "--repo-root", str(tmp_path)])

    # 終了コード1（失敗）で、それぞれの警告が出力されているか
    assert result.exit_code == 1
    assert "テストが実装されていない仕様" in result.stdout
    assert "SPEC-002" in result.stdout
    assert "仕様書に存在しない孤児タグ" in result.stdout
    assert "@SPEC-003" in result.stdout


@patch("spec_weaver.cli.get_item_map")
@patch("spec_weaver.cli.get_tags")
@patch("spec_weaver.cli.get_specs")
def test_audit_suspect_specs(mock_get_specs, mock_get_tags, mock_get_item_map, tmp_path):
    # SPEC-002 がSuspect状態
    mock_get_specs.return_value = {"SPEC-001", "SPEC-002"}
    mock_get_tags.return_value = {"SPEC-001", "SPEC-002"}
    mock_get_item_map.return_value = {
        "SPEC-001": _make_mock_item("SPEC-001", suspect=False),
        "SPEC-002": _make_mock_item("SPEC-002", suspect=True),
    }

    result = runner.invoke(app, ["audit", str(tmp_path), "--repo-root", str(tmp_path)])

    # Suspectがあれば終了コード1
    assert result.exit_code == 1
    assert "Suspect" in result.stdout
    assert "SPEC-002" in result.stdout
    assert "レビューが必要" in result.stdout


@patch("spec_weaver.cli.get_item_map")
@patch("spec_weaver.cli.get_tags")
@patch("spec_weaver.cli.get_specs")
def test_audit_no_suspect_does_not_report_suspect(
    mock_get_specs, mock_get_tags, mock_get_item_map, tmp_path
):
    # Suspectが1件もない場合はSuspect警告が出ないこと
    mock_get_specs.return_value = {"SPEC-001", "SPEC-002"}
    mock_get_tags.return_value = {"SPEC-001", "SPEC-002"}
    mock_get_item_map.return_value = {
        "SPEC-001": _make_mock_item("SPEC-001"),
        "SPEC-002": _make_mock_item("SPEC-002"),
    }

    result = runner.invoke(app, ["audit", str(tmp_path), "--repo-root", str(tmp_path)])

    assert result.exit_code == 0
    assert "Suspect" not in result.stdout


# ---------------------------------------------------------------------------
# status コマンドのテスト
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.get_item_map")
def test_status_shows_all_items(mock_get_item_map, tmp_path):
    """status コマンドが全アイテムを一覧表示する。"""
    mock_get_item_map.return_value = {
        "REQ-001": _make_mock_item("REQ-001", status="draft"),
        "SPEC-001": _make_mock_item("SPEC-001", status="implemented"),
    }

    result = runner.invoke(app, ["status", "--repo-root", str(tmp_path)])

    assert result.exit_code == 0
    assert "REQ-001" in result.stdout
    assert "SPEC-001" in result.stdout
    assert "draft" in result.stdout
    assert "implemented" in result.stdout


@patch("spec_weaver.cli.get_item_map")
def test_status_filter_by_status(mock_get_item_map, tmp_path):
    """--filter オプションで指定ステータスだけを表示する。"""
    mock_get_item_map.return_value = {
        "REQ-001": _make_mock_item("REQ-001", status="draft"),
        "REQ-002": _make_mock_item("REQ-002", status="implemented"),
        "SPEC-001": _make_mock_item("SPEC-001", status="in-progress"),
    }

    result = runner.invoke(app, ["status", "--repo-root", str(tmp_path), "--filter", "implemented"])

    assert result.exit_code == 0
    assert "REQ-002" in result.stdout
    assert "REQ-001" not in result.stdout
    assert "SPEC-001" not in result.stdout


@patch("spec_weaver.cli.get_item_map")
def test_status_unset_shows_dash(mock_get_item_map, tmp_path):
    """status フィールドが未設定のアイテムは '-' と表示される。"""
    mock_get_item_map.return_value = {
        "SPEC-001": _make_mock_item("SPEC-001", status=None),
    }

    result = runner.invoke(app, ["status", "--repo-root", str(tmp_path)])

    assert result.exit_code == 0
    assert "SPEC-001" in result.stdout
    assert "-" in result.stdout
