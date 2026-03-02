# src/spec_weaver/codegen.py
# implements: AUT-001

"""
Gherkin .feature ファイルから behave テストコードの雛形を自動生成・差分マージする。

関数名にはステップ文の SHA256 ハッシュ先頭8文字を使用し、
日本語等の非ASCII文字が関数名に混入するのを防ぐ。
ダブルクォーテーションで囲まれた文字列を自動的にパラメータ化し、DRY原則を保つ。
既存のステップファイルがある場合は、仮想新規ファイル方式により
.feature の出現順を維持しながら未実装ステップを差分追記し、
Docstring 内の Scenarios セクションを自動更新する。
"""

import ast as python_ast
import difflib
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner

# behave ステップデコレータ名
STEP_DECORATORS = frozenset({"given", "when", "then", "step"})


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
    text = text.replace("\\", "\\\\")
    parts = text.split('"')
    result = []
    for i, part in enumerate(parts):
        result.append(part)
        if i < len(parts) - 1:
            result.append("<" if i % 2 == 0 else ">")
    return "".join(result)


def _escape_docstring(text: str) -> str:
    """docstring（三重引用符）内で安全に使えるようエスケープする。"""
    return text.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')


# ---------------------------------------------------------------------------
# Python ソース AST 解析
# ---------------------------------------------------------------------------


@dataclass
class StepFunctionInfo:
    """既存ステップファイル内の1関数ブロックを表すデータクラス。"""

    name: str  # 関数名（e.g., "given_abc12345"）
    param_texts: list[str]  # デコレータ引数のステップテキスト
    source_text: str  # デコレータ〜関数末尾の生テキスト（後続の空行・コメント含む）
    is_stub: bool  # NotImplementedError('STEP:...') を含むか


def _extract_step_params(node: python_ast.FunctionDef) -> list[str]:
    """FunctionDef のデコレータから behave ステップテキストを抽出する。"""
    params: list[str] = []
    for deco in node.decorator_list:
        if (
            isinstance(deco, python_ast.Call)
            and isinstance(deco.func, python_ast.Name)
            and deco.func.id in STEP_DECORATORS
            and deco.args
            and isinstance(deco.args[0], python_ast.Constant)
            and isinstance(deco.args[0].value, str)
        ):
            params.append(deco.args[0].value)
    return params


def _has_stub_raise(node: python_ast.FunctionDef) -> bool:
    """関数内に raise NotImplementedError('STEP: ...') があるか判定する。"""
    for child in python_ast.walk(node):
        if isinstance(child, python_ast.Raise) and child.exc:
            exc = child.exc
            if (
                isinstance(exc, python_ast.Call)
                and isinstance(exc.func, python_ast.Name)
                and exc.func.id == "NotImplementedError"
                and exc.args
                and isinstance(exc.args[0], python_ast.Constant)
                and isinstance(exc.args[0].value, str)
                and exc.args[0].value.startswith("STEP:")
            ):
                return True
    return False


def _parse_step_file(content: str) -> tuple[str, list[StepFunctionInfo]]:
    """
    Python ステップファイルを AST 解析し、(ヘッダー, [StepFunctionInfo]) に分解する。

    ステップデコレータ (given/when/then/step) を持つトップレベル関数のみを抽出する。
    関数間のコメント・空行・ヘルパー関数は、直前のステップ関数の source_text に含まれる。
    構文エラーのあるファイルでは (content, []) を返す（マージ不可）。
    """
    try:
        tree = python_ast.parse(content)
    except SyntaxError:
        return content, []

    lines = content.splitlines(keepends=True)

    # トップレベルのステップ関数を収集（デコレータ開始行でソート）
    step_funcs: list[tuple[python_ast.FunctionDef, list[str], int]] = []
    for node in python_ast.iter_child_nodes(tree):
        if isinstance(node, python_ast.FunctionDef):
            params = _extract_step_params(node)
            if params:
                start = (
                    min(d.lineno for d in node.decorator_list)
                    if node.decorator_list
                    else node.lineno
                )
                step_funcs.append((node, params, start))

    step_funcs.sort(key=lambda x: x[2])

    if not step_funcs:
        return content, []

    # ヘッダー: 最初のステップ関数のデコレータ開始行より前
    header = "".join(lines[: step_funcs[0][2] - 1])

    # 各ステップ関数のブロックを構築
    infos: list[StepFunctionInfo] = []
    for i, (node, params, start) in enumerate(step_funcs):
        if i + 1 < len(step_funcs):
            end = step_funcs[i + 1][2] - 1  # 次の関数の開始行の前まで
        else:
            end = len(lines)  # 最後の関数はファイル末尾まで
        source_text = "".join(lines[start - 1 : end])
        infos.append(
            StepFunctionInfo(
                name=node.name,
                param_texts=params,
                source_text=source_text,
                is_stub=_has_stub_raise(node),
            )
        )

    return header, infos


