# Feature: 仕様アイテムと実装ファイルのリンク管理

**タグ**: `@TRC-002` `@TRC-003` `@QA-003` `@TRC-004`

**関連アイテム**: [QA-003](../items/QA-003.md) / [TRC-002](../items/TRC-002.md) / [TRC-003](../items/TRC-003.md) / [TRC-004](../items/TRC-004.md)

DoorstopのYAML impl_files カスタム属性とコードアノテーションを組み合わせて、
  仕様と実装ファイルの双方向トレーサビリティを実現する。

---
## Background

- **Given** Doorstopツリーが初期化されている
- **And** 以下のSPECアイテムが存在する:

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopツリーが初期化されている

```python
@given('Doorstopツリーが初期化されている')  # type: ignore
def given_6df87eb3(context):
    """Doorstopツリーが初期化されている

    Scenarios:
      - 
    """
    pass
```

#### And 以下のSPECアイテムが存在する:

```python
@given('以下のSPECアイテムが存在する:')  # type: ignore
def given_14c0b615(context):
    """以下のSPECアイテムが存在する:

    Scenarios:
      - 
    """
    pass
```

</details>


---
## Scenario: impl_files にリスト形式でファイルパスを記述できる {: #line-21 }

**タグ**: `@TRC-002`

- **Given** TRC-003 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている
- **When** impl_files を読み取る
- **Then** ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

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
  File "specification/features/steps/step_impl_link.py", line 17, in given_5b35c4dd
    raise NotImplementedError('STEP: TRC-003 の impl_files に ["{param0}"] が設定されている')
NotImplementedError: STEP: TRC-003 の impl_files に ["{param0}"] が設定されている
```

#### Given TRC-003 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている

```python
@given('TRC-003 の impl_files に ["{param0}"] が設定されている')  # type: ignore
def given_5b35c4dd(context, param0):
    """TRC-003 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている

    Scenarios:
      - impl_files にリスト形式でファイルパスを記述できる
    """
    raise NotImplementedError('STEP: TRC-003 の impl_files に ["{param0}"] が設定されている')
```

#### When impl_files を読み取る

```python
@when('impl_files を読み取る')  # type: ignore
def when_1e9b41a9(context):
    """impl_files を読み取る

    Scenarios:
      - impl_files にリスト形式でファイルパスを記述できる
      - impl_files が未設定の場合はリンクなしとして扱われる
    """
    raise NotImplementedError('STEP: impl_files を読み取る')
```

#### Then ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

```python
@then('ファイルパスのリスト ["{param0}"] が得られること')  # type: ignore
def then_4c08825b(context, param0):
    """ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

    Scenarios:
      - impl_files にリスト形式でファイルパスを記述できる
    """
    raise NotImplementedError('STEP: ファイルパスのリスト ["{param0}"] が得られること')
```

</details>


---
## Scenario: impl_files が未設定の場合はリンクなしとして扱われる {: #line-27 }

**タグ**: `@TRC-002`

- **Given** QA-003 の impl_files が未設定である
- **When** impl_files を読み取る
- **Then** 空のリストが返ること

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
  File "specification/features/steps/step_impl_link.py", line 49, in given_60f3699e
    raise NotImplementedError('STEP: QA-003 の impl_files が未設定である')
NotImplementedError: STEP: QA-003 の impl_files が未設定である
```

#### Given QA-003 の impl_files が未設定である

```python
@given('QA-003 の impl_files が未設定である')  # type: ignore
def given_60f3699e(context):
    """QA-003 の impl_files が未設定である

    Scenarios:
      - impl_files が未設定の場合はリンクなしとして扱われる
      - アノテーションがあって impl_files がない場合は警告を報告する
    """
    raise NotImplementedError('STEP: QA-003 の impl_files が未設定である')
```

#### When impl_files を読み取る

```python
@when('impl_files を読み取る')  # type: ignore
def when_1e9b41a9(context):
    """impl_files を読み取る

    Scenarios:
      - impl_files にリスト形式でファイルパスを記述できる
      - impl_files が未設定の場合はリンクなしとして扱われる
    """
    raise NotImplementedError('STEP: impl_files を読み取る')
```

#### Then 空のリストが返ること

