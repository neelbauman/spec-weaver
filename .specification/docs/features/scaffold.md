# Feature: scaffold コマンド

**タグ**: `@SPEC-015`

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
@given('"{param0}" ファイルが存在するディレクトリがある')  # type: ignore
def given_488529e3(context, param0):
    """".feature" ファイルが存在するディレクトリがある

    Scenarios:
      - 基本的なテストコード生成
      - Docstring にシナリオリストを記載
    """
    pass
```

#### When scaffold コマンドを実行する

```python
@when(u'scaffold コマンドを実行する')
def step_impl(context):
    context.exit_code = 0
    context.output = ''
```

#### Then 各 .feature に対応する "step_<stem>.py" が生成されること

```python
@then('各 .feature に対応する "{param0}" が生成されること')  # type: ignore
def then_38f9dc8b(context, param0):
    """各 .feature に対応する "step_<stem>.py" が生成されること

    Scenarios:
      - 基本的なテストコード生成
    """
    pass
```

#### And 各ステップに "@given", "@when", "@then" デコレータ付き関数が含まれること

```python
@then('各ステップに "{param0}", "{param1}", "{param2}" デコレータ付き関数が含まれること')  # type: ignore
def then_398bb2af(context, param0, param1, param2):
    """各ステップに "@given", "@when", "@then" デコレータ付き関数が含まれること

    Scenarios:
      - 基本的なテストコード生成
    """
    pass
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
@given(u'日本語のシナリオ名を持つ .feature ファイルがある')
def step_impl(context):
    pass
```

#### When scaffold コマンドを実行する

```python
@when(u'scaffold コマンドを実行する')
def step_impl(context):
    context.exit_code = 0
    context.output = ''
```

#### Then 生成されたステップ関数名が ASCII 文字のみで構成されること

```python
@then(u'生成されたステップ関数名が ASCII 文字のみで構成されること')
def step_impl(context):
    pass
```

#### And 関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること

```python
@then(u'関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること')
def step_impl(context):
    pass
```

#### And docstring にオリジナルのステップ文が記載されること

```python
@then(u'docstring にオリジナルのステップ文が記載されること')
def step_impl(context):
    pass
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
@given(u'複数のシナリオで同一のステップ文が使用されている')
def step_impl(context):
    pass
```

#### When scaffold コマンドを実行する

```python
@when(u'scaffold コマンドを実行する')
def step_impl(context):
    context.exit_code = 0
    context.output = ''
```

#### Then 同一ステップに対する関数は1回のみ生成されること

```python
@then(u'同一ステップに対する関数は1回のみ生成されること')
def step_impl(context):
    pass
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
@given('"{param0}" ファイルが存在するディレクトリがある')  # type: ignore
def given_488529e3(context, param0):
    """".feature" ファイルが存在するディレクトリがある

    Scenarios:
      - 基本的なテストコード生成
      - Docstring にシナリオリストを記載
    """
    pass
```

#### When scaffold コマンドを実行する

```python
@when(u'scaffold コマンドを実行する')
def step_impl(context):
    context.exit_code = 0
    context.output = ''
```

#### Then 各ステップ関数の Docstring に "Scenarios:" セクションが含まれること

```python
@then('各ステップ関数の Docstring に "{param0}" セクションが含まれること')  # type: ignore
def then_5ab7d202(context, param0):
    """各ステップ関数の Docstring に "Scenarios:" セクションが含まれること

    Scenarios:
      - Docstring にシナリオリストを記載
    """
    pass
```

#### And そのステップを使用するシナリオ名が列挙されること

```python
@then(u'そのステップを使用するシナリオ名が列挙されること')
def step_impl(context):
    pass
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
@given(u'出力先に既存のテストファイルが存在する')
def step_impl(context):
    pass
```

#### And .feature に既存ファイルにないステップが追加されている

```python
@given(u'.feature に既存ファイルにないステップが追加されている')
def step_impl(context):
    pass
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when(u'scaffold コマンドをデフォルトオプションで実行する')
def step_impl(context):
    context.exit_code = 0
    context.output = ''
```

#### Then 既存ファイルに新規ステップのみが追記されること

```python
@then(u'既存ファイルに新規ステップのみが追記されること')
def step_impl(context):
    pass
```

#### And 既存のステップ定義は保持されること

```python
@then(u'既存のステップ定義は保持されること')
def step_impl(context):
    pass
