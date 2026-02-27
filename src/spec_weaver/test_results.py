# src/spec_weaver/test_results.py

"""
Cucumber/Behave互換JSONテスト結果レポートの読み込みと集計ユーティリティ（REQ-005）。
"""

import json
from pathlib import Path
from typing import Dict, Optional, Tuple

# (feature_file_stem, scenario_or_feature_name) -> status
TestResultMap = Dict[Tuple[str, str], str]

# ステータスの優先度（error/failedを最優先する）
_STATUS_PRIORITY = {
    "failed": 3,
    "error": 3,
    "skipped": 2,
    "passed": 1,
    "pending": 0,
    "undefined": 0,
}

def _scenario_status(steps: list) -> str:
    """ステップのリストからシナリオ全体のステータスをフォールバック判定する。"""
    if not steps:
        return "undefined"
    statuses = [step.get("result", {}).get("status") for step in steps]
    valid = [s for s in statuses if s]
    if not valid:
        return "undefined"
    if "failed" in valid or "error" in valid:
        return "failed"
    if "skipped" in valid:
        return "skipped"
    if all(s == "passed" for s in valid):
        return "passed"
    return "undefined"

def load_test_results(results_file: Path) -> TestResultMap:
    """
    JSONレポートを読み込み、TestResultMapを返す。
    Featureレベル・Scenarioレベルの両方のタグ付けに完全対応する。
    """
    with open(results_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    result_map: TestResultMap = {}

    for feature in data:
        # Featureレベルの情報を取得（名前の空白を除去）
        feature_name = feature.get("name", "").strip()
        feat_loc = feature.get("uri") or feature.get("location") or ""
        feat_stem = Path(feat_loc.split(":")[0]).stem if feat_loc else ""

        # 【重要】Feature全体のステータスも辞書に登録する
        # （タグがFeature自体に付与されていた場合のマッピング用）
        if feat_stem and feature_name:
            feat_status = feature.get("status", "undefined")
            if feat_status == "error": feat_status = "failed"
            result_map[(feat_stem, feature_name)] = feat_status

        for element in feature.get("elements", []):
            if element.get("type") == "background":
                continue

            # 要素固有のパスを取得（なければFeatureのものを引き継ぐ）
            elem_loc = element.get("location") or feat_loc
            stem = Path(elem_loc.split(":")[0]).stem if elem_loc else feat_stem
            
            # シナリオ名の取得とアウトラインサフィックスの除去
            raw_name = element.get("name", "").strip()
            scenario_name = raw_name.split(" -- @")[0] if " -- @" in raw_name else raw_name

            # Behaveは要素自体に直接 'status' を持っているので最優先で使う
            new_status = element.get("status")
            if not new_status:
                new_status = _scenario_status(element.get("steps", []))
            
            if new_status == "error":
                new_status = "failed"

            key = (stem, scenario_name)
            existing = result_map.get(key)
            if existing is None or (
                _STATUS_PRIORITY.get(new_status, 0) > _STATUS_PRIORITY.get(existing, -1)
            ):
                result_map[key] = new_status

    return result_map

def format_status_badge(status: Optional[str]) -> str:
    if status == "passed": return "✅ PASS"
    elif status in ("failed", "error"): return "❌ FAIL"
    elif status == "skipped": return "⏭️ SKIP"
    else: return f"⏳ {(status or 'UNKNOWN').upper()}"

def result_badge(passed: int, failed: int, total: int) -> str:
    if total == 0 or (passed + failed == 0): return "-"
    if failed == 0: return f"✅ {passed}/{total} PASS"
    if passed == 0: return f"❌ {failed}/{total} FAIL"
    return f"🟡 {passed}✅ {failed}❌ /{total}"

def spec_result_summary(
    uid: str, tag_map: dict, test_result_map: TestResultMap
) -> Tuple[int, int, int]:
    scenarios = tag_map.get(uid, [])
    passed = failed = 0
    for sc in scenarios:
        # ドキュメント側（AST）の名前もstrip()して確実な一致を担保
        key = (Path(sc["file"]).stem, sc["name"].strip())
        status = test_result_map.get(key)
        
        if status == "passed": passed += 1
        elif status in ("failed", "error"): failed += 1
            
    return (passed, failed, len(scenarios))
