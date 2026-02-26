# tests/test_trace.py
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from pathlib import Path

from spec_weaver.cli import (
    app,
    _collect_all_ancestors,
    _format_trace_node,
    _build_trace_rich_tree,
)

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
    item.suspect = False
    item.links = [_make_link(lu) for lu in (link_uids or [])]
    item.header = header or uid

    def _get(key, default=None):
        if key == "status":
            return status
        if key == "testable":
            return default
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
# trace コマンド - direction=down
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.get_all_prefixes")
@patch("spec_weaver.cli.get_tag_map")
@patch("spec_weaver.cli.get_item_map")
def test_trace_down_shows_descendants(mock_get_item_map, mock_get_tag_map, mock_get_all_prefixes, tmp_path):
    """--direction down でREQを起点にした場合、子SPECとシナリオが表示される。"""
    mock_get_item_map.return_value = {
        "REQ-001": _make_mock_item("REQ-001", header="上位要件"),
        "SPEC-001": _make_mock_item("SPEC-001", header="仕様", link_uids=["REQ-001"]),
    }
    mock_get_tag_map.return_value = {
        "SPEC-001": [
            {"file": "features/spec.feature", "line": 5, "name": "シナリオA", "keyword": "Scenario"}
        ],
    }
    mock_get_all_prefixes.return_value = {"REQ", "SPEC"}

    result = runner.invoke(app, [
        "trace", "REQ-001",
        "--feature-dir", str(tmp_path),
        "--repo-root", str(tmp_path),
        "--direction", "down",
    ])

    assert result.exit_code == 0
    assert "REQ-001" in result.stdout
    assert "SPEC-001" in result.stdout
    assert "シナリオA" in result.stdout


@patch("spec_weaver.cli.get_all_prefixes")
@patch("spec_weaver.cli.get_tag_map")
@patch("spec_weaver.cli.get_item_map")
def test_trace_down_no_ancestors(mock_get_item_map, mock_get_tag_map, mock_get_all_prefixes, tmp_path):
    """--direction down では祖先が表示されない。"""
    mock_get_item_map.return_value = {
        "REQ-001": _make_mock_item("REQ-001", header="上位要件"),
        "SPEC-001": _make_mock_item("SPEC-001", header="仕様", link_uids=["REQ-001"]),
    }
    mock_get_tag_map.return_value = {}
    mock_get_all_prefixes.return_value = {"REQ", "SPEC"}

    result = runner.invoke(app, [
        "trace", "SPEC-001",
        "--feature-dir", str(tmp_path),
        "--repo-root", str(tmp_path),
        "--direction", "down",
    ])

    assert result.exit_code == 0
    assert "SPEC-001" in result.stdout
    # down モードでは REQ-001（祖先）は表示されない
    assert "REQ-001" not in result.stdout


# ---------------------------------------------------------------------------
# trace コマンド - direction=both
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.get_all_prefixes")
@patch("spec_weaver.cli.get_tag_map")
@patch("spec_weaver.cli.get_item_map")
def test_trace_both_shows_ancestors_and_descendants(
    mock_get_item_map, mock_get_tag_map, mock_get_all_prefixes, tmp_path
):
    """--direction both でSPECを起点にした場合、祖先REQが上に★強調origin、シナリオが下に表示される。"""
    mock_get_item_map.return_value = {
        "REQ-001": _make_mock_item("REQ-001", header="上位要件"),
        "SPEC-001": _make_mock_item(
            "SPEC-001", header="仕様詳細", link_uids=["REQ-001"], status="implemented"
        ),
    }
    mock_get_tag_map.return_value = {
        "SPEC-001": [
            {"file": "features/audit.feature", "line": 10, "name": "監査成功", "keyword": "Scenario"}
        ],
    }
    mock_get_all_prefixes.return_value = {"REQ", "SPEC"}

    result = runner.invoke(app, [
        "trace", "SPEC-001",
        "--feature-dir", str(tmp_path),
        "--repo-root", str(tmp_path),
        "--direction", "both",
    ])

    assert result.exit_code == 0
    # 祖先が表示される
    assert "REQ-001" in result.stdout
    # 起点が★強調で表示される
    assert "★" in result.stdout
    assert "SPEC-001" in result.stdout
    # シナリオが表示される
    assert "監査成功" in result.stdout
    assert "audit.feature" in result.stdout


