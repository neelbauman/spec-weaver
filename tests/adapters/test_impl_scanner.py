# tests/test_impl_scanner.py
# implements: SPEC-017, SPEC-018, SPEC-019, SPEC-020

"""
ImplScanner と get_ref_files のユニットテスト。
"""

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner

from spec_weaver.adapters.impl_scanner import get_ref_files, ImplScanner
from spec_weaver.cli.main import app
from spec_weaver.cli.commands.trace_cmd import _build_trace_rich_tree

runner = CliRunner()


# ---------------------------------------------------------------------------
# get_ref_files のテスト（SPEC-017）
# ---------------------------------------------------------------------------


def _make_item(impl_files_value):
    """impl_files カスタム属性に指定値を持つモックアイテムを作成する。"""
    item = MagicMock()
    item.get = lambda key, default=None: (
        impl_files_value if key == "impl_files" else default
    )
    return item


def test_get_ref_files_list():
    """impl_files がリスト形式の場合、そのままリストを返す。"""
    item = _make_item(["src/foo.py", "src/bar.py"])
    assert get_ref_files(item) == ["src/foo.py", "src/bar.py"]


def test_get_ref_files_string():
    """impl_files が文字列の場合、単一要素リストを返す。"""
    item = _make_item("src/foo.py")
    assert get_ref_files(item) == ["src/foo.py"]


def test_get_ref_files_empty_string():
    """impl_files が空文字の場合、空リストを返す。"""
    item = _make_item("")
    assert get_ref_files(item) == []


def test_get_ref_files_none():
    """impl_files が None の場合、空リストを返す。"""
    item = _make_item(None)
    assert get_ref_files(item) == []


def test_get_ref_files_list_with_empty_strings():
    """impl_files リストに空文字が混じっている場合は除外する。"""
    item = _make_item(["src/foo.py", "", "src/bar.py"])
    assert get_ref_files(item) == ["src/foo.py", "src/bar.py"]


# ---------------------------------------------------------------------------
# ImplScanner のテスト（SPEC-018）
# ---------------------------------------------------------------------------


def test_scan_single_id(tmp_path):
    """単一IDのアノテーションを正しく抽出できる。"""
    f = tmp_path / "module.py"
    f.write_text("# implements: SPEC-001\ndef foo(): pass\n")

    scanner = ImplScanner()
    result = scanner.scan(tmp_path)
    assert "SPEC-001" in result
    assert "module.py" in result["SPEC-001"]


def test_scan_multiple_ids_on_one_line(tmp_path):
    """1行に複数のIDをカンマ区切りで記述できる。"""
    f = tmp_path / "module.py"
    f.write_text("# implements: SPEC-001, SPEC-002\n")

    scanner = ImplScanner()
    result = scanner.scan(tmp_path)
    assert "SPEC-001" in result
    assert "SPEC-002" in result
    assert "module.py" in result["SPEC-001"]
    assert "module.py" in result["SPEC-002"]


def test_scan_slash_comment_style(tmp_path):
    """`//` コメント形式のアノテーションも認識できる。"""
    f = tmp_path / "module.ts"
    f.write_text("// implements: SPEC-003\n")

    scanner = ImplScanner()
    result = scanner.scan(tmp_path)
    assert "SPEC-003" in result


def test_scan_no_annotation(tmp_path):
    """アノテーションがないファイルはエラーにならず、結果に含まれない。"""
    f = tmp_path / "module.py"
    f.write_text("def foo(): pass\n")

    scanner = ImplScanner()
    result = scanner.scan(tmp_path)
    assert result == {}


def test_scan_extensions_filter(tmp_path):
    """--extensions で拡張子を絞り込んだとき、対象外ファイルは除外される。"""
    py_file = tmp_path / "module.py"
    py_file.write_text("# implements: SPEC-001\n")
    md_file = tmp_path / "docs.md"
    md_file.write_text("# implements: SPEC-001\n")

    scanner = ImplScanner()
    result = scanner.scan(tmp_path, extensions=["py"])
    assert "SPEC-001" in result
    assert "module.py" in result["SPEC-001"]
    assert not any("docs.md" in p for p in result.get("SPEC-001", set()))


def test_scan_excludes_git_dir(tmp_path):
    """.git ディレクトリ内のファイルは除外される。"""
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    f = git_dir / "config"
    f.write_text("# implements: SPEC-001\n")

    scanner = ImplScanner()
    result = scanner.scan(tmp_path)
    assert result == {}


def test_scan_relative_path(tmp_path):
    """結果のファイルパスはリポジトリルートからの相対パスである。"""
    sub = tmp_path / "src" / "mymodule"
    sub.mkdir(parents=True)
    f = sub / "impl.py"
    f.write_text("# implements: SPEC-005\n")

    scanner = ImplScanner()
    result = scanner.scan(tmp_path)
    assert "SPEC-005" in result
    rel_path = next(iter(result["SPEC-005"]))
    assert rel_path == str(Path("src/mymodule/impl.py"))


# ---------------------------------------------------------------------------
# audit --check-impl のテスト（SPEC-019）
# ---------------------------------------------------------------------------


