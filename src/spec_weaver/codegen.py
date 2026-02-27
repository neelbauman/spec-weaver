# src/spec_weaver/codegen.py
# implements: SPEC-015

"""
Gherkin .feature ファイルから behave テストコードの雛形を自動生成・差分マージする。

関数名にはステップ文の SHA256 ハッシュ先頭8文字を使用し、
日本語等の非ASCII文字が関数名に混入するのを防ぐ。
ダブルクォーテーションで囲まれた文字列を自動的にパラメータ化し、DRY原則を保つ。
既存のステップファイルがある場合は、仮想新規ファイル方式により
.feature の出現順を維持しながら未実装ステップを差分追記し、
Docstring 内の Scenarios セクションを自動更新する。
"""

import difflib
import hashlib
import re
from pathlib import Path
from typing import Any

from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner


# ---------------------------------------------------------------------------
# ユーティリティ
# ---------------------------------------------------------------------------


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
    params: list[str] = []

    def replacer(match: re.Match) -> str:
        param_name = f"param{len(params)}"
        params.append(param_name)
        return f'"{{{param_name}}}"'

    parameterized_text = re.sub(r'"([^"]*)"', replacer, text)
    parameterized_text = parameterized_text.replace("'", "\\'")
    return parameterized_text, params


def _escape_string(text: str) -> str:
    """
    文字列内のバックスラッシュをエスケープし、ダブルクォーテーションを < > に置換する。
    （テスト互換用）
    """
    text = text.replace('\\', '\\\\')
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


# ---------------------------------------------------------------------------
# AST パース・ステップ収集
# ---------------------------------------------------------------------------


def _collect_scenarios(ast: dict) -> list[dict[str, Any]]:
    """AST から Scenario / Background ノードを収集する。"""
    feature = ast.get("feature")
    if not feature:
        return []
    blocks = []
    for child in feature.get("children", []):
        if "background" in child:
            blocks.append(child["background"])
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


def _collect_existing_steps(steps_dir: Path, exclude_file: Path | None = None) -> set[str]:
    """
    指定ディレクトリ配下の Python ファイルから定義済みの behave ステップ文を収集する。
    exclude_file を指定するとそのファイルは走査対象から除外する。
    """
    existing_steps: set[str] = set()
    if not steps_dir.exists():
        return existing_steps

    pattern = re.compile(r'@(?:given|when|then|step)\s*\(\s*["\'](.*?)["\']\s*\)')

    for py_file in steps_dir.glob("*.py"):
        if exclude_file and py_file.resolve() == exclude_file.resolve():
            continue
        try:
            content = py_file.read_text(encoding="utf-8")
            for match in pattern.finditer(content):
                existing_steps.add(match.group(1))
        except Exception:
            continue
    return existing_steps


def _build_step_registry(ast: dict) -> dict[str, dict]:
    """
    AST からステップレジストリを構築する。
    キー: "prefix:param_text"、値: ステップのメタデータ（.feature の出現順を保持）
    """
    step_registry: dict[str, dict] = {}
    for sc in _collect_scenarios(ast):
        scenario_name = sc.get("name", "Unknown Scenario")
        for prefix, raw_text in _resolve_step_prefixes(sc.get("steps", [])):
            param_text, params = _parameterize_step(raw_text)
            step_key = f"{prefix}:{param_text}"
            if step_key not in step_registry:
                step_registry[step_key] = {
                    "prefix": prefix,
                    "param_text": param_text,
                    "raw_text": raw_text,
                    "params": params,
                    "scenarios": [],
                }
            if scenario_name not in step_registry[step_key]["scenarios"]:
                step_registry[step_key]["scenarios"].append(scenario_name)
    return step_registry


# ---------------------------------------------------------------------------
# コードブロック生成
# ---------------------------------------------------------------------------


