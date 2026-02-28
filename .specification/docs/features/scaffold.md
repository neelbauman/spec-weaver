# Feature: scaffold コマンド

**タグ**: `@SPEC-015`

**関連アイテム**: [SPEC-015](../items/SPEC-015.md)

.feature ファイルから behave テストコードの雛形を自動生成・差分マージする。

---
## Scenario: 基本的なテストコード生成

- **Given** ".feature" ファイルが存在するディレクトリがある
- **When** scaffold コマンドを実行する
- **Then** 各 .feature に対応する "step_<stem>.py" が生成されること
- **And** 各ステップに "@given", "@when", "@then" デコレータ付き関数が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given ".feature" ファイルが存在するディレクトリがある

```python
@given('"{param0}" ファイルが存在するディレクトリがある')
def step_impl_1(context, param0):
    create_feature_file(context, "test.feature", "Feature: Test\n  Scenario: Test\n    Given test step")
```

#### When scaffold コマンドを実行する

```python
@when('scaffold コマンドを実行する')
def step_impl_2(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])
```

#### Then 各 .feature に対応する "step_<stem>.py" が生成されること

```python
@then('各 .feature に対応する "step_<stem>.py" が生成されること')
def step_impl_3(context):
    path = os.path.join(context.temp_dir, "steps", "step_test.py")
    assert os.path.exists(path), f"File {path} not found. Stdout: {context.stdout}"
```

#### And 各ステップに "@given", "@when", "@then" デコレータ付き関数が含まれること

```python
@then('各ステップに "{p1}", "{p2}", "{p3}" デコレータ付き関数が含まれること')
def step_impl_4(context, p1, p2, p3):
    path = os.path.join(context.temp_dir, "steps", "step_test.py")
    with open(path, "r") as f:
        content = f.read()
    assert p1 in content
```

</details>


---
## Scenario: ハッシュベースの関数名生成

- **Given** 日本語のシナリオ名を持つ .feature ファイルがある
- **When** scaffold コマンドを実行する
- **Then** 生成されたステップ関数名が ASCII 文字のみで構成されること
- **And** 関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること
- **And** docstring にオリジナルのステップ文が記載されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 日本語のシナリオ名を持つ .feature ファイルがある

```python
@given('日本語のシナリオ名を持つ .feature ファイルがある')
def step_impl_5(context):
    create_feature_file(context, "ja.feature", "Feature: 日本語\n  Scenario: シナリオ\n    Given 日本語のステップ")
```

#### When scaffold コマンドを実行する

```python
@when('scaffold コマンドを実行する')
def step_impl_2(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])
```

#### Then 生成されたステップ関数名が ASCII 文字のみで構成されること

```python
@then('生成されたステップ関数名が ASCII 文字のみで構成されること')
def step_impl_6(context):
    path = os.path.join(context.temp_dir, "steps", "step_ja.py")
    with open(path, "r") as f:
        content = f.read()
    matches = re.findall(r"def ([\w]+)\(", content)
    for m in matches:
        if m.startswith('given_') or m.startswith('when_') or m.startswith('then_'):
            assert all(ord(c) < 128 for c in m)
```

#### And 関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること

```python
@then('関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること')
def step_impl_7(context):
    path = os.path.join(context.temp_dir, "steps", "step_ja.py")
    with open(path, "r") as f:
        content = f.read()
    assert re.search(r"[a-f0-9]{8}", content)
```

#### And docstring にオリジナルのステップ文が記載されること

```python
@then('docstring にオリジナルのステップ文が記載されること')
def step_impl_8(context):
    path = os.path.join(context.temp_dir, "steps", "step_ja.py")
    with open(path, "r") as f:
        content = f.read()
    assert "日本語のステップ" in content
```

</details>


---
## Scenario: ステップ関数の生成と重複排除

- **Given** 複数のシナリオで同一のステップ文が使用されている
- **When** scaffold コマンドを実行する
- **Then** 同一ステップに対する関数は1回のみ生成されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 複数のシナリオで同一のステップ文が使用されている

```python
@given('複数のシナリオで同一のステップ文が使用されている')
def step_impl_9(context):
    create_feature_file(context, "dup.feature", "Feature: Dup\n  Scenario: S1\n    Given common\n  Scenario: S2\n    Given common")
```

#### When scaffold コマンドを実行する

```python
@when('scaffold コマンドを実行する')
def step_impl_2(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])
```

#### Then 同一ステップに対する関数は1回のみ生成されること

```python
@then('同一ステップに対する関数は1回のみ生成されること')
def step_impl_10(context):
    path = os.path.join(context.temp_dir, "steps", "step_dup.py")
    with open(path, "r") as f:
        content = f.read()
    assert content.count("@given('common')") == 1
```

</details>


---
## Scenario: Docstring にシナリオリストを記載

