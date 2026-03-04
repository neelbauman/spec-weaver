# Feature: scaffold コマンド

**タグ**: `@AUT-001`

**関連アイテム**: [AUT-001](../items/AUT-001.md)

.feature ファイルから behave テストコードの雛形を自動生成・差分マージする。

---
## Scenario: 基本的なテストコード生成 {: #line-7 }

- **Given** ".feature" ファイルが存在するディレクトリがある
- **When** scaffold コマンドを実行する
- **Then** 各 .feature に対応する "step_<stem>.py" が生成されること
- **And** 各ステップに "@given", "@when", "@then" デコレータ付き関数が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given ".feature" ファイルが存在するディレクトリがある

```python
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
    

    Scenarios:
      - 基本的なテストコード生成
      - Docstring にシナリオリストを記載
    """)
    context.feature_dir = features_dir
    context.out_dir = context.temp_dir / "specification" / "features" / "steps"
```

#### When scaffold コマンドを実行する

```python
@when('scaffold コマンドを実行する')  # type: ignore
def when_4cda1d3b(context):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)]
    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 各 .feature に対応する "step_<stem>.py" が生成されること

```python
@then('各 .feature に対応する "{param0}" が生成されること')  # type: ignore
def then_38f9dc8b(context, param0):
    expected_file = context.out_dir / param0.replace("<stem>", "test")
    assert expected_file.exists(), f"Expected {expected_file} to exist"
```

#### And 各ステップに "@given", "@when", "@then" デコレータ付き関数が含まれること

```python
@then('各ステップに "{param0}", "{param1}", "{param2}" デコレータ付き関数が含まれること')  # type: ignore
def then_398bb2af(context, param0, param1, param2):
    step_file = context.out_dir / "step_test.py"
    content = step_file.read_text()
    assert param0 in content
    assert param1 in content
    assert param2 in content
```

</details>


---
## Scenario: ハッシュベースの関数名生成 {: #line-13 }

- **Given** 日本語のシナリオ名を持つ .feature ファイルがある
- **When** scaffold コマンドを実行する
- **Then** 生成されたステップ関数名が ASCII 文字のみで構成されること
- **And** 関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること
- **And** docstring にオリジナルのステップ文が記載されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 日本語のシナリオ名を持つ .feature ファイルがある

```python
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
    

    Scenarios:
      - ハッシュベースの関数名生成
    """)
    context.feature_dir = features_dir
    context.out_dir = context.temp_dir / "specification" / "features" / "steps"
```

#### When scaffold コマンドを実行する

```python
@when('scaffold コマンドを実行する')  # type: ignore
def when_4cda1d3b(context):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)]
    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 生成されたステップ関数名が ASCII 文字のみで構成されること

```python
@then('生成されたステップ関数名が ASCII 文字のみで構成されること')  # type: ignore
def then_75178cb9(context):
    step_file = context.out_dir / "step_jp.py"
    content = step_file.read_text()
    import re
    # find def func_name(context)
    func_names = re.findall(r"def\s+([a-zA-Z0-9_]+)\(", content)
    for name in func_names:
        assert all(ord(c) < 128 for c in name), f"Non-ASCII function name found: {name}"
```

#### And 関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること

```python
@then('関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること')  # type: ignore
def then_3649a406(context):
    pass
```

#### And docstring にオリジナルのステップ文が記載されること

```python
@then('docstring にオリジナルのステップ文が記載されること')  # type: ignore
def then_c876ede8(context):
    step_file = context.out_dir / "step_jp.py"
    content = step_file.read_text()
    assert "日本語のステップ" in content
```

</details>


---
## Scenario: ステップ関数の生成と重複排除 {: #line-20 }

- **Given** 複数のシナリオで同一のステップ文が使用されている
- **When** scaffold コマンドを実行する
- **Then** 同一ステップに対する関数は1回のみ生成されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 複数のシナリオで同一のステップ文が使用されている

```python
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
    

    Scenarios:
      - ステップ関数の生成と重複排除
    """)
    context.feature_dir = features_dir
    context.out_dir = context.temp_dir / "specification" / "features" / "steps"
```

#### When scaffold コマンドを実行する

```python
@when('scaffold コマンドを実行する')  # type: ignore
def when_4cda1d3b(context):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)]
    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 同一ステップに対する関数は1回のみ生成されること

```python
@then('同一ステップに対する関数は1回のみ生成されること')  # type: ignore
def then_67099eaf(context):
    step_file = context.out_dir / "step_dup.py"
    content = step_file.read_text()
    assert content.count("@given('same step')") == 1
```

</details>


---
## Scenario: Docstring にシナリオリストを記載 {: #line-25 }

