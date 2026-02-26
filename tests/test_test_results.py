"""
test_results モジュールのユニットテスト。
pytest-bdd 生成の Cucumber 互換 JSON を読み込み、
(feature_stem, scenario_name) → status マッピングを検証する。
"""

import json
import pytest
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
    data = _make_cucumber_json([
        {
            "name": "ログインに成功する",
            "tags": [{"name": "@SPEC-001"}],
            "steps": [
                {"result": {"status": "passed"}},
                {"result": {"status": "passed"}},
            ],
        }
    ])
    json_file = tmp_path / "results.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_test_results(json_file)
    assert result == {("auth", "ログインに成功する"): "passed"}


def test_load_test_results_failed(tmp_path: Path):
    data = _make_cucumber_json([
        {
            "name": "無効なパスワードでログインを試みる",
            "tags": [{"name": "@SPEC-002"}],
            "steps": [
                {"result": {"status": "passed"}},
                {"result": {"status": "failed"}},
            ],
        }
    ])
    json_file = tmp_path / "results.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_test_results(json_file)
    assert result == {("auth", "無効なパスワードでログインを試みる"): "failed"}


def test_load_test_results_failed_takes_priority_over_passed(tmp_path: Path):
    """同名シナリオが複数回実行された場合、failed が passed より優先される。"""
    data = [
        {
            "uri": "features/auth.feature",
            "elements": [{"name": "シナリオA", "steps": [{"result": {"status": "passed"}}]}],
        },
        {
            "uri": "features/auth.feature",
            "elements": [{"name": "シナリオA", "steps": [{"result": {"status": "failed"}}]}],
        },
    ]
    json_file = tmp_path / "results.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_test_results(json_file)
    assert result[("auth", "シナリオA")] == "failed"


def test_load_test_results_multiple_features(tmp_path: Path):
    data = [
        {
            "uri": "features/login.feature",
            "elements": [{"name": "ログイン", "steps": [{"result": {"status": "passed"}}]}],
        },
        {
            "uri": "features/logout.feature",
            "elements": [{"name": "ログアウト", "steps": [{"result": {"status": "failed"}}]}],
        },
    ]
    json_file = tmp_path / "results.json"
    json_file.write_text(json.dumps(data), encoding="utf-8")

    result = load_test_results(json_file)
    assert result[("login", "ログイン")] == "passed"
    assert result[("logout", "ログアウト")] == "failed"


def test_load_test_results_empty_json(tmp_path: Path):
    json_file = tmp_path / "results.json"
    json_file.write_text("[]", encoding="utf-8")

    result = load_test_results(json_file)
    assert result == {}


# ---------------------------------------------------------------------------
# spec_result_summary のテスト
# ---------------------------------------------------------------------------

def test_spec_result_summary_all_passed():
    tag_map = {
        "SPEC-001": [
            {"file": "features/auth.feature", "name": "ログイン", "line": 5, "keyword": "Scenario"},
        ]
    }
    test_result_map = {("auth", "ログイン"): "passed"}

    passed, failed, total = spec_result_summary("SPEC-001", tag_map, test_result_map)
    assert passed == 1
    assert failed == 0
    assert total == 1


def test_spec_result_summary_with_failure():
    tag_map = {
        "SPEC-001": [
            {"file": "features/auth.feature", "name": "ログイン成功", "line": 5, "keyword": "Scenario"},
            {"file": "features/auth.feature", "name": "ログイン失敗", "line": 10, "keyword": "Scenario"},
        ]
    }
    test_result_map = {
        ("auth", "ログイン成功"): "passed",
        ("auth", "ログイン失敗"): "failed",
    }

    passed, failed, total = spec_result_summary("SPEC-001", tag_map, test_result_map)
    assert passed == 1
    assert failed == 1
    assert total == 2


def test_spec_result_summary_no_scenarios():
    tag_map: dict = {}
    test_result_map = {("auth", "ログイン"): "passed"}

    passed, failed, total = spec_result_summary("SPEC-001", tag_map, test_result_map)
    assert (passed, failed, total) == (0, 0, 0)


def test_spec_result_summary_scenario_not_in_results():
    """シナリオが存在するが結果ファイルに含まれていない場合。"""
    tag_map = {
        "SPEC-001": [
            {"file": "features/auth.feature", "name": "未実行シナリオ", "line": 5, "keyword": "Scenario"},
        ]
    }
    test_result_map: dict = {}

    passed, failed, total = spec_result_summary("SPEC-001", tag_map, test_result_map)
    assert passed == 0
    assert failed == 0
    assert total == 1


# ---------------------------------------------------------------------------
# result_badge のテスト
# ---------------------------------------------------------------------------

def test_result_badge_all_passed():
    assert result_badge(3, 0, 3) == "✅ 3/3 PASS"


def test_result_badge_all_failed():
    assert result_badge(0, 3, 3) == "❌ 3/3 FAIL"


def test_result_badge_partial():
    badge = result_badge(2, 1, 3)
    assert "🟡" in badge
    assert "2✅" in badge
    assert "1❌" in badge


def test_result_badge_no_results():
    """シナリオは存在するが実行結果がない場合。"""
    assert result_badge(0, 0, 2) == "❓ -"


def test_result_badge_no_scenarios():
    assert result_badge(0, 0, 0) == "❓ -"


# ---------------------------------------------------------------------------
# test_status_badge のテスト
# ---------------------------------------------------------------------------

def test_format_status_badge_passed():
    assert format_status_badge("passed") == "✅ PASS"


def test_format_status_badge_failed():
    assert format_status_badge("failed") == "❌ FAIL"


def test_format_status_badge_skipped():
    assert format_status_badge("skipped") == "⏭️ SKIP"


def test_format_status_badge_unknown():
    badge = format_status_badge("pending")
    assert "PENDING" in badge