```

#### And 新規ステップは .feature の出現順で挿入されること

```python
@then(u'新規ステップは .feature の出現順で挿入されること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: 差分なし時のスキップ

- **Given** 出力先の既存テストファイルが .feature と完全に同期している
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** ファイルへの書き込みは行われないこと
- **And** スキップ（差分なし）が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先の既存テストファイルが .feature と完全に同期している

```python
@given(u'出力先の既存テストファイルが .feature と完全に同期している')
def step_impl(context):
    pass
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when(u'scaffold コマンドをデフォルトオプションで実行する')
def step_impl(context):
    context.exit_code = 0
    context.output = ''
```

#### Then ファイルへの書き込みは行われないこと

```python
@then(u'ファイルへの書き込みは行われないこと')
def step_impl(context):
    pass
```

#### And スキップ（差分なし）が表示されること

```python
@then(u'スキップ（差分なし）が表示されること')
def step_impl(context):
    pass
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
@given(u'出力先に既存のテストファイルが存在する')
def step_impl(context):
    pass
```

#### When scaffold コマンドを "--overwrite" オプション付きで実行する

```python
@when('scaffold コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_b42c7e05(context, param0):
    """scaffold コマンドを "--overwrite" オプション付きで実行する

    Scenarios:
      - 既存ファイルの上書き
      - --force オプションで確認プロンプトをスキップ
    """
    pass
```

#### Then 既存ファイルが上書きされること

```python
@then(u'既存ファイルが上書きされること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: Git 未コミット変更の確認プロンプト

- **Given** 出力先のテストファイルに未コミットの変更がある
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** マージするか確認プロンプトが表示されること
- **And** キャンセルするとそのファイルはスキップされること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先のテストファイルに未コミットの変更がある

```python
@given(u'出力先のテストファイルに未コミットの変更がある')
def step_impl(context):
    pass
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when(u'scaffold コマンドをデフォルトオプションで実行する')
def step_impl(context):
    context.exit_code = 0
    context.output = ''
```

#### Then マージするか確認プロンプトが表示されること

```python
@then(u'マージするか確認プロンプトが表示されること')
def step_impl(context):
    pass
```

#### And キャンセルするとそのファイルはスキップされること

```python
@then(u'キャンセルするとそのファイルはスキップされること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: --force オプションで確認プロンプトをスキップ

- **Given** 出力先のテストファイルに未コミットの変更がある
- **When** scaffold コマンドを "--force" オプション付きで実行する
- **Then** 確認プロンプトなしでマージが実行されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 出力先のテストファイルに未コミットの変更がある

```python
@given(u'出力先のテストファイルに未コミットの変更がある')
def step_impl(context):
    pass
```

#### When scaffold コマンドを "--force" オプション付きで実行する

```python
@when('scaffold コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_b42c7e05(context, param0):
    """scaffold コマンドを "--overwrite" オプション付きで実行する

    Scenarios:
      - 既存ファイルの上書き
      - --force オプションで確認プロンプトをスキップ
    """
    pass
```

#### Then 確認プロンプトなしでマージが実行されること

```python
@then(u'確認プロンプトなしでマージが実行されること')
def step_impl(context):
    pass
```

</details>


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
@given(u'出力先に既存のテストファイルが存在する')
def step_impl(context):
    pass
```

#### And 別のステップファイルに同一ステップの実装が追加されている

```python
@given(u'別のステップファイルに同一ステップの実装が追加されている')
def step_impl(context):
    pass
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when(u'scaffold コマンドをデフォルトオプションで実行する')
def step_impl(context):
    context.exit_code = 0
    context.output = ''
```

#### Then 既存ファイルのスタブが Duplicate コメントに置き換わること

```python
@then(u'既存ファイルのスタブが Duplicate コメントに置き換わること')
def step_impl(context):
    pass
```

#### And 他のステップのスタブは保持されること

```python
@then(u'他のステップのスタブは保持されること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない

- **Given** 別のステップファイルに同一ステップが Duplicate コメントとして記載されている
- **And** その同一ステップを実際に定義しているファイルは存在しない
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** そのステップが Duplicate としてではなくスタブとして生成されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 別のステップファイルに同一ステップが Duplicate コメントとして記載されている

```python
@given(u'別のステップファイルに同一ステップが Duplicate コメントとして記載されている')
def step_impl(context):
    pass
```

#### And その同一ステップを実際に定義しているファイルは存在しない

```python
@given(u'その同一ステップを実際に定義しているファイルは存在しない')
def step_impl(context):
    pass
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when(u'scaffold コマンドをデフォルトオプションで実行する')
def step_impl(context):
    context.exit_code = 0
    context.output = ''
```

#### Then そのステップが Duplicate としてではなくスタブとして生成されること

```python
@then(u'そのステップが Duplicate としてではなくスタブとして生成されること')
def step_impl(context):
    pass
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: ac749f5b22acae3a56e7afe46f7303fcc05eeb9fe7aa5007ce208559648dc4e4
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