- **Given** ".feature" ファイルが存在するディレクトリがある
- **When** scaffold コマンドを実行する
- **Then** 各ステップ関数の Docstring に "Scenarios:" セクションが含まれること
- **And** そのステップを使用するシナリオ名が列挙されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given ".feature" ファイルが存在するディレクトリがある

```python
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
    

    Scenarios:
      - 基本的なテストコード生成
      - Docstring にシナリオリストを記載
    """)
    context.feature_dir = features_dir
    context.out_dir = context.temp_dir / "specification" / "features" / "steps"
```

#### When scaffold コマンドを実行する

```python
@when('scaffold コマンドを実行する')  # type: ignore
def when_4cda1d3b(context):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)]
    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 各ステップ関数の Docstring に "Scenarios:" セクションが含まれること

```python
@then('各ステップ関数の Docstring に "{param0}" セクションが含まれること')  # type: ignore
def then_5ab7d202(context, param0):
    step_file = context.out_dir / "step_test.py"
    content = step_file.read_text()
    assert param0 in content
```

#### And そのステップを使用するシナリオ名が列挙されること

```python
@then('そのステップを使用するシナリオ名が列挙されること')  # type: ignore
def then_6fd54334(context):
    step_file = context.out_dir / "step_test.py"
    content = step_file.read_text()
    assert "Test Scenario" in content
```

</details>


---
## Scenario: 差分マージ（新規ステップ追記） {: #line-31 }

- **Given** 出力先に既存のテストファイルが存在する
- **And** .feature に既存ファイルにないステップが追加されている
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** 既存ファイルに新規ステップのみが追記されること
- **And** 既存のステップ定義は保持されること
- **And** 新規ステップは .feature の出現順で挿入されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先に既存のテストファイルが存在する

```python
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


    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 既存ファイルの上書き
      - 差分マージ時の Duplicate スタブのコメント化
    """)
    subprocess.run(["git", "add", "."], cwd=context.temp_dir)
    subprocess.run(["git", "commit", "-m", "init step"], cwd=context.temp_dir)
```

#### And .feature に既存ファイルにないステップが追加されている

```python
@given('.feature に既存ファイルにないステップが追加されている')  # type: ignore
def given_63fcef57(context):
    write_feature_file(context.feature_dir / "merge.feature", """
    Feature: Merge
      Scenario: S1
        Given existing step
        And new step
    

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """)
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)]
    # Provide "n" input to simulate cancellation on prompt
    context.result = run_spec_weaver(args, cwd=context.temp_dir, input="n\n")
```

#### Then 既存ファイルに新規ステップのみが追記されること

```python
@then('既存ファイルに新規ステップのみが追記されること')  # type: ignore
def then_84ae62d5(context):
    step_file = context.out_dir / "step_merge.py"
    content = step_file.read_text()
    assert "existing step" in content
    assert "new step" in content
```

#### And 既存のステップ定義は保持されること

```python
@then('既存のステップ定義は保持されること')  # type: ignore
def then_0cdc5832(context):
    step_file = context.out_dir / "step_merge.py"
    content = step_file.read_text()
    assert "pass" in content
```

#### And 新規ステップは .feature の出現順で挿入されること

```python
@then('新規ステップは .feature の出現順で挿入されること')  # type: ignore
def then_5c2cc2d3(context):
    pass
```

</details>


---
## Scenario: 差分なし時のスキップ {: #line-39 }

- **Given** 出力先の既存テストファイルが .feature と完全に同期している
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** ファイルへの書き込みは行われないこと
- **And** スキップ（差分なし）が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先の既存テストファイルが .feature と完全に同期している

```python
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
    

    Scenarios:
      - 差分なし時のスキップ
    """)
    context.feature_dir = features_dir
    context.out_dir = context.temp_dir / "specification" / "features" / "steps"
    context.out_dir.mkdir(parents=True, exist_ok=True)
    
    run_spec_weaver(["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)], cwd=context.temp_dir)
    subprocess.run(["git", "add", "."], cwd=context.temp_dir)
    subprocess.run(["git", "commit", "-m", "sync"], cwd=context.temp_dir)
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)]
    # Provide "n" input to simulate cancellation on prompt
    context.result = run_spec_weaver(args, cwd=context.temp_dir, input="n\n")
```

#### Then ファイルへの書き込みは行われないこと

```python
@then('ファイルへの書き込みは行われないこと')  # type: ignore
def then_834cd5e1(context):
    pass
```

#### And スキップ（差分なし）が表示されること

```python
@then('スキップ（差分なし）が表示されること')  # type: ignore
def then_f45c0000(context):
    assert "Skip" in context.result.stdout or "skip" in context.result.stdout or "差分なし" in context.result.stdout or "一致" in context.result.stdout
