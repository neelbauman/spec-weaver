"""behave steps for: 仕様アイテムと実装ファイルのリンク管理"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml
from behave import given, when, then

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _helpers import (
    PROJECT_ROOT,
    create_doorstop_project_yaml,
    run_spec_weaver,
)

from spec_weaver.impl_scanner import get_ref_files, ImplScanner


# ======================================================================
# ヘルパー
# ======================================================================


def _update_spec_yaml(context, spec_id: str, key: str, value) -> None:
    """SPEC YAML ファイルの指定キーを更新または削除する。"""
    spec_file = context.repo_root / "specs" / f"{spec_id}.yml"
    with open(spec_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if value is None:
        data.pop(key, None)
    else:
        data[key] = value
    with open(spec_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=True)


def _create_source_file(context, rel_path: str, content: str) -> None:
    """context.repo_root 以下にソースファイルを作成する。"""
    file_path = context.repo_root / rel_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def _run_cmd(context, param0: str) -> None:
    """'spec-weaver <subcommand> [options]' 形式のコマンドを解釈して実行する。"""
    # "spec-weaver " プレフィックスを除去
    cmd = param0
    if cmd.startswith("spec-weaver "):
        cmd = cmd[len("spec-weaver ") :]

    parts = cmd.split()
    subcommand = parts[0]
    remaining = parts[1:]

    # -f ./specification/features を実際の feature_dir に置換
    processed = []
    i = 0
    while i < len(remaining):
        if remaining[i] == "-f" and i + 1 < len(remaining):
            processed += ["-f", str(context.feature_dir)]
            i += 2
        else:
            processed.append(remaining[i])
            i += 1

    # audit の場合: feature_dir 引数を先頭に追加
    if subcommand == "audit":
        args = ["audit", str(context.feature_dir)] + processed
    else:
        args = [subcommand] + processed

    # --repo-root が未指定の場合は追加
    if "--repo-root" not in args:
        args += ["--repo-root", str(context.repo_root)]

    context.result = run_spec_weaver(args)
    context.exit_code = context.result.returncode
    context.output = context.result.stdout + context.result.stderr


# ======================================================================
# Steps（trace.feature / impl_link.feature 共通 Background）
# ======================================================================


@given("Doorstopツリーが初期化されている")  # type: ignore
def given_6df87eb3(context):
    """Doorstopツリーが初期化されている

    Scenarios:
      - (trace.feature Background)
      - (impl_link.feature Background)
    """
    context.repo_root = context.temp_dir / "repo"
    context.repo_root.mkdir(parents=True, exist_ok=True)
    context.feature_dir = context.temp_dir / "features"
    context.feature_dir.mkdir(parents=True, exist_ok=True)
    # 遅延プロジェクト作成用の蓄積リスト
    context._pending_req_items = []
    context._pending_spec_items = []
    # scan / impl_files 読み取り用
    context.target_spec_id = None
    context.impl_files_result = None
    context.scan_result = {}


@given("以下のSPECアイテムが存在する:")  # type: ignore
def given_14c0b615(context):
    """以下のSPECアイテムが存在する:

    Scenarios:
      - (impl_link.feature Background: ID / Header / impl_files)
      - (trace.feature Background: ID / Header / Status / Links)
    """
    headings = [h.strip() for h in context.table.headings]

    for row in context.table:
        uid = row["ID"].strip()
        header = row.get("Header", "").strip() if "Header" in headings else ""
        item_cfg: dict = {"uid": uid, "header": header, "testable": True}

        if "Status" in headings:
            status = row["Status"].strip()
            if status:
                item_cfg["status"] = status

        if "Links" in headings:
            links_str = row["Links"].strip()
            if links_str:
                item_cfg["links"] = [
                    l.strip() for l in links_str.split(",") if l.strip()
                ]

        if "impl_files" in headings:
            impl_str = row["impl_files"].strip()
            if impl_str:
                item_cfg["extra"] = {"impl_files": [impl_str]}

        context._pending_spec_items.append(item_cfg)

    # SPEC ステップが Background の最後（REQ は既に蓄積済み）なので、ここでプロジェクトを作成する
    documents = []
    req_items = getattr(context, "_pending_req_items", [])
    if req_items:
        documents.append(
            {
                "dir": "reqs",
                "prefix": "REQ",
                "parent": None,
                "items": req_items,
            }
        )
    documents.append(
        {
            "dir": "specs",
            "prefix": "SPEC",
            "parent": "REQ" if req_items else None,
            "items": context._pending_spec_items,
        }
    )
    create_doorstop_project_yaml(context.repo_root, documents)


# ======================================================================
# Steps（SPEC-017: impl_files カスタム属性）
# ======================================================================


@given('SPEC-018 の impl_files に ["{param0}"] が設定されている')  # type: ignore
def given_5b35c4dd(context, param0):
    """SPEC-018 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている

    Scenarios:
      - impl_files にリスト形式でファイルパスを記述できる
    """
    _update_spec_yaml(context, "SPEC-018", "impl_files", [param0])
    context.target_spec_id = "SPEC-018"


@when("impl_files を読み取る")  # type: ignore
def when_1e9b41a9(context):
    """impl_files を読み取る

    Scenarios:
      - impl_files にリスト形式でファイルパスを記述できる
      - impl_files が未設定の場合はリンクなしとして扱われる
    """
    import doorstop

    orig = os.getcwd()
    os.chdir(context.repo_root)
    try:
        tree = doorstop.build()
        item = tree.find_item(str(context.target_spec_id))
        context.impl_files_result = get_ref_files(item)
    finally:
        os.chdir(orig)


@then('ファイルパスのリスト ["{param0}"] が得られること')  # type: ignore
def then_4c08825b(context, param0):
    """ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

    Scenarios:
      - impl_files にリスト形式でファイルパスを記述できる
    """
    assert context.impl_files_result == [param0], (
        f"期待: [{param0!r}]\n実際: {context.impl_files_result}"
    )


@given("SPEC-019 の impl_files が未設定である")  # type: ignore
def given_60f3699e(context):
    """SPEC-019 の impl_files が未設定である

    Scenarios:
      - impl_files が未設定の場合はリンクなしとして扱われる
      - アノテーションがあって impl_files がない場合は警告を報告する
    """
    # Background では SPEC-019 に impl_files が設定されていないため、
    # YAML を更新して impl_files キーを削除する（念のため）
    _update_spec_yaml(context, "SPEC-019", "impl_files", None)
    context.target_spec_id = "SPEC-019"


@then("空のリストが返ること")  # type: ignore
def then_3cd52b0f(context):
    """空のリストが返ること

    Scenarios:
      - impl_files が未設定の場合はリンクなしとして扱われる
    """
    assert context.impl_files_result == [], (
        f"期待: []\n実際: {context.impl_files_result}"
    )


# ======================================================================
# Steps（SPEC-018: アノテーションスキャン）
# ======================================================================


@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    """ "src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがあって impl_files がない場合は警告を報告する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _create_source_file(
        context, param0, f"{param1}\n# This is a generated test file.\n"
    )


