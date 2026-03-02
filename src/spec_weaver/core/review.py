# src/spec_weaver/review.py
# implements: AUT-003

"""
セマンティックレビュー機能。

- collect_review_files: アイテムIDから仕様・Gherkin・実装コードのパスを収集する
- build_review_prompt: Claude に渡すプロンプトを組み立てる
- run_claude_review: Claude を subprocess で呼び出し、結果を ReviewResult として返す
- run_all_reviews: 全アイテムを ThreadPoolExecutor で並列レビューする
"""

from __future__ import annotations

import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

from spec_weaver.adopters.doorstop import get_item_map, _get_custom_attribute
from spec_weaver.adopters.gherkin import get_tag_map
from spec_weaver.adopters.impl_scanner import get_ref_files, ImplScanner

# ---------------------------------------------------------------------------
# 定数
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "1.0"

SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2}

FINDING_KINDS = {"missing_implementation", "undocumented_feature", "semantic_contradiction"}


# ---------------------------------------------------------------------------
# データクラス (Task 1)
# ---------------------------------------------------------------------------

@dataclass
class ReviewFinding:
    kind: str        # missing_implementation | undocumented_feature | semantic_contradiction
    severity: str    # high | medium | low
    title: str
    detail: str
    location: str = ""

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "severity": self.severity,
            "title": self.title,
            "detail": self.detail,
            "location": self.location,
        }


@dataclass
class ReviewResult:
    schema_version: str
    item_id: str
    item_title: str
    reviewed_files: list[str]
    findings: list[ReviewFinding]
    summary: str

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "item_id": self.item_id,
            "item_title": self.item_title,
            "reviewed_files": self.reviewed_files,
            "findings": [f.to_dict() for f in self.findings],
            "summary": self.summary,
        }


@dataclass
class ReviewReport:
    schema_version: str
    items: list[ReviewResult] = field(default_factory=list)

    def to_dict(self) -> dict:
        total = len(self.items)
        high = sum(
            1 for r in self.items
            for f in r.findings if f.severity == "high"
        )
        medium = sum(
            1 for r in self.items
            for f in r.findings if f.severity == "medium"
        )
        low = sum(
            1 for r in self.items
            for f in r.findings if f.severity == "low"
        )
        return {
            "schema_version": self.schema_version,
            "items": [r.to_dict() for r in self.items],
            "summary": {
                "total_items": total,
                "findings_by_severity": {"high": high, "medium": medium, "low": low},
            },
        }


# ---------------------------------------------------------------------------
# ヘルパー
# ---------------------------------------------------------------------------

def severity_gte(a: str, b: str) -> bool:
    """severity a が b 以上なら True を返す。"""
    return SEVERITY_ORDER.get(a, 0) >= SEVERITY_ORDER.get(b, 0)


def filter_findings(findings: list[ReviewFinding], min_severity: str) -> list[ReviewFinding]:
    """min_severity 以上の severity を持つ finding のみを返す。"""
    return [f for f in findings if severity_gte(f.severity, min_severity)]


# ---------------------------------------------------------------------------
# ファイル収集 (Task 2)
# ---------------------------------------------------------------------------

def collect_review_files(
    item_id: str,
    feature_dir: Path,
    repo_root: Path,
) -> dict[str, list[Path]]:
    """アイテムIDから仕様・Gherkin・実装コードのパスを収集する。

    Returns:
        {"spec": [...], "feature": [...], "steps": [...], "impl": [...]}

    Raises:
        ValueError: アイテムIDが見つからない場合
    """
    item_map = get_item_map(repo_root)
    if item_id not in item_map:
        raise ValueError(f"アイテム '{item_id}' が Doorstop で見つかりません")

    item = item_map[item_id]

    # 仕様 YAML
    spec_paths: list[Path] = []
    if hasattr(item, "path") and item.path:
        spec_paths = [Path(item.path)]

    # Gherkin .feature ファイル
    feature_paths: list[Path] = []
    try:
        tag_map = get_tag_map(feature_dir, prefixes={item_id.split("-")[0]})
        for scenario_info in tag_map.get(item_id, []):
            raw = scenario_info.get("file", "")
            # get_tag_map は features_dir.parent からの相対パスを返す
            candidate = feature_dir.parent / raw
            if candidate.exists() and candidate not in feature_paths:
                feature_paths.append(candidate)
    except Exception:
        pass

    # ステップ定義ファイル（feature ファイルと同ディレクトリの steps/ から探索）
    step_paths: list[Path] = []
    visited_steps_dirs: set[Path] = set()
    for fp in feature_paths:
        steps_dir = fp.parent / "steps"
        if steps_dir.exists() and steps_dir not in visited_steps_dirs:
            visited_steps_dirs.add(steps_dir)
            for sp in sorted(steps_dir.glob("*.py")):
                step_paths.append(sp)

    # 実装ファイル（impl_files 属性 + アノテーションスキャン）
    impl_paths: list[Path] = []
    seen_impl: set[Path] = set()

    # impl_files カスタム属性から
    for rel in get_ref_files(item):
        p = (repo_root / rel).resolve()
        if p.exists() and p not in seen_impl:
            seen_impl.add(p)
            impl_paths.append(p)

    # アノテーションスキャンから
    scanner = ImplScanner()
    annotation_map = scanner.scan(repo_root, extensions=["py", "ts", "js"])
    for rel in annotation_map.get(item_id, set()):
        p = (repo_root / rel).resolve()
        if p.exists() and p not in seen_impl:
            seen_impl.add(p)
            impl_paths.append(p)

    return {
        "spec": spec_paths,
        "feature": feature_paths,
        "steps": step_paths,
        "impl": impl_paths,
    }