# ---------------------------------------------------------------------------
# Gherkin AST パース・ステップ収集
# ---------------------------------------------------------------------------


def _collect_scenarios(ast: dict) -> list[dict[str, Any]]:
    """AST から Scenario / Background ノードを収集する。Rule ブロック内のシナリオも対象とする。"""
    feature = ast.get("feature")
    if not feature:
        return []
    blocks = []
    for child in feature.get("children", []):
        if "background" in child:
            blocks.append(child["background"])
        if "scenario" in child:
            blocks.append(child["scenario"])
        if "rule" in child:
            for rule_child in child["rule"].get("children", []):
                if "background" in rule_child:
                    blocks.append(rule_child["background"])
                if "scenario" in rule_child:
                    blocks.append(rule_child["scenario"])
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


def _collect_existing_steps(
    steps_dir: Path, exclude_file: Path | None = None
) -> set[str]:
    """
    指定ディレクトリ配下の Python ファイルから定義済みの behave ステップ文を収集する。
    AST 解析により、コメント行のデコレータは自然に無視される。
    exclude_file を指定するとそのファイルは走査対象から除外する。
    """
    existing_steps: set[str] = set()
    if not steps_dir.exists():
        return existing_steps

    for py_file in steps_dir.glob("*.py"):
        if exclude_file and py_file.resolve() == exclude_file.resolve():
            continue
        try:
            content = py_file.read_text(encoding="utf-8")
            tree = python_ast.parse(content)
            for node in python_ast.walk(tree):
                if isinstance(node, python_ast.FunctionDef):
                    for param_text in _extract_step_params(node):
                        existing_steps.add(param_text)
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
        return (
            f"# [Duplicate Skip] This step is already defined elsewhere\n{commented}\n"
        )
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
    ideal_func_to_info: dict[str, StepFunctionInfo],
    duplicate_func_names: set[str] | None = None,
) -> str:
    """
    仮想新規ファイルの関数順序を基に、既存ファイルへ差分マージを行う。

    - 既存関数: Docstring の Scenarios セクションに不足シナリオを追記
    - 新規関数: .feature の出現順（ideal_order）に従い適切な位置に挿入
    - スタブ関数で他ファイルに実装済みのもの: Duplicate コメントブロックへ置き換え
    """
    header, existing_infos = _parse_step_file(existing_content)

    # 既存ブロックのメタデータを構築
    result_infos: list[StepFunctionInfo] = list(existing_infos)
    existing_param_texts: dict[str, int] = {}
    for i, info in enumerate(result_infos):
        for pt in info.param_texts:
            existing_param_texts[pt] = i

    result_names = [info.name for info in result_infos]

    for i, func_name in enumerate(ideal_order):
        ideal_info = ideal_func_to_info[func_name]
        ideal_pt = ideal_info.param_texts[0] if ideal_info.param_texts else None

        match_idx = -1
        if func_name in result_names:
            match_idx = result_names.index(func_name)
        elif ideal_pt and ideal_pt in existing_param_texts:
            match_idx = existing_param_texts[ideal_pt]

        if match_idx != -1:
            # 既存関数: Scenarios セクションを更新
            existing_info = result_infos[match_idx]
            ideal_scenarios = _extract_scenarios_from_block(ideal_info.source_text)
            existing_scenarios = _extract_scenarios_from_block(
                existing_info.source_text
            )
            missing = [s for s in ideal_scenarios if s not in existing_scenarios]
            if missing:
                result_infos[match_idx] = StepFunctionInfo(
                    name=existing_info.name,
                    param_texts=existing_info.param_texts,
                    source_text=_add_scenarios_to_block(
                        existing_info.source_text, missing
                    ),
                    is_stub=existing_info.is_stub,
                )
        else:
            # 新規関数: アンカーを探して挿入位置を決定
            # ideal_order[i] より前で result_names に存在する最後の関数 = アンカー
            anchor_idx = -1
            for j in range(i - 1, -1, -1):
                if ideal_order[j] in result_names:
                    anchor_idx = result_names.index(ideal_order[j])
                    break

            insert_pos = anchor_idx + 1  # アンカーなし(-1)のときは先頭(0)
            result_infos.insert(insert_pos, ideal_info)
            result_names.insert(insert_pos, func_name)

    # 他ファイルに実装済みのスタブを Duplicate コメントブロックへ置き換える
    if duplicate_func_names:
        for i, info in enumerate(result_infos):
            if info.name in duplicate_func_names and info.is_stub:
                commented = "\n".join(
                    f"# {line}"
                    for line in info.source_text.rstrip("\n").split("\n")
                )
                result_infos[i] = StepFunctionInfo(
                    name=info.name,
                    param_texts=info.param_texts,
                    source_text=(
                        "# [Duplicate Skip] This step is already defined "
                        f"elsewhere\n{commented}\n\n"
                    ),
                    is_stub=False,
                )

    return header + "".join(info.source_text for info in result_infos)