@when("impl-scanner でリポジトリをスキャンする")  # type: ignore
def when_59b7b6ae(context):
    """impl-scanner でリポジトリをスキャンする

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがないファイルはエラーにならない
    """
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.repo_root)


@then('"{param0}" に対して "{param1}" が紐づくこと')  # type: ignore
def then_6cd9ae6b(context, param0, param1):
    """ "SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
    """
    assert param0 in context.scan_result, (
        f'"{param0}" がスキャン結果にありません: {list(context.scan_result.keys())}'
    )
    # スキャン結果のパスは OS のパス区切り文字を使用する可能性があるため正規化して比較
    found_paths = {str(p).replace("\\", "/") for p in context.scan_result[param0]}
    expected = param1.replace("\\", "/")
    assert expected in found_paths, (
        f'"{param1}" が "{param0}" のスキャン結果にありません: {found_paths}'
    )


@given("リポジトリに .py ファイルと .md ファイルが存在する")  # type: ignore
def given_6f18a295(context):
    """リポジトリに .py ファイルと .md ファイルが存在する

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    _create_source_file(
        context, "src/dummy.py", "# Python file without annotation\npass\n"
    )


@given('.md ファイルの行頭に "{param0}" が記述されている')  # type: ignore
def given_d9c1b21a(context, param0):
    """.md ファイルの行頭に "# implements: SPEC-018" が記述されている

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    _create_source_file(context, "docs/annotation.md", f"{param0}\n# Markdown file\n")
    context.md_file_path = "docs/annotation.md"


