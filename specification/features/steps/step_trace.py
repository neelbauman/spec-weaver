"""behave steps for: trace コマンド"""

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

def create_feature_file(context, filename, content):
    feature_dir = os.path.join(context.temp_dir, "features")
    os.makedirs(feature_dir, exist_ok=True)
    path = os.path.join(feature_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

# ======================================================================
# Steps
# ======================================================================

@when('`spec-weaver trace REQ-001 -f ./specification/features` を実行する')  # type: ignore
def when_6629a1b8(context):
    """`spec-weaver trace REQ-001 -f ./specification/features` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - 各ノードにステータスバッジが表示される
    """
    raise NotImplementedError('STEP: `spec-weaver trace REQ-001 -f ./specification/features` を実行する')


# [Duplicate Skip] common_steps.py の @then('終了コードが{code:d}である') で処理される
# @then('終了コードが0である')  # type: ignore
# def then_0f800e56(context):
#     raise NotImplementedError('STEP: 終了コードが0である')


@then('"{param0}" がルートノードとして表示される')  # type: ignore
def then_24c28817(context, param0):
    """"REQ-001" がルートノードとして表示される

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
    """
    raise NotImplementedError('STEP: "{param0}" がルートノードとして表示される')


@then('"{param0}" が "{param1}" の子ノードとして表示される')  # type: ignore
def then_5c046e43(context, param0, param1):
    """"REQ-002" が "REQ-001" の子ノードとして表示される

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
    """
    raise NotImplementedError('STEP: "{param0}" が "{param1}" の子ノードとして表示される')


@when('`spec-weaver trace SPEC-003 -f ./specification/features` を実行する')  # type: ignore
def when_b1a2f499(context):
    """`spec-weaver trace SPEC-003 -f ./specification/features` を実行する

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    raise NotImplementedError('STEP: `spec-weaver trace SPEC-003 -f ./specification/features` を実行する')


@then('上位に "{param0}" が表示される')  # type: ignore
def then_0d60d0d2(context, param0):
    """上位に "REQ-002" が表示される

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    raise NotImplementedError('STEP: 上位に "{param0}" が表示される')


@then('下位に "{param0}" のシナリオが表示される')  # type: ignore
def then_b2f19b22(context, param0):
    """下位に "audit.feature" のシナリオが表示される

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    raise NotImplementedError('STEP: 下位に "{param0}" のシナリオが表示される')


@when('`spec-weaver trace audit.feature -f ./specification/features` を実行する')  # type: ignore
def when_53222a94(context):
    """`spec-weaver trace audit.feature -f ./specification/features` を実行する

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
    """
    raise NotImplementedError('STEP: `spec-weaver trace audit.feature -f ./specification/features` を実行する')


@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
    """
    raise NotImplementedError('STEP: 出力に "{param0}" が表示される')


@when('`spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する')  # type: ignore
def when_770f884f(context):
    """`spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する

    Scenarios:
      - --direction up で上方向のみ探索
    """
    raise NotImplementedError('STEP: `spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する')


@then('出力に "{param0}" が表示されない')  # type: ignore
def then_1c0ce4ff(context, param0):
    """出力に "audit.feature" が表示されない

    Scenarios:
      - --direction up で上方向のみ探索
    """
    raise NotImplementedError('STEP: 出力に "{param0}" が表示されない')


@when('`spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する')  # type: ignore
def when_24d70f7f(context):
    """`spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する

    Scenarios:
      - --direction down で下方向のみ探索
    """
    raise NotImplementedError('STEP: `spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する')


@when('`spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する')  # type: ignore
def when_816b7b2c(context):
    """`spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する

    Scenarios:
      - --format flat でフラットリスト表示
    """
    raise NotImplementedError('STEP: `spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する')


@then('各行に "{param0}" または "{param1}" または "{param2}" のラベルが含まれる')  # type: ignore
def then_29017220(context, param0, param1, param2):
    """各行に "[REQ]" または "[SPEC]" または "[TEST]" のラベルが含まれる

    Scenarios:
      - --format flat でフラットリスト表示
    """
    raise NotImplementedError('STEP: 各行に "{param0}" または "{param1}" または "{param2}" のラベルが含まれる')


@when('`spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する')  # type: ignore
def when_44385436(context):
    """`spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する

    Scenarios:
      - 存在しないIDを指定した場合のエラー
    """
    raise NotImplementedError('STEP: `spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する')


# [Duplicate Skip] common_steps.py の @then('終了コードが{code:d}である') で処理される
# @then('終了コードが1である')  # type: ignore
# def then_9b731a71(context):
#     raise NotImplementedError('STEP: 終了コードが1である')


@then('エラーメッセージに "{param0}" が含まれる')  # type: ignore
def then_9998fad9(context, param0):
    """エラーメッセージに "not found" が含まれる

    Scenarios:
      - 存在しないIDを指定した場合のエラー
    """
    raise NotImplementedError('STEP: エラーメッセージに "{param0}" が含まれる')


@then('"{param0}" のノードに "{param1}" のステータスバッジが表示される')  # type: ignore
def then_f676df97(context, param0, param1):
    """"REQ-001" のノードに "implemented" のステータスバッジが表示される

    Scenarios:
      - 各ノードにステータスバッジが表示される
    """
    raise NotImplementedError('STEP: "{param0}" のノードに "{param1}" のステータスバッジが表示される')
@given('Doorstopツリーが初期化されている')
def step_impl_1(context):
    setup_doorstop(context, prefixes=["REQ", "SPEC"])

@given('以下のREQアイテムが存在する:')
def step_impl_2(context):
    for row in context.table:
        item_path = os.path.join(context.temp_dir, "reqs", f"{row['ID']}.yml")
        os.makedirs(os.path.dirname(item_path), exist_ok=True)
        with open(item_path, "w") as f:
            f.write(f"active: True\nheader: {row['Header']}\n")
            if 'Status' in row and row['Status']:
                f.write(f"status: {row['Status']}\n")
            if 'Links' in row and row['Links']:
                links = row['Links'].split(',')
                f.write("links:\n")
                for l in links:
                    f.write(f"- {l.strip()}\n")

@given('以下のSPECアイテムが存在する:')
def step_impl_3(context):
    for row in context.table:
        item_path = os.path.join(context.temp_dir, "specs", f"{row['ID']}.yml")
        os.makedirs(os.path.dirname(item_path), exist_ok=True)
        with open(item_path, "w") as f:
            f.write(f"active: True\nheader: {row['Header']}\n")
            if 'Status' in row and row['Status']:
                f.write(f"status: {row['Status']}\n")
            if 'Links' in row and row['Links']:
                links = row['Links'].split(',')
                f.write("links:\n")
                for l in links:
                    f.write(f"- {l.strip()}\n")

@given('以下のfeatureファイルが存在する:')
def step_impl_4(context):
    for row in context.table:
        content = f"{row['Tags']}\nFeature: {row['File']}\n"
        scenarios = row['Scenarios'].split(',')
        for s in scenarios:
            content += f"  Scenario: {s.strip()}\n    Given test\n"
        create_feature_file(context, row['File'], content)

@when('`spec-weaver trace {item_id} -f ./specification/features` を実行する')
def step_impl_5(context, item_id):
    run_cli(context, ["trace", item_id, "-f", "features", "--repo-root", "."])

@when('`spec-weaver trace {item_id} -f ./specification/features --direction {direction}` を実行する')
def step_impl_6(context, item_id, direction):
    run_cli(context, ["trace", item_id, "-f", "features", "--repo-root", ".", "--direction", direction])

@when('`spec-weaver trace {item_id} -f ./specification/features --format {fmt}` を実行する')
def step_impl_7(context, item_id, fmt):
    run_cli(context, ["trace", item_id, "-f", "features", "--repo-root", ".", "--format", fmt])

@then('出力にツリー構造が含まれる')
def step_impl_8(context):
    assert "REQ-" in context.stdout or "SPEC-" in context.stdout

# [Duplicate Skip] line 75 の @then('"{param0}" がルートノードとして表示される') で処理される
# @then('"{uid}" がルートノードとして表示される')  # type: ignore
def step_impl_9(context, uid):
    assert uid in context.stdout

# [Duplicate Skip] line 85 の @then('"{param0}" が "{param1}" の子ノードとして表示される') で処理される
# @step('"{child}" が "{parent}" の子ノードとして表示される')  # type: ignore
def step_impl_10(context, child, parent):
    assert child in context.stdout
    assert parent in context.stdout

# [Duplicate Skip] line 105 の @then('上位に "{param0}" が表示される') で処理される
# @then('上位に "{uid}" が表示される')  # type: ignore
def step_impl_12(context, uid):
    assert uid in context.stdout

# [Duplicate Skip] line 115 の @then('下位に "{param0}" のシナリオが表示される') で処理される
# @then('下位に "{filename}" のシナリオが表示される')  # type: ignore
def step_impl_13(context, filename):
    assert "Scenario:" in context.stdout

@then('出力がフラットリスト形式である')
def step_impl_17(context):
    assert "ID" in context.stdout

# [Duplicate Skip] line 187 の @then('各行に "{param0}" または "{param1}" または "{param2}" のラベルが含まれる') で処理される
# @then('各行に "{label1}" または "{label2}" または "{label3}" のラベルが含まれる')  # type: ignore
def step_impl_18(context, label1, label2, label3):
    assert label1.strip('[]') in context.stdout or label2.strip('[]') in context.stdout or label3.strip('[]') in context.stdout

# [Duplicate Skip] line 213 の @then('エラーメッセージに "{param0}" が含まれる') で処理される
# @then('エラーメッセージに "{msg}" が含まれる')  # type: ignore
def step_impl_19(context, msg):
    assert msg.lower() in context.stdout.lower() or msg.lower() in context.stderr.lower()

# [Duplicate Skip] line 223 の @then('"{param0}" のノードに "{param1}" のステータスバッジが表示される') で処理される
# @then('"{uid}" のノードに "{status}" のステータスバッジが表示される')  # type: ignore
def step_impl_20(context, uid, status):
    assert uid in context.stdout
    assert status in context.stdout
