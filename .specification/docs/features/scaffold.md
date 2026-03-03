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

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_scaffold.py", line 31, in when_4cda1d3b
    raise NotImplementedError('STEP: scaffold コマンドを実行する')
NotImplementedError: STEP: scaffold コマンドを実行する
```

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
@when('scaffold コマンドを実行する')  # type: ignore
def when_4cda1d3b(context):
    """scaffold コマンドを実行する

    Scenarios:
      - 基本的なテストコード生成
      - ハッシュベースの関数名生成
      - ステップ関数の生成と重複排除
      - Docstring にシナリオリストを記載
    """
    raise NotImplementedError('STEP: scaffold コマンドを実行する')
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
## Scenario: ハッシュベースの関数名生成 {: #line-13 }

- **Given** 日本語のシナリオ名を持つ .feature ファイルがある
- **When** scaffold コマンドを実行する
- **Then** 生成されたステップ関数名が ASCII 文字のみで構成されること
- **And** 関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること
- **And** docstring にオリジナルのステップ文が記載されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_scaffold.py", line 61, in given_a87fa38a
    raise NotImplementedError('STEP: 日本語のシナリオ名を持つ .feature ファイルがある')
NotImplementedError: STEP: 日本語のシナリオ名を持つ .feature ファイルがある
```

#### Given 日本語のシナリオ名を持つ .feature ファイルがある

```python
@given('日本語のシナリオ名を持つ .feature ファイルがある')  # type: ignore
def given_a87fa38a(context):
    """日本語のシナリオ名を持つ .feature ファイルがある

    Scenarios:
      - ハッシュベースの関数名生成
    """
    raise NotImplementedError('STEP: 日本語のシナリオ名を持つ .feature ファイルがある')
```

#### When scaffold コマンドを実行する

```python
@when('scaffold コマンドを実行する')  # type: ignore
def when_4cda1d3b(context):
    """scaffold コマンドを実行する

    Scenarios:
      - 基本的なテストコード生成
      - ハッシュベースの関数名生成
      - ステップ関数の生成と重複排除
      - Docstring にシナリオリストを記載
    """
    raise NotImplementedError('STEP: scaffold コマンドを実行する')
```

#### Then 生成されたステップ関数名が ASCII 文字のみで構成されること

```python
@then('生成されたステップ関数名が ASCII 文字のみで構成されること')  # type: ignore
def then_75178cb9(context):
    """生成されたステップ関数名が ASCII 文字のみで構成されること

    Scenarios:
      - ハッシュベースの関数名生成
    """
    raise NotImplementedError('STEP: 生成されたステップ関数名が ASCII 文字のみで構成されること')
```

#### And 関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること

```python
@then('関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること')  # type: ignore
def then_3649a406(context):
    """関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること

    Scenarios:
      - ハッシュベースの関数名生成
    """
    raise NotImplementedError('STEP: 関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること')
```

#### And docstring にオリジナルのステップ文が記載されること

```python
@then('docstring にオリジナルのステップ文が記載されること')  # type: ignore
def then_c876ede8(context):
    """docstring にオリジナルのステップ文が記載されること

    Scenarios:
      - ハッシュベースの関数名生成
    """
    raise NotImplementedError('STEP: docstring にオリジナルのステップ文が記載されること')
```

</details>


---
## Scenario: ステップ関数の生成と重複排除 {: #line-20 }

- **Given** 複数のシナリオで同一のステップ文が使用されている
- **When** scaffold コマンドを実行する
- **Then** 同一ステップに対する関数は1回のみ生成されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_scaffold.py", line 101, in given_ae2a90a1
    raise NotImplementedError('STEP: 複数のシナリオで同一のステップ文が使用されている')
NotImplementedError: STEP: 複数のシナリオで同一のステップ文が使用されている
```

#### Given 複数のシナリオで同一のステップ文が使用されている

```python
@given('複数のシナリオで同一のステップ文が使用されている')  # type: ignore
def given_ae2a90a1(context):
    """複数のシナリオで同一のステップ文が使用されている

    Scenarios:
      - ステップ関数の生成と重複排除
    """
    raise NotImplementedError('STEP: 複数のシナリオで同一のステップ文が使用されている')
```

#### When scaffold コマンドを実行する

```python
@when('scaffold コマンドを実行する')  # type: ignore
def when_4cda1d3b(context):
    """scaffold コマンドを実行する

    Scenarios:
      - 基本的なテストコード生成
      - ハッシュベースの関数名生成
      - ステップ関数の生成と重複排除
      - Docstring にシナリオリストを記載
    """
    raise NotImplementedError('STEP: scaffold コマンドを実行する')