```

</details>


---
## Scenario: 既存ファイルの上書き {: #line-45 }

- **Given** 出力先に既存のテストファイルが存在する
- **When** scaffold コマンドを "--overwrite" オプション付きで実行する
- **Then** 既存ファイルが上書きされること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先に既存のテストファイルが存在する

```python
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


    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 既存ファイルの上書き
      - 差分マージ時の Duplicate スタブのコメント化
    """)
    subprocess.run(["git", "add", "."], cwd=context.temp_dir)
    subprocess.run(["git", "commit", "-m", "init step"], cwd=context.temp_dir)
```

#### When scaffold コマンドを "--overwrite" オプション付きで実行する

```python
@when('scaffold コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_b42c7e05(context, param0):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir), param0]
    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 既存ファイルが上書きされること

```python
@then('既存ファイルが上書きされること')  # type: ignore
def then_6f27dfe3(context):
    pass
```

</details>


---
## Scenario: Git 未コミット変更の確認プロンプト {: #line-50 }

- **Given** 出力先のテストファイルに未コミットの変更がある
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** マージするか確認プロンプトが表示されること
- **And** キャンセルするとそのファイルはスキップされること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先のテストファイルに未コミットの変更がある

```python
@given('出力先のテストファイルに未コミットの変更がある')  # type: ignore
def given_3f60de62(context):
    given_f54fe40f(context)
    step_file = context.out_dir / "step_merge.py"
    step_file.write_text(step_file.read_text() + "\n# dirty change\n")
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)]
    # Provide "n" input to simulate cancellation on prompt
    context.result = run_spec_weaver(args, cwd=context.temp_dir, input="n\n")
```

#### Then マージするか確認プロンプトが表示されること

```python
@then('マージするか確認プロンプトが表示されること')  # type: ignore
def then_fe932c66(context):
    # If stdin is empty, Confirm.ask will print the prompt and potentially error or return default
    # We check if the warning message about uncommitted changes is present in output
    assert "未コミットの変更があります" in context.result.stdout or "uncommitted" in context.result.stdout
```

#### And キャンセルするとそのファイルはスキップされること

```python
@then('キャンセルするとそのファイルはスキップされること')  # type: ignore
def then_c8096039(context):
    # Confirm.ask returns False on EOF if no default is set, leading to skip
    if "スキップ" not in context.result.stdout or "キャンセル" not in context.result.stdout:
        print(f"STDOUT: {context.result.stdout}")
        print(f"STDERR: {context.result.stderr}")
    assert "スキップ" in context.result.stdout
    assert "キャンセル" in context.result.stdout
```

</details>


---
## Scenario: --force オプションで確認プロンプトをスキップ {: #line-56 }

- **Given** 出力先のテストファイルに未コミットの変更がある
- **When** scaffold コマンドを "--force" オプション付きで実行する
- **Then** 確認プロンプトなしでマージが実行されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先のテストファイルに未コミットの変更がある

```python
@given('出力先のテストファイルに未コミットの変更がある')  # type: ignore
def given_3f60de62(context):
    given_f54fe40f(context)
    step_file = context.out_dir / "step_merge.py"
    step_file.write_text(step_file.read_text() + "\n# dirty change\n")
```

#### When scaffold コマンドを "--force" オプション付きで実行する

```python
@when('scaffold コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_b42c7e05(context, param0):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir), param0]
    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 確認プロンプトなしでマージが実行されること

```python
@then('確認プロンプトなしでマージが実行されること')  # type: ignore
def then_4b7c11ee(context):
    assert context.result.returncode == 0
```

</details>


---
## Scenario: 差分マージ時の Duplicate スタブのコメント化 {: #line-61 }

- **Given** 出力先に既存のテストファイルが存在する
- **And** 別のステップファイルに同一ステップの実装が追加されている
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** 既存ファイルのスタブが Duplicate コメントに置き換わること
- **And** 他のステップのスタブは保持されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先に既存のテストファイルが存在する

```python
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


    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 既存ファイルの上書き
      - 差分マージ時の Duplicate スタブのコメント化
    """)
    subprocess.run(["git", "add", "."], cwd=context.temp_dir)
    subprocess.run(["git", "commit", "-m", "init step"], cwd=context.temp_dir)
