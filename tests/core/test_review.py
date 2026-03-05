# tests/test_review.py
# implements: SPEC-022

"""
review.py のユニットテスト。
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from spec_weaver.core.review import (
    SCHEMA_VERSION,
    ReviewFinding,
    ReviewReport,
    ReviewResult,
    _extract_last_json,
    _parse_review_result,
    collect_review_files,
    filter_findings,
    run_claude_review,
    severity_gte,
)

# ---------------------------------------------------------------------------
# severity_gte のテスト
# ---------------------------------------------------------------------------

def test_severity_gte_equal():
    assert severity_gte("high", "high") is True
    assert severity_gte("medium", "medium") is True
    assert severity_gte("low", "low") is True


def test_severity_gte_higher():
    assert severity_gte("high", "medium") is True
    assert severity_gte("high", "low") is True
    assert severity_gte("medium", "low") is True


def test_severity_gte_lower():
    assert severity_gte("low", "medium") is False
    assert severity_gte("low", "high") is False
    assert severity_gte("medium", "high") is False


# ---------------------------------------------------------------------------
# filter_findings のテスト
# ---------------------------------------------------------------------------

def _make_finding(severity: str) -> ReviewFinding:
    return ReviewFinding(
        kind="missing_implementation",
        severity=severity,
        title="test",
        detail="",
    )


def test_filter_findings_min_low():
    findings = [_make_finding("high"), _make_finding("medium"), _make_finding("low")]
    result = filter_findings(findings, "low")
    assert len(result) == 3


def test_filter_findings_min_medium():
    findings = [_make_finding("high"), _make_finding("medium"), _make_finding("low")]
    result = filter_findings(findings, "medium")
    assert len(result) == 2
    assert all(f.severity in ("high", "medium") for f in result)


def test_filter_findings_min_high():
    findings = [_make_finding("high"), _make_finding("medium"), _make_finding("low")]
    result = filter_findings(findings, "high")
    assert len(result) == 1
    assert result[0].severity == "high"


def test_filter_findings_empty():
    assert filter_findings([], "high") == []


# ---------------------------------------------------------------------------
# _extract_last_json のテスト
# ---------------------------------------------------------------------------

def test_extract_last_json_pure():
    text = '{"schema_version": "1.0", "item_id": "SPEC-001", "findings": []}'
    result = _extract_last_json(text)
    assert result is not None
    assert result["item_id"] == "SPEC-001"


def test_extract_last_json_with_log_lines():
    text = (
        "Processing...\n"
        "Loading files...\n"
        '{"schema_version": "1.0", "item_id": "SPEC-002", "findings": [], "summary": "ok"}\n'
        "Done.\n"
    )
    result = _extract_last_json(text)
    assert result is not None
    assert result["item_id"] == "SPEC-002"


def test_extract_last_json_code_block():
    text = (
        "Here is the result:\n"
        "```json\n"
        '{"schema_version": "1.0", "item_id": "SPEC-003", "findings": []}\n'
        "```\n"
    )
    result = _extract_last_json(text)
    assert result is not None
    assert result["item_id"] == "SPEC-003"


def test_extract_last_json_picks_last():
    text = (
        '{"item_id": "FIRST"}\n'
        "some text\n"
        '{"item_id": "LAST", "findings": []}\n'
    )
    result = _extract_last_json(text)
    assert result is not None
    assert result["item_id"] == "LAST"


def test_extract_last_json_no_json():
    result = _extract_last_json("no json here at all")
    assert result is None


# ---------------------------------------------------------------------------
# _parse_review_result のテスト
# ---------------------------------------------------------------------------

def test_parse_review_result_full():
    data = {
        "schema_version": "1.0",
        "item_id": "SPEC-003",
        "item_title": "audit コマンド",
        "reviewed_files": ["spec.yml", "audit.feature"],
        "findings": [
            {
                "kind": "missing_implementation",
                "severity": "medium",
                "title": "テスト未実装",
                "detail": "詳細",
                "location": "spec.yml:10",
            }
        ],
        "summary": "問題なし",
    }
    result = _parse_review_result(data)
    assert result.item_id == "SPEC-003"
    assert result.item_title == "audit コマンド"
    assert len(result.findings) == 1
    assert result.findings[0].severity == "medium"
    assert result.summary == "問題なし"


def test_parse_review_result_no_findings():
    data = {
        "schema_version": "1.0",
        "item_id": "SPEC-003",
        "item_title": "",
        "reviewed_files": [],
        "findings": [],
        "summary": "",
    }
    result = _parse_review_result(data)
    assert result.findings == []


# ---------------------------------------------------------------------------
# collect_review_files のテスト
# ---------------------------------------------------------------------------

def _make_mock_item(uid: str, yaml_path: str = "/tmp/SPEC-999.yml") -> MagicMock:
    item = MagicMock()
    item.path = yaml_path
    item.get = lambda key, default=None: [] if key == "impl_files" else default
    return item


def test_collect_review_files_item_not_found(tmp_path):
    with patch("spec_weaver.core.review.get_item_map", return_value={}):
        with pytest.raises(ValueError, match="見つかりません"):
            collect_review_files("SPEC-999", tmp_path / "features", tmp_path)


def test_collect_review_files_returns_dict_keys(tmp_path):
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()

    mock_item = _make_mock_item("SPEC-999", str(tmp_path / "SPEC-999.yml"))
    (tmp_path / "SPEC-999.yml").write_text("text: test")

    with patch("spec_weaver.core.review.get_item_map", return_value={"SPEC-999": mock_item}), \
         patch("spec_weaver.core.review.get_tag_map", return_value={}), \
         patch("spec_weaver.core.review.get_ref_files", return_value=[]), \
         patch("spec_weaver.core.review.ImplScanner") as MockScanner:
        MockScanner.return_value.scan.return_value = {}
        files = collect_review_files("SPEC-999", feature_dir, tmp_path)

    assert set(files.keys()) == {"spec", "feature", "steps", "impl"}
    assert len(files["spec"]) == 1


# ---------------------------------------------------------------------------
# run_claude_review のテスト
# ---------------------------------------------------------------------------

def test_run_claude_review_claude_not_found(tmp_path):
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()

    mock_item = _make_mock_item("SPEC-999")

    with patch("spec_weaver.core.review.get_item_map", return_value={"SPEC-999": mock_item}), \
         patch("shutil.which", return_value=None):
        with pytest.raises(FileNotFoundError, match="claude"):
            run_claude_review("SPEC-999", feature_dir, tmp_path)


def test_run_claude_review_item_not_found(tmp_path):
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()

    with patch("spec_weaver.core.review.get_item_map", return_value={}), \
         patch("shutil.which", return_value="/usr/bin/claude"):
        with pytest.raises(ValueError, match="見つかりません"):
            run_claude_review("SPEC-999", feature_dir, tmp_path)


def test_run_claude_review_json_parse_failure(tmp_path):
    """JSON 解析失敗時は high finding を含む ReviewResult を返す。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()

    mock_item = _make_mock_item("SPEC-999")

    with patch("spec_weaver.core.review.get_item_map", return_value={"SPEC-999": mock_item}), \
         patch("shutil.which", return_value="/usr/bin/claude"), \
         patch("spec_weaver.core.review.collect_review_files", return_value={"spec": [], "feature": [], "steps": [], "impl": []}), \
         patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="no json output here", returncode=0)
        result = run_claude_review("SPEC-999", feature_dir, tmp_path)

    assert result.item_id == "SPEC-999"
    assert len(result.findings) == 1
    assert result.findings[0].severity == "high"


