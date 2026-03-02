# src/spec_weaver/test_results.py

"""
Cucumber/Behave互換JSONテスト結果レポートの読み込みと集計ユーティリティ（REQ-005）。
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# (feature_file_stem, scenario_or_feature_name) -> {status: str, error: str}
TestResultMap = Dict[Tuple[str, str], Dict[str, Any]]

# ステータスの優先度（error/failedを最優先する）
_STATUS_PRIORITY = {
    "error": 4,
    "failed": 3,
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
    if "error" in valid:
        return "error"
    if "failed" in valid:
        return "failed"
    if "skipped" in valid:
        return "skipped"
    if all(s == "passed" for s in valid):
        return "passed"
    return "undefined"


def _extract_error(steps: list) -> Optional[str]:
    """失敗したステップからエラーメッセージまたはトレースバックを抽出する。"""
    for step in steps:
        result = step.get("result", {})
        if result.get("status") in ("failed", "error"):
            err = result.get("error_message")
            if isinstance(err, list):
                return "\n".join(err)
            return err
    return None


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
        # 明示的な status フィールドがある場合のみ登録する（デフォルト undefined は無視）
        feat_status = feature.get("status")
        if feat_stem and feature_name and feat_status is not None:
            result_map[(feat_stem, feature_name)] = {
                "status": feat_status,
                "error": _extract_error(feature.get("elements", [])),
            }

        for element in feature.get("elements", []):
            if element.get("type") == "background":
                continue

            # 要素固有のパスを取得（なければFeatureのものを引き継ぐ）
            elem_loc = element.get("location") or feat_loc
            stem = Path(elem_loc.split(":")[0]).stem if elem_loc else feat_stem

            # シナリオ名の取得とアウトラインサフィックスの除去
            raw_name = element.get("name", "").strip()
            scenario_name = (
                raw_name.split(" -- @")[0] if " -- @" in raw_name else raw_name
            )

            # Behaveは要素自体に直接 'status' を持っているので最優先で使う
            new_status = element.get("status")
            if not new_status:
                new_status = _scenario_status(element.get("steps", []))

            key = (stem, scenario_name)
            existing = result_map.get(key)
            if existing is None or (
                _STATUS_PRIORITY.get(new_status, 0)
                >= _STATUS_PRIORITY.get(existing["status"], -1)
            ):
                result_map[key] = {
                    "status": new_status,
                    "error": _extract_error(element.get("steps", [])),
                }

    return result_map


def format_status_badge(status: Optional[str]) -> str:
    if status == "passed":
        return "✅ PASS"
    elif status == "failed":
        return "🔴 FAIL"
    elif status == "error":
        return "❌ ERROR"
    elif status == "skipped":
        return "⏭️ SKIP"
    else:
        return f"⏳ {(status or 'UNKNOWN').upper()}"


def result_badge(passed: int, failed: int, error: int, skipped: int, total: int) -> str:
    if total == 0:
        return "-"
    return f"✅ {passed}/{total} PASS, 🔴 {failed}/{total} FAIL, ❌ {error}/{total} ERROR, ⏭️{skipped}/{total} SKIP"


def spec_result_summary(
    uid: str, tag_map: dict, test_result_map: TestResultMap
) -> Tuple[int, int, int, int, int]:
    scenarios = tag_map.get(uid, [])
    passed = failed = error = skipped = 0
    for sc in scenarios:
        # ドキュメント側（AST）の名前もstrip()して確実な一致を担保
        key = (Path(sc["file"]).stem, sc["name"].strip())
        res = test_result_map.get(key)
        status = res["status"] if res else None

        if status == "passed":
            passed += 1
        elif status == "failed":
            failed += 1
        elif status == "error":
            error += 1
        elif status == "skipped":
            skipped += 1

    return (passed, failed, error, skipped, len(scenarios))