```

#### Then 同一ステップに対する関数は1回のみ生成されること

```python
@then('同一ステップに対する関数は1回のみ生成されること')  # type: ignore
def then_67099eaf(context):
    """同一ステップに対する関数は1回のみ生成されること

    Scenarios:
      - ステップ関数の生成と重複排除
    """
    raise NotImplementedError('STEP: 同一ステップに対する関数は1回のみ生成されること')
```

</details>


---
## Scenario: Docstring にシナリオリストを記載 {: #line-25 }

- **Given** ".feature" ファイルが存在するディレクトリがある
- **When** scaffold コマンドを実行する
- **Then** 各ステップ関数の Docstring に "Scenarios:" セクションが含まれること
- **And** そのステップを使用するシナリオ名が列挙されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_scaffold.py", line 31, in when_4cda1d3b
    raise NotImplementedError('STEP: scaffold コマンドを実行する')
NotImplementedError: STEP: scaffold コマンドを実行する
```

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
@when('scaffold コマンドを実行する')  # type: ignore
def when_4cda1d3b(context):
    """scaffold コマンドを実行する

    Scenarios:
      - 基本的なテストコード生成
      - ハッシュベースの関数名生成
      - ステップ関数の生成と重複排除
      - Docstring にシナリオリストを記載
    """
    raise NotImplementedError('STEP: scaffold コマンドを実行する')
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
@then('そのステップを使用するシナリオ名が列挙されること')  # type: ignore
def then_6fd54334(context):
    """そのステップを使用するシナリオ名が列挙されること

    Scenarios:
      - Docstring にシナリオリストを記載
    """
    raise NotImplementedError('STEP: そのステップを使用するシナリオ名が列挙されること')
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

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_scaffold.py", line 143, in given_f54fe40f
    raise NotImplementedError('STEP: 出力先に既存のテストファイルが存在する')
NotImplementedError: STEP: 出力先に既存のテストファイルが存在する
```

#### Given 出力先に既存のテストファイルが存在する

```python
@given('出力先に既存のテストファイルが存在する')  # type: ignore
def given_f54fe40f(context):
    """出力先に既存のテストファイルが存在する

    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 既存ファイルの上書き
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 出力先に既存のテストファイルが存在する')
```

#### And .feature に既存ファイルにないステップが追加されている

```python
@given('.feature に既存ファイルにないステップが追加されている')  # type: ignore
def given_63fcef57(context):
    """.feature に既存ファイルにないステップが追加されている

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: .feature に既存ファイルにないステップが追加されている')
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    """scaffold コマンドをデフォルトオプションで実行する

    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 差分なし時のスキップ
      - Git 未コミット変更の確認プロンプト
      - 差分マージ時の Duplicate スタブのコメント化
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: scaffold コマンドをデフォルトオプションで実行する')
```

#### Then 既存ファイルに新規ステップのみが追記されること

```python
@then('既存ファイルに新規ステップのみが追記されること')  # type: ignore
def then_84ae62d5(context):
    """既存ファイルに新規ステップのみが追記されること

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: 既存ファイルに新規ステップのみが追記されること')
```

#### And 既存のステップ定義は保持されること

```python
@then('既存のステップ定義は保持されること')  # type: ignore
def then_0cdc5832(context):
    """既存のステップ定義は保持されること

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: 既存のステップ定義は保持されること')
```

#### And 新規ステップは .feature の出現順で挿入されること

```python
@then('新規ステップは .feature の出現順で挿入されること')  # type: ignore
def then_5c2cc2d3(context):
    """新規ステップは .feature の出現順で挿入されること

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: 新規ステップは .feature の出現順で挿入されること')
```

</details>


---
## Scenario: 差分なし時のスキップ {: #line-39 }

- **Given** 出力先の既存テストファイルが .feature と完全に同期している
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** ファイルへの書き込みは行われないこと
- **And** スキップ（差分なし）が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_scaffold.py", line 207, in given_fdb17660
    raise NotImplementedError('STEP: 出力先の既存テストファイルが .feature と完全に同期している')
NotImplementedError: STEP: 出力先の既存テストファイルが .feature と完全に同期している
```

#### Given 出力先の既存テストファイルが .feature と完全に同期している

```python
@given('出力先の既存テストファイルが .feature と完全に同期している')  # type: ignore
def given_fdb17660(context):
    """出力先の既存テストファイルが .feature と完全に同期している

    Scenarios:
      - 差分なし時のスキップ
    """
    raise NotImplementedError('STEP: 出力先の既存テストファイルが .feature と完全に同期している')
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    """scaffold コマンドをデフォルトオプションで実行する

    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 差分なし時のスキップ
      - Git 未コミット変更の確認プロンプト
      - 差分マージ時の Duplicate スタブのコメント化
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: scaffold コマンドをデフォルトオプションで実行する')
```