def test_run_claude_review_success(tmp_path):
    """正常なJSONを返す場合は ReviewResult を正しく返す。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()

    mock_item = _make_mock_item("SPEC-999")

    expected_json = {
        "schema_version": "1.0",
        "item_id": "SPEC-999",
        "item_title": "テスト",
        "reviewed_files": [],
        "findings": [],
        "summary": "問題なし",
    }

    with patch("spec_weaver.core.review.get_item_map", return_value={"SPEC-999": mock_item}), \
         patch("shutil.which", return_value="/usr/bin/claude"), \
         patch("spec_weaver.core.review.collect_review_files", return_value={"spec": [], "feature": [], "steps": [], "impl": []}), \
         patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout=json.dumps(expected_json), returncode=0)
        result = run_claude_review("SPEC-999", feature_dir, tmp_path)

    assert result.item_id == "SPEC-999"
    assert result.findings == []
    assert result.summary == "問題なし"


# ---------------------------------------------------------------------------
# ReviewResult.to_dict のテスト
# ---------------------------------------------------------------------------

def test_review_result_to_dict():
    result = ReviewResult(
        schema_version=SCHEMA_VERSION,
        item_id="SPEC-001",
        item_title="テスト",
        reviewed_files=["a.py"],
        findings=[
            ReviewFinding(
                kind="missing_implementation",
                severity="high",
                title="漏れ",
                detail="詳細",
                location="a.py:10",
            )
        ],
        summary="要対応",
    )
    d = result.to_dict()
    assert d["item_id"] == "SPEC-001"
    assert len(d["findings"]) == 1
    assert d["findings"][0]["severity"] == "high"


# ---------------------------------------------------------------------------
# ReviewReport.to_dict のテスト
# ---------------------------------------------------------------------------

def test_review_report_to_dict_summary():
    report = ReviewReport(schema_version=SCHEMA_VERSION)
    report.items = [
        ReviewResult(
            schema_version=SCHEMA_VERSION,
            item_id="SPEC-001",
            item_title="A",
            reviewed_files=[],
            findings=[_make_finding("high"), _make_finding("low")],
            summary="",
        ),
        ReviewResult(
            schema_version=SCHEMA_VERSION,
            item_id="SPEC-002",
            item_title="B",
            reviewed_files=[],
            findings=[_make_finding("medium")],
            summary="",
        ),
    ]
    d = report.to_dict()
    assert d["summary"]["total_items"] == 2
    assert d["summary"]["findings_by_severity"]["high"] == 1
    assert d["summary"]["findings_by_severity"]["medium"] == 1
    assert d["summary"]["findings_by_severity"]["low"] == 1