# ---------------------------------------------------------------------------
# 公開 API
# ---------------------------------------------------------------------------


ENVIRONMENT_PY_TEMPLATE = """\"""behave 環境設定: シナリオごとの共通 setup / teardown。\"""

import os
import shutil
import tempfile
import traceback
from pathlib import Path
from behave.model_core import Status

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def before_scenario(context, scenario):
    \"""各シナリオ開始前にテスト用一時ディレクトリを用意する。\"""
    context.project_root = PROJECT_ROOT
    context.temp_dir = Path(tempfile.mkdtemp(prefix="sw_test_"))
    context.repo_root = None  # ステップで設定
    context.feature_dir = None  # ステップで設定
    context.out_dir = None  # ステップで設定
    context.result = None  # subprocess.CompletedProcess
    context.exit_code = None
    context.output = ""
    # 単体テスト用
    context.item = None
    context.value = None
    context.error = None
    context.items_dir = None


def after_scenario(context, scenario):
    \"""各シナリオ終了後に一時ファイルを削除し、作業ディレクトリを戻す。\"""
    os.chdir(PROJECT_ROOT)
    if hasattr(context, "temp_dir") and context.temp_dir and context.temp_dir.exists():
        shutil.rmtree(context.temp_dir, ignore_errors=True)


def after_step(context, step):
    \"""ステップ実行後の処理。エラー時に詳細な実行ログを記録する（REQ-005 拡張）。\"""
    if step.status == Status.error:
        # トレースバックをキャプチャして step.error_message に格納
        if hasattr(step, "exception") and step.exception:
            if hasattr(step, "exc_traceback") and step.exc_traceback:
                # exc_traceback がある場合は完全なトレースバックを取得
                tb = "".join(
                    traceback.format_exception(
                        type(step.exception), step.exception, step.exc_traceback
                    )
                )
                step.error_message = tb
            else:
                # 例外のみの場合
                step.error_message = (
                    f"{type(step.exception).__name__}: {str(step.exception)}"
                )

        # JSON フォーマッタに error_message フィールドを出力させるため、
        # error ステータスを failed に強制する（behave の JSON フォーマッタの制約への対策）
        step.status = Status.failed
"""


def generate_environment_file(
    feature_dir: Path,
    overwrite: bool = False,
) -> tuple[Path, str, str] | None:
    """
    environment.py を生成する。

    Returns:
        (out_file, "created", "") — 新規作成
        None                    — スキップ（既存かつ overwrite=False）
    """
    env_file = feature_dir / "environment.py"
    if env_file.exists() and not overwrite:
        return None

    env_file.write_text(ENVIRONMENT_PY_TEMPLATE, encoding="utf-8")
    return env_file, "created", ""


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
        new_content = _generate_file_content(
            feature_name, step_registry, global_existing_steps
        )
        out_file.write_text(new_content, encoding="utf-8")
        return out_file, "created", ""

    # --- 差分マージ ---
    # 自ファイルを除いた他のステップファイルから重複チェック用ステップを収集
    global_existing_steps = _collect_existing_steps(out_dir, exclude_file=out_file)
    ideal_content = _generate_file_content(
        feature_name, step_registry, global_existing_steps
    )

    # 仮想新規ファイルから関数順序と StepFunctionInfo を取得
    _, ideal_infos = _parse_step_file(ideal_content)
    ideal_order: list[str] = [info.name for info in ideal_infos]
    ideal_func_to_info: dict[str, StepFunctionInfo] = {
        info.name: info for info in ideal_infos
    }

    # 他ファイルに実装済みのステップ関数名を収集（スタブ→Duplicate コメント変換用）
    duplicate_func_names: set[str] = set()
    for meta in step_registry.values():
        if meta["param_text"] in global_existing_steps:
            fname = f"{meta['prefix']}_{_hash_name(meta['prefix'] + ':' + meta['param_text'])}"
            duplicate_func_names.add(fname)

    existing_content = out_file.read_text(encoding="utf-8")
    new_content = _merge_content(
        existing_content, ideal_order, ideal_func_to_info, duplicate_func_names
    )

    if new_content == existing_content:
        return None

    diff_lines = list(
        difflib.unified_diff(
            existing_content.splitlines(),
            new_content.splitlines(),
            fromfile=f"a/{out_file.name}",
            tofile=f"b/{out_file.name}",
            lineterm="",
        )
    )
    diff_text = "\n".join(diff_lines)

    out_file.write_text(new_content, encoding="utf-8")
    return out_file, "updated", diff_text