def _build_step_block(
    prefix: str,
    param_text: str,
    params: list[str],
    raw_text: str,
    scenario_names: list[str],
    is_duplicate: bool,
) -> str:
    """
    1つのステップ関数コードブロックを文字列として生成する。
    Docstring には Scenarios セクションを含む。
    """
    func_name = f"{prefix}_{_hash_name(f'{prefix}:{param_text}')}"
    args = ", ".join(["context"] + params)
    doc_text = _escape_docstring(raw_text)
    scenario_lines = "\n".join(f"      - {sn}" for sn in scenario_names)
    docstring = f'    """{doc_text}\n\n    Scenarios:\n{scenario_lines}\n    """'

    code = (
        f"@{prefix}('{param_text}')  # type: ignore\n"
        f"def {func_name}({args}):\n"
        f"{docstring}\n"
        f"    raise NotImplementedError('STEP: {param_text}')\n"
    )

    if is_duplicate:
        commented = "\n".join(f"# {line}" for line in code.strip().split("\n"))
        return f"# [Duplicate Skip] This step is already defined elsewhere\n{commented}\n"
    return code


def _generate_file_content(
    feature_name: str,
    step_registry: dict[str, dict],
    global_existing_steps: set[str],
) -> str:
    """ステップレジストリからファイル全体の内容を生成する。"""
    lines: list[str] = [
        f'"""behave steps for: {_escape_docstring(feature_name)}"""',
        "",
        "from behave import given, when, then, step",
        "",
        "# " + "=" * 70,
        "# Steps",
        "# " + "=" * 70,
        "",
    ]

    for meta in step_registry.values():
        is_duplicate = meta["param_text"] in global_existing_steps
        block = _build_step_block(
            meta["prefix"],
            meta["param_text"],
            meta["params"],
            meta["raw_text"],
            meta["scenarios"],
            is_duplicate,
        )
        lines.append(block)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# マージ用ヘルパー
# ---------------------------------------------------------------------------


def _split_by_decorators(content: str) -> tuple[str, list[str]]:
    """
    ファイル内容を (ヘッダー, [@デコレータ起点のブロックリスト]) に分割する。
    各ブロックは @ で始まり、次の @ の直前で終わる。
    """
    parts = re.split(r"(?m)^(?=@)", content)
    if len(parts) == 1:
        return content, []
    return parts[0], parts[1:]


def _get_func_name_from_block(block: str) -> str | None:
    """デコレータ起点のブロックから関数名を取得する。"""
    m = re.search(r"^def (\w+)\(", block, re.MULTILINE)
    return m.group(1) if m else None


def _extract_scenarios_from_block(block: str) -> list[str]:
    """ブロック内の Scenarios セクションからシナリオ名のリストを返す。"""
    m = re.search(r"Scenarios:\s*\n((?:\s+- .+\n)*)", block)
    if not m:
        return []
    return re.findall(r"^\s+- (.+)$", m.group(1), re.MULTILINE)


def _add_scenarios_to_block(block: str, new_scenarios: list[str]) -> str:
    """既存ブロックの Docstring に不足シナリオを追記する。"""
    insert_text = "".join(f"      - {s}\n" for s in new_scenarios)

    scenarios_match = re.search(r"(Scenarios:\s*\n)((?:\s+- .+\n)*)", block)
    if scenarios_match:
        # 既存 Scenarios セクションの末尾に追記
        end = scenarios_match.end(2)
        return block[:end] + insert_text + block[end:]

    # Scenarios セクションがない場合、Docstring の閉じ """ の直前に追加
    closing = block.rfind('"""')
    if closing == -1:
        return block
    insert = f"\n\n    Scenarios:\n{insert_text}    "
    return block[:closing] + insert + block[closing:]


