"""behave steps for: status コマンド"""

import os
import subprocess
import doorstop
import re
from behave import given, when, then, step

# ======================================================================
# Helpers
# ======================================================================

def run_cli(context, args):
    cmd = ["spec-weaver"] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=context.temp_dir
    )
    context.stdout = result.stdout
    context.stderr = result.stderr
    context.exit_code = result.returncode
    return result

def setup_doorstop(context, prefixes=["REQ", "SPEC"]):
    last_prefix = None
    for prefix in prefixes:
        doc_dir = prefix.lower() + "s"
        cmd = ["doorstop", "create", prefix, doc_dir]
        if last_prefix:
            cmd += ["--parent", last_prefix]
        subprocess.run(cmd, cwd=context.temp_dir, capture_output=True, check=True)
        
        # Set sep: '-'
        doorstop_yml = os.path.join(context.temp_dir, doc_dir, ".doorstop.yml")
        with open(doorstop_yml, "r") as f:
            content = f.read()
        content = re.sub(r"sep:.*", "sep: '-'", content)
        if "sep: '-'" not in content:
             content += "\nsettings:\n  sep: '-'\n"
        with open(doorstop_yml, "w") as f:
            f.write(content)
        last_prefix = prefix

def add_item_manual(context, prefix, uid, status=None):
    doc_dir = prefix.lower() + "s"
    os.makedirs(os.path.join(context.temp_dir, doc_dir), exist_ok=True)
    item_path = os.path.join(context.temp_dir, doc_dir, f"{uid}.yml")
    with open(item_path, "w") as f:
        f.write("active: True\n")
        if status:
            f.write(f"status: {status}\n")

# ======================================================================
# Steps
# ======================================================================

@then('REQ-001 が "{param0}" バッジとともに表示されること')  # type: ignore
def then_6e220346(context, param0):
    """REQ-001 が "draft" バッジとともに表示されること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    raise NotImplementedError('STEP: REQ-001 が "{param0}" バッジとともに表示されること')


@then('SPEC-001 が "{param0}" バッジとともに表示されること')  # type: ignore
def then_9f0d7f01(context, param0):
    """SPEC-001 が "implemented" バッジとともに表示されること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    raise NotImplementedError('STEP: SPEC-001 が "{param0}" バッジとともに表示されること')


@then('SPEC-001 の実装状況が "{param0}" と表示されること')  # type: ignore
def then_5818121f(context, param0):
    """SPEC-001 の実装状況が "-" と表示されること

    Scenarios:
      - status 未設定のアイテムは "-" と表示される
    """
    raise NotImplementedError('STEP: SPEC-001 の実装状況が "{param0}" と表示されること')


@when('status コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_d36ae1bf(context, param0):
    """status コマンドを "--filter implemented" オプション付きで実行する

    Scenarios:
      - --filter で特定ステータスに絞り込める
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    raise NotImplementedError('STEP: status コマンドを "{param0}" オプション付きで実行する')


@given('すべてのアイテムの status が "{param0}" に設定されている')  # type: ignore
def given_f93df893(context, param0):
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

@then('REQ-001 が "draft" バッジとともに表示されること')
def step_impl_4(context):
    assert "REQ-001" in context.stdout
    assert "draft" in context.stdout

@then('SPEC-001 が "implemented" バッジとともに表示されること')
def step_impl_5(context):
    assert "SPEC-001" in context.stdout
    assert "implemented" in context.stdout

@given('SPEC-001 に status フィールドが設定されていない')
def step_impl_6(context):
    setup_doorstop(context, prefixes=["SPEC"])
    add_item_manual(context, "SPEC", "SPEC-001", status=None)

@then('SPEC-001 の実装状況が "-" と表示されること')
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

@when('status コマンドを "--filter implemented" オプション付きで実行する')
def step_impl_9(context):
    run_cli(context, ["status", "--repo-root", ".", "--filter", "implemented"])

@then('REQ-001 が表示されること')
def step_impl_10(context):
    assert "REQ-001" in context.stdout

@then('REQ-002 は表示されないこと')
def step_impl_11(context):
    assert "REQ-002" not in context.stdout

@given('すべてのアイテムの status が "draft" に設定されている')
def step_impl_12(context):
    setup_doorstop(context, prefixes=["SPEC"])
    add_item_manual(context, "SPEC", "SPEC-001", "draft")

@then('一致するアイテムが見つからなかった旨が表示されること')
def step_impl_13(context):
    assert "見つかりませんでした" in context.stdout or "一致するアイテムが存在しません" in context.stdout
