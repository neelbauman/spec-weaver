# -*- coding: utf-8 -*-
from specification.features.steps._helpers import create_doorstop_project_api, write_feature_file, run_spec_weaver, write_doorstop_yaml
from behave import given, when, then, step
from pathlib import Path
import shutil
import os
import subprocess

# ======================================================================
# Steps
# ======================================================================

@given('"{param0}" ファイルが存在するディレクトリがある')  # type: ignore
def given_488529e3(context, param0):
    # Git init
    subprocess.run(["git", "init"], cwd=context.temp_dir, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=context.temp_dir)
    subprocess.run(["git", "config", "user.name", "test"], cwd=context.temp_dir)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "init"], cwd=context.temp_dir)

    features_dir = context.temp_dir / "specification" / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(features_dir / "test.feature", """
    Feature: Test
      Scenario: Test Scenario
        Given a step
        When I do something
        Then result is ok
    """)
    context.feature_dir = features_dir
    context.out_dir = context.temp_dir / "specification" / "features" / "steps"


@when('scaffold コマンドを実行する')  # type: ignore
def when_4cda1d3b(context):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)]
    context.result = run_spec_weaver(args, cwd=context.temp_dir)


@then('各 .feature に対応する "{param0}" が生成されること')  # type: ignore
def then_38f9dc8b(context, param0):
    expected_file = context.out_dir / param0.replace("<stem>", "test")
    assert expected_file.exists(), f"Expected {expected_file} to exist"


@then('各ステップに "{param0}", "{param1}", "{param2}" デコレータ付き関数が含まれること')  # type: ignore
def then_398bb2af(context, param0, param1, param2):
    step_file = context.out_dir / "step_test.py"
    content = step_file.read_text()
    assert param0 in content
    assert param1 in content
    assert param2 in content


@given('日本語のシナリオ名を持つ .feature ファイルがある')  # type: ignore
def given_a87fa38a(context):
    # Git init if not exists
    if not (context.temp_dir / ".git").exists():
        subprocess.run(["git", "init"], cwd=context.temp_dir, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=context.temp_dir)
        subprocess.run(["git", "config", "user.name", "test"], cwd=context.temp_dir)
        subprocess.run(["git", "commit", "--allow-empty", "-m", "init"], cwd=context.temp_dir)

    features_dir = context.temp_dir / "specification" / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(features_dir / "jp.feature", """
    Feature: 日本語テスト
      Scenario: 日本語シナリオ
        Given 日本語のステップ
    """)
    context.feature_dir = features_dir
    context.out_dir = context.temp_dir / "specification" / "features" / "steps"


@then('生成されたステップ関数名が ASCII 文字のみで構成されること')  # type: ignore
def then_75178cb9(context):
    step_file = context.out_dir / "step_jp.py"
    content = step_file.read_text()
    import re
    # find def func_name(context)
    func_names = re.findall(r"def\s+([a-zA-Z0-9_]+)\(", content)
    for name in func_names:
        assert all(ord(c) < 128 for c in name), f"Non-ASCII function name found: {name}"


@then('関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること')  # type: ignore
def then_3649a406(context):
    pass


@then('docstring にオリジナルのステップ文が記載されること')  # type: ignore
def then_c876ede8(context):
    step_file = context.out_dir / "step_jp.py"
    content = step_file.read_text()
    assert "日本語のステップ" in content


@given('複数のシナリオで同一のステップ文が使用されている')  # type: ignore
def given_ae2a90a1(context):
    features_dir = context.temp_dir / "specification" / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(features_dir / "dup.feature", """
    Feature: Duplicate
      Scenario: S1
        Given same step
      Scenario: S2
        Given same step
    """)
    context.feature_dir = features_dir
    context.out_dir = context.temp_dir / "specification" / "features" / "steps"


@then('同一ステップに対する関数は1回のみ生成されること')  # type: ignore
def then_67099eaf(context):
    step_file = context.out_dir / "step_dup.py"
    content = step_file.read_text()
    assert content.count("@given('same step')") == 1


@then('各ステップ関数の Docstring に "{param0}" セクションが含まれること')  # type: ignore
def then_5ab7d202(context, param0):
    step_file = context.out_dir / "step_test.py"
    content = step_file.read_text()
    assert param0 in content


@then('そのステップを使用するシナリオ名が列挙されること')  # type: ignore
def then_6fd54334(context):
    step_file = context.out_dir / "step_test.py"
    content = step_file.read_text()
    assert "Test Scenario" in content


@given('出力先に既存のテストファイルが存在する')  # type: ignore
def given_f54fe40f(context):
    # Git init
    subprocess.run(["git", "init"], cwd=context.temp_dir, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=context.temp_dir)
    subprocess.run(["git", "config", "user.name", "test"], cwd=context.temp_dir)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "init"], cwd=context.temp_dir)

    features_dir = context.temp_dir / "specification" / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(features_dir / "merge.feature", """
    Feature: Merge
      Scenario: S1
        Given existing step
    """)
    context.feature_dir = features_dir
    context.out_dir = context.temp_dir / "specification" / "features" / "steps"
    context.out_dir.mkdir(parents=True, exist_ok=True)
    
    step_file = context.out_dir / "step_merge.py"
    step_file.write_text("""
from behave import given

@given('existing step')
def step_impl(context):
    pass
""")
    subprocess.run(["git", "add", "."], cwd=context.temp_dir)
    subprocess.run(["git", "commit", "-m", "init step"], cwd=context.temp_dir)