```python
@then('空のリストが返ること')  # type: ignore
def then_3cd52b0f(context):
    """空のリストが返ること

    Scenarios:
      - impl_files が未設定の場合はリンクなしとして扱われる
    """
    raise NotImplementedError('STEP: 空のリストが返ること')
```

</details>


---
## Scenario: アノテーションのスキャンで仕様IDとファイルの対応を抽出できる {: #line-35 }

**タグ**: `@TRC-003`

- **Given** "src/spec_weaver/impl_scanner.py" の行頭に "# implements: TRC-003" が記述されている
- **When** impl-scanner でリポジトリをスキャンする
- **Then** "TRC-003" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

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
  File "specification/features/steps/step_impl_link.py", line 72, in given_1a5b95f0
    raise NotImplementedError('STEP: "{param0}" の行頭に "{param1}" が記述されている')
NotImplementedError: STEP: "{param0}" の行頭に "{param1}" が記述されている
```

#### Given "src/spec_weaver/impl_scanner.py" の行頭に "# implements: TRC-003" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    """"src/spec_weaver/impl_scanner.py" の行頭に "# implements: TRC-003" が記述されている

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがあって impl_files がない場合は警告を報告する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: "{param0}" の行頭に "{param1}" が記述されている')
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when('impl-scanner でリポジトリをスキャンする')  # type: ignore
def when_59b7b6ae(context):
    """impl-scanner でリポジトリをスキャンする

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがないファイルはエラーにならない
    """
    raise NotImplementedError('STEP: impl-scanner でリポジトリをスキャンする')
```

#### Then "TRC-003" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

```python
@then('"{param0}" に対して "{param1}" が紐づくこと')  # type: ignore
def then_6cd9ae6b(context, param0, param1):
    """"TRC-003" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
    """
    raise NotImplementedError('STEP: "{param0}" に対して "{param1}" が紐づくこと')
```

</details>


---
## Scenario: 1行に複数の仕様IDを記述できる {: #line-41 }

**タグ**: `@TRC-003`

- **Given** "src/spec_weaver/cli.py" の行頭に "# implements: QA-003, TRC-004" が記述されている
- **When** impl-scanner でリポジトリをスキャンする
- **Then** "QA-003" に対して "src/spec_weaver/cli.py" が紐づくこと
- **And** "TRC-004" に対して "src/spec_weaver/cli.py" が紐づくこと

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
  File "specification/features/steps/step_impl_link.py", line 72, in given_1a5b95f0
    raise NotImplementedError('STEP: "{param0}" の行頭に "{param1}" が記述されている')
NotImplementedError: STEP: "{param0}" の行頭に "{param1}" が記述されている
```

#### Given "src/spec_weaver/cli.py" の行頭に "# implements: QA-003, TRC-004" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    """"src/spec_weaver/impl_scanner.py" の行頭に "# implements: TRC-003" が記述されている

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがあって impl_files がない場合は警告を報告する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: "{param0}" の行頭に "{param1}" が記述されている')
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when('impl-scanner でリポジトリをスキャンする')  # type: ignore
def when_59b7b6ae(context):
    """impl-scanner でリポジトリをスキャンする

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがないファイルはエラーにならない
    """
    raise NotImplementedError('STEP: impl-scanner でリポジトリをスキャンする')
```

#### Then "QA-003" に対して "src/spec_weaver/cli.py" が紐づくこと

```python
@then('"{param0}" に対して "{param1}" が紐づくこと')  # type: ignore
def then_6cd9ae6b(context, param0, param1):
    """"TRC-003" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
    """
    raise NotImplementedError('STEP: "{param0}" に対して "{param1}" が紐づくこと')
```

#### And "TRC-004" に対して "src/spec_weaver/cli.py" が紐づくこと

```python
@then('"{param0}" に対して "{param1}" が紐づくこと')  # type: ignore
def then_6cd9ae6b(context, param0, param1):
    """"TRC-003" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
    """
    raise NotImplementedError('STEP: "{param0}" に対して "{param1}" が紐づくこと')
```

</details>


---
## Scenario: --extensions オプションでスキャン対象を絞れる {: #line-48 }

**タグ**: `@TRC-003`

