# src/spec_weaver/codegen.py
"""
Gherkin .feature ファイルから pytest-bdd テストコードの雛形を自動生成する。

関数名にはシナリオ名・ステップ文の SHA256 ハッシュ先頭8文字を使用し、
日本語等の非ASCII文字が関数名に混入するのを防ぐ（SPEC-015）。
"""

import hashlib
import textwrap
from pathlib import Path
from typing import Any

from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner


def _hash_name(text: str) -> str:
    """テキストの SHA256 ハッシュ先頭8文字を返す。"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def _step_keyword_to_prefix(keyword: str) -> str:
    """Gherkin ステップキーワードを pytest-bdd デコレータプレフィックスに変換する。"""
    k = keyword.strip().lower()
    if k in ("given", "前提"):
        return "given"
    if k in ("when", "もし"):
        return "when"
    if k in ("then", "ならば"):
        return "then"
    # And / But は直前のキーワードを引き継ぐため、呼び出し側で解決する
    return ""


def _escape_docstring(text: str) -> str:
    """docstring 内の三重引用符をエスケープする。"""
    return text.replace('"""', '\\"\\"\\"')


def _collect_scenarios(ast: dict) -> list[dict[str, Any]]:
    """AST から Scenario / Scenario Outline ノードを収集する。"""
    feature = ast.get("feature")
    if not feature:
        return []
    scenarios = []
    for child in feature.get("children", []):
        sc = child.get("scenario")
        if sc:
            scenarios.append(sc)
    return scenarios


def _resolve_step_prefixes(steps: list[dict]) -> list[tuple[str, str]]:
    """
    ステップリストを解析し、各ステップの (pytest_bdd_prefix, step_text) を返す。

    And / But キーワードは直前の Given/When/Then を引き継ぐ。
    """
    resolved: list[tuple[str, str]] = []
    current_prefix = "given"  # デフォルト
    for step in steps:
        keyword = step.get("keyword", "").strip()
        text = step.get("text", "").strip()
        prefix = _step_keyword_to_prefix(keyword)
        if prefix:
            current_prefix = prefix
        resolved.append((current_prefix, text))
    return resolved


def generate_test_file(
    feature_path: Path,
    out_dir: Path,
    features_base_dir: Path,
    overwrite: bool = False,
) -> Path | None:
    """
    単一の .feature ファイルから pytest-bdd テストファイルを生成する。

    Args:
        feature_path: 対象の .feature ファイルパス
        out_dir: テストコード出力先ディレクトリ
        features_base_dir: .feature ファイルのベースディレクトリ（conftest の bdd_features_base_dir に対応）
        overwrite: True の場合、既存ファイルを上書きする

    Returns:
        生成されたファイルの Path。スキップした場合は None。
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"test_{feature_path.stem}.py"

    if out_file.exists() and not overwrite:
        return None

    # Gherkin AST 解析
    with open(feature_path, "r", encoding="utf-8") as f:
        content = f.read()
    parser = Parser()
    ast = parser.parse(TokenScanner(content))

    feature = ast.get("feature")
    if not feature:
        return None

    feature_name = feature.get("name", feature_path.stem)
    scenarios = _collect_scenarios(ast)
    if not scenarios:
        return None

    # .feature ファイルの相対パス（pytest-bdd の @scenario デコレータ用）
    try:
        feature_rel = feature_path.relative_to(features_base_dir)
    except ValueError:
        feature_rel = Path(feature_path.name)
    feature_rel_posix = feature_rel.as_posix()

    # ステップ関数の重複排除用セット
    seen_steps: set[str] = set()  # (prefix, text) の hash をキーに
    step_functions: list[str] = []
    scenario_functions: list[str] = []

    for sc in scenarios:
        sc_name = sc.get("name", "Unnamed")
        sc_hash = _hash_name(sc_name)
        sc_docstring = _escape_docstring(sc_name)

        scenario_functions.append(
            f'@scenario("{feature_rel_posix}", "{_escape_docstring(sc_name)}")\n'
            f"def test_{sc_hash}():\n"
            f'    """{sc_docstring}"""\n'
            f"    pass\n"
        )

        # ステップ関数の生成
        steps = sc.get("steps", [])
        resolved = _resolve_step_prefixes(steps)
        for prefix, text in resolved:
            step_key = f"{prefix}:{text}"
            if step_key in seen_steps:
                continue
            seen_steps.add(step_key)

            step_hash = _hash_name(step_key)
            step_docstring = _escape_docstring(text)
            step_functions.append(
                f'@{prefix}("{_escape_docstring(text)}")\n'
                f"def {prefix}_{step_hash}():\n"
                f'    """{step_docstring}"""\n'
                f"    pass\n"
            )

    # ファイル組み立て
    lines: list[str] = []
    lines.append(f'"""pytest-bdd tests for: {_escape_docstring(feature_name)}"""')
    lines.append("")
    lines.append("from pytest_bdd import given, when, then, scenario")
    lines.append("")
    lines.append("")
    # シナリオ関数
    lines.append("# " + "=" * 70)
    lines.append("# Scenarios")
    lines.append("# " + "=" * 70)
    lines.append("")
    for sf in scenario_functions:
        lines.append(sf)
        lines.append("")

    # ステップ関数
    lines.append("# " + "=" * 70)
    lines.append("# Steps")
    lines.append("# " + "=" * 70)
    lines.append("")
    for stf in step_functions:
        lines.append(stf)
        lines.append("")

    out_file.write_text("\n".join(lines), encoding="utf-8")
    return out_file


def generate_conftest(
    out_dir: Path,
    features_base_dir: Path,
    overwrite: bool = False,
) -> Path | None:
    """
    pytest-bdd 用の conftest.py を生成する。

    Args:
        out_dir: conftest.py の出力先ディレクトリ
        features_base_dir: .feature ファイルのベースディレクトリ
        overwrite: True の場合、既存ファイルを上書きする

    Returns:
        生成されたファイルの Path。スキップした場合は None。
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    conftest_path = out_dir / "conftest.py"

    if conftest_path.exists() and not overwrite:
        return None

    # features_base_dir を conftest.py からの相対パスに変換
    try:
        rel = features_base_dir.resolve().relative_to(out_dir.resolve())
        rel_str = rel.as_posix()
    except ValueError:
        # 相対パスが作れない場合は絶対パスを使用
        rel_str = str(features_base_dir.resolve())

    content = textwrap.dedent(f"""\
        \"\"\"pytest-bdd conftest — auto-generated by spec-weaver scaffold.\"\"\"

        import pytest

        # .feature ファイルのベースディレクトリ
        # pytest-bdd はこのパスを基準に @scenario のファイルパスを解決します
        @pytest.fixture
        def bdd_features_base_dir():
            return "{rel_str}"
    """)

    conftest_path.write_text(content, encoding="utf-8")
    return conftest_path