#### Then ファイルへの書き込みは行われないこと

```python
@then('ファイルへの書き込みは行われないこと')  # type: ignore
def then_834cd5e1(context):
    """ファイルへの書き込みは行われないこと

    Scenarios:
      - 差分なし時のスキップ
    """
    raise NotImplementedError('STEP: ファイルへの書き込みは行われないこと')
```

#### And スキップ（差分なし）が表示されること

```python
@then('スキップ（差分なし）が表示されること')  # type: ignore
def then_f45c0000(context):
    """スキップ（差分なし）が表示されること

    Scenarios:
      - 差分なし時のスキップ
    """
    raise NotImplementedError('STEP: スキップ（差分なし）が表示されること')
```

</details>


---
## Scenario: 既存ファイルの上書き {: #line-45 }

- **Given** 出力先に既存のテストファイルが存在する
- **When** scaffold コマンドを "--overwrite" オプション付きで実行する
- **Then** 既存ファイルが上書きされること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_scaffold.py", line 143, in given_f54fe40f
    raise NotImplementedError('STEP: 出力先に既存のテストファイルが存在する')
NotImplementedError: STEP: 出力先に既存のテストファイルが存在する
```

#### Given 出力先に既存のテストファイルが存在する

```python
@given('出力先に既存のテストファイルが存在する')  # type: ignore
def given_f54fe40f(context):
    """出力先に既存のテストファイルが存在する

    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 既存ファイルの上書き
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 出力先に既存のテストファイルが存在する')
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
@then('既存ファイルが上書きされること')  # type: ignore
def then_6f27dfe3(context):
    """既存ファイルが上書きされること

    Scenarios:
      - 既存ファイルの上書き
    """
    raise NotImplementedError('STEP: 既存ファイルが上書きされること')
```

</details>


---
## Scenario: Git 未コミット変更の確認プロンプト {: #line-50 }

- **Given** 出力先のテストファイルに未コミットの変更がある
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** マージするか確認プロンプトが表示されること
- **And** キャンセルするとそのファイルはスキップされること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_scaffold.py", line 259, in given_3f60de62
    raise NotImplementedError('STEP: 出力先のテストファイルに未コミットの変更がある')
NotImplementedError: STEP: 出力先のテストファイルに未コミットの変更がある
```

#### Given 出力先のテストファイルに未コミットの変更がある

```python
@given('出力先のテストファイルに未コミットの変更がある')  # type: ignore
def given_3f60de62(context):
    """出力先のテストファイルに未コミットの変更がある

    Scenarios:
      - Git 未コミット変更の確認プロンプト
      - --force オプションで確認プロンプトをスキップ
    """
    raise NotImplementedError('STEP: 出力先のテストファイルに未コミットの変更がある')
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    """scaffold コマンドをデフォルトオプションで実行する

    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 差分なし時のスキップ
      - Git 未コミット変更の確認プロンプト
      - 差分マージ時の Duplicate スタブのコメント化
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: scaffold コマンドをデフォルトオプションで実行する')
```

#### Then マージするか確認プロンプトが表示されること

```python
@then('マージするか確認プロンプトが表示されること')  # type: ignore
def then_fe932c66(context):
    """マージするか確認プロンプトが表示されること

    Scenarios:
      - Git 未コミット変更の確認プロンプト
    """
    raise NotImplementedError('STEP: マージするか確認プロンプトが表示されること')
```

#### And キャンセルするとそのファイルはスキップされること

```python
@then('キャンセルするとそのファイルはスキップされること')  # type: ignore
def then_c8096039(context):
    """キャンセルするとそのファイルはスキップされること

    Scenarios:
      - Git 未コミット変更の確認プロンプト
    """
    raise NotImplementedError('STEP: キャンセルするとそのファイルはスキップされること')
```

</details>


---
## Scenario: --force オプションで確認プロンプトをスキップ {: #line-56 }

- **Given** 出力先のテストファイルに未コミットの変更がある
- **When** scaffold コマンドを "--force" オプション付きで実行する
- **Then** 確認プロンプトなしでマージが実行されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_scaffold.py", line 259, in given_3f60de62
    raise NotImplementedError('STEP: 出力先のテストファイルに未コミットの変更がある')
NotImplementedError: STEP: 出力先のテストファイルに未コミットの変更がある
```

#### Given 出力先のテストファイルに未コミットの変更がある

