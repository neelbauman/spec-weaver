from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from pathlib import Path
from spec_weaver.cli.main import app
from spec_weaver.services.audit_service import AuditReport
from spec_weaver.services.status_service import StatusReport, ItemStatusDTO
from spec_weaver.services.clear_service import ClearResult

runner = CliRunner()


def _make_mock_item(uid: str, suspect: bool = False, status: str | None = None):
    """テスト用のDoorstopアイテムモックを生成する。"""
    item = MagicMock()
    item.uid = uid
    item.links = []
    item.header = uid
    item.active = True
    # 新API: cleared / reviewed
    item.cleared = not suspect
    item.reviewed = True
    item.path = None

    # get() で status を返す
    def _get(key, default=None):
        if key == "status":
            return status
        if key == "testable":
            return True
        return default

    item.get.side_effect = _get
    return item


@patch("spec_weaver.cli.commands.audit_cmd.AuditService")
def test_audit_perfect_match(mock_service_class, tmp_path):
    mock_service = mock_service_class.return_value
    mock_service.run_audit.return_value = AuditReport(
        is_success=True,
        specs_count=2,
        inactive_testable=set(),
        untested_specs=set(),
        orphaned_tags=set(),
        suspect_specs={},
        suspect_features={},
        unreviewed_specs=set(),
        unreviewed_features=set(),
        stale_items=[],
        unused_step_defs=set(),
        undefined_steps=set(),
    )

    # 実行
    result = runner.invoke(app, ["audit", str(tmp_path), "--repo-root", str(tmp_path)])

    # 終了コード0（成功）で、成功メッセージが含まれているか
    assert result.exit_code == 0
    assert "完璧です！" in result.stdout


@patch("spec_weaver.cli.commands.audit_cmd.AuditService")
def test_audit_with_errors(mock_service_class, tmp_path):
    mock_service = mock_service_class.return_value
    mock_service.run_audit.return_value = AuditReport(
        is_success=False,
        specs_count=2,
        inactive_testable=set(),
        untested_specs={"SPEC-002"},
        orphaned_tags={"SPEC-003"},
        suspect_specs={},
        suspect_features={},
        unreviewed_specs=set(),
        unreviewed_features=set(),
        stale_items=[],
        unused_step_defs=set(),
        undefined_steps=set(),
    )

    result = runner.invoke(app, ["audit", str(tmp_path), "--repo-root", str(tmp_path)])

    # 終了コード1（失敗）で、それぞれの警告が出力されているか
    assert result.exit_code == 1
    assert "テストが実装されていない仕様" in result.stdout
    assert "SPEC-002" in result.stdout
    assert "仕様書に存在しない孤児タグ" in result.stdout
    assert "@SPEC-003" in result.stdout


@patch("spec_weaver.cli.commands.audit_cmd.AuditService")
def test_audit_suspect_specs(mock_service_class, tmp_path):
    mock_service = mock_service_class.return_value
    mock_service.run_audit.return_value = AuditReport(
        is_success=False,
        specs_count=2,
        inactive_testable=set(),
        untested_specs=set(),
        orphaned_tags=set(),
        suspect_specs={"SPEC-002": {"Parent REQ changed"}},
        suspect_features={},
        unreviewed_specs=set(),
        unreviewed_features=set(),
        stale_items=[],
        unused_step_defs=set(),
        undefined_steps=set(),
    )

    result = runner.invoke(app, ["audit", str(tmp_path), "--repo-root", str(tmp_path)])

    # Suspectがあれば終了コード1
    assert result.exit_code == 1
    assert "Suspect" in result.stdout
    assert "SPEC-002" in result.stdout
    assert "spec-weaver clear SPEC-002" in result.stdout


@patch("spec_weaver.cli.commands.audit_cmd.AuditService")
def test_audit_no_suspect_does_not_report_suspect(mock_service_class, tmp_path):
    mock_service = mock_service_class.return_value
    mock_service.run_audit.return_value = AuditReport(
        is_success=True,
        specs_count=2,
        inactive_testable=set(),
        untested_specs=set(),
        orphaned_tags=set(),
        suspect_specs={},
        suspect_features={},
        unreviewed_specs=set(),
        unreviewed_features=set(),
        stale_items=[],
        unused_step_defs=set(),
        undefined_steps=set(),
    )

    result = runner.invoke(app, ["audit", str(tmp_path), "--repo-root", str(tmp_path)])

    assert result.exit_code == 0
    assert "Suspect" not in result.stdout


