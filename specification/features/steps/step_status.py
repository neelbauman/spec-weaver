"""behave steps for: status コマンド"""

from __future__ import annotations

import sys
from pathlib import Path

from behave import given, when, then

sys.path.insert(0, str(Path(__file__).resolve().parent))
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


@given('REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている')  # type: ignore
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


@when('status コマンドを実行する')  # type: ignore
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
    assert badge in context.output, f"バッジ {badge!r} が出力にありません:\n{context.output}"


@then('SPEC-001 が "{badge}" バッジとともに表示されること')  # type: ignore
def then_9f0d7f01(context, badge):
    """SPEC-001 が "implemented" バッジとともに表示されること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    assert "SPEC-001" in context.output, f"SPEC-001 が出力にありません:\n{context.output}"
    assert badge in context.output, f"バッジ {badge!r} が出力にありません:\n{context.output}"


@given('SPEC-001 に status フィールドが設定されていない')  # type: ignore
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


@given('REQ-001 が status: implemented、REQ-002 が status: draft に設定されている')  # type: ignore
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


@then('REQ-001 が表示されること')  # type: ignore
def then_2847178d(context):
    """REQ-001 が表示されること

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    assert "REQ-001" in context.output, f"REQ-001 が出力にありません:\n{context.output}"


@then('REQ-002 は表示されないこと')  # type: ignore
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
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        spec_items=[{"header": "仕様A", "testable": True, "status": status}],
    )


@then('一致するアイテムが見つからなかった旨が表示されること')  # type: ignore
def then_897c0cfb(context):
    """一致するアイテムが見つからなかった旨が表示されること

    Scenarios:
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    assert any(kw in context.output for kw in ["見つかりません", "not found", "0 件", "一致"]), (
        f"'見つからない' 旨が出力にありません:\n{context.output}"
    )


@given('Doorstopのアイテムが存在する')  # type: ignore
def given_0da078b7(context):
    """Doorstopのアイテムが存在する

    Scenarios:
      - レビューステータスと最終更新日が表示される
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        spec_items=[{"header": "仕様A", "testable": True, "status": "implemented"}],
    )


@then('レビューステータス列が表示されること')  # type: ignore
def then_33e7dc19(context):
    """レビューステータス列が表示されること

    Scenarios:
      - レビューステータスと最終更新日が表示される
    """
    assert any(kw in context.output for kw in ["レビュー", "reviewed", "suspect", "✅", "⚠️", "📋"]), (
        f"レビューステータス列が見つかりません:\n{context.output}"
    )


@then('最終更新日列が表示されること')  # type: ignore
def then_49bd7463(context):
    """最終更新日列が表示されること

    Scenarios:
      - レビューステータスと最終更新日が表示される
    """
    assert any(kw in context.output for kw in ["更新日", "updated", "最終"]), (
        f"最終更新日列が見つかりません:\n{context.output}"
    )