```python
@given('出力先のテストファイルに未コミットの変更がある')  # type: ignore
def given_3f60de62(context):
    """出力先のテストファイルに未コミットの変更がある

    Scenarios:
      - Git 未コミット変更の確認プロンプト
      - --force オプションで確認プロンプトをスキップ
    """
    raise NotImplementedError('STEP: 出力先のテストファイルに未コミットの変更がある')
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
@then('確認プロンプトなしでマージが実行されること')  # type: ignore
def then_4b7c11ee(context):
    """確認プロンプトなしでマージが実行されること

    Scenarios:
      - --force オプションで確認プロンプトをスキップ
    """
    raise NotImplementedError('STEP: 確認プロンプトなしでマージが実行されること')
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

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_scaffold.py", line 143, in given_f54fe40f
    raise NotImplementedError('STEP: 出力先に既存のテストファイルが存在する')
NotImplementedError: STEP: 出力先に既存のテストファイルが存在する
```

#### Given 出力先に既存のテストファイルが存在する

```python
@given('出力先に既存のテストファイルが存在する')  # type: ignore
def given_f54fe40f(context):
    """出力先に既存のテストファイルが存在する

    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 既存ファイルの上書き
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 出力先に既存のテストファイルが存在する')
```

#### And 別のステップファイルに同一ステップの実装が追加されている

```python
@given('別のステップファイルに同一ステップの実装が追加されている')  # type: ignore
def given_b99b973a(context):
    """別のステップファイルに同一ステップの実装が追加されている

    Scenarios:
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 別のステップファイルに同一ステップの実装が追加されている')
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    """scaffold コマンドをデフォルトオプションで実行する

    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 差分なし時のスキップ
      - Git 未コミット変更の確認プロンプト
      - 差分マージ時の Duplicate スタブのコメント化
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: scaffold コマンドをデフォルトオプションで実行する')
```

#### Then 既存ファイルのスタブが Duplicate コメントに置き換わること

```python
@then('既存ファイルのスタブが Duplicate コメントに置き換わること')  # type: ignore
def then_df56f0cc(context):
    """既存ファイルのスタブが Duplicate コメントに置き換わること

    Scenarios:
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 既存ファイルのスタブが Duplicate コメントに置き換わること')
```

#### And 他のステップのスタブは保持されること

```python
@then('他のステップのスタブは保持されること')  # type: ignore
def then_d0e8d8d6(context):
    """他のステップのスタブは保持されること

    Scenarios:
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 他のステップのスタブは保持されること')
```

</details>


---
## Scenario: 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない {: #line-68 }

- **Given** 別のステップファイルに同一ステップが Duplicate コメントとして記載されている
- **And** その同一ステップを実際に定義しているファイルは存在しない
- **When** scaffold コマンドをデフォルトオプションで実行する
- **Then** そのステップが Duplicate としてではなくスタブとして生成されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_scaffold.py", line 329, in given_e0006816
    raise NotImplementedError('STEP: 別のステップファイルに同一ステップが Duplicate コメントとして記載されている')
NotImplementedError: STEP: 別のステップファイルに同一ステップが Duplicate コメントとして記載されている
```

#### Given 別のステップファイルに同一ステップが Duplicate コメントとして記載されている

```python
@given('別のステップファイルに同一ステップが Duplicate コメントとして記載されている')  # type: ignore
def given_e0006816(context):
    """別のステップファイルに同一ステップが Duplicate コメントとして記載されている

    Scenarios:
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: 別のステップファイルに同一ステップが Duplicate コメントとして記載されている')
```

#### And その同一ステップを実際に定義しているファイルは存在しない

```python
@given('その同一ステップを実際に定義しているファイルは存在しない')  # type: ignore
def given_0e535b1f(context):
    """その同一ステップを実際に定義しているファイルは存在しない

    Scenarios:
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: その同一ステップを実際に定義しているファイルは存在しない')
```

#### When scaffold コマンドをデフォルトオプションで実行する

```python
@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    """scaffold コマンドをデフォルトオプションで実行する

    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 差分なし時のスキップ
      - Git 未コミット変更の確認プロンプト
      - 差分マージ時の Duplicate スタブのコメント化
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: scaffold コマンドをデフォルトオプションで実行する')
```

#### Then そのステップが Duplicate としてではなくスタブとして生成されること

```python
@then('そのステップが Duplicate としてではなくスタブとして生成されること')  # type: ignore
def then_35ff3425(context):
    """そのステップが Duplicate としてではなくスタブとして生成されること

    Scenarios:
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: そのステップが Duplicate としてではなくスタブとして生成されること')
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: ac749f5b22acae3a56e7afe46f7303fcc05eeb9fe7aa5007ce208559648dc4e4
# spec-weaver-fingerprint-AUT-001: FnmTOZIIA7Vf35CV-yoWSn5nUOY43-qpxJP98jDBnew=
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