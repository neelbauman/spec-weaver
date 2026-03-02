# Feature: 仕様アイテムと実装ファイルのリンク管理

**タグ**: `@SPEC-017` `@SPEC-018` `@SPEC-019` `@SPEC-020`

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
## Scenario: impl_files にリスト形式でファイルパスを記述できる

**タグ**: `@SPEC-017`

- **Given** SPEC-018 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている
- **When** impl_files を読み取る
- **Then** ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-018 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている

```python
@given(u'SPEC-018 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている')
def step_impl(context):
    pass
```

#### When impl_files を読み取る

```python
@when(u'impl_files を読み取る')
def step_impl(context):
    pass
```

#### Then ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

```python
@then(u'ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: impl_files が未設定の場合はリンクなしとして扱われる

**タグ**: `@SPEC-017`

- **Given** SPEC-019 の impl_files が未設定である
- **When** impl_files を読み取る
- **Then** 空のリストが返ること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-019 の impl_files が未設定である

```python
@given(u'SPEC-019 の impl_files が未設定である')
def step_impl(context):
    pass
```

#### When impl_files を読み取る

```python
@when(u'impl_files を読み取る')
def step_impl(context):
    pass
```

#### Then 空のリストが返ること

```python
@then(u'空のリストが返ること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: アノテーションのスキャンで仕様IDとファイルの対応を抽出できる

**タグ**: `@SPEC-018`

- **Given** "src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている
- **When** impl-scanner でリポジトリをスキャンする
- **Then** "SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている

```python
@given(u'"src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている')
def step_impl(context):
    pass
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when(u'impl-scanner でリポジトリをスキャンする')
def step_impl(context):
    pass
```

#### Then "SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

```python
@then(u'"SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと')
def step_impl(context):
    pass
```

</details>


---
## Scenario: 1行に複数の仕様IDを記述できる

**タグ**: `@SPEC-018`

- **Given** "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-019, SPEC-020" が記述されている
- **When** impl-scanner でリポジトリをスキャンする
- **Then** "SPEC-019" に対して "src/spec_weaver/cli.py" が紐づくこと
- **And** "SPEC-020" に対して "src/spec_weaver/cli.py" が紐づくこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-019, SPEC-020" が記述されている

```python
@given(u'"src/spec_weaver/cli.py" の行頭に "# implements: SPEC-019, SPEC-020" が記述されている')
def step_impl(context):
    pass
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when(u'impl-scanner でリポジトリをスキャンする')
def step_impl(context):
    pass
```

#### Then "SPEC-019" に対して "src/spec_weaver/cli.py" が紐づくこと

```python
@then(u'"SPEC-019" に対して "src/spec_weaver/cli.py" が紐づくこと')
def step_impl(context):
    pass
```

#### And "SPEC-020" に対して "src/spec_weaver/cli.py" が紐づくこと

```python
@then(u'"SPEC-020" に対して "src/spec_weaver/cli.py" が紐づくこと')
def step_impl(context):
    pass
```

</details>


---
## Scenario: --extensions オプションでスキャン対象を絞れる

**タグ**: `@SPEC-018`

- **Given** リポジトリに .py ファイルと .md ファイルが存在する
- **And** .md ファイルの行頭に "# implements: SPEC-018" が記述されている
- **When** --extensions py を指定して impl-scanner でスキャンする
- **Then** .md ファイルは結果に含まれないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given リポジトリに .py ファイルと .md ファイルが存在する

```python
@given(u'リポジトリに .py ファイルと .md ファイルが存在する')
def step_impl(context):
    pass
```

#### And .md ファイルの行頭に "# implements: SPEC-018" が記述されている

```python
@given(u'.md ファイルの行頭に "# implements: SPEC-018" が記述されている')
def step_impl(context):
    pass
```

#### When --extensions py を指定して impl-scanner でスキャンする

```python
@when(u'--extensions py を指定して impl-scanner でスキャンする')
def step_impl(context):
    pass
```

#### Then .md ファイルは結果に含まれないこと

```python
@then(u'.md ファイルは結果に含まれないこと')
def step_impl(context):
    pass
```

</details>


---
## Scenario: アノテーションがないファイルはエラーにならない

**タグ**: `@SPEC-018`

- **Given** "src/spec_weaver/gherkin.py" にアノテーションが存在しない
- **When** impl-scanner でリポジトリをスキャンする
- **Then** エラーが発生しないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/gherkin.py" にアノテーションが存在しない

```python
@given(u'"src/spec_weaver/gherkin.py" にアノテーションが存在しない')
def step_impl(context):
    pass
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when(u'impl-scanner でリポジトリをスキャンする')
def step_impl(context):
    pass
```

#### Then エラーが発生しないこと

```python
@then(u'エラーが発生しないこと')
def step_impl(context):
    pass
```

</details>


---
## Scenario: --check-impl オプションで存在しないファイルへの impl_files を検出する

**タグ**: `@SPEC-019`

- **Given** SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** 終了コードが 1 であること
- **And** "nonexistent.py" が存在しないファイルとして報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

```python
@given(u'SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている')
def step_impl(context):
    pass
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when(u'"spec-weaver audit --check-impl" を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('audit --check-impl')
    res = run_spec_weaver(args, cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コードが 1 であること

```python
@then(u'終了コードが 1 であること')
def step_impl(context):
    pass
```

#### And "nonexistent.py" が存在しないファイルとして報告されること

```python
@then(u'"nonexistent.py" が存在しないファイルとして報告されること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: impl_files にあってアノテーションがない場合は警告を報告する

**タグ**: `@SPEC-019`

- **Given** SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている
- **And** "src/spec_weaver/cli.py" に SPEC-018 のアノテーションが存在しない
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** "SPEC-018 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている

```python
@given(u'SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている')
def step_impl(context):
    pass
```

#### And "src/spec_weaver/cli.py" に SPEC-018 のアノテーションが存在しない

```python
@given(u'"src/spec_weaver/cli.py" に SPEC-018 のアノテーションが存在しない')
def step_impl(context):
    pass
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when(u'"spec-weaver audit --check-impl" を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('audit --check-impl')
    res = run_spec_weaver(args, cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then "SPEC-018 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

```python
@then(u'"SPEC-018 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: アノテーションがあって impl_files がない場合は警告を報告する

**タグ**: `@SPEC-019`

- **Given** "src/spec_weaver/gherkin.py" の行頭に "# implements: SPEC-019" が記述されている
- **And** SPEC-019 の impl_files が未設定である
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** "SPEC-019 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/gherkin.py" の行頭に "# implements: SPEC-019" が記述されている

```python
@given(u'"src/spec_weaver/gherkin.py" の行頭に "# implements: SPEC-019" が記述されている')
def step_impl(context):
    pass
```

#### And SPEC-019 の impl_files が未設定である

```python
@given(u'SPEC-019 の impl_files が未設定である')
def step_impl(context):
    pass
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when(u'"spec-weaver audit --check-impl" を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('audit --check-impl')
    res = run_spec_weaver(args, cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then "SPEC-019 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

```python
@then(u'"SPEC-019 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: --check-impl なしでは実装リンク検証は実行されない

**タグ**: `@SPEC-019`

- **Given** SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
- **When** 通常の "spec-weaver audit" を実行する（--check-impl なし）
- **Then** 実装ファイルリンクのセクションが出力されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

```python
@given(u'SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている')
def step_impl(context):
    pass
```

#### When 通常の "spec-weaver audit" を実行する（--check-impl なし）

```python
@when(u'通常の "spec-weaver audit" を実行する（--check-impl なし）')
def step_impl(context):
    import shlex
    args = shlex.split('audit')
    res = run_spec_weaver(args, cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 実装ファイルリンクのセクションが出力されないこと

```python
@then(u'実装ファイルリンクのセクションが出力されないこと')
def step_impl(context):
    pass
```

</details>


---
## Scenario: --show-impl オプションで trace ツリーに実装ファイルを表示する

**タグ**: `@SPEC-020`

- **Given** SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
- **When** "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する
- **Then** 出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている

```python
@given(u'SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている')
def step_impl(context):
    pass
```

#### When "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する

```python
@when(u'"spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace SPEC-018 -f ./specification/features --show-impl')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

```python
@then(u'出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: アノテーション由来のファイルも trace ツリーに表示される

**タグ**: `@SPEC-020`

- **Given** "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-018" が記述されている
- **And** SPEC-018 の impl_files が未設定である
- **When** "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する
- **Then** 出力ツリーに "src/spec_weaver/cli.py" が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-018" が記述されている

```python
@given(u'"src/spec_weaver/cli.py" の行頭に "# implements: SPEC-018" が記述されている')
def step_impl(context):
    pass
```

#### And SPEC-018 の impl_files が未設定である

```python
@given(u'SPEC-018 の impl_files が未設定である')
def step_impl(context):
    pass
```

#### When "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する

```python
@when(u'"spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace SPEC-018 -f ./specification/features --show-impl')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 出力ツリーに "src/spec_weaver/cli.py" が含まれること

```python
@then(u'出力ツリーに "src/spec_weaver/cli.py" が含まれること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: --show-impl なしでは実装ファイルは表示されない

**タグ**: `@SPEC-020`

- **Given** SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
- **When** "spec-weaver trace SPEC-018 -f ./specification/features" を実行する（--show-impl なし）
- **Then** 出力ツリーに "impl_scanner.py" が含まれないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている

```python
@given(u'SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている')
def step_impl(context):
    pass
```

#### When "spec-weaver trace SPEC-018 -f ./specification/features" を実行する（--show-impl なし）

```python
@when(u'"spec-weaver trace SPEC-018 -f ./specification/features" を実行する（--show-impl なし）')
def step_impl(context):
    import shlex
    args = shlex.split('trace SPEC-018 -f ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 出力ツリーに "impl_scanner.py" が含まれないこと

```python
@then(u'出力ツリーに "impl_scanner.py" が含まれないこと')
def step_impl(context):
    pass
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: cf89b3e4e58d61268dc81d76d9f7769fc56d5d3ed31d5221ccd2cfe07947fdb3
@SPEC-017 @SPEC-018 @SPEC-019 @SPEC-020
Feature: 仕様アイテムと実装ファイルのリンク管理
  DoorstopのYAML impl_files カスタム属性とコードアノテーションを組み合わせて、
  仕様と実装ファイルの双方向トレーサビリティを実現する。

  Background:
    Given Doorstopツリーが初期化されている
    And 以下のSPECアイテムが存在する:
      | ID       | Header             | impl_files                       |
      | SPEC-018 | アノテーションスキャン | src/spec_weaver/impl_scanner.py |
      | SPEC-019 | audit拡張          |                                  |

  # ---- SPEC-017: impl_files カスタム属性 ----

  @SPEC-017
  Scenario: impl_files にリスト形式でファイルパスを記述できる
    Given SPEC-018 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている
    When impl_files を読み取る
    Then ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

  @SPEC-017
  Scenario: impl_files が未設定の場合はリンクなしとして扱われる
    Given SPEC-019 の impl_files が未設定である
    When impl_files を読み取る
    Then 空のリストが返ること

  # ---- SPEC-018: アノテーションスキャン ----

  @SPEC-018
  Scenario: アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
    Given "src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている
    When impl-scanner でリポジトリをスキャンする
    Then "SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

  @SPEC-018
  Scenario: 1行に複数の仕様IDを記述できる
    Given "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-019, SPEC-020" が記述されている
    When impl-scanner でリポジトリをスキャンする
    Then "SPEC-019" に対して "src/spec_weaver/cli.py" が紐づくこと
    And  "SPEC-020" に対して "src/spec_weaver/cli.py" が紐づくこと

  @SPEC-018
  Scenario: --extensions オプションでスキャン対象を絞れる
    Given リポジトリに .py ファイルと .md ファイルが存在する
    And .md ファイルの行頭に "# implements: SPEC-018" が記述されている
    When --extensions py を指定して impl-scanner でスキャンする
    Then .md ファイルは結果に含まれないこと

  @SPEC-018
  Scenario: アノテーションがないファイルはエラーにならない
    Given "src/spec_weaver/gherkin.py" にアノテーションが存在しない
    When impl-scanner でリポジトリをスキャンする
    Then エラーが発生しないこと

  # ---- SPEC-019: audit 拡張 ----

  @SPEC-019
  Scenario: --check-impl オプションで存在しないファイルへの impl_files を検出する
    Given SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
    When "spec-weaver audit --check-impl" を実行する
    Then 終了コードが 1 であること
    And  "nonexistent.py" が存在しないファイルとして報告されること

  @SPEC-019
  Scenario: impl_files にあってアノテーションがない場合は警告を報告する
    Given SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている
    And "src/spec_weaver/cli.py" に SPEC-018 のアノテーションが存在しない
    When "spec-weaver audit --check-impl" を実行する
    Then "SPEC-018 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

  @SPEC-019
  Scenario: アノテーションがあって impl_files がない場合は警告を報告する
    Given "src/spec_weaver/gherkin.py" の行頭に "# implements: SPEC-019" が記述されている
    And SPEC-019 の impl_files が未設定である
    When "spec-weaver audit --check-impl" を実行する
    Then "SPEC-019 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

  @SPEC-019
  Scenario: --check-impl なしでは実装リンク検証は実行されない
    Given SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
    When 通常の "spec-weaver audit" を実行する（--check-impl なし）
    Then 実装ファイルリンクのセクションが出力されないこと

  # ---- SPEC-020: trace 拡張 ----

  @SPEC-020
  Scenario: --show-impl オプションで trace ツリーに実装ファイルを表示する
    Given SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
    When "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する
    Then 出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

  @SPEC-020
  Scenario: アノテーション由来のファイルも trace ツリーに表示される
    Given "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-018" が記述されている
    And SPEC-018 の impl_files が未設定である
    When "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する
    Then 出力ツリーに "src/spec_weaver/cli.py" が含まれること

  @SPEC-020
  Scenario: --show-impl なしでは実装ファイルは表示されない
    Given SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
    When "spec-weaver trace SPEC-018 -f ./specification/features" を実行する（--show-impl なし）
    Then 出力ツリーに "impl_scanner.py" が含まれないこと

```
</details>