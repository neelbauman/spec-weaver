# src/spec_weaver/test_results.py
"""
pytest-bdd が生成する Cucumber 互換 JSON レポートを読み込み、
テスト結果と SPEC ID を突き合わせるためのモジュール。
"""

import json
from pathlib import Path
from typing import Any

# (feature_file_stem, scenario_name) -> "passed"|"failed"|"skipped"|"undefined"
TestResultMap = dict[tuple[str, str], str]


def _scenario_status(steps: list[dict[str, Any]]) -> str:
    """ステップ一覧からシナリオのステータスを判定する。

    すべてのステップが passed なら "passed"、
    それ以外は最初に見つかった非 passed ステータスを返す。
    """
    if not steps:
        return "undefined"
    for step in steps:
        result = step.get("result", {})
        status = result.get("status", "undefined")
        if status != "passed":
            return status  # "failed", "skipped", "undefined", "pending" など
    return "passed"


def load_test_results(json_path: Path) -> TestResultMap:
    """pytest-bdd 生成の Cucumber 互換 JSON レポートを読み込む。

    Args:
        json_path: Cucumber 互換 JSON ファイルのパス

    Returns:
        TestResultMap: (featureファイルstem, シナリオ名) → ステータス のマッピング。
        同名シナリオが複数回実行された場合、failed が passed より優先される。
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result_map: TestResultMap = {}

    for feature in data:
        uri = feature.get("uri", "")
        feature_stem = Path(uri).stem
        for element in feature.get("elements", []):
            scenario_name = element.get("name", "")
            steps = element.get("steps", [])
            status = _scenario_status(steps)
            key = (feature_stem, scenario_name)
            # 同名シナリオが複数回実行された場合、failed を優先する
            if key not in result_map or result_map[key] == "passed":
                result_map[key] = status

    return result_map


def format_status_badge(status: str) -> str:
    """テスト結果ステータスを絵文字バッジ付きの文字列に変換する。"""
    return {
        "passed": "✅ PASS",
        "failed": "❌ FAIL",
        "skipped": "⏭️ SKIP",
        "undefined": "❓ UNDEF",
        "pending": "⏳ PENDING",
    }.get(status, f"❓ {status}")


def spec_result_summary(
    uid: str,
    tag_map: dict,
    test_result_map: TestResultMap,
) -> tuple[int, int, int]:
    """SPEC 単体のテスト結果集計を返す。

    Returns:
        (passed_count, failed_count, total_count)
        シナリオが存在しない場合はすべて 0。
    """
    scenarios = tag_map.get(uid, [])
    if not scenarios:
        return (0, 0, 0)

    passed = 0
    failed = 0
    for s in scenarios:
        key = (Path(s["file"]).stem, s["name"])
        status = test_result_map.get(key)
        if status == "passed":
            passed += 1
        elif status is not None:
            failed += 1
    return (passed, failed, len(scenarios))


def result_badge(passed: int, failed: int, total: int) -> str:
    """PASS/FAIL 集計を絵文字付きの文字列に変換する。

    Args:
        passed: PASS 件数
        failed: FAIL 件数
        total: シナリオ総数

    Returns:
        "✅ 3/3 PASS" / "❌ 1/3 FAIL" / "🟡 2/3 PASS" / "❓ -" など
    """
    if total == 0:
        return "❓ -"
    no_result = total - passed - failed
    if no_result == total:
        # 結果が1件もない
        return "❓ -"
    if failed == 0 and no_result == 0:
        return f"✅ {passed}/{total} PASS"
    if passed == 0 and no_result == 0:
        return f"❌ {failed}/{total} FAIL"
    return f"🟡 {passed}✅/{failed}❌/{no_result}❓ ({total})"
