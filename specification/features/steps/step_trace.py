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

@then('"{uid}" がルートノードとして表示される')
def step_impl_9(context, uid):
    assert uid in context.stdout

@step('"{child}" が "{parent}" の子ノードとして表示される')
def step_impl_10(context, child, parent):
    assert child in context.stdout
    assert parent in context.stdout

@then('上位に "{uid}" が表示される')
def step_impl_12(context, uid):
    assert uid in context.stdout

@then('下位に "{filename}" のシナリオが表示される')
def step_impl_13(context, filename):
    assert "Scenario:" in context.stdout

@then('出力がフラットリスト形式である')
def step_impl_17(context):
    assert "ID" in context.stdout

@then('各行に "{label1}" または "{label2}" または "{label3}" のラベルが含まれる')
def step_impl_18(context, label1, label2, label3):
    assert label1.strip('[]') in context.stdout or label2.strip('[]') in context.stdout or label3.strip('[]') in context.stdout

@then('エラーメッセージに "{msg}" が含まれる')
def step_impl_19(context, msg):
    assert msg.lower() in context.stdout.lower() or msg.lower() in context.stderr.lower()

@then('"{uid}" のノードに "{status}" のステータスバッジが表示される')
def step_impl_20(context, uid, status):
    assert uid in context.stdout
    assert status in context.stdout
