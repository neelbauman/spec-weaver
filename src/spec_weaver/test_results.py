# src/spec_weaver/test_results.py
"""
Cucumber互換JSONテスト結果レポートの読み込みと集計ユーティリティ（REQ-005）。
"""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple

# (feature_file_stem, scenario_name) -> status ("passed" / "failed" / "skipped" 等)
TestResultMap = Dict[Tuple[str, str], str]

# ステータスの優先度（同名シナリオが複数回実行された場合に使用）
_STATUS_PRIORITY = {
    "failed": 3,
    "skipped": 2,
    "passed": 1,
    "pending": 0,
    "undefined": 0,
}


def _scenario_status(steps: list) -> str:
    """
    ステップのリストからシナリオ全体のステータスを判定する。

    優先順: failed > skipped > passed > undefined
    """
    if not steps:
        return "undefined"
    statuses = [step.get("result", {}).get("status") for step in steps]
    valid = [s for s in statuses if s]
    if not valid:
        return "undefined"
    if "failed" in valid:
        return "failed"
    if "skipped" in valid:
        return "skipped"
    if all(s == "passed" for s in valid):
        return "passed"
    return "undefined"


def load_test_results(results_file: Path) -> TestResultMap:
    """
    Cucumber互換JSONレポートを読み込み、TestResultMapを返す。

    同名シナリオが複数回出現した場合は優先度の高いステータスを採用する
    （failed > skipped > passed）。
    """
    with open(results_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    result_map: TestResultMap = {}

    for feature in data:
        uri = feature.get("uri", "")
        stem = Path(uri).stem
        for element in feature.get("elements", []):
            scenario_name = element.get("name", "")
            steps = element.get("steps", [])
            new_status = _scenario_status(steps)
            key = (stem, scenario_name)
            existing = result_map.get(key)
            if existing is None or (
                _STATUS_PRIORITY.get(new_status, 0) > _STATUS_PRIORITY.get(existing, 0)
            ):
                result_map[key] = new_status

    return result_map


def format_status_badge(status: Optional[str]) -> str:
    """テスト実行ステータスを絵文字バッジ文字列に変換する。"""
    if status == "passed":
        return "✅ PASS"
    elif status == "failed":
        return "❌ FAIL"
    elif status == "skipped":
        return "⏭️ SKIP"
    else:
        label = (status or "UNKNOWN").upper()
        return f"⏳ {label}"


def result_badge(passed: int, failed: int, total: int) -> str:
    """
    テスト集計結果（passed/failed/total）を絵文字バッジ文字列で返す。

    - total==0 またはいずれも未実行: "❓ -"
    - 全件成功:  "✅ N/N PASS"
    - 全件失敗:  "❌ N/N FAIL"
    - 混在:      "🟡 P✅ F❌ /N"
    """
    if total == 0 or (passed + failed == 0):
        return "❓ -"
    if failed == 0:
        return f"✅ {passed}/{total} PASS"
    if passed == 0:
        return f"❌ {failed}/{total} FAIL"
    return f"🟡 {passed}✅ {failed}❌ /{total}"


def spec_result_summary(
    uid: str, tag_map: dict, test_result_map: TestResultMap
) -> Tuple[int, int, int]:
    """
    指定UIDに紐づく全シナリオのテスト結果を集計する。

    Returns:
        (passed, failed, total)
    """
    scenarios = tag_map.get(uid, [])
    passed = failed = 0
    for sc in scenarios:
        key = (Path(sc["file"]).stem, sc["name"])
        status = test_result_map.get(key)
        if status == "passed":
            passed += 1
        elif status == "failed":
            failed += 1
    total = len(scenarios)
    return (passed, failed, total)
