
# tests/test_trace.py
from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from spec_weaver.cli.commands.trace_cmd import (
    _collect_all_ancestors,
    _format_trace_node,
)
from spec_weaver.cli.main import app
from spec_weaver.services.trace_service import TraceData

runner = CliRunner()


# ---------------------------------------------------------------------------
# テスト用フィクスチャ
# ---------------------------------------------------------------------------


def _make_link(uid_str: str):
    """str() で uid_str を返すリンクモック。"""
    link = MagicMock()
    link.__str__ = lambda self: uid_str
    return link


def _make_mock_item(
    uid: str,
    header: str | None = None,
    link_uids: list | None = None,
    status: str | None = None,
):
    """テスト用のDoorstopアイテムモック。"""
    item = MagicMock()
    item.uid = uid
    item.active = True
    item.suspect = False
    item.links = [_make_link(lu) for lu in (link_uids or [])]
    item.header = header or uid

    def _get(key, default=None):
        if key == "status":
            return status
        if key == "testable":
            return True
        return default

    item.get.side_effect = _get
    return item


# ---------------------------------------------------------------------------
# _collect_all_ancestors のユニットテスト
# ---------------------------------------------------------------------------


def test_collect_all_ancestors_simple():
    """REQ-001 ← SPEC-001 のリンク構造で、SPEC-001の祖先として REQ-001 が収集される。"""
    items = {
        "REQ-001": _make_mock_item("REQ-001"),
        "SPEC-001": _make_mock_item("SPEC-001", link_uids=["REQ-001"]),
    }
    ancestors = _collect_all_ancestors("SPEC-001", items)
    assert ancestors == {"REQ-001"}


def test_collect_all_ancestors_deep():
    """REQ-001 ← REQ-002 ← SPEC-001 の3段構造で SPEC-001 の全祖先を取得する。"""
    items = {
        "REQ-001": _make_mock_item("REQ-001"),
        "REQ-002": _make_mock_item("REQ-002", link_uids=["REQ-001"]),
        "SPEC-001": _make_mock_item("SPEC-001", link_uids=["REQ-002"]),
    }
    ancestors = _collect_all_ancestors("SPEC-001", items)
    assert ancestors == {"REQ-001", "REQ-002"}


def test_collect_all_ancestors_no_parent():
    """親がいないルートアイテムの祖先は空集合。"""
    items = {
        "REQ-001": _make_mock_item("REQ-001"),
    }
    ancestors = _collect_all_ancestors("REQ-001", items)
    assert ancestors == set()


def test_collect_all_ancestors_cycle_safety():
    """循環参照があっても無限ループしない。"""
    items = {
        "REQ-001": _make_mock_item("REQ-001", link_uids=["REQ-002"]),
        "REQ-002": _make_mock_item("REQ-002", link_uids=["REQ-001"]),
    }
    # 例外が発生せず終了すること
    ancestors = _collect_all_ancestors("REQ-001", items)
    assert "REQ-002" in ancestors


# ---------------------------------------------------------------------------
# _format_trace_node のユニットテスト
# ---------------------------------------------------------------------------


def test_format_trace_node_normal():
    """通常ノードのラベルに★が含まれない。"""
    item = _make_mock_item("REQ-001", header="テスト要件")
    label = _format_trace_node("REQ-001", item, is_origin=False)
    assert "REQ-001" in label
    assert "テスト要件" in label
    assert "★" not in label


def test_format_trace_node_origin():
    """is_origin=True のとき★が含まれる。"""
    item = _make_mock_item("SPEC-001", header="仕様")
    label = _format_trace_node("SPEC-001", item, is_origin=True)
    assert "★" in label
    assert "SPEC-001" in label


# ---------------------------------------------------------------------------
# CLI tests using mocked TraceService
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.commands.trace_cmd.TraceService")
def test_trace_down_shows_descendants(mock_service_class, tmp_path):
    mock_service = mock_service_class.return_value
    mock_service.prepare_trace_data.return_value = TraceData(
        all_items_str={
            "REQ-001": _make_mock_item("REQ-001", header="上位要件"),
            "SPEC-001": _make_mock_item("SPEC-001", header="仕様", link_uids=["REQ-001"]),
        },
        child_map={"REQ-001": ["SPEC-001"]},
        tag_map={
            "SPEC-001": [
                {"file": "features/spec.feature", "name": "シナリオA", "keyword": "Scenario"}
            ],
        },
        review_state=None,
        impl_map=None
    )

    result = runner.invoke(app, ["trace", "REQ-001", "--direction", "down"])

    assert result.exit_code == 0
    assert "REQ-001" in result.stdout
    assert "SPEC-001" in result.stdout
    assert "シナリオA" in result.stdout


@patch("spec_weaver.cli.commands.trace_cmd.TraceService")
def test_trace_both_shows_ancestors_and_descendants(mock_service_class, tmp_path):
    mock_service = mock_service_class.return_value
    mock_service.prepare_trace_data.return_value = TraceData(
        all_items_str={
            "REQ-001": _make_mock_item("REQ-001", header="上位要件"),
            "SPEC-001": _make_mock_item("SPEC-001", header="仕様詳細", link_uids=["REQ-001"]),
        },
        child_map={"REQ-001": ["SPEC-001"]},
        tag_map={
            "SPEC-001": [
                {"file": "features/audit.feature", "name": "監査成功", "keyword": "Scenario"}
            ],
        },
        review_state=None,
        impl_map=None
    )

    result = runner.invoke(app, ["trace", "SPEC-001", "--direction", "both"])

    assert result.exit_code == 0
    assert "REQ-001" in result.stdout
    assert "★" in result.stdout
    assert "SPEC-001" in result.stdout
    assert "監査成功" in result.stdout


@patch("spec_weaver.cli.commands.trace_cmd.TraceService")
def test_trace_nonexistent_id_exits_with_error(mock_service_class, tmp_path):
    mock_service = mock_service_class.return_value
    mock_service.prepare_trace_data.return_value = TraceData(
        all_items_str={"REQ-001": _make_mock_item("REQ-001")},
        child_map={}, tag_map={}, review_state=None, impl_map=None
    )

    result = runner.invoke(app, ["trace", "NONEXIST-999"])

    assert result.exit_code == 1
    assert "not found" in result.stdout


@patch("spec_weaver.cli.commands.trace_cmd.TraceService")
def test_trace_shows_review_status(mock_service_class, tmp_path):
    mock_service = mock_service_class.return_value
    
    mock_review_state = MagicMock()
    mock_review_state.get_status.return_value = "📋 unreviewed"
    
    mock_service.prepare_trace_data.return_value = TraceData(
        all_items_str={"REQ-001": _make_mock_item("REQ-001")},
        child_map={}, tag_map={}, 
        review_state=mock_review_state,
        impl_map=None
    )

    result = runner.invoke(app, ["trace", "REQ-001"])

    assert result.exit_code == 0
    assert "unreviewed" in result.stdout