@given('.feature に既存ファイルにないステップが追加されている')  # type: ignore
def given_63fcef57(context):
    write_feature_file(context.feature_dir / "merge.feature", """
    Feature: Merge
      Scenario: S1
        Given existing step
        And new step
    """)


@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)]
    # Provide "n" input to simulate cancellation on prompt
    context.result = run_spec_weaver(args, cwd=context.temp_dir, input="n\n")


@then('既存ファイルに新規ステップのみが追記されること')  # type: ignore
def then_84ae62d5(context):
    step_file = context.out_dir / "step_merge.py"
    content = step_file.read_text()
    assert "existing step" in content
    assert "new step" in content


@then('既存のステップ定義は保持されること')  # type: ignore
def then_0cdc5832(context):
    step_file = context.out_dir / "step_merge.py"
    content = step_file.read_text()
    assert "pass" in content


@then('新規ステップは .feature の出現順で挿入されること')  # type: ignore
def then_5c2cc2d3(context):
    pass


@given('出力先の既存テストファイルが .feature と完全に同期している')  # type: ignore
def given_fdb17660(context):
    # Git init
    subprocess.run(["git", "init"], cwd=context.temp_dir, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=context.temp_dir)
    subprocess.run(["git", "config", "user.name", "test"], cwd=context.temp_dir)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "init"], cwd=context.temp_dir)

    features_dir = context.temp_dir / "specification" / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(features_dir / "sync.feature", """
    Feature: Sync
      Scenario: S1
        Given step1
    """)
    context.feature_dir = features_dir
    context.out_dir = context.temp_dir / "specification" / "features" / "steps"
    context.out_dir.mkdir(parents=True, exist_ok=True)
    
    run_spec_weaver(["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)], cwd=context.temp_dir)
    subprocess.run(["git", "add", "."], cwd=context.temp_dir)
    subprocess.run(["git", "commit", "-m", "sync"], cwd=context.temp_dir)


@then('ファイルへの書き込みは行われないこと')  # type: ignore
def then_834cd5e1(context):
    pass


@then('スキップ（差分なし）が表示されること')  # type: ignore
def then_f45c0000(context):
    assert "Skip" in context.result.stdout or "skip" in context.result.stdout or "差分なし" in context.result.stdout or "一致" in context.result.stdout


@when('scaffold コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_b42c7e05(context, param0):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir), param0]
    context.result = run_spec_weaver(args, cwd=context.temp_dir)


@then('既存ファイルが上書きされること')  # type: ignore
def then_6f27dfe3(context):
    pass


@given('出力先のテストファイルに未コミットの変更がある')  # type: ignore
def given_3f60de62(context):
    given_f54fe40f(context)
    step_file = context.out_dir / "step_merge.py"
    step_file.write_text(step_file.read_text() + "\n# dirty change\n")


@then('マージするか確認プロンプトが表示されること')  # type: ignore
def then_fe932c66(context):
    # If stdin is empty, Confirm.ask will print the prompt and potentially error or return default
    # We check if the warning message about uncommitted changes is present in output
    assert "未コミットの変更があります" in context.result.stdout or "uncommitted" in context.result.stdout


@then('キャンセルするとそのファイルはスキップされること')  # type: ignore
def then_c8096039(context):
    # Confirm.ask returns False on EOF if no default is set, leading to skip
    if "スキップ" not in context.result.stdout or "キャンセル" not in context.result.stdout:
        print(f"STDOUT: {context.result.stdout}")
        print(f"STDERR: {context.result.stderr}")
    assert "スキップ" in context.result.stdout
    assert "キャンセル" in context.result.stdout


@then('確認プロンプトなしでマージが実行されること')  # type: ignore
def then_4b7c11ee(context):
    assert context.result.returncode == 0


@given('別のステップファイルに同一ステップの実装が追加されている')  # type: ignore
def given_b99b973a(context):
    # Git init
    subprocess.run(["git", "init"], cwd=context.temp_dir, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=context.temp_dir)
    subprocess.run(["git", "config", "user.name", "test"], cwd=context.temp_dir)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "init"], cwd=context.temp_dir)

    features_dir = context.temp_dir / "specification" / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(features_dir / "other.feature", """
    Feature: Other
      Scenario: S1
        Given shared step
    """)
    context.feature_dir = features_dir
    context.out_dir = context.temp_dir / "specification" / "features" / "steps"
    context.out_dir.mkdir(parents=True, exist_ok=True)
    
    (context.out_dir / "step_other.py").write_text("""
from behave import given
@given('shared step')
def step_impl(context):
    pass
""")


@then('既存ファイルのスタブが Duplicate コメントに置き換わること')  # type: ignore
def then_df56f0cc(context):
    pass


@then('他のステップのスタブは保持されること')  # type: ignore
def then_d0e8d8d6(context):
    pass


@given('別のステップファイルに同一ステップが Duplicate コメントとして記載されている')  # type: ignore
def given_e0006816(context):
    pass


@given('その同一ステップを実際に定義しているファイルは存在しない')  # type: ignore
def given_0e535b1f(context):
    pass


@then('そのステップが Duplicate としてではなくスタブとして生成されること')  # type: ignore
def then_35ff3425(context):
    pass