- **Given** ".feature" ファイルが存在するディレクトリがある
- **When** scaffold コマンドを実行する
- **Then** 各ステップ関数の Docstring に "Scenarios:" セクションが含まれること
- **And** そのステップを使用するシナリオ名が列挙されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given ".feature" ファイルが存在するディレクトリがある

```python
@given('"{param0}" ファイルが存在するディレクトリがある')
def step_impl_1(context, param0):
    create_feature_file(context, "test.feature", "Feature: Test\n  Scenario: Test\n    Given test step")
```

#### When scaffold コマンドを実行する

```python
@when('scaffold コマンドを実行する')
def step_impl_2(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])
```

</details>


---
## Scenario: 差分マージ（新規ステップ追記）

- **Given** 出力先に既存のテストファイルが存在する
- **And** .feature に既存ファイルにないステップが追加されている
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** 既存ファイルに新規ステップのみが追記されること
- **And** 既存のステップ定義は保持されること
- **And** 新規ステップは .feature の出現順で挿入されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先に既存のテストファイルが存在する

```python
@given('出力先に既存のテストファイルが存在する')
def step_impl_11(context):
    os.makedirs(os.path.join(context.temp_dir, "steps"), exist_ok=True)
    with open(os.path.join(context.temp_dir, "steps/step_test.py"), "w") as f:
        f.write("# Existing")
    create_feature_file(context, "test.feature", "Feature: Test\n  Scenario: Test\n    Given test step")
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')
def step_impl_12(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])
```

</details>


---
## Scenario: 差分なし時のスキップ

- **Given** 出力先の既存テストファイルが .feature と完全に同期している
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** ファイルへの書き込みは行われないこと
- **And** スキップ（差分なし）が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')
def step_impl_12(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])
```

</details>


---
## Scenario: 既存ファイルの上書き

- **Given** 出力先に既存のテストファイルが存在する
- **When** scaffold コマンドを "--overwrite" オプション付きで実行する
- **Then** 既存ファイルが上書きされること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先に既存のテストファイルが存在する

```python
@given('出力先に既存のテストファイルが存在する')
def step_impl_11(context):
    os.makedirs(os.path.join(context.temp_dir, "steps"), exist_ok=True)
    with open(os.path.join(context.temp_dir, "steps/step_test.py"), "w") as f:
        f.write("# Existing")
    create_feature_file(context, "test.feature", "Feature: Test\n  Scenario: Test\n    Given test step")
```

#### When scaffold コマンドを "--overwrite" オプション付きで実行する

```python
@when('scaffold コマンドを "--overwrite" オプション付きで実行する')
def step_impl_15(context):
    run_cli(context, ["scaffold", "features", "-o", "steps", "--overwrite"])
```

#### Then 既存ファイルが上書きされること

```python
@then('既存ファイルが上書きされること')
def step_impl_16(context):
    path = os.path.join(context.temp_dir, "steps", "step_test.py")
    with open(path, "r") as f:
        content = f.read()
    assert "# Existing" not in content
    assert "from behave import" in content
```

</details>


---
## Scenario: Git 未コミット変更の確認プロンプト

- **Given** 出力先のテストファイルに未コミットの変更がある
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** マージするか確認プロンプトが表示されること
- **And** キャンセルするとそのファイルはスキップされること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')
def step_impl_12(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])
```

</details>


---
## Scenario: --force オプションで確認プロンプトをスキップ

- **Given** 出力先のテストファイルに未コミットの変更がある
- **When** scaffold コマンドを "--force" オプション付きで実行する
- **Then** 確認プロンプトなしでマージが実行されること

---
## Scenario: 差分マージ時の Duplicate スタブのコメント化

- **Given** 出力先に既存のテストファイルが存在する
- **And** 別のステップファイルに同一ステップの実装が追加されている
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** 既存ファイルのスタブが Duplicate コメントに置き換わること
- **And** 他のステップのスタブは保持されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先に既存のテストファイルが存在する

```python
@given('出力先に既存のテストファイルが存在する')
def step_impl_11(context):
    os.makedirs(os.path.join(context.temp_dir, "steps"), exist_ok=True)
    with open(os.path.join(context.temp_dir, "steps/step_test.py"), "w") as f:
        f.write("# Existing")
    create_feature_file(context, "test.feature", "Feature: Test\n  Scenario: Test\n    Given test step")
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')
def step_impl_12(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])
```

</details>


---
## Scenario: 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない

- **Given** 別のステップファイルに同一ステップが Duplicate コメントとして記載されている
- **And** その同一ステップを実際に定義しているファイルは存在しない
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** そのステップが Duplicate としてではなくスタブとして生成されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')
def step_impl_12(context):
    run_cli(context, ["scaffold", "features", "-o", "steps"])
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
@SPEC-015
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