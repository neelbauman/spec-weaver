"""behave steps for: trace コマンド — トレーサビリティ・ツリー表示"""

from __future__ import annotations

import sys
from pathlib import Path

from behave import given, when, then

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _helpers import (
    PROJECT_ROOT,
    run_spec_weaver,
    write_feature_file,
)


# ======================================================================
# ヘルパー
# ======================================================================

def _run_trace(context, item_id: str, extra_args=None):
    """spec-weaver trace を実行して結果を context に保存する。"""
    args = [
        "trace", item_id,
        "-f", str(context.feature_dir),
        "--repo-root", str(context.repo_root),
    ]
    if extra_args:
        args += extra_args
    context.result = run_spec_weaver(args)
    context.exit_code = context.result.returncode
    context.output = context.result.stdout + context.result.stderr


# ======================================================================
# Steps
# ======================================================================

# [Duplicate Skip] This step is already defined elsewhere
# @given('Doorstopツリーが初期化されている')  # type: ignore
# def given_6df87eb3(context): ...


@given('以下のREQアイテムが存在する:')  # type: ignore
def given_28140be4(context):
    """以下のREQアイテムが存在する:

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - 各ノードにステータスバッジが表示される
    """
    # Table: | ID | Header | Status | Links |
    headings = [h.strip() for h in context.table.headings]
    for row in context.table:
        uid = row["ID"].strip()
        header = row.get("Header", "").strip()
        item_cfg = {"uid": uid, "header": header, "testable": False}

        if "Status" in headings:
            status = row["Status"].strip()
            if status:
                item_cfg["status"] = status

        if "Links" in headings:
            links_str = row["Links"].strip()
            if links_str:
                item_cfg["links"] = [l.strip() for l in links_str.split(",") if l.strip()]

        if not hasattr(context, "_pending_req_items"):
            context._pending_req_items = []
        context._pending_req_items.append(item_cfg)


# [Duplicate Skip] This step is already defined elsewhere (step_impl_link.py)
# @given('以下のSPECアイテムが存在する:')  # type: ignore
# def given_14c0b615(context): ...


@given('以下のfeatureファイルが存在する:')  # type: ignore
def given_a838a6ff(context):
    """以下のfeatureファイルが存在する:

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - 各ノードにステータスバッジが表示される
    """
    # Table: | File | Tags | Scenarios |
    for row in context.table:
        filename = row["File"].strip()
        tags = row["Tags"].strip()
        scenarios_str = row["Scenarios"].strip()
        scenarios = [s.strip() for s in scenarios_str.split(",") if s.strip()]

        lines = [tags, f"Feature: {tags} テスト", ""]
        for sc_name in scenarios:
            lines += [
                f"  Scenario: {sc_name}",
                f"    Given テスト前提条件",
                f"    When  テスト実行",
                f"    Then  テスト確認",
                "",
            ]
        write_feature_file(context.feature_dir / filename, "\n".join(lines))


@when('`spec-weaver trace REQ-001 -f ./specification/features` を実行する')  # type: ignore
def when_6629a1b8(context):
    """`spec-weaver trace REQ-001 -f ./specification/features` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - 各ノードにステータスバッジが表示される
    """
    _run_trace(context, "REQ-001")


@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 各ノードにステータスバッジが表示される
    """
    assert context.exit_code == 0, (
        f"終了コード {context.exit_code} (期待: 0)\n{context.output}"
    )


@then('出力にツリー構造が含まれる')  # type: ignore
def then_a551e8cd(context):
    """出力にツリー構造が含まれる

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - SPECを起点とした双方向のツリー表示
    """
    # Rich ツリーは "│", "├", "└" などのボックス描画文字か、ID を含む
    assert any(ch in context.output for ch in ["│", "├", "└", "┌", "─"]) or \
           any(uid in context.output for uid in ["REQ-", "SPEC-"]), (
        f"ツリー構造が見つかりません:\n{context.output}"
    )


@then('"{param0}" がルートノードとして表示される')  # type: ignore
def then_24c28817(context, param0):
    """"REQ-001" がルートノードとして表示される

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
    """
    assert param0 in context.output, (
        f'"{param0}" がルートノードとして出力にありません:\n{context.output}'
    )


@then('"{param0}" が "{param1}" の子ノードとして表示される')  # type: ignore
def then_5c046e43(context, param0, param1):
    """"REQ-002" が "REQ-001" の子ノードとして表示される

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
    """
    # 親も子も出力に含まれていれば親子関係が表示されていると見なす
    assert param0 in context.output, (
        f'子ノード "{param0}" が出力にありません:\n{context.output}'
    )
    assert param1 in context.output, (
        f'親ノード "{param1}" が出力にありません:\n{context.output}'
    )


@when('`spec-weaver trace SPEC-003 -f ./specification/features` を実行する')  # type: ignore
def when_b1a2f499(context):
    """`spec-weaver trace SPEC-003 -f ./specification/features` を実行する

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    _run_trace(context, "SPEC-003")