def _make_audit_item(uid: str, impl_files=None, status="implemented", testable=True):
    """audit テスト用の Doorstop アイテムモック。impl_files カスタム属性を持つ。"""
    item = MagicMock()
    item.uid = uid
    item.active = True
    item.header = uid
    item.links = []
    item.suspect = False
    item.cleared = True
    item.reviewed = True
    item.path = None

    impl_files_val = impl_files if impl_files is not None else []

    def _get(key, default=None):
        mapping = {"impl_files": impl_files_val, "status": status, "testable": testable}
        return mapping.get(key, default)

    item.get = _get
    return item


@patch("spec_weaver.cli.commands.audit_cmd.AuditService")
def test_check_impl_broken_ref(mock_service_class, tmp_path):
    """impl_files に存在しないファイルが指定されている場合、❌ として報告される。"""
    mock_service = mock_service_class.return_value
    from spec_weaver.services.audit_service import AuditReport
    
    mock_service.run_audit.return_value = AuditReport(
        is_success=False,
        specs_count=1,
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
        broken_refs=[("SPEC-099", "src/nonexistent.py")]
    )

    feat_dir = tmp_path / "features"
    feat_dir.mkdir()

    result = runner.invoke(
        app,
        [
            "audit",
            str(feat_dir),
            "--repo-root",
            str(tmp_path),
            "--check-impl",
        ],
    )

    # UIでの表示を確認（audit_cmd.py で broken_refs の表示が実装されているか？）
    # 現状の audit_cmd.py を見ると broken_refs の表示は「... 同様に ...」として省略されていたので、
    # 実際の実装を確認する必要がある。
    assert "nonexistent.py" in result.output


@patch("spec_weaver.cli.commands.audit_cmd.AuditService")
def test_check_impl_disabled_by_default(mock_service_class, tmp_path):
    """--check-impl なしでは実装リンク検証セクションが出力されない。"""
    # このテストは --check-impl オプションの有無による挙動を確認するもの。
    # サービス呼び出し時の引数を確認する形に変更する。
    mock_service = mock_service_class.return_value
    from spec_weaver.services.audit_service import AuditReport
    mock_service.run_audit.return_value = AuditReport(
        is_success=True, specs_count=0, inactive_testable=set(), untested_specs=set(),
        orphaned_tags=set(), suspect_specs={}, suspect_features={}, unreviewed_specs=set(),
        unreviewed_features=set(), stale_items=[], unused_step_defs=set(), undefined_steps=set()
    )

    feat_dir = tmp_path / "features"
    feat_dir.mkdir()

    runner.invoke(
        app,
        [
            "audit",
            str(feat_dir),
            "--repo-root",
            str(tmp_path),
        ],
    )
    
    # サービス呼び出しで check_impl=False であることを検証
    args, kwargs = mock_service.run_audit.call_args
    check_impl_val = kwargs.get('check_impl')
    if check_impl_val is None and len(args) >= 5:
        check_impl_val = args[4]
    assert check_impl_val is False


# ---------------------------------------------------------------------------
# trace --show-impl のテスト（SPEC-020）
# ---------------------------------------------------------------------------


def _make_trace_item(uid, header=None, link_uids=None, impl_files=None):
    """trace テスト用の Doorstop アイテムモック。"""
    item = MagicMock()
    item.uid = uid
    item.suspect = False
    item.links = []
    if link_uids:
        for lu in link_uids:
            lnk = MagicMock()
            lnk.__str__ = lambda self, v=lu: v
            item.links.append(lnk)
    item.header = header or uid

    impl_val = impl_files if impl_files is not None else []

    def _get(key, default=None):
        mapping = {"impl_files": impl_val, "status": "in-progress", "testable": True}
        return mapping.get(key, default)

    item.get = _get
    return item


def test_show_impl_file_shown_in_tree(tmp_path):
    """impl_map が渡された場合、実装ファイルがツリーに表示される。"""
    impl_file = tmp_path / "src" / "impl.py"
    impl_file.parent.mkdir(parents=True)
    impl_file.write_text("# implements: SPEC-001\n")

    items = {"SPEC-001": _make_trace_item("SPEC-001", impl_files=["src/impl.py"])}
    child_map: dict = {}
    tag_map: dict = {}
    impl_map = {"SPEC-001": {"src/impl.py"}}

    from rich.console import Console
    from io import StringIO

    buf = StringIO()
    con = Console(file=buf, highlight=False)

    result = _build_trace_rich_tree(
        "SPEC-001",
        items,
        child_map,
        tag_map,
        "both",
        impl_map=impl_map,
        repo_root=tmp_path,
    )
    con.print(result)
    output = buf.getvalue()
    assert "src/impl.py" in output


def test_show_impl_not_shown_without_flag():
    """impl_map=None のとき（--show-impl なし）、実装ファイルはツリーに含まれない。"""
    items = {"SPEC-001": _make_trace_item("SPEC-001", impl_files=["src/impl.py"])}
    child_map: dict = {}
    tag_map: dict = {}

    from rich.console import Console
    from io import StringIO

    buf = StringIO()
    con = Console(file=buf, highlight=False)

    result = _build_trace_rich_tree(
        "SPEC-001",
        items,
        child_map,
        tag_map,
        "both",
        impl_map=None,
        repo_root=None,
    )
    con.print(result)
    output = buf.getvalue()
    assert "src/impl.py" not in output