def _merge_content(
    existing_content: str,
    ideal_order: list[str],
    ideal_func_to_block: dict[str, str],
) -> str:
    """
    仮想新規ファイルの関数順序を基に、既存ファイルへ差分マージを行う。

    - 既存関数: Docstring の Scenarios セクションに不足シナリオを追記
    - 新規関数: .feature の出現順（ideal_order）に従い適切な位置に挿入
    """
    header, existing_blocks = _split_by_decorators(existing_content)

    # 既存ブロックを (func_name, block_str) のリストに変換
    result_pairs: list[tuple[str, str]] = []
    for block in existing_blocks:
        fname = _get_func_name_from_block(block)
        if fname:
            result_pairs.append((fname, block))
        elif result_pairs:
            # 関数名が取れないブロック（コメントアウトされた重複など）は直前ブロックに結合
            prev_name, prev_block = result_pairs[-1]
            result_pairs[-1] = (prev_name, prev_block + block)

    result_names = [name for name, _ in result_pairs]

    for i, func_name in enumerate(ideal_order):
        if func_name in result_names:
            # 既存関数: Scenarios セクションを更新
            idx = result_names.index(func_name)
            existing_block = result_pairs[idx][1]
            ideal_scenarios = _extract_scenarios_from_block(ideal_func_to_block[func_name])
            existing_scenarios = _extract_scenarios_from_block(existing_block)
            missing = [s for s in ideal_scenarios if s not in existing_scenarios]
            if missing:
                result_pairs[idx] = (func_name, _add_scenarios_to_block(existing_block, missing))
        else:
            # 新規関数: アンカーを探して挿入位置を決定
            # ideal_order[i] より前で result_names に存在する最後の関数 = アンカー
            anchor_idx = -1
            for j in range(i - 1, -1, -1):
                if ideal_order[j] in result_names:
                    anchor_idx = result_names.index(ideal_order[j])
                    break

            insert_pos = anchor_idx + 1  # アンカーなし(-1)のときは先頭(0)
            new_block = ideal_func_to_block[func_name]
            result_pairs.insert(insert_pos, (func_name, new_block))
            result_names.insert(insert_pos, func_name)

    return header + "".join(block for _, block in result_pairs)


# ---------------------------------------------------------------------------
# 公開 API
# ---------------------------------------------------------------------------


def generate_test_file(
    feature_path: Path,
    out_dir: Path,
    features_base_dir: Path,
    overwrite: bool = False,
) -> tuple[Path, str, str] | None:
    """
    単一の .feature ファイルから behave ステップ定義ファイルを生成・マージする。

    Returns:
        (out_file, "created", "")        — 新規ファイルを作成した
        (out_file, "updated", diff_text) — 既存ファイルを差分マージした
        None                             — 変更なし（スキップ）
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"step_{feature_path.stem}.py"

    content = feature_path.read_text(encoding="utf-8")
    ast = Parser().parse(TokenScanner(content))
    feature = ast.get("feature")
    if not feature:
        return None

    feature_name = feature.get("name", feature_path.stem)
    step_registry = _build_step_registry(ast)
    if not step_registry:
        return None

    # --- 新規作成 / 全上書き ---
    if not out_file.exists() or overwrite:
        global_existing_steps = _collect_existing_steps(out_dir)
        new_content = _generate_file_content(feature_name, step_registry, global_existing_steps)
        out_file.write_text(new_content, encoding="utf-8")
        return out_file, "created", ""

    # --- 差分マージ ---
    # 自ファイルを除いた他のステップファイルから重複チェック用ステップを収集
    global_existing_steps = _collect_existing_steps(out_dir, exclude_file=out_file)
    ideal_content = _generate_file_content(feature_name, step_registry, global_existing_steps)

    # 仮想新規ファイルから関数順序とブロックを取得
    _, ideal_blocks = _split_by_decorators(ideal_content)
    ideal_order: list[str] = []
    ideal_func_to_block: dict[str, str] = {}
    for block in ideal_blocks:
        fname = _get_func_name_from_block(block)
        if fname:
            ideal_order.append(fname)
            ideal_func_to_block[fname] = block

    existing_content = out_file.read_text(encoding="utf-8")
    new_content = _merge_content(existing_content, ideal_order, ideal_func_to_block)

    if new_content == existing_content:
        return None

    diff_lines = list(difflib.unified_diff(
        existing_content.splitlines(),
        new_content.splitlines(),
        fromfile=f"a/{out_file.name}",
        tofile=f"b/{out_file.name}",
        lineterm="",
    ))
    diff_text = "\n".join(diff_lines)

    out_file.write_text(new_content, encoding="utf-8")
    return out_file, "updated", diff_text