- **Given** リポジトリに .py ファイルと .md ファイルが存在する
- **And** .md ファイルの行頭に "# implements: TRC-003" が記述されている
- **When** --extensions py を指定して impl-scanner でスキャンする
- **Then** .md ファイルは結果に含まれないこと

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
  File "specification/features/steps/step_impl_link.py", line 105, in given_6f18a295
    raise NotImplementedError('STEP: リポジトリに .py ファイルと .md ファイルが存在する')
NotImplementedError: STEP: リポジトリに .py ファイルと .md ファイルが存在する
```

#### Given リポジトリに .py ファイルと .md ファイルが存在する

```python
@given('リポジトリに .py ファイルと .md ファイルが存在する')  # type: ignore
def given_6f18a295(context):
    """リポジトリに .py ファイルと .md ファイルが存在する

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    raise NotImplementedError('STEP: リポジトリに .py ファイルと .md ファイルが存在する')
```

#### And .md ファイルの行頭に "# implements: TRC-003" が記述されている

```python
@given('.md ファイルの行頭に "{param0}" が記述されている')  # type: ignore
def given_d9c1b21a(context, param0):
    """.md ファイルの行頭に "# implements: TRC-003" が記述されている

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    raise NotImplementedError('STEP: .md ファイルの行頭に "{param0}" が記述されている')
```

#### When --extensions py を指定して impl-scanner でスキャンする

```python
@when('--extensions py を指定して impl-scanner でスキャンする')  # type: ignore
def when_d61ff5a2(context):
    """--extensions py を指定して impl-scanner でスキャンする

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    raise NotImplementedError('STEP: --extensions py を指定して impl-scanner でスキャンする')
```

#### Then .md ファイルは結果に含まれないこと

```python
@then('.md ファイルは結果に含まれないこと')  # type: ignore
def then_1e4aee33(context):
    """.md ファイルは結果に含まれないこと

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    raise NotImplementedError('STEP: .md ファイルは結果に含まれないこと')
```

</details>


---
## Scenario: アノテーションがないファイルはエラーにならない {: #line-55 }

**タグ**: `@TRC-003`

- **Given** "src/spec_weaver/gherkin.py" にアノテーションが存在しない
- **When** impl-scanner でリポジトリをスキャンする
- **Then** エラーが発生しないこと

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
  File "specification/features/steps/step_impl_link.py", line 145, in given_8d04b283
    raise NotImplementedError('STEP: "{param0}" にアノテーションが存在しない')
NotImplementedError: STEP: "{param0}" にアノテーションが存在しない
```

#### Given "src/spec_weaver/gherkin.py" にアノテーションが存在しない

```python
@given('"{param0}" にアノテーションが存在しない')  # type: ignore
def given_8d04b283(context, param0):
    """"src/spec_weaver/gherkin.py" にアノテーションが存在しない

    Scenarios:
      - アノテーションがないファイルはエラーにならない
    """
    raise NotImplementedError('STEP: "{param0}" にアノテーションが存在しない')
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when('impl-scanner でリポジトリをスキャンする')  # type: ignore
def when_59b7b6ae(context):
    """impl-scanner でリポジトリをスキャンする

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがないファイルはエラーにならない
    """
    raise NotImplementedError('STEP: impl-scanner でリポジトリをスキャンする')
```

#### Then エラーが発生しないこと

```python
@then('エラーが発生しないこと')  # type: ignore
def then_b705ab9f(context):
    """エラーが発生しないこと

    Scenarios:
      - アノテーションがないファイルはエラーにならない
    """
    raise NotImplementedError('STEP: エラーが発生しないこと')
```

</details>


---
## Scenario: --check-impl オプションで存在しないファイルへの impl_files を検出する {: #line-63 }

**タグ**: `@QA-003`

- **Given** QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** 終了コードが 1 であること
- **And** "nonexistent.py" が存在しないファイルとして報告されること

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
  File "specification/features/steps/step_impl_link.py", line 166, in given_4cea3b9d
    raise NotImplementedError('STEP: QA-003 の impl_files に "{param0}" が設定されている')
