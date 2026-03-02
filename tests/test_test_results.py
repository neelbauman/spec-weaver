"""
test_results モジュールのユニットテスト。
pytest-bdd 生成の Cucumber 互換 JSON を読み込み、
(feature_stem, scenario_name) → status マッピングを検証する。
"""

import json
from pathlib import Path

from spec_weaver.test_results import (
    _scenario_status,
    format_status_badge,
    load_test_results,
    result_badge,
    spec_result_summary,
)


# ---------------------------------------------------------------------------
# _scenario_status のテスト
# ---------------------------------------------------------------------------


def test_scenario_status_all_passed():
    steps = [
        {"result": {"status": "passed"}},
        {"result": {"status": "passed"}},
    ]
    assert _scenario_status(steps) == "passed"


def test_scenario_status_with_failed_step():
    steps = [
        {"result": {"status": "passed"}},
        {"result": {"status": "failed"}},
        {"result": {"status": "passed"}},
    ]
    assert _scenario_status(steps) == "failed"


def test_scenario_status_with_error_step():
    steps = [
        {"result": {"status": "passed"}},
        {"result": {"status": "error"}},
    ]
    assert _scenario_status(steps) == "error"


def test_scenario_status_with_skipped_step():
    steps = [
        {"result": {"status": "passed"}},
        {"result": {"status": "skipped"}},
    ]
    assert _scenario_status(steps) == "skipped"


def test_scenario_status_empty_steps():
    assert _scenario_status([]) == "undefined"


def test_scenario_status_missing_result():
    steps = [{"keyword": "Given", "name": "something"}]
    assert _scenario_status(steps) == "undefined"


# ---------------------------------------------------------------------------
# load_test_results のテスト
# ---------------------------------------------------------------------------


def _make_cucumber_json(scenarios: list[dict]) -> list[dict]:
    """テスト用の Cucumber JSON データを構築するヘルパー。"""
    return [
        {
            "uri": "features/auth.feature",
            "name": "Auth Feature",
            "elements": scenarios,
        }
    ]


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
    assert result == {("auth", "ログインに成功する"): "passed"}


def test_load_test_results_failed(tmp_path: Path):
    data = _make_cucumber_json(
        [
            {
                "name": "無効なパスワードでログインを試みる",
                "tags": [{"name": "@SPEC-002"}],
                "steps": [
                    {"result": {"status": "passed"}},
                    {"result": {"status": "failed"}},
                ],
            }
        ]
    )
    json_file = tmp_path / "results.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_test_results(json_file)
    assert result == {("auth", "無効なパスワードでログインを試みる"): "failed"}


def test_load_test_results_error(tmp_path: Path):
    data = _make_cucumber_json(
        [
            {
                "name": "システムエラーが発生する",
                "steps": [
                    {"result": {"status": "error"}},
                ],
            }
        ]
    )
    json_file = tmp_path / "results.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_test_results(json_file)
    assert result == {("auth", "システムエラーが発生する"): "error"}


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
    assert result[("auth", "シナリオA")] == "failed"


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
    # どちらも優先度3なので、後のもので上書きされる
    assert result[("auth", "シナリオA")] == "error"


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
    test_result_map = {("auth", "ログイン"): "passed"}

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
        ("a", "P"): "passed",
        ("a", "F"): "failed",
        ("a", "E"): "error",
        ("a", "S"): "skipped",
    }

    p, f, e, s, t = spec_result_summary("SPEC-001", tag_map, test_result_map)
    assert (p, f, e, s, t) == (1, 1, 1, 1, 4)


def test_spec_result_summary_no_scenarios():
    tag_map: dict = {}
    test_result_map = {("auth", "ログイン"): "passed"}

    p, f, e, s, t = spec_result_summary("SPEC-001", tag_map, test_result_map)
    assert (p, f, e, s, t) == (0, 0, 0, 0, 0)


# ---------------------------------------------------------------------------
# result_badge のテスト
# ---------------------------------------------------------------------------


def test_result_badge_all_passed():
    assert "3/3 PASS" in result_badge(3, 0, 0, 0, 3)
    assert "0/3 FAIL" in result_badge(3, 0, 0, 0, 3)


def test_result_badge_mixed():
    badge = result_badge(1, 1, 1, 1, 4)
    assert "1/4 PASS" in badge
    assert "1/4 FAIL" in badge
    assert "1/4 ERROR" in badge
    assert "1/4 SKIP" in badge


def test_result_badge_no_scenarios():
    assert result_badge(0, 0, 0, 0, 0) == "-"


# ---------------------------------------------------------------------------
# test_status_badge のテスト
# ---------------------------------------------------------------------------


def test_format_status_badge_passed():
    assert format_status_badge("passed") == "✅ PASS"


def test_format_status_badge_failed():
    assert format_status_badge("failed") == "🔴 FAIL"


def test_format_status_badge_error():
    assert format_status_badge("error") == "❌ ERROR"


def test_format_status_badge_skipped():
    assert format_status_badge("skipped") == "⏭️ SKIP"
