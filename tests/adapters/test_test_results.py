# tests/test_test_results.py
# implements: SPEC-005, SPEC-014

"""
test_results.py のユニットテスト。
"""

import json
from pathlib import Path
from typing import List

from spec_weaver.adapters.test_results import (
    format_status_badge,
    load_test_results,
    result_badge,
    spec_result_summary,
)


def _make_cucumber_json(elements: List[dict], uri: str = "features/auth.feature"):
    """テスト用の Cucumber JSON 構造を作成するヘルパー。"""
    return [
        {
            "keyword": "Feature",
            "name": "ユーザー認証",
            "uri": uri,
            "elements": elements,
        }
    ]


# ---------------------------------------------------------------------------
# load_test_results のテスト
# ---------------------------------------------------------------------------


def test_load_test_results_empty(tmp_path: Path):
    json_file = tmp_path / "empty.json"
    json_file.write_text("[]", encoding="utf-8")
    assert load_test_results(json_file) == {}


def test_load_test_results_passed(tmp_path: Path):
    data = _make_cucumber_json(
        [
            {
                "name": "ログインに成功する",
                "tags": [{"name": "@SPEC-001"}],
                "steps": [
                    {"result": {"status": "passed"}},
                    {"result": {"status": "passed"}},
                ],
            }
        ]
    )
    json_file = tmp_path / "results.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_test_results(json_file)
    assert result == {("auth", "ログインに成功する"): {"status": "passed", "error": None}}


def test_load_test_results_failed(tmp_path: Path):
    data = _make_cucumber_json(
        [
            {
                "name": "無効なパスワードでログインを試みる",
                "tags": [{"name": "@SPEC-002"}],
                "steps": [
                    {"result": {"status": "passed"}},
                    {"result": {"status": "failed", "error_message": "Assertion failed"}},
                ],
            }
        ]
    )
    json_file = tmp_path / "results.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_test_results(json_file)
    assert result == {("auth", "無効なパスワードでログインを試みる"): {"status": "failed", "error": "Assertion failed"}}


def test_load_test_results_error(tmp_path: Path):
    data = _make_cucumber_json(
        [
            {
                "name": "システムエラーが発生する",
                "steps": [
                    {"result": {"status": "error", "error_message": "Connection timeout"}},
                ],
            }
        ]
    )
    json_file = tmp_path / "results.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_test_results(json_file)
    assert result == {("auth", "システムエラーが発生する"): {"status": "error", "error": "Connection timeout"}}


def test_load_test_results_failed_takes_priority_over_passed(tmp_path: Path):
    """同名シナリオが複数回実行された場合、failed が passed より優先される。"""
    data = [
        {
            "uri": "features/auth.feature",
            "elements": [
                {"name": "シナリオA", "steps": [{"result": {"status": "passed"}}]}
            ],
        },
        {
            "uri": "features/auth.feature",
            "elements": [
                {"name": "シナリオA", "steps": [{"result": {"status": "failed"}}]}
            ],
        },
    ]
    json_file = tmp_path / "results.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_test_results(json_file)
    assert result[("auth", "シナリオA")]["status"] == "failed"


def test_load_test_results_error_takes_priority_over_failed(tmp_path: Path):
    """error と failed は同じ優先度（_STATUS_PRIORITY）だが、後から来たもので上書きされる（現状の仕様）。"""
    data = [
        {
            "uri": "features/auth.feature",
            "elements": [
                {"name": "シナリオA", "steps": [{"result": {"status": "failed"}}]}
            ],
        },
        {
            "uri": "features/auth.feature",
            "elements": [
                {"name": "シナリオA", "steps": [{"result": {"status": "error"}}]}
            ],
        },
    ]
    json_file = tmp_path / "results.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_test_results(json_file)
    # どちらも優先度4 or 3なので、後のもので上書きされる
    assert result[("auth", "シナリオA")]["status"] == "error"


# ---------------------------------------------------------------------------
# spec_result_summary のテスト
# ---------------------------------------------------------------------------


def test_spec_result_summary_all_passed():
    tag_map = {
        "SPEC-001": [
            {
                "file": "features/auth.feature",
                "name": "ログイン",
                "line": 5,
                "keyword": "Scenario",
            },
        ]
    }
    test_result_map = {("auth", "ログイン"): {"status": "passed", "error": None}}

    p, f, e, s, t = spec_result_summary("SPEC-001", tag_map, test_result_map)
    assert (p, f, e, s, t) == (1, 0, 0, 0, 1)


def test_spec_result_summary_mixed():
    tag_map = {
        "SPEC-001": [
            {"file": "features/a.feature", "name": "P", "line": 1, "keyword": "Scenario"},
            {"file": "features/a.feature", "name": "F", "line": 2, "keyword": "Scenario"},
            {"file": "features/a.feature", "name": "E", "line": 3, "keyword": "Scenario"},
            {"file": "features/a.feature", "name": "S", "line": 4, "keyword": "Scenario"},
        ]
    }
    test_result_map = {
        ("a", "P"): {"status": "passed", "error": None},
        ("a", "F"): {"status": "failed", "error": "err"},
        ("a", "E"): {"status": "error", "error": "err"},
        ("a", "S"): {"status": "skipped", "error": None},
    }

    p, f, e, s, t = spec_result_summary("SPEC-001", tag_map, test_result_map)
    assert (p, f, e, s, t) == (1, 1, 1, 1, 4)


# ---------------------------------------------------------------------------
# format_status_badge / result_badge のテスト
# ---------------------------------------------------------------------------


def test_format_status_badge():
    assert "PASS" in format_status_badge("passed")
    assert "FAIL" in format_status_badge("failed")
    assert "ERROR" in format_status_badge("error")
    assert "SKIP" in format_status_badge("skipped")
    assert "UNKNOWN" in format_status_badge(None)


def test_result_badge_all_passed():
    assert "1/1 PASS" in result_badge(1, 0, 0, 0, 1)
    assert "🔴 0/1 FAIL" in result_badge(1, 0, 0, 0, 1)


def test_result_badge_empty():
    assert result_badge(0, 0, 0, 0, 0) == "-"