# ---------------------------------------------------------------------------
# trace コマンド - direction=up
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.get_all_prefixes")
@patch("spec_weaver.cli.get_tag_map")
@patch("spec_weaver.cli.get_item_map")
def test_trace_up_no_scenarios(mock_get_item_map, mock_get_tag_map, mock_get_all_prefixes, tmp_path):
    """--direction up ではシナリオが表示されない（祖先のみ）。"""
    mock_get_item_map.return_value = {
        "REQ-001": _make_mock_item("REQ-001", header="上位要件"),
        "SPEC-001": _make_mock_item("SPEC-001", header="仕様", link_uids=["REQ-001"]),
    }
    mock_get_tag_map.return_value = {
        "SPEC-001": [
            {"file": "features/spec.feature", "line": 5, "name": "シナリオA", "keyword": "Scenario"}
        ],
    }
    mock_get_all_prefixes.return_value = {"REQ", "SPEC"}

    result = runner.invoke(app, [
        "trace", "SPEC-001",
        "--feature-dir", str(tmp_path),
        "--repo-root", str(tmp_path),
        "--direction", "up",
    ])

    assert result.exit_code == 0
    assert "REQ-001" in result.stdout
    assert "SPEC-001" in result.stdout
    # up モードではシナリオは展開されない
    assert "シナリオA" not in result.stdout
    assert "spec.feature" not in result.stdout


# ---------------------------------------------------------------------------
# trace コマンド - format=flat
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.get_all_prefixes")
@patch("spec_weaver.cli.get_tag_map")
@patch("spec_weaver.cli.get_item_map")
def test_trace_flat_format(mock_get_item_map, mock_get_tag_map, mock_get_all_prefixes, tmp_path):
    """--format flat でREQとSPECが両方テーブル形式で表示される。"""
    mock_get_item_map.return_value = {
        "REQ-001": _make_mock_item("REQ-001", header="上位要件", status="implemented"),
        "SPEC-001": _make_mock_item(
            "SPEC-001", header="仕様詳細", link_uids=["REQ-001"], status="draft"
        ),
    }
    mock_get_tag_map.return_value = {}
    mock_get_all_prefixes.return_value = {"REQ", "SPEC"}

    result = runner.invoke(app, [
        "trace", "SPEC-001",
        "--feature-dir", str(tmp_path),
        "--repo-root", str(tmp_path),
        "--format", "flat",
    ])

    assert result.exit_code == 0
    assert "REQ-001" in result.stdout
    assert "SPEC-001" in result.stdout
    assert "上位要件" in result.stdout
    assert "仕様詳細" in result.stdout


# ---------------------------------------------------------------------------
# trace コマンド - エラーケース
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.get_item_map")
def test_trace_nonexistent_id_exits_with_error(mock_get_item_map, tmp_path):
    """存在しないIDを指定すると Exit(1) とエラーメッセージが表示される。"""
    mock_get_item_map.return_value = {
        "REQ-001": _make_mock_item("REQ-001"),
    }

    result = runner.invoke(app, [
        "trace", "NONEXIST-999",
        "--repo-root", str(tmp_path),
    ])

    assert result.exit_code == 1
    assert "not found" in result.stdout or "Error" in result.stdout


# ---------------------------------------------------------------------------
# trace コマンド - .feature ファイルを起点
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.get_all_prefixes")
@patch("spec_weaver.cli.get_tag_map")
@patch("spec_weaver.cli.get_item_map")
def test_trace_feature_file_as_origin_up(
    mock_get_item_map, mock_get_tag_map, mock_get_all_prefixes, tmp_path
):
    """.featureファイルを起点にした場合、対応するSPECの祖先REQまで表示される。"""
    mock_get_item_map.return_value = {
        "REQ-001": _make_mock_item("REQ-001", header="上位要件"),
        "SPEC-001": _make_mock_item("SPEC-001", header="仕様", link_uids=["REQ-001"]),
    }
    mock_get_tag_map.return_value = {
        "SPEC-001": [
            {"file": "features/audit.feature", "line": 5, "name": "監査成功", "keyword": "Scenario"}
        ],
    }
    mock_get_all_prefixes.return_value = {"REQ", "SPEC"}

    result = runner.invoke(app, [
        "trace", "audit.feature",
        "--feature-dir", str(tmp_path),
        "--repo-root", str(tmp_path),
        "--direction", "up",
    ])

    assert result.exit_code == 0
    assert "REQ-001" in result.stdout
    assert "SPEC-001" in result.stdout
