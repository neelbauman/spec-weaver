# src/spec_weaver/adapters/codegen.py
# implements: AUT-001

"""
Gherkin .feature ファイルから behave テストコードの雛形を自動生成・差分マージする。

関数名にはステップ文の SHA256 ハッシュ先頭8文字を使用し、
日本語等の非ASCII文字が関数名に混入するのを防ぐ。
ダブルクォーテーションで囲まれた文字列を自動的にパラメータ化し、DRY原則を保つ。
既存のステップファイルがある場合は、仮想新規ファイル方式により
.feature の出現順を維持しながら未実装ステップを差分追記し、
Docstring 内の Scenarios セクションを自動更新する。

【重複判定戦略（AmbiguousStepの防止）】
1. Prefix違いの吸収:
   同一のステップテキストに対して "Given" や "When" などの Prefix が異なる場合、
   behave ではグローバル空間で衝突し AmbiguousStep となる。
   そのため、ステップレジストリのキーをプレフィックスを含まないテキスト単体とし、
   最初に出現したPrefixで代表して関数を生成する。
2. リネーム耐性 (StepResolverの活用):
   開発者が可読性のために `{param0}` を `{user_name}` のように手動リネームした場合、
   単純なテキストの完全一致では「未実装の新規ステップ」と誤認し再生成してしまう。
   これを防ぐため、`StepResolver` (内部的に parse ライブラリを利用) を用いた
   意味論的なマッチングを行い、既存のステップ（スタブ含む）と一致するかを
   動的に判定して重複生成をスキップ、または Duplicate コメントとして処理する。
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

from spec_weaver.core.step_resolver import StepDefinition, StepResolver

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
    ステップ文の中の "..." や <placeholder> を検知し、
    behave 形式のパラメータ {param0}, {placeholder} に置換する。

    Returns:
        tuple[str, list[str]]: (パラメータ化されたテキスト, パラメータ名のリスト)
    """
    params: list[str] = []

    # 1. ダブルクォーテーションで囲まれた部分を {paramN} に置換
    def quote_replacer(match: re.Match) -> str:
        param_name = f"param{len(params)}"
        params.append(param_name)
        return f'"{{{param_name}}}"'

    text = re.sub(r'"([^"]*)"', quote_replacer, text)

    # 2. <placeholder> 部分を {placeholder} に置換 (Scenario Outline)
    def angle_replacer(match: re.Match) -> str:
        param_name = match.group(1)
        if param_name not in params:
            params.append(param_name)
        return f"{{{param_name}}}"

    parameterized_text = re.sub(r"<([\w\d_-]+)>", angle_replacer, text)
    parameterized_text = parameterized_text.replace("'", "\\'")
    return parameterized_text, params


def _escape_string(text: str) -> str:
    """文字列内の二重引用符を不等号に、バックスラッシュをエスケープする。"""
    res = text.replace("\\", "\\\\")
    # 対になった二重引用符を < > に置換する簡易的な実装
    count = 0
    def replacer(m):
        nonlocal count
        res = "<" if count % 2 == 0 else ">"
        count += 1
        return res
    return re.sub(r'"', replacer, res)


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

    header = "".join(lines[: step_funcs[0][2] - 1])

    infos: list[StepFunctionInfo] = []
    for i, (node, params, start) in enumerate(step_funcs):
        if i + 1 < len(step_funcs):
            end = step_funcs[i + 1][2] - 1
        else:
            end = len(lines)
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


def _load_existing_resolver(
    steps_dir: Path, exclude_file: Path | None = None
) -> StepResolver:
    """
    指定ディレクトリ配下の Python ファイルから定義済みのステップを読み込み、
    リネーム耐性のあるマッチングを行うための StepResolver を返す。
    """
    resolver = StepResolver()
    if not steps_dir.exists():
        return resolver

    for py_file in steps_dir.glob("*.py"):
        if exclude_file and py_file.resolve() == exclude_file.resolve():
            continue
        # Resolverの内部関数を利用してファイルごとにパースさせる
        resolver._parse_file(py_file)
        
    return resolver