@when("--extensions py を指定して impl-scanner でスキャンする")  # type: ignore
def when_d61ff5a2(context):
    """--extensions py を指定して impl-scanner でスキャンする

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.repo_root, extensions=["py"])


@then(".md ファイルは結果に含まれないこと")  # type: ignore
def then_1e4aee33(context):
    """.md ファイルは結果に含まれないこと

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    for spec_id, paths in context.scan_result.items():
        for path_str in paths:
            assert not str(path_str).endswith(".md"), (
                f".md ファイル {path_str!r} がスキャン結果に含まれています"
            )


@given('"{param0}" にアノテーションが存在しない')  # type: ignore
def given_8d04b283(context, param0):
    """ "src/spec_weaver/gherkin.py" にアノテーションが存在しない

    Scenarios:
      - アノテーションがないファイルはエラーにならない
    """
    _create_source_file(context, param0, "# No annotation here\npass\n")


@then("エラーが発生しないこと")  # type: ignore
def then_b705ab9f(context):
    """エラーが発生しないこと

    Scenarios:
      - アノテーションがないファイルはエラーにならない
    """
    # scan_result が None でなければスキャンは成功している
    assert context.scan_result is not None, "スキャン中にエラーが発生しました"


# ======================================================================
# Steps（SPEC-019: audit --check-impl）
# ======================================================================