# ---------------------------------------------------------------------------
# プロンプト生成 (Task 3)
# ---------------------------------------------------------------------------

def _get_item_title(item: Any) -> str:
    """Doorstop アイテムのタイトル（header または text の先頭行）を返す。"""
    header = _get_custom_attribute(item, "header", None)
    if header and str(header).strip():
        return str(header).strip().splitlines()[0].strip()
    text = _get_custom_attribute(item, "text", "")
    if text:
        return str(text).strip().splitlines()[0].strip()[:80]
    return ""


def build_review_prompt(item_id: str, item_title: str, files: list[Path] | None = None) -> str:
    """Claude に渡すプロンプトを組み立てる。

    files を指定した場合、各ファイルの内容をプロンプトに埋め込む。
    """
    file_section = ""
    if files:
        parts: list[str] = []
        for fp in files:
            try:
                content = fp.read_text(encoding="utf-8", errors="replace")
                parts.append(f"### {fp}\n```\n{content}\n```")
            except Exception:
                parts.append(f"### {fp}\n（読み込み失敗）")
        file_section = "\n\n## 対象ファイル\n\n" + "\n\n".join(parts)

    return f"""以下のファイルを解析し、仕様・Gherkin・実装コードの意味的整合性をレビューしてください。

対象アイテム: {item_id} — {item_title}{file_section}

## 評価観点
1. missing_implementation: 仕様に記述された要件が実装に存在するか
2. undocumented_feature: 実装に存在する振る舞いが仕様に記述されているか
3. semantic_contradiction: 仕様とコードの両方に記述はあるが内容が食い違っていないか

## 出力形式
以下のJSONスキーマに従い、純粋なJSONのみで出力してください（説明文・Markdownコードブロック不要）。

{{
  "schema_version": "1.0",
  "item_id": "{item_id}",
  "item_title": "{item_title}",
  "reviewed_files": ["<path>", "..."],
  "findings": [
    {{
      "kind": "missing_implementation|undocumented_feature|semantic_contradiction",
      "severity": "high|medium|low",
      "title": "<短い説明>",
      "detail": "<詳細>",
      "location": "<該当箇所>"
    }}
  ],
  "summary": "<全体的な評価コメント>"
}}

findingが存在しない場合は "findings": [] としてください。
severity の基準:
- high: セキュリティ・データ整合性・主要機能に関わる乖離
- medium: エラーハンドリング・境界値・副作用の不一致
- low: 軽微な表現の違い・補足情報の欠落
"""


# ---------------------------------------------------------------------------
# JSON 抽出ヘルパー
# ---------------------------------------------------------------------------

def _extract_last_json(text: str) -> dict | None:
    """stdout テキストから末尾の JSON オブジェクトを抽出する。

    非 JSON 行（ログ・進捗表示等）を無視し、最後に出現した {} ブロックを返す。
    """
    # JSON コードブロック（```json ... ```）の中身を優先
    code_block = re.findall(r"```(?:json)?\s*([\s\S]*?)```", text)
    candidates = list(code_block)

    # それ以外に { で始まる行を探す
    brace_blocks: list[str] = []
    depth = 0
    buf: list[str] = []
    for ch in text:
        if ch == "{":
            depth += 1
        if depth > 0:
            buf.append(ch)
        if ch == "}":
            depth -= 1
            if depth == 0 and buf:
                brace_blocks.append("".join(buf))
                buf = []

    candidates.extend(brace_blocks)

    # 末尾から順に valid な JSON を探す
    for candidate in reversed(candidates):
        try:
            obj = json.loads(candidate.strip())
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    return None


