# src/spec_weaver/codegen.py

"""
Gherkin .feature ファイルから behave テストコードの雛形を自動生成する。

関数名にはシナリオ名・ステップ文の SHA256 ハッシュ先頭8文字を使用し、
日本語等の非ASCII文字が関数名に混入するのを防ぐ。
また、ダブルクォーテーションで囲まれた文字列を自動的にパラメータ化し、DRY原則を保つ。
"""

import hashlib
from pathlib import Path
from typing import Any
import re

from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner


def _hash_name(text: str) -> str:
    """テキストの SHA256 ハッシュ先頭8文字を返す。"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def _step_keyword_to_prefix(keyword: str) -> str:
    """Gherkin ステップキーワードを behave デコレータプレフィックスに変換する。"""
    k = keyword.strip().lower()
    if k in ("given", "前提"):
        return "given"
    if k in ("when", "もし"):
        return "when"
    if k in ("then", "ならば"):
        return "then"
    return ""


def _parameterize_step(text: str) -> tuple[str, list[str]]:
    """
    ステップ文の中の "..." を検知し、behave 形式のパラメータ {param0}, {param1} に置換する。
    
    Returns:
        tuple[str, list[str]]: (パラメータ化されたテキスト, パラメータ名のリスト)
    """
    params = []
    
    def replacer(match):
        param_name = f"param{len(params)}"
        params.append(param_name)
        # behaveのフォーマットである "{param_name}" に置換
        return f'"{{{param_name}}}"'

    # "任意の文字列" を抽出して置換
    parameterized_text = re.sub(r'"([^"]*)"', replacer, text)
    
    # デコレータをシングルクォートで囲むため、テキスト内のシングルクォートをエスケープ
    parameterized_text = parameterized_text.replace("'", "\\'")
    return parameterized_text, params


def _escape_string(text: str) -> str:
    """
    文字列内のバックスラッシュをエスケープし、ダブルクォーテーションを < > に置換する。
    （テスト互換用）
    """
    # バックスラッシュのエスケープ
    text = text.replace('\\', '\\\\')
    # クオーテーションの置換
    parts = text.split('"')
    result = []
    for i, part in enumerate(parts):
        result.append(part)
        if i < len(parts) - 1:
            result.append('<' if i % 2 == 0 else '>')
    return "".join(result)


def _escape_docstring(text: str) -> str:
    """docstring（三重引用符）内で安全に使えるようエスケープする。"""
    return text.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')

def _collect_scenarios(ast: dict) -> list[dict[str, Any]]:
    """AST から Scenario / Scenario Outline および Background ノードを収集する。"""
    feature = ast.get("feature")
    if not feature:
        return []
    blocks = []
    for child in feature.get("children", []):
        # 背景（Background）ブロックも収集対象に含める
        if "background" in child:
            blocks.append(child["background"])
        # シナリオブロック
        if "scenario" in child:
            blocks.append(child["scenario"])
    return blocks


def _resolve_step_prefixes(steps: list[dict]) -> list[tuple[str, str]]:
    """And / But キーワードを直前の Given/When/Then に解決して返す。"""
    resolved: list[tuple[str, str]] = []
    current_prefix = "given"
    for step in steps:
        keyword = step.get("keyword", "").strip()
        text = step.get("text", "").strip()
        prefix = _step_keyword_to_prefix(keyword)
        if prefix:
            current_prefix = prefix
        resolved.append((current_prefix, text))
    return resolved


def _collect_existing_steps(steps_dir: Path) -> set[str]:
    """
    指定ディレクトリ配下の Python ファイルから、定義済みの behave ステップ文を収集する。
    """
    existing_steps = set()
    if not steps_dir.exists():
        return existing_steps

    pattern = re.compile(r'@(?:given|when|then|step)\s*\(\s*["\'](.*?)["\']\s*\)')
    
    for py_file in steps_dir.glob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
            for match in pattern.finditer(content):
                existing_steps.add(match.group(1))
        except Exception:
            continue
    return existing_steps

def generate_test_file(
    feature_path: Path,
    out_dir: Path,
    features_base_dir: Path,
    overwrite: bool = False,
) -> Path | None:
    """単一の .feature ファイルから behave ステップ定義ファイルを生成する。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"step_{feature_path.stem}.py"

    if out_file.exists() and not overwrite:
        return None

    global_existing_steps = _collect_existing_steps(out_dir)

    with open(feature_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    ast = Parser().parse(TokenScanner(content))
    feature = ast.get("feature")
    if not feature:
        return None

    feature_name = feature.get("name", feature_path.stem)
    scenarios = _collect_scenarios(ast)
    if not scenarios:
        return None

    # --- 変更点 1: ステップとシナリオの対応関係を記録する辞書を構築 ---
    # key: step_key ("prefix:param_text")
    # value: ステップのメタデータと、それを使用するシナリオ名のリスト
    step_registry: dict[str, dict] = {}

    for sc in scenarios:
        scenario_name = sc.get("name", "Unknown Scenario")
        steps = sc.get("steps", [])
        resolved = _resolve_step_prefixes(steps)
        
        for prefix, raw_text in resolved:
            param_text, params = _parameterize_step(raw_text)
            step_key = f"{prefix}:{param_text}"
            
            if step_key not in step_registry:
                step_registry[step_key] = {
                    "prefix": prefix,
                    "param_text": param_text,
                    "raw_text": raw_text,
                    "params": params,
                    "scenarios": []
                }
            
            # 同じステップが同じシナリオ内で複数回呼ばれるケースを考慮し、重複を防ぐ
            if scenario_name not in step_registry[step_key]["scenarios"]:
                step_registry[step_key]["scenarios"].append(scenario_name)

    # --- 変更点 2: 構築した辞書を元にPythonコードを生成 ---
    step_functions: list[str] = []

    for step_key, meta in step_registry.items():
        prefix = meta["prefix"]
        param_text = meta["param_text"]
        params = meta["params"]
        scenario_names = meta["scenarios"]

        is_duplicate = param_text in global_existing_steps
        step_hash = _hash_name(step_key)
        doc_text = _escape_docstring(meta["raw_text"])
        args = ", ".join(["context"] + params)

        # シナリオ参照コメントの組み立て
        comment_lines = ["# 使用されるシナリオ:"]
        for sn in scenario_names:
            comment_lines.append(f"# - {sn}")
        scenario_comments = "\n".join(comment_lines)

        # Pyrightの誤検知を防ぐ # type: ignore もここで付与
        func_code = (
            f"{scenario_comments}\n"
            f"@{prefix}('{param_text}')  # type: ignore\n"
            f"def {prefix}_{step_hash}({args}):\n"
            f'    """{doc_text}"""\n'
            f"    raise NotImplementedError('STEP: {param_text}')\n"
        )

        if is_duplicate:
            commented = "\n".join([f"# {line}" for line in func_code.strip().split("\n")])
            step_functions.append(f"# [Duplicate Skip] This step is already defined elsewhere\n{commented}\n")
        else:
            step_functions.append(func_code)

    if not step_functions:
        return None

    # --- ファイル組み立て ---
    lines: list[str] = [
        f'"""behave steps for: {_escape_docstring(feature_name)}"""',
        "",
        "from behave import given, when, then, step",
        "",
        "# " + "=" * 70,
        "# Steps",
        "# " + "=" * 70,
        ""
    ]
    
    for stf in step_functions:
        lines.append(stf)
        lines.append("")

    out_file.write_text("\n".join(lines), encoding="utf-8")
    return out_file

