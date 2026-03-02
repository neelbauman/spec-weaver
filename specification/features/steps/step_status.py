"""behave steps for: status コマンド"""

from __future__ import annotations

import sys
from pathlib import Path

from behave import given, when, then

from _helpers import (
    PROJECT_ROOT,
    create_doorstop_project_api,
    run_spec_weaver,
)

# ======================================================================
# Steps
# ======================================================================


def _run_status(context, extra_args=None):
    args = ["status", "--repo-root", str(context.repo_root)]
    if extra_args:
        args += extra_args
    context.result = run_spec_weaver(args)
    context.exit_code = context.result.returncode
    context.output = context.result.stdout + context.result.stderr


@given("REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている")  # type: ignore
def given_ef098fcf(context):
    """REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        req_items=[{"header": "要件A", "testable": False, "status": "draft"}],
        spec_items=[{"header": "仕様A", "testable": True, "status": "implemented"}],
    )


@when("status コマンドを実行する")  # type: ignore
def when_d68a8d9a(context):
    """status コマンドを実行する

    Scenarios:
      - 全アイテムのステータスを一覧表示する
      - status 未設定のアイテムは "-" と表示される
      - レビューステータスと最終更新日が表示される
    """
    _run_status(context)


# [Duplicate Skip] This step is already defined in step_audit.py
# @then('終了コード 0 が返ること')  # type: ignore
# def then_4f25c571(context):
#     """終了コード 0 が返ること
#
#     Scenarios:
#       - 全アイテムのステータスを一覧表示する
#       - status 未設定のアイテムは "-" と表示される
#       - --filter で特定ステータスに絞り込める
#       - --filter に一致するアイテムが存在しない場合に通知される
#       - レビューステータスと最終更新日が表示される
#     """


@then('REQ-001 が "{badge}" バッジとともに表示されること')  # type: ignore
def then_6e220346(context, badge):
    """REQ-001 が "draft" バッジとともに表示されること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    assert "REQ-001" in context.output, f"REQ-001 が出力にありません:\n{context.output}"
    assert badge in context.output, (
        f"バッジ {badge!r} が出力にありません:\n{context.output}"
    )


@then('SPEC-001 が "{badge}" バッジとともに表示されること')  # type: ignore
def then_9f0d7f01(context, badge):
    """SPEC-001 が "implemented" バッジとともに表示されること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    assert "SPEC-001" in context.output, (
        f"SPEC-001 が出力にありません:\n{context.output}"
    )
    assert badge in context.output, (
        f"バッジ {badge!r} が出力にありません:\n{context.output}"
    )


@given("SPEC-001 に status フィールドが設定されていない")  # type: ignore
def given_0d995d24(context):
    """SPEC-001 に status フィールドが設定されていない

    Scenarios:
      - status 未設定のアイテムは "-" と表示される
    """
    context.repo_root = context.temp_dir / "repo"
    # status なしで作成
    create_doorstop_project_api(
        context.repo_root,
        spec_items=[{"header": "仕様A", "testable": True}],
    )


@then('SPEC-001 の実装状況が "{expected}" と表示されること')  # type: ignore
def then_5818121f(context, expected):
    """SPEC-001 の実装状況が "-" と表示されること

    Scenarios:
      - status 未設定のアイテムは "-" と表示される
    """
    assert expected in context.output, (
        f"{expected!r} が出力にありません:\n{context.output}"
    )


@given("REQ-001 が status: implemented、REQ-002 が status: draft に設定されている")  # type: ignore
def given_58beb4fc(context):
    """REQ-001 が status: implemented、REQ-002 が status: draft に設定されている

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        req_items=[
            {"header": "実装済み要件", "testable": False, "status": "implemented"},
            {"header": "ドラフト要件", "testable": False, "status": "draft"},
        ],
    )


@when('status コマンドを "{option}" オプション付きで実行する')  # type: ignore
def when_d36ae1bf(context, option):
    """status コマンドを "--filter implemented" オプション付きで実行する

    Scenarios:
      - --filter で特定ステータスに絞り込める
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    # option例: "--filter implemented"
    parts = option.split()
    _run_status(context, extra_args=parts)