def _parse_review_result(data: dict) -> ReviewResult:
    """dict を ReviewResult に変換する。"""
    findings = []
    for f in data.get("findings", []):
        findings.append(ReviewFinding(
            kind=f.get("kind", "semantic_contradiction"),
            severity=f.get("severity", "low"),
            title=f.get("title", ""),
            detail=f.get("detail", ""),
            location=f.get("location", ""),
        ))
    return ReviewResult(
        schema_version=data.get("schema_version", SCHEMA_VERSION),
        item_id=data.get("item_id", ""),
        item_title=data.get("item_title", ""),
        reviewed_files=data.get("reviewed_files", []),
        findings=findings,
        summary=data.get("summary", ""),
    )


# ---------------------------------------------------------------------------
# Claude 呼び出し (Task 3)
# ---------------------------------------------------------------------------

def run_claude_review(
    item_id: str,
    feature_dir: Path,
    repo_root: Path,
    timeout: int = 300,
) -> ReviewResult:
    """Claude を subprocess で呼び出し、セマンティックレビュー結果を返す。

    Args:
        timeout: Claude プロセスの最大待機秒数（デフォルト300秒）。

    Raises:
        FileNotFoundError: claude バイナリが見つからない場合
        ValueError: アイテムIDが見つからない場合 / JSON 解析に失敗した場合
    """
    import os
    import shutil
    if shutil.which("claude") is None:
        raise FileNotFoundError(
            "'claude' コマンドが見つかりません。Claude Code CLI をインストールしてください。"
        )

    item_map = get_item_map(repo_root)
    if item_id not in item_map:
        raise ValueError(f"アイテム '{item_id}' が Doorstop で見つかりません")

    item = item_map[item_id]
    item_title = _get_item_title(item)

    files_dict = collect_review_files(item_id, feature_dir, repo_root)
    all_files: list[Path] = (
        files_dict["spec"] + files_dict["feature"] + files_dict["steps"] + files_dict["impl"]
    )

    # ファイル内容をプロンプトに埋め込む（--file フラグは API File ID 形式のため使用不可）
    prompt = build_review_prompt(item_id, item_title, files=all_files)

    # CLAUDECODE 環境変数を除外してネスト制限を回避する
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    cmd = ["claude", "-p", prompt]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        env=env,
    )

    stdout = result.stdout
    data = _extract_last_json(stdout)
    if data is None:
        # JSON が取れなかった場合は error finding として返す
        return ReviewResult(
            schema_version=SCHEMA_VERSION,
            item_id=item_id,
            item_title=item_title,
            reviewed_files=[str(f) for f in all_files],
            findings=[ReviewFinding(
                kind="semantic_contradiction",
                severity="high",
                title="レビュー結果の解析に失敗",
                detail=f"Claude の出力から JSON を抽出できませんでした。stdout: {stdout[:500]} stderr: {result.stderr[:200]}",
                location="",
            )],
            summary="レビュー実行時にエラーが発生しました。",
        )

    review = _parse_review_result(data)
    # item_id / reviewed_files を補完
    if not review.item_id:
        review.item_id = item_id
    if not review.item_title:
        review.item_title = item_title
    if not review.reviewed_files:
        review.reviewed_files = [str(f) for f in all_files]
    return review


# ---------------------------------------------------------------------------
# 並列実行 (Task 4)
# ---------------------------------------------------------------------------

def run_all_reviews(
    feature_dir: Path,
    repo_root: Path,
    max_workers: int = 3,
    on_complete: Optional[Callable[[str, ReviewResult], None]] = None,
    timeout: int = 300,
) -> ReviewReport:
    """全アイテムを ThreadPoolExecutor で並列レビューする。

    Args:
        on_complete: アイテム1件のレビュー完了時に呼ばれるコールバック。
                     引数は (item_id, result)。進捗表示に利用する。
        timeout: 各アイテムの Claude プロセス最大待機秒数。
    """
    item_map = get_item_map(repo_root)
    item_ids = list(item_map.keys())

    report = ReviewReport(schema_version=SCHEMA_VERSION)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(run_claude_review, item_id, feature_dir, repo_root, timeout): item_id
            for item_id in item_ids
        }
        for future in as_completed(futures):
            item_id = futures[future]
            try:
                result = future.result()
            except Exception as e:
                item = item_map.get(item_id)
                title = _get_item_title(item) if item else ""
                result = ReviewResult(
                    schema_version=SCHEMA_VERSION,
                    item_id=item_id,
                    item_title=title,
                    reviewed_files=[],
                    findings=[ReviewFinding(
                        kind="semantic_contradiction",
                        severity="high",
                        title="レビュー実行エラー",
                        detail=str(e),
                        location="",
                    )],
                    summary="レビュー実行時にエラーが発生しました。",
                )
            report.items.append(result)
            if on_complete is not None:
                on_complete(item_id, result)

    # item_id でソートして順序を安定させる
    report.items.sort(key=lambda r: r.item_id)
    return report