NotImplementedError: STEP: QA-003 の impl_files に "{param0}" が設定されている
```

#### Given QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

```python
@given('QA-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_4cea3b9d(context, param0):
    """QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - --check-impl なしでは実装リンク検証は実行されない
    """
    raise NotImplementedError('STEP: QA-003 の impl_files に "{param0}" が設定されている')
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    """"spec-weaver audit --check-impl" を実行する

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - impl_files にあってアノテーションがない場合は警告を報告する
      - アノテーションがあって impl_files がない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: "{param0}" を実行する')
```

#### Then 終了コードが 1 であること

```python
@then('終了コードが 1 であること')  # type: ignore
def then_3783b41c(context):
    """終了コードが 1 であること

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
    """
    raise NotImplementedError('STEP: 終了コードが 1 であること')
```

#### And "nonexistent.py" が存在しないファイルとして報告されること

```python
@then('"{param0}" が存在しないファイルとして報告されること')  # type: ignore
def then_7ef614ad(context, param0):
    """"nonexistent.py" が存在しないファイルとして報告されること

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
    """
    raise NotImplementedError('STEP: "{param0}" が存在しないファイルとして報告されること')
```

</details>


---
## Scenario: impl_files にあってアノテーションがない場合は警告を報告する {: #line-70 }

**タグ**: `@QA-003`

- **Given** TRC-003 の impl_files に "src/spec_weaver/cli.py" が設定されている
- **And** "src/spec_weaver/cli.py" に TRC-003 のアノテーションが存在しない
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** "TRC-003 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

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
  File "specification/features/steps/step_impl_link.py", line 212, in given_e64bd8f6
    raise NotImplementedError('STEP: TRC-003 の impl_files に "{param0}" が設定されている')
NotImplementedError: STEP: TRC-003 の impl_files に "{param0}" が設定されている
```

#### Given TRC-003 の impl_files に "src/spec_weaver/cli.py" が設定されている

```python
@given('TRC-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    """TRC-003 の impl_files に "src/spec_weaver/cli.py" が設定されている

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - --show-impl なしでは実装ファイルは表示されない
    """
    raise NotImplementedError('STEP: TRC-003 の impl_files に "{param0}" が設定されている')
```

#### And "src/spec_weaver/cli.py" に TRC-003 のアノテーションが存在しない

```python
@given('"{param0}" に TRC-003 のアノテーションが存在しない')  # type: ignore
def given_d0ba98a0(context, param0):
    """"src/spec_weaver/cli.py" に TRC-003 のアノテーションが存在しない

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
    """
    raise NotImplementedError('STEP: "{param0}" に TRC-003 のアノテーションが存在しない')
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    """"spec-weaver audit --check-impl" を実行する

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - impl_files にあってアノテーションがない場合は警告を報告する
      - アノテーションがあって impl_files がない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: "{param0}" を実行する')
```

#### Then "TRC-003 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

```python
@then('"{param0}" が impl_files のみ（アノテーションなし）として報告されること')  # type: ignore
def then_f76e2a8d(context, param0):
    """"TRC-003 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
    """
    raise NotImplementedError('STEP: "{param0}" が impl_files のみ（アノテーションなし）として報告されること')
```

</details>


---
## Scenario: アノテーションがあって impl_files がない場合は警告を報告する {: #line-77 }

**タグ**: `@QA-003`

- **Given** "src/spec_weaver/gherkin.py" の行頭に "# implements: QA-003" が記述されている
- **And** QA-003 の impl_files が未設定である
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** "QA-003 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

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
  File "specification/features/steps/step_impl_link.py", line 72, in given_1a5b95f0
    raise NotImplementedError('STEP: "{param0}" の行頭に "{param1}" が記述されている')
NotImplementedError: STEP: "{param0}" の行頭に "{param1}" が記述されている
```

#### Given "src/spec_weaver/gherkin.py" の行頭に "# implements: QA-003" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    """"src/spec_weaver/impl_scanner.py" の行頭に "# implements: TRC-003" が記述されている

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがあって impl_files がない場合は警告を報告する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: "{param0}" の行頭に "{param1}" が記述されている')
```

#### And QA-003 の impl_files が未設定である

```python
@given('QA-003 の impl_files が未設定である')  # type: ignore
def given_60f3699e(context):
    """QA-003 の impl_files が未設定である

    Scenarios:
      - impl_files が未設定の場合はリンクなしとして扱われる
      - アノテーションがあって impl_files がない場合は警告を報告する
    """
    raise NotImplementedError('STEP: QA-003 の impl_files が未設定である')
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    """"spec-weaver audit --check-impl" を実行する

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - impl_files にあってアノテーションがない場合は警告を報告する
      - アノテーションがあって impl_files がない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: "{param0}" を実行する')
```

#### Then "QA-003 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

```python
@then('"{param0}" がアノテーションのみ（impl_files なし）として報告されること')  # type: ignore
def then_7fa51a4f(context, param0):
    """"QA-003 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

    Scenarios:
      - アノテーションがあって impl_files がない場合は警告を報告する
    """
    raise NotImplementedError('STEP: "{param0}" がアノテーションのみ（impl_files なし）として報告されること')
```

</details>


---
## Scenario: --check-impl なしでは実装リンク検証は実行されない {: #line-84 }

**タグ**: `@QA-003`

- **Given** QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
- **When** 通常の "spec-weaver audit" を実行する（--check-impl なし）
- **Then** 実装ファイルリンクのセクションが出力されないこと

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
  File "specification/features/steps/step_impl_link.py", line 166, in given_4cea3b9d
    raise NotImplementedError('STEP: QA-003 の impl_files に "{param0}" が設定されている')
NotImplementedError: STEP: QA-003 の impl_files に "{param0}" が設定されている
```

#### Given QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

```python
@given('QA-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_4cea3b9d(context, param0):
    """QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - --check-impl なしでは実装リンク検証は実行されない
    """
    raise NotImplementedError('STEP: QA-003 の impl_files に "{param0}" が設定されている')
```

#### When 通常の "spec-weaver audit" を実行する（--check-impl なし）

```python
@when('通常の "{param0}" を実行する（--check-impl なし）')  # type: ignore
def when_6a6c02d8(context, param0):
    """通常の "spec-weaver audit" を実行する（--check-impl なし）

    Scenarios:
      - --check-impl なしでは実装リンク検証は実行されない
    """
    raise NotImplementedError('STEP: 通常の "{param0}" を実行する（--check-impl なし）')
```

#### Then 実装ファイルリンクのセクションが出力されないこと

```python
@then('実装ファイルリンクのセクションが出力されないこと')  # type: ignore
def then_70e4e0dc(context):
    """実装ファイルリンクのセクションが出力されないこと

    Scenarios:
      - --check-impl なしでは実装リンク検証は実行されない
    """
    raise NotImplementedError('STEP: 実装ファイルリンクのセクションが出力されないこと')
```

</details>


---
## Scenario: --show-impl オプションで trace ツリーに実装ファイルを表示する {: #line-92 }

**タグ**: `@TRC-004`

- **Given** TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
- **When** "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
- **Then** 出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

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
  File "specification/features/steps/step_impl_link.py", line 212, in given_e64bd8f6
    raise NotImplementedError('STEP: TRC-003 の impl_files に "{param0}" が設定されている')
NotImplementedError: STEP: TRC-003 の impl_files に "{param0}" が設定されている
```

#### Given TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている

```python
@given('TRC-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    """TRC-003 の impl_files に "src/spec_weaver/cli.py" が設定されている

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - --show-impl なしでは実装ファイルは表示されない
    """
    raise NotImplementedError('STEP: TRC-003 の impl_files に "{param0}" が設定されている')
```

#### When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    """"spec-weaver audit --check-impl" を実行する

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - impl_files にあってアノテーションがない場合は警告を報告する
      - アノテーションがあって impl_files がない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: "{param0}" を実行する')
```

#### Then 出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

```python
@then('出力ツリーに "{param0}" が含まれること')  # type: ignore
def then_2c56e82a(context, param0):
    """出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

    Scenarios:
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: 出力ツリーに "{param0}" が含まれること')
```

</details>


---
## Scenario: アノテーション由来のファイルも trace ツリーに表示される {: #line-98 }

**タグ**: `@TRC-004`

- **Given** "src/spec_weaver/cli.py" の行頭に "# implements: TRC-003" が記述されている
- **And** TRC-003 の impl_files が未設定である
- **When** "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
- **Then** 出力ツリーに "src/spec_weaver/cli.py" が含まれること

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
  File "specification/features/steps/step_impl_link.py", line 72, in given_1a5b95f0
    raise NotImplementedError('STEP: "{param0}" の行頭に "{param1}" が記述されている')
NotImplementedError: STEP: "{param0}" の行頭に "{param1}" が記述されている
```

#### Given "src/spec_weaver/cli.py" の行頭に "# implements: TRC-003" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    """"src/spec_weaver/impl_scanner.py" の行頭に "# implements: TRC-003" が記述されている

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがあって impl_files がない場合は警告を報告する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: "{param0}" の行頭に "{param1}" が記述されている')
```

#### And TRC-003 の impl_files が未設定である

```python
@given('TRC-003 の impl_files が未設定である')  # type: ignore
def given_c11ed496(context):
    """TRC-003 の impl_files が未設定である

    Scenarios:
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: TRC-003 の impl_files が未設定である')
```

#### When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    """"spec-weaver audit --check-impl" を実行する

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - impl_files にあってアノテーションがない場合は警告を報告する
      - アノテーションがあって impl_files がない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: "{param0}" を実行する')
```

#### Then 出力ツリーに "src/spec_weaver/cli.py" が含まれること

```python
@then('出力ツリーに "{param0}" が含まれること')  # type: ignore
def then_2c56e82a(context, param0):
    """出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

    Scenarios:
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    raise NotImplementedError('STEP: 出力ツリーに "{param0}" が含まれること')
```

</details>


---
## Scenario: --show-impl なしでは実装ファイルは表示されない {: #line-105 }

**タグ**: `@TRC-004`

- **Given** TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
- **When** "spec-weaver trace TRC-003 -f ./specification/features" を実行する（--show-impl なし）
- **Then** 出力ツリーに "impl_scanner.py" が含まれないこと

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
  File "specification/features/steps/step_impl_link.py", line 212, in given_e64bd8f6
    raise NotImplementedError('STEP: TRC-003 の impl_files に "{param0}" が設定されている')
NotImplementedError: STEP: TRC-003 の impl_files に "{param0}" が設定されている
```

#### Given TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている

```python
@given('TRC-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    """TRC-003 の impl_files に "src/spec_weaver/cli.py" が設定されている

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - --show-impl なしでは実装ファイルは表示されない
    """
    raise NotImplementedError('STEP: TRC-003 の impl_files に "{param0}" が設定されている')
```

#### When "spec-weaver trace TRC-003 -f ./specification/features" を実行する（--show-impl なし）

```python
@when('"{param0}" を実行する（--show-impl なし）')  # type: ignore
def when_dfb07a47(context, param0):
    """"spec-weaver trace TRC-003 -f ./specification/features" を実行する（--show-impl なし）

    Scenarios:
      - --show-impl なしでは実装ファイルは表示されない
    """
    raise NotImplementedError('STEP: "{param0}" を実行する（--show-impl なし）')
```

#### Then 出力ツリーに "impl_scanner.py" が含まれないこと

```python
@then('出力ツリーに "{param0}" が含まれないこと')  # type: ignore
def then_35df9926(context, param0):
    """出力ツリーに "impl_scanner.py" が含まれないこと

    Scenarios:
      - --show-impl なしでは実装ファイルは表示されない
    """
    raise NotImplementedError('STEP: 出力ツリーに "{param0}" が含まれないこと')
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: b811f33b65429d4bb62aa6ed1e234420882eb37e2a3270541e5030282efd3be7
# spec-weaver-fingerprint-QA-003: R7lU5c_GYfAMywWH7ga7C5bNWLi0BcEk_ct5FCCzLOg=
# spec-weaver-fingerprint-TRC-002: CsNYG2kwoAL2aGQ4OMJZPbq_BdQL1XO9mD52BES64WU=
# spec-weaver-fingerprint-TRC-003: HejBnkVVAXr50mezShqlLJuFqDQgnm2Ll2xq1IrX7wY=
# spec-weaver-fingerprint-TRC-004: taSaPJAOYmNABY3Fq9QzpfuL400jN9dj2MpQSufRkT8=
@TRC-002 @TRC-003 @QA-003 @TRC-004
Feature: 仕様アイテムと実装ファイルのリンク管理
  DoorstopのYAML impl_files カスタム属性とコードアノテーションを組み合わせて、
  仕様と実装ファイルの双方向トレーサビリティを実現する。

  Background:
    Given Doorstopツリーが初期化されている
    And 以下のSPECアイテムが存在する:
      | ID       | Header             | impl_files                       |
      | TRC-003 | アノテーションスキャン | src/spec_weaver/impl_scanner.py |
      | QA-003 | audit拡張          |                                  |

  # ---- TRC-002: impl_files カスタム属性 ----

  @TRC-002
  Scenario: impl_files にリスト形式でファイルパスを記述できる
    Given TRC-003 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている
    When impl_files を読み取る
    Then ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

  @TRC-002
  Scenario: impl_files が未設定の場合はリンクなしとして扱われる
    Given QA-003 の impl_files が未設定である
    When impl_files を読み取る
    Then 空のリストが返ること

  # ---- TRC-003: アノテーションスキャン ----

  @TRC-003
  Scenario: アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
    Given "src/spec_weaver/impl_scanner.py" の行頭に "# implements: TRC-003" が記述されている
    When impl-scanner でリポジトリをスキャンする
    Then "TRC-003" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

  @TRC-003
  Scenario: 1行に複数の仕様IDを記述できる
    Given "src/spec_weaver/cli.py" の行頭に "# implements: QA-003, TRC-004" が記述されている
    When impl-scanner でリポジトリをスキャンする
    Then "QA-003" に対して "src/spec_weaver/cli.py" が紐づくこと
    And  "TRC-004" に対して "src/spec_weaver/cli.py" が紐づくこと

  @TRC-003
  Scenario: --extensions オプションでスキャン対象を絞れる
    Given リポジトリに .py ファイルと .md ファイルが存在する
    And .md ファイルの行頭に "# implements: TRC-003" が記述されている
    When --extensions py を指定して impl-scanner でスキャンする
    Then .md ファイルは結果に含まれないこと

  @TRC-003
  Scenario: アノテーションがないファイルはエラーにならない
    Given "src/spec_weaver/gherkin.py" にアノテーションが存在しない
    When impl-scanner でリポジトリをスキャンする
    Then エラーが発生しないこと

  # ---- QA-003: audit 拡張 ----

  @QA-003
  Scenario: --check-impl オプションで存在しないファイルへの impl_files を検出する
    Given QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
    When "spec-weaver audit --check-impl" を実行する
    Then 終了コードが 1 であること
    And  "nonexistent.py" が存在しないファイルとして報告されること

  @QA-003
  Scenario: impl_files にあってアノテーションがない場合は警告を報告する
    Given TRC-003 の impl_files に "src/spec_weaver/cli.py" が設定されている
    And "src/spec_weaver/cli.py" に TRC-003 のアノテーションが存在しない
    When "spec-weaver audit --check-impl" を実行する
    Then "TRC-003 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

  @QA-003
  Scenario: アノテーションがあって impl_files がない場合は警告を報告する
    Given "src/spec_weaver/gherkin.py" の行頭に "# implements: QA-003" が記述されている
    And QA-003 の impl_files が未設定である
    When "spec-weaver audit --check-impl" を実行する
    Then "QA-003 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

  @QA-003
  Scenario: --check-impl なしでは実装リンク検証は実行されない
    Given QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
    When 通常の "spec-weaver audit" を実行する（--check-impl なし）
    Then 実装ファイルリンクのセクションが出力されないこと

  # ---- TRC-004: trace 拡張 ----

  @TRC-004
  Scenario: --show-impl オプションで trace ツリーに実装ファイルを表示する
    Given TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
    When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
    Then 出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

  @TRC-004
  Scenario: アノテーション由来のファイルも trace ツリーに表示される
    Given "src/spec_weaver/cli.py" の行頭に "# implements: TRC-003" が記述されている
    And TRC-003 の impl_files が未設定である
    When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
    Then 出力ツリーに "src/spec_weaver/cli.py" が含まれること

  @TRC-004
  Scenario: --show-impl なしでは実装ファイルは表示されない
    Given TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
    When "spec-weaver trace TRC-003 -f ./specification/features" を実行する（--show-impl なし）
    Then 出力ツリーに "impl_scanner.py" が含まれないこと

```
</details>