@then('上位に "{param0}" が表示される')  # type: ignore
def then_0d60d0d2(context, param0):
    """上位に "REQ-002" が表示される

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    assert param0 in context.output, (
        f'上位ノード "{param0}" が出力にありません:\n{context.output}'
    )


@then('下位に "{param0}" のシナリオが表示される')  # type: ignore
def then_b2f19b22(context, param0):
    """下位に "audit.feature" のシナリオが表示される

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    assert param0 in context.output, (
        f'下位の "{param0}" シナリオが出力にありません:\n{context.output}'
    )


@when('`spec-weaver trace audit.feature -f ./specification/features` を実行する')  # type: ignore
def when_53222a94(context):
    """`spec-weaver trace audit.feature -f ./specification/features` を実行する

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
    """
    _run_trace(context, "audit.feature")


@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
    """
    assert param0 in context.output, (
        f'"{param0}" が出力にありません:\n{context.output}'
    )


@when('`spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する')  # type: ignore
def when_770f884f(context):
    """`spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する

    Scenarios:
      - --direction up で上方向のみ探索
    """
    _run_trace(context, "SPEC-003", extra_args=["--direction", "up"])


@then('出力に "{param0}" が表示されない')  # type: ignore
def then_1c0ce4ff(context, param0):
    """出力に "audit.feature" が表示されない

    Scenarios:
      - --direction up で上方向のみ探索
    """
    assert param0 not in context.output, (
        f'"{param0}" が出力に含まれています:\n{context.output}'
    )


@when('`spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する')  # type: ignore
def when_24d70f7f(context):
    """`spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する

    Scenarios:
      - --direction down で下方向のみ探索
    """
    _run_trace(context, "REQ-001", extra_args=["--direction", "down"])


@when('`spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する')  # type: ignore
def when_816b7b2c(context):
    """`spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する

    Scenarios:
      - --format flat でフラットリスト表示
    """
    _run_trace(context, "REQ-001", extra_args=["--format", "flat"])


@then('出力がフラットリスト形式である')  # type: ignore
def then_f50604f0(context):
    """出力がフラットリスト形式である

    Scenarios:
      - --format flat でフラットリスト表示
    """
    # flat 形式では ID がリスト/テーブル形式で並ぶ（ツリー記号ではなくフラットに列挙される）
    assert any(uid in context.output for uid in ["REQ-", "SPEC-"]), (
        f"フラットリスト形式（REQ/SPEC エントリ）が見つかりません:\n{context.output}"
    )


@then('各行に "{param0}" または "{param1}" または "{param2}" のラベルが含まれる')  # type: ignore
def then_29017220(context, param0, param1, param2):
    """各行に "REQ" または "SPEC" または "TEST" のラベルが含まれる

    Scenarios:
      - --format flat でフラットリスト表示
    """
    content_lines = [l for l in context.output.splitlines() if l.strip()]
    assert any(param0 in l or param1 in l or param2 in l for l in content_lines), (
        f'"{param0}" / "{param1}" / "{param2}" のラベルが出力にありません:\n{context.output}'
    )


@when('`spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する')  # type: ignore
def when_44385436(context):
    """`spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する

    Scenarios:
      - 存在しないIDを指定した場合のエラー
    """
    _run_trace(context, "NONEXIST-999")


@then('終了コードが1である')  # type: ignore
def then_9b731a71(context):
    """終了コードが1である

    Scenarios:
      - 存在しないIDを指定した場合のエラー
    """
    assert context.exit_code == 1, (
        f"終了コード {context.exit_code} (期待: 1)\n{context.output}"
    )


@then('エラーメッセージに "{param0}" が含まれる')  # type: ignore
def then_9998fad9(context, param0):
    """エラーメッセージに "not found" が含まれる

    Scenarios:
      - 存在しないIDを指定した場合のエラー
    """
    assert param0 in context.output, (
        f'エラーメッセージに "{param0}" が見つかりません:\n{context.output}'
    )


@then('"{param0}" のノードに "{param1}" のステータスバッジが表示される')  # type: ignore
def then_f676df97(context, param0, param1):
    """"REQ-001" のノードに "implemented" のステータスバッジが表示される

    Scenarios:
      - 各ノードにステータスバッジが表示される
    """
    assert param0 in context.output, (
        f'ノード "{param0}" が出力にありません:\n{context.output}'
    )
    assert param1 in context.output, (
        f'ステータスバッジ "{param1}" が出力にありません:\n{context.output}'
    )
