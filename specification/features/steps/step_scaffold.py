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

@then('各 .feature に対応する "{param0}" が生成されること')  # type: ignore
def then_38f9dc8b(context, param0):
    """各 .feature に対応する "step_<stem>.py" が生成されること

    Scenarios:
      - 基本的なテストコード生成
    """
    raise NotImplementedError('STEP: 各 .feature に対応する "{param0}" が生成されること')


@then('各ステップに "{param0}", "{param1}", "{param2}" デコレータ付き関数が含まれること')  # type: ignore
def then_398bb2af(context, param0, param1, param2):
    """各ステップに "@given", "@when", "@then" デコレータ付き関数が含まれること

    Scenarios:
      - 基本的なテストコード生成
    """
    raise NotImplementedError('STEP: 各ステップに "{param0}", "{param1}", "{param2}" デコレータ付き関数が含まれること')


@then('各ステップ関数の Docstring に "{param0}" セクションが含まれること')  # type: ignore
def then_5ab7d202(context, param0):
    """各ステップ関数の Docstring に "Scenarios:" セクションが含まれること

    Scenarios:
      - Docstring にシナリオリストを記載
    """
    raise NotImplementedError('STEP: 各ステップ関数の Docstring に "{param0}" セクションが含まれること')


@then('そのステップを使用するシナリオ名が列挙されること')  # type: ignore
def then_6fd54334(context):
    """そのステップを使用するシナリオ名が列挙されること

    Scenarios:
      - Docstring にシナリオリストを記載
    """
    raise NotImplementedError('STEP: そのステップを使用するシナリオ名が列挙されること')


@given('.feature に既存ファイルにないステップが追加されている')  # type: ignore
def given_63fcef57(context):
    """.feature に既存ファイルにないステップが追加されている

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: .feature に既存ファイルにないステップが追加されている')


@then('既存ファイルに新規ステップのみが追記されること')  # type: ignore
def then_84ae62d5(context):
    """既存ファイルに新規ステップのみが追記されること

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: 既存ファイルに新規ステップのみが追記されること')


@then('既存のステップ定義は保持されること')  # type: ignore
def then_0cdc5832(context):
    """既存のステップ定義は保持されること

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: 既存のステップ定義は保持されること')


@then('新規ステップは .feature の出現順で挿入されること')  # type: ignore
def then_5c2cc2d3(context):
    """新規ステップは .feature の出現順で挿入されること

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: 新規ステップは .feature の出現順で挿入されること')


@given('出力先の既存テストファイルが .feature と完全に同期している')  # type: ignore
def given_fdb17660(context):
    """出力先の既存テストファイルが .feature と完全に同期している

    Scenarios:
      - 差分なし時のスキップ
    """
    raise NotImplementedError('STEP: 出力先の既存テストファイルが .feature と完全に同期している')


@then('ファイルへの書き込みは行われないこと')  # type: ignore
def then_834cd5e1(context):
    """ファイルへの書き込みは行われないこと

    Scenarios:
      - 差分なし時のスキップ
    """
    raise NotImplementedError('STEP: ファイルへの書き込みは行われないこと')


@then('スキップ（差分なし）が表示されること')  # type: ignore
def then_f45c0000(context):
    """スキップ（差分なし）が表示されること

    Scenarios:
      - 差分なし時のスキップ
    """
    raise NotImplementedError('STEP: スキップ（差分なし）が表示されること')