def _build_step_registry(ast: dict) -> dict[str, dict]:
    """
    AST からステップレジストリを構築する。
    キー: "param_text" (Prefix違いを吸収する)、値: ステップのメタデータ
    """
    step_registry: dict[str, dict] = {}
    for sc in _collect_scenarios(ast):
        scenario_name = sc.get("name", "Unknown Scenario")
        for prefix, raw_text in _resolve_step_prefixes(sc.get("steps", [])):
            param_text, params = _parameterize_step(raw_text)
            
            # キーを param_text にし、異なるPrefixでも同じテキストなら1つにまとめる
            step_key = param_text
            if step_key not in step_registry:
                step_registry[step_key] = {
                    "prefix": prefix,  # 最初に出現したPrefixを生成時に使用
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
    """1つのステップ関数コードブロックを文字列として生成する。"""
    # 関数名ハッシュは prefix:param_text から生成し、テストとの互換性を保つ
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
    existing_resolver: StepResolver,
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
        # StepResolver を用いて既存実装（リネームされたもの含む）にマッチするか判定
        match = existing_resolver.resolve_step(meta["prefix"], meta["raw_text"])
        is_duplicate = match is not None
        
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
        end = scenarios_match.end(2)
        return block[:end] + insert_text + block[end:]

    closing = block.rfind('"""')
    if closing == -1:
        return block
    insert = f"\n\n    Scenarios:\n{insert_text}    "
    return block[:closing] + insert + block[closing:]


def _merge_content(
    existing_content: str,
    ideal_order: list[str],
    ideal_func_to_info: dict[str, StepFunctionInfo],
    step_registry: dict[str, dict],
    existing_resolver: StepResolver,
    out_file_path: Path,
) -> str:
    """仮想新規ファイルの関数順序を基に、既存ファイルへ差分マージを行う。"""
    header, existing_infos = _parse_step_file(existing_content)
    out_file_abs = out_file_path.resolve()

    result_infos: list[StepFunctionInfo] = list(existing_infos)

    for i, func_name in enumerate(ideal_order):
        # 挿入が発生するたび、現在の result_infos に基づいてマッピングを再構築する。
        # これにより、挿入によるインデックスのズレを防ぐ。
        result_names = [info.name for info in result_infos]
        current_param_texts: dict[str, int] = {}
        for idx, info in enumerate(result_infos):
            for pt in info.param_texts:
                current_param_texts[pt] = idx

        ideal_info = ideal_func_to_info[func_name]
        ideal_pt = ideal_info.param_texts[0] if ideal_info.param_texts else None
        meta = step_registry.get(ideal_pt)

        match_idx = -1
        if func_name in result_names:
            match_idx = result_names.index(func_name)
        elif ideal_pt and ideal_pt in current_param_texts:
            match_idx = current_param_texts[ideal_pt]
        elif meta:
            # Semantic match check (Rename/Parameterization tolerance)
            # 現在の result_infos を対象に、Semantic なマッチングを試みる
            for idx, info in enumerate(result_infos):
                matched = False
                for pt in info.param_texts:
                    sd = StepDefinition(meta["prefix"], pt, info.source_text, str(out_file_abs), 0)
                    if sd.matches(meta["prefix"], meta["raw_text"]):
                        match_idx = idx
                        matched = True
                        break
                if matched:
                    break

        if match_idx != -1:
            existing_info = result_infos[match_idx]
            # 重複判定された場合（他ファイルに実体がある）、既存がスタブならコメント化
            is_globally_implemented = False
            if meta:
                # すべての登録ステップからマッチするものを探し、他ファイルに「スタブでない」実装があるか確認
                for step_def in existing_resolver.steps:
                    if step_def.matches(meta["prefix"], meta["raw_text"]):
                        if (
                            Path(step_def.file).resolve() != out_file_abs
                            and not step_def.is_stub
                        ):
                            is_globally_implemented = True
                            break

            if is_globally_implemented and existing_info.is_stub:
                commented = "\n".join(
                    f"# {line}"
                    for line in existing_info.source_text.rstrip("\n").split("\n")
                )
                result_infos[match_idx] = StepFunctionInfo(
                    name=existing_info.name,
                    param_texts=existing_info.param_texts,
                    source_text=(
                        "# [Duplicate Skip] This step is already defined "
                        f"elsewhere\n{commented}\n\n"
                    ),
                    is_stub=False,
                )
            else:
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
            anchor_idx = -1
            for j in range(i - 1, -1, -1):
                if ideal_order[j] in result_names:
                    anchor_idx = result_names.index(ideal_order[j])
                    break

            insert_pos = anchor_idx + 1
            result_infos.insert(insert_pos, ideal_info)

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


def _collect_existing_steps(steps_dir: Path) -> list[str]:
    """
    指定ディレクトリ配下の Python ファイルから定義済みのステップパターンを抽出する。
    後方互換性とテストのために残す。
    """
    resolver = StepResolver()
    resolver.load_steps(steps_dir)
    # コメントアウトされているものを除外するために、
    # 実際の内容を確認する（StepResolverの実装に依存するが、
    # 簡易的に source を見て # で始まっていないか確認）
    return [
        s.pattern
        for s in resolver.steps
        if not s.source.lstrip().startswith("#")
    ]


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

def collect_all_feature_steps(feature_files: list[Path]) -> set[tuple[str, str]]:
    """
    全 .feature ファイルから使われているステップの (prefix, raw_text) のセットを返す。
    """
    all_steps: set[tuple[str, str]] = set()
    for fpath in feature_files:
        try:
            content = fpath.read_text(encoding="utf-8")
            ast = Parser().parse(TokenScanner(content))
            for sc in _collect_scenarios(ast):
                for prefix, raw_text in _resolve_step_prefixes(sc.get("steps", [])):
                    all_steps.add((prefix, raw_text))
        except Exception:
            continue
    return all_steps


def prepare_test_file_content(
    feature_path: Path,
    out_dir: Path,
    features_base_dir: Path,
    overwrite: bool = False,
) -> tuple[str, str, str] | None:
    """
    テストファイルの新規作成またはマージ後の内容を計算する。

    Returns:
        tuple[str, str, str] | None: (status, new_content, diff_text)
        status: "created" or "updated"
        new_content: 生成されたファイル全体の内容
        diff_text: 差分（新規作成時は空文字列）
        変更がない場合は None を返す。
    """
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
        existing_resolver = _load_existing_resolver(out_dir)
        new_content = _generate_file_content(
            feature_name, step_registry, existing_resolver
        )
        return "created", new_content, ""

    # --- 差分マージ ---
    existing_resolver = _load_existing_resolver(out_dir, exclude_file=out_file)
    
    # ideal_content 生成時は、すべてのステップを FunctionDef として出力させるため
    # 空の Resolver を使用する（そうしないと重複ステップがコメントアウトされ AST パースで消えてしまう）
    ideal_content = _generate_file_content(
        feature_name, step_registry, StepResolver()
    )

    _, ideal_infos = _parse_step_file(ideal_content)
    ideal_order: list[str] = [info.name for info in ideal_infos]
    ideal_func_to_info: dict[str, StepFunctionInfo] = {
        info.name: info for info in ideal_infos
    }

    existing_content = out_file.read_text(encoding="utf-8")
    new_content = _merge_content(
        existing_content,
        ideal_order,
        ideal_func_to_info,
        step_registry,
        existing_resolver,
        out_file,
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

    return "updated", new_content, diff_text


def generate_test_file(
    feature_path: Path,
    out_dir: Path,
    features_base_dir: Path,
    overwrite: bool = False,
) -> tuple[Path, str, str] | None:
    """単一の .feature ファイルから behave ステップ定義ファイルを生成・マージする。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"step_{feature_path.stem}.py"

    res = prepare_test_file_content(feature_path, out_dir, features_base_dir, overwrite)
    if res is None:
        return None

    status, new_content, diff_text = res
    out_file.write_text(new_content, encoding="utf-8")
    return out_file, status, diff_text