```

#### And 別のステップファイルに同一ステップの実装が追加されている

```python
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


    Scenarios:
      - 差分マージ時の Duplicate スタブのコメント化
    """)
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)]
    # Provide "n" input to simulate cancellation on prompt
    context.result = run_spec_weaver(args, cwd=context.temp_dir, input="n\n")
```

#### Then 既存ファイルのスタブが Duplicate コメントに置き換わること

```python
@then('既存ファイルのスタブが Duplicate コメントに置き換わること')  # type: ignore
def then_df56f0cc(context):
    pass
```

#### And 他のステップのスタブは保持されること

```python
@then('他のステップのスタブは保持されること')  # type: ignore
def then_d0e8d8d6(context):
    pass
```

</details>


---
## Scenario: 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない {: #line-68 }

- **Given** 別のステップファイルに同一ステップが Duplicate コメントとして記載されている
- **And** その同一ステップを実際に定義しているファイルは存在しない
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** そのステップが Duplicate としてではなくスタブとして生成されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 別のステップファイルに同一ステップが Duplicate コメントとして記載されている

```python
@given('別のステップファイルに同一ステップが Duplicate コメントとして記載されている')  # type: ignore
def given_e0006816(context):
    pass
```

#### And その同一ステップを実際に定義しているファイルは存在しない

```python
@given('その同一ステップを実際に定義しているファイルは存在しない')  # type: ignore
def given_0e535b1f(context):
    pass
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    args = ["scaffold", str(context.feature_dir), "--out-dir", str(context.out_dir)]
    # Provide "n" input to simulate cancellation on prompt
    context.result = run_spec_weaver(args, cwd=context.temp_dir, input="n\n")
```

#### Then そのステップが Duplicate としてではなくスタブとして生成されること

```python
@then('そのステップが Duplicate としてではなくスタブとして生成されること')  # type: ignore
def then_35ff3425(context):
    pass
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: ac749f5b22acae3a56e7afe46f7303fcc05eeb9fe7aa5007ce208559648dc4e4
# spec-weaver-fingerprint-AUT-001: UTfJmEYPmcQuHrgOv1vN08apU6dXlB-qvJ9nQVVfUts=
@AUT-001
Feature: scaffold コマンド
  .feature ファイルから behave テストコードの雛形を自動生成・差分マージする。

  Scenario: 基本的なテストコード生成
    Given ".feature" ファイルが存在するディレクトリがある
    When  scaffold コマンドを実行する
    Then  各 .feature に対応する "step_<stem>.py" が生成されること
    And   各ステップに "@given", "@when", "@then" デコレータ付き関数が含まれること

  Scenario: ハッシュベースの関数名生成
    Given 日本語のシナリオ名を持つ .feature ファイルがある
    When  scaffold コマンドを実行する
    Then  生成されたステップ関数名が ASCII 文字のみで構成されること
    And   関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること
    And   docstring にオリジナルのステップ文が記載されること

  Scenario: ステップ関数の生成と重複排除
    Given 複数のシナリオで同一のステップ文が使用されている
    When  scaffold コマンドを実行する
    Then  同一ステップに対する関数は1回のみ生成されること

  Scenario: Docstring にシナリオリストを記載
    Given ".feature" ファイルが存在するディレクトリがある
    When  scaffold コマンドを実行する
    Then  各ステップ関数の Docstring に "Scenarios:" セクションが含まれること
    And   そのステップを使用するシナリオ名が列挙されること

  Scenario: 差分マージ（新規ステップ追記）
    Given 出力先に既存のテストファイルが存在する
    And   .feature に既存ファイルにないステップが追加されている
    When  scaffold コマンドをデフォルトオプションで実行する
    Then  既存ファイルに新規ステップのみが追記されること
    And   既存のステップ定義は保持されること
    And   新規ステップは .feature の出現順で挿入されること

  Scenario: 差分なし時のスキップ
    Given 出力先の既存テストファイルが .feature と完全に同期している
    When  scaffold コマンドをデフォルトオプションで実行する
    Then  ファイルへの書き込みは行われないこと
    And   スキップ（差分なし）が表示されること

  Scenario: 既存ファイルの上書き
    Given 出力先に既存のテストファイルが存在する
    When  scaffold コマンドを "--overwrite" オプション付きで実行する
    Then  既存ファイルが上書きされること

  Scenario: Git 未コミット変更の確認プロンプト
    Given 出力先のテストファイルに未コミットの変更がある
    When  scaffold コマンドをデフォルトオプションで実行する
    Then  マージするか確認プロンプトが表示されること
    And   キャンセルするとそのファイルはスキップされること

  Scenario: --force オプションで確認プロンプトをスキップ
    Given 出力先のテストファイルに未コミットの変更がある
    When  scaffold コマンドを "--force" オプション付きで実行する
    Then  確認プロンプトなしでマージが実行されること

  Scenario: 差分マージ時の Duplicate スタブのコメント化
    Given 出力先に既存のテストファイルが存在する
    And   別のステップファイルに同一ステップの実装が追加されている
    When  scaffold コマンドをデフォルトオプションで実行する
    Then  既存ファイルのスタブが Duplicate コメントに置き換わること
    And   他のステップのスタブは保持されること

  Scenario: 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    Given 別のステップファイルに同一ステップが Duplicate コメントとして記載されている
    And   その同一ステップを実際に定義しているファイルは存在しない
    When  scaffold コマンドをデフォルトオプションで実行する
    Then  そのステップが Duplicate としてではなくスタブとして生成されること

```
</details>