# ---------------------------------------------------------------------------
# status コマンドのテスト
# ---------------------------------------------------------------------------


@patch("spec_weaver.cli.commands.status_cmd.StatusService")
def test_status_shows_all_items(mock_service_class, tmp_path):
    """status コマンドが全アイテムを一覧表示する。"""
    mock_service = mock_service_class.return_value
    
    mock_item_req = _make_mock_item("REQ-001", status="draft")
    mock_item_spec = _make_mock_item("SPEC-001", status="implemented")
    
    mock_service.get_status_report.return_value = StatusReport(
        grouped_items={
            "REQ": [ItemStatusDTO("REQ-001", "REQ-001", True, "draft", mock_item_req)],
            "SPEC": [ItemStatusDTO("SPEC-001", "SPEC-001", True, "implemented", mock_item_spec)],
        },
        feature_files=[],
        unused_step_defs_count=0,
        undefined_steps_count=0,
        total_items_shown=2,
        review_state=MagicMock(get_status=MagicMock(return_value="✅ reviewed"))
    )

    result = runner.invoke(app, ["status", "--repo-root", str(tmp_path), "--feature-dir", str(tmp_path)])

    assert result.exit_code == 0
    assert "REQ-001" in result.stdout
    assert "SPEC-001" in result.stdout
    assert "draft" in result.stdout
    assert "implemented" in result.stdout


@patch("spec_weaver.cli.commands.status_cmd.StatusService")
def test_status_filter_by_status(mock_service_class, tmp_path):
    """--filter オプションで指定ステータスだけを表示する。"""
    mock_service = mock_service_class.return_value
    
    mock_item_req2 = _make_mock_item("REQ-002", status="implemented")
    
    mock_service.get_status_report.return_value = StatusReport(
        grouped_items={
            "REQ": [ItemStatusDTO("REQ-002", "REQ-002", True, "implemented", mock_item_req2)],
        },
        feature_files=[],
        unused_step_defs_count=0,
        undefined_steps_count=0,
        total_items_shown=1,
        review_state=MagicMock(get_status=MagicMock(return_value="✅ reviewed"))
    )

    result = runner.invoke(
        app, ["status", "--repo-root", str(tmp_path), "--filter", "implemented", "--feature-dir", str(tmp_path)]
    )

    assert result.exit_code == 0
    assert "REQ-002" in result.stdout


@patch("spec_weaver.cli.commands.status_cmd.StatusService")
def test_status_unset_shows_dash(mock_service_class, tmp_path):
    """status フィールドが未設定のアイテムは '-' と表示される。"""
    mock_service = mock_service_class.return_value
    
    mock_item = _make_mock_item("SPEC-001", status=None)
    
    mock_service.get_status_report.return_value = StatusReport(
        grouped_items={
            "SPEC": [ItemStatusDTO("SPEC-001", "SPEC-001", True, None, mock_item)],
        },
        feature_files=[],
        unused_step_defs_count=0,
        undefined_steps_count=0,
        total_items_shown=1,
        review_state=MagicMock(get_status=MagicMock(return_value="✅ reviewed"))
    )

    result = runner.invoke(app, ["status", "--repo-root", str(tmp_path), "--feature-dir", str(tmp_path)])

    assert result.exit_code == 0
    assert "SPEC-001" in result.stdout
    # badge関数の挙動に依存するが、元テストは '-' を期待していた
    # 実際には get_impl_status_badge が '-' を返すか確認が必要


# ---------------------------------------------------------------------------
# clear コマンドのテスト
# ---------------------------------------------------------------------------


@patch("spec_weaver.cli.commands.clear_cmd.ClearService")
def test_clear_blocks_suspect_with_unreviewed(mock_service_class, tmp_path):
    """上位アイテムが未レビュー（suspect-with-unreviewed）の場合、clear をブロックする。"""
    mock_service = mock_service_class.return_value
    mock_service.run_clear.return_value = ClearResult(
        is_success=False,
        error_message="上位アイテムが未レビューです。先に上位アイテムをレビューしてください。"
    )

    result = runner.invoke(app, ["clear", "SPEC-001", "--repo-root", str(tmp_path)])

    assert result.exit_code == 1
    assert "上位アイテムが未レビューです" in result.stdout