@when('scaffold コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_b42c7e05(context, param0):
    """scaffold コマンドを "--overwrite" オプション付きで実行する

    Scenarios:
      - 既存ファイルの上書き
      - --force オプションで確認プロンプトをスキップ
    """
    raise NotImplementedError('STEP: scaffold コマンドを "{param0}" オプション付きで実行する')


@given('出力先のテストファイルに未コミットの変更がある')  # type: ignore
def given_3f60de62(context):
    """出力先のテストファイルに未コミットの変更がある

    Scenarios:
      - Git 未コミット変更の確認プロンプト
      - --force オプションで確認プロンプトをスキップ
    """
    raise NotImplementedError('STEP: 出力先のテストファイルに未コミットの変更がある')


@then('マージするか確認プロンプトが表示されること')  # type: ignore
def then_fe932c66(context):
    """マージするか確認プロンプトが表示されること

    Scenarios:
      - Git 未コミット変更の確認プロンプト
    """
    raise NotImplementedError('STEP: マージするか確認プロンプトが表示されること')


@then('キャンセルするとそのファイルはスキップされること')  # type: ignore
def then_c8096039(context):
    """キャンセルするとそのファイルはスキップされること

    Scenarios:
      - Git 未コミット変更の確認プロンプト
    """
    raise NotImplementedError('STEP: キャンセルするとそのファイルはスキップされること')


@then('確認プロンプトなしでマージが実行されること')  # type: ignore
def then_4b7c11ee(context):
    """確認プロンプトなしでマージが実行されること

    Scenarios:
      - --force オプションで確認プロンプトをスキップ
    """
    raise NotImplementedError('STEP: 確認プロンプトなしでマージが実行されること')


@given('別のステップファイルに同一ステップの実装が追加されている')  # type: ignore
def given_b99b973a(context):
    """別のステップファイルに同一ステップの実装が追加されている

    Scenarios:
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 別のステップファイルに同一ステップの実装が追加されている')


@then('既存ファイルのスタブが Duplicate コメントに置き換わること')  # type: ignore
def then_df56f0cc(context):
    """既存ファイルのスタブが Duplicate コメントに置き換わること

    Scenarios:
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 既存ファイルのスタブが Duplicate コメントに置き換わること')


@then('他のステップのスタブは保持されること')  # type: ignore
def then_d0e8d8d6(context):
    """他のステップのスタブは保持されること

    Scenarios:
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 他のステップのスタブは保持されること')


@given('別のステップファイルに同一ステップが Duplicate コメントとして記載されている')  # type: ignore
def given_e0006816(context):
    """別のステップファイルに同一ステップが Duplicate コメントとして記載されている

    Scenarios:
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: 別のステップファイルに同一ステップが Duplicate コメントとして記載されている')


@given('その同一ステップを実際に定義しているファイルは存在しない')  # type: ignore
def given_0e535b1f(context):
    """その同一ステップを実際に定義しているファイルは存在しない

    Scenarios:
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: その同一ステップを実際に定義しているファイルは存在しない')


@then('そのステップが Duplicate としてではなくスタブとして生成されること')  # type: ignore
def then_35ff3425(context):
    """そのステップが Duplicate としてではなくスタブとして生成されること

    Scenarios:
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: そのステップが Duplicate としてではなくスタブとして生成されること')
@given('"{param0}" ファイルが存在するディレクトリがある')
def step_impl_1(context, param0):
    create_feature_file(context, "test.feature", "Feature: Test\n  Scenario: Test\n    Given test step")

@when('scaffold コマンドを実行する')
def step_impl_2(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])

# [Duplicate Skip] line 37 の @then('各 .feature に対応する "{param0}" が生成されること') で処理される
# @then('各 .feature に対応する "step_<stem>.py" が生成されること')
def _check_step_file_generated(context):
    path = os.path.join(context.temp_dir, "steps", "step_test.py")
    assert os.path.exists(path), f"File {path} not found. Stdout: {context.stdout}"

# [Duplicate Skip] line 47 の @then('各ステップに "{param0}", "{param1}", "{param2}" デコレータ付き関数が含まれること') で処理される
# @then('各ステップに "{p1}", "{p2}", "{p3}" デコレータ付き関数が含まれること')
# def step_impl_4(context, p1, p2, p3): ...

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

# [Duplicate Skip] line 147 の @when('scaffold コマンドを "{param0}" オプション付きで実行する') で処理される
# @when('scaffold コマンドを "--overwrite" オプション付きで実行する')
def _scaffold_with_overwrite(context):
    run_cli(context, ["scaffold", "features", "-o", "steps", "--overwrite"])

@then('既存ファイルが上書きされること')
def step_impl_16(context):
    path = os.path.join(context.temp_dir, "steps", "step_test.py")
    with open(path, "r") as f:
        content = f.read()
    assert "# Existing" not in content
    assert "from behave import" in content
