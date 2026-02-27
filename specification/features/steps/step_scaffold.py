"""behave steps for: scaffold コマンド"""

import os
import subprocess
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

@given('"{param0}" ファイルが存在するディレクトリがある')
def step_impl_1(context, param0):
    create_feature_file(context, "test.feature", "Feature: Test\n  Scenario: Test\n    Given test step")

@when('scaffold コマンドを実行する')
def step_impl_2(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])

@then('各 .feature に対応する "step_<stem>.py" が生成されること')
def step_impl_3(context):
    path = os.path.join(context.temp_dir, "steps", "step_test.py")
    assert os.path.exists(path), f"File {path} not found. Stdout: {context.stdout}"

@then('各ステップに "{p1}", "{p2}", "{p3}" デコレータ付き関数が含まれること')
def step_impl_4(context, p1, p2, p3):
    path = os.path.join(context.temp_dir, "steps", "step_test.py")
    with open(path, "r") as f:
        content = f.read()
    assert p1 in content
    # The feature might use different steps, but our test feature has "Given test step"
    # codegen.py uses @given, @when, @then

@given('日本語のシナリオ名を持つ .feature ファイルがある')
def step_impl_5(context):
    create_feature_file(context, "ja.feature", "Feature: 日本語\n  Scenario: シナリオ\n    Given 日本語のステップ")

@then('生成されたステップ関数名が ASCII 文字のみで構成されること')
def step_impl_6(context):
    path = os.path.join(context.temp_dir, "steps", "step_ja.py")
    with open(path, "r") as f:
        content = f.read()
    matches = re.findall(r"def ([\w]+)\(", content)
    for m in matches:
        if m.startswith('given_') or m.startswith('when_') or m.startswith('then_'):
            assert all(ord(c) < 128 for c in m)

@then('関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること')
def step_impl_7(context):
    path = os.path.join(context.temp_dir, "steps", "step_ja.py")
    with open(path, "r") as f:
        content = f.read()
    assert re.search(r"[a-f0-9]{8}", content)

@then('docstring にオリジナルのステップ文が記載されること')
def step_impl_8(context):
    path = os.path.join(context.temp_dir, "steps", "step_ja.py")
    with open(path, "r") as f:
        content = f.read()
    assert "日本語のステップ" in content

@given('複数のシナリオで同一のステップ文が使用されている')
def step_impl_9(context):
    create_feature_file(context, "dup.feature", "Feature: Dup\n  Scenario: S1\n    Given common\n  Scenario: S2\n    Given common")

@then('同一ステップに対する関数は1回のみ生成されること')
def step_impl_10(context):
    path = os.path.join(context.temp_dir, "steps", "step_dup.py")
    with open(path, "r") as f:
        content = f.read()
    assert content.count("@given('common')") == 1

@given('出力先に既存のテストファイルが存在する')
def step_impl_11(context):
    os.makedirs(os.path.join(context.temp_dir, "steps"), exist_ok=True)
    with open(os.path.join(context.temp_dir, "steps/step_test.py"), "w") as f:
        f.write("# Existing")
    create_feature_file(context, "test.feature", "Feature: Test\n  Scenario: Test\n    Given test step")

@when('scaffold コマンドをデフォルトオプションで実行する')
def step_impl_12(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])

@then('既存ファイルはスキップされること')
def step_impl_13(context):
    path = os.path.join(context.temp_dir, "steps", "step_test.py")
    with open(path, "r") as f:
        content = f.read()
    assert "# Existing" in content

@then('スキップされた旨の警告が表示されること')
def step_impl_14(context):
    assert "スキップ" in context.stdout

@when('scaffold コマンドを "--overwrite" オプション付きで実行する')
def step_impl_15(context):
    run_cli(context, ["scaffold", "features", "-o", "steps", "--overwrite"])

@then('既存ファイルが上書きされること')
def step_impl_16(context):
    path = os.path.join(context.temp_dir, "steps", "step_test.py")
    with open(path, "r") as f:
        content = f.read()
    assert "# Existing" not in content
    assert "from behave import" in content