@given('SPEC-019 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_4cea3b9d(context, param0):
    """SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - --check-impl なしでは実装リンク検証は実行されない
    """
    _update_spec_yaml(context, "SPEC-019", "impl_files", [param0])


@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    """ "spec-weaver audit --check-impl" を実行する

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - impl_files にあってアノテーションがない場合は警告を報告する
      - アノテーションがあって impl_files がない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _run_cmd(context, param0)


@then("終了コードが 1 であること")  # type: ignore
def then_3783b41c(context):
    """終了コードが 1 であること

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
    """
    assert context.exit_code == 1, (
        f"終了コード {context.exit_code} (期待: 1)\n{context.output}"
    )


@then('"{param0}" が存在しないファイルとして報告されること')  # type: ignore
def then_7ef614ad(context, param0):
    """ "nonexistent.py" が存在しないファイルとして報告されること

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
    """
    assert param0 in context.output, (
        f'"{param0}" が存在しないファイルとして報告されていません:\n{context.output}'
    )


@given('SPEC-018 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    """SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - --show-impl なしでは実装ファイルは表示されない
    """
    _update_spec_yaml(context, "SPEC-018", "impl_files", [param0])


@given('"{param0}" に SPEC-018 のアノテーションが存在しない')  # type: ignore
def given_d0ba98a0(context, param0):
    """ "src/spec_weaver/cli.py" に SPEC-018 のアノテーションが存在しない

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
    """
    # ファイルを作成するが、SPEC-018 アノテーションは含めない
    _create_source_file(
        context, param0, "# This file has no SPEC-018 annotation\npass\n"
    )


@then('"{param0}" が impl_files のみ（アノテーションなし）として報告されること')  # type: ignore
def then_f76e2a8d(context, param0):
    """ "SPEC-018 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
    """
    # CLI 出力例: "   SPEC-018 → src/spec_weaver/cli.py"
    # param0: "SPEC-018 → src/spec_weaver/cli.py"
    parts = param0.split("→")
    spec_id = parts[0].strip()
    file_path = parts[1].strip() if len(parts) > 1 else ""
    assert spec_id in context.output, (
        f'"{spec_id}" が impl_files のみ（ref-only）セクションにありません:\n{context.output}'
    )
    assert file_path in context.output, (
        f'"{file_path}" が impl_files のみ（ref-only）セクションにありません:\n{context.output}'
    )


@then('"{param0}" がアノテーションのみ（impl_files なし）として報告されること')  # type: ignore
def then_7fa51a4f(context, param0):
    """ "SPEC-019 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

    Scenarios:
      - アノテーションがあって impl_files がない場合は警告を報告する
    """
    # CLI 出力例: "   SPEC-019 ← src/spec_weaver/gherkin.py"
    # param0: "SPEC-019 ← src/spec_weaver/gherkin.py"
    parts = param0.split("←")
    spec_id = parts[0].strip()
    file_path = parts[1].strip() if len(parts) > 1 else ""
    assert spec_id in context.output, (
        f'"{spec_id}" がアノテーションのみ（annotation-only）セクションにありません:\n{context.output}'
    )
    assert file_path in context.output, (
        f'"{file_path}" がアノテーションのみ（annotation-only）セクションにありません:\n{context.output}'
    )


@when('通常の "{param0}" を実行する（--check-impl なし）')  # type: ignore
def when_6a6c02d8(context, param0):
    """通常の "spec-weaver audit" を実行する（--check-impl なし）

    Scenarios:
      - --check-impl なしでは実装リンク検証は実行されない
    """
    _run_cmd(context, param0)


@then("実装ファイルリンクのセクションが出力されないこと")  # type: ignore
def then_70e4e0dc(context):
    """実装ファイルリンクのセクションが出力されないこと

    Scenarios:
      - --check-impl なしでは実装リンク検証は実行されない
    """
    # --check-impl なしでは "🔗 実装ファイルリンクの検証" セクションが出力されない
    impl_section_keywords = ["実装ファイルリンクの検証", "🔗", "check-impl"]
    assert not any(kw in context.output for kw in impl_section_keywords), (
        f"実装ファイルリンクのセクションが誤って出力されています:\n{context.output}"
    )


# ======================================================================
# Steps（SPEC-020: trace --show-impl）
# ======================================================================


@then('出力ツリーに "{param0}" が含まれること')  # type: ignore
def then_2c56e82a(context, param0):
    """出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

    Scenarios:
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    assert param0 in context.output, (
        f'出力ツリーに "{param0}" が含まれていません:\n{context.output}'
    )


@given("SPEC-018 の impl_files が未設定である")  # type: ignore
def given_c11ed496(context):
    """SPEC-018 の impl_files が未設定である

    Scenarios:
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _update_spec_yaml(context, "SPEC-018", "impl_files", None)


@when('"{param0}" を実行する（--show-impl なし）')  # type: ignore
def when_dfb07a47(context, param0):
    """ "spec-weaver trace SPEC-018 -f ./specification/features" を実行する（--show-impl なし）

    Scenarios:
      - --show-impl なしでは実装ファイルは表示されない
    """
    _run_cmd(context, param0)


@then('出力ツリーに "{param0}" が含まれないこと')  # type: ignore
def then_35df9926(context, param0):
    """出力ツリーに "impl_scanner.py" が含まれないこと

    Scenarios:
      - --show-impl なしでは実装ファイルは表示されない
    """
    assert param0 not in context.output, (
        f'出力ツリーに "{param0}" が含まれています（含まれないべき）:\n{context.output}'
    )