@then("REQ-001 が表示されること")  # type: ignore
def then_2847178d(context):
    """REQ-001 が表示されること

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    assert "REQ-001" in context.output, f"REQ-001 が出力にありません:\n{context.output}"


@then("REQ-002 は表示されないこと")  # type: ignore
def then_9fc4e668(context):
    """REQ-002 は表示されないこと

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    assert "REQ-002" not in context.output, (
        f"REQ-002 が出力に含まれています:\n{context.output}"
    )


@given('すべてのアイテムの status が "{status}" に設定されている')  # type: ignore
def given_f93df893(context, status):
    """すべてのアイテムの status が "draft" に設定されている

    Scenarios:
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    raise NotImplementedError('STEP: すべてのアイテムの status が "{param0}" に設定されている')


@given('REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている')
def step_impl_1(context):
    setup_doorstop(context, prefixes=["REQ", "SPEC"])
    add_item_manual(context, "REQ", "REQ-001", "draft")
    add_item_manual(context, "SPEC", "SPEC-001", "implemented")

@when('status コマンドを実行する')
def step_impl_2(context):
    run_cli(context, ["status", "--repo-root", "."])

# [Duplicate Skip] line 59 の @then('REQ-001 が "{param0}" バッジとともに表示されること') で処理される
# @then('REQ-001 が "draft" バッジとともに表示されること')  # type: ignore
def step_impl_4(context):
    assert "REQ-001" in context.stdout
    assert "draft" in context.stdout

# [Duplicate Skip] line 69 の @then('SPEC-001 が "{param0}" バッジとともに表示されること') で処理される
# @then('SPEC-001 が "implemented" バッジとともに表示されること')  # type: ignore
def step_impl_5(context):
    assert "SPEC-001" in context.stdout
    assert "implemented" in context.stdout

@given('SPEC-001 に status フィールドが設定されていない')
def step_impl_6(context):
    setup_doorstop(context, prefixes=["SPEC"])
    add_item_manual(context, "SPEC", "SPEC-001", status=None)

# [Duplicate Skip] line 79 の @then('SPEC-001 の実装状況が "{param0}" と表示されること') で処理される
# @then('SPEC-001 の実装状況が "-" と表示されること')  # type: ignore
def step_impl_7(context):
    for line in context.stdout.splitlines():
        if "SPEC-001" in line:
            assert "-" in line
            return
    assert False

@given('REQ-001 が status: implemented、REQ-002 が status: draft に設定されている')
def step_impl_8(context):
    setup_doorstop(context, prefixes=["REQ"])
    add_item_manual(context, "REQ", "REQ-001", "implemented")
    add_item_manual(context, "REQ", "REQ-002", "draft")

# [Duplicate Skip] line 89 の @when('status コマンドを "{param0}" オプション付きで実行する') で処理される
# @when('status コマンドを "--filter implemented" オプション付きで実行する')  # type: ignore
def step_impl_9(context):
    run_cli(context, ["status", "--repo-root", ".", "--filter", "implemented"])

@then('REQ-001 が表示されること')
def step_impl_10(context):
    assert "REQ-001" in context.stdout

@then('REQ-002 は表示されないこと')
def step_impl_11(context):
    assert "REQ-002" not in context.stdout

# [Duplicate Skip] line 100 の @given('すべてのアイテムの status が "{param0}" に設定されている') で処理される
# @given('すべてのアイテムの status が "draft" に設定されている')  # type: ignore
def step_impl_12(context):
    setup_doorstop(context, prefixes=["SPEC"])
    add_item_manual(context, "SPEC", "SPEC-001", "draft")

@then('一致するアイテムが見つからなかった旨が表示されること')
def step_impl_13(context):
    assert "見つかりませんでした" in context.stdout or "一致するアイテムが存在しません" in context.stdout
