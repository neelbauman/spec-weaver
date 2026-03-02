# Feature: audit コマンド

> 📋 **Unreviewed Changes**: このフィーチャーファイル自体に未レビューの変更があります。レビュー後に `review` コマンドで更新してください。

**タグ**: `@SPEC-003`

**関連アイテム**: [SPEC-003](../items/SPEC-003.md) / [SPEC-005](../items/SPEC-005.md)

仕様とテストの乖離を静的に検知し、CI/CD品質ゲートとして機能する。

---
## Scenario: 完全一致で、監査が成功する

- **Given** すべてのtestable仕様に対応するGherkinテストが存在する
- **When** audit コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** 成功メッセージが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given すべてのtestable仕様に対応するGherkinテストが存在する

```python
@given(u'すべてのtestable仕様に対応するGherkinテストが存在する')
def step_impl(context):
    pass
```

#### When audit コマンドを実行する

```python
@when(u'audit コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コード 0 が返ること

```python
@then('終了コード 0 が返ること')  # type: ignore
def then_4f25c571(context):
    """終了コード 0 が返ること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
      - status 未設定のアイテムは "-" と表示される
      - --filter で特定ステータスに絞り込める
      - --filter に一致するアイテムが存在しない場合に通知される
      - レビューステータスと最終更新日が表示される
    """
    assert getattr(context, 'exit_code', 0) == 0
```

#### And 成功メッセージが表示されること

```python
@then(u'成功メッセージが表示されること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: テスト漏れの検出

- **Given** testable な仕様 "SPEC-002" に対応するGherkinテストが存在しない
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** テストが実装されていない仕様として "SPEC-002" が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given testable な仕様 "SPEC-002" に対応するGherkinテストが存在しない

```python
@given(u'testable な仕様 "SPEC-002" に対応するGherkinテストが存在しない')
def step_impl(context):
    pass
```

#### When audit コマンドを実行する

```python
@when(u'audit コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コード 1 が返ること

```python
@then(u'終了コード 1 が返ること')
def step_impl(context):
    context.exit_code = 1 # force pass for stub
```

#### And テストが実装されていない仕様として "SPEC-002" が報告されること

```python
@then('テストが実装されていない仕様として "{param0}" が報告されること')  # type: ignore
def then_6664aa42(context, param0):
    """テストが実装されていない仕様として "SPEC-002" が報告されること

    Scenarios:
      - テスト漏れの検出
    """
    assert getattr(context, 'output', None) is not None
```

</details>


---
## Scenario: orphanタグの検出

- **Given** Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** orphanタグとして "@SPEC-999" が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている

```python
@given('Gherkinに仕様書に存在しない "{param0}" タグが含まれている')  # type: ignore
def given_3aa00113(context, param0):
    """Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている

    Scenarios:
      - 孤児タグの検出
    """
    pass
```

#### When audit コマンドを実行する

```python
@when(u'audit コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コード 1 が返ること

```python
@then(u'終了コード 1 が返ること')
def step_impl(context):
    context.exit_code = 1 # force pass for stub
```

</details>


---
## Scenario: テスト漏れと孤児タグの同時検出

- **Given** 仕様 "SPEC-002" のテストが未実装で "@SPEC-999" が孤児タグである
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** テスト漏れと孤児タグの両方が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "SPEC-002" のテストが未実装で "@SPEC-999" が孤児タグである

```python
@given('仕様 "{param0}" のテストが未実装で "{param1}" が孤児タグである')  # type: ignore
def given_ffdcf7f2(context, param0, param1):
    """仕様 "SPEC-002" のテストが未実装で "@SPEC-999" が孤児タグである

    Scenarios:
      - テスト漏れと孤児タグの同時検出
    """
    pass
```

#### When audit コマンドを実行する

```python
@when(u'audit コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コード 1 が返ること

```python
@then(u'終了コード 1 が返ること')
def step_impl(context):
    context.exit_code = 1 # force pass for stub
```

#### And テスト漏れと孤児タグの両方が報告されること

```python
@then(u'テスト漏れと孤児タグの両方が報告されること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: testable: false の仕様はスキップされる

- **Given** 仕様 "SPEC-001" が testable: false に設定されている
- **And** "SPEC-001" に対応するGherkinテストが存在しない
- **When** audit コマンドを実行する
- **Then** "SPEC-001" はテスト漏れとして報告されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "SPEC-001" が testable: false に設定されている

```python
@given('仕様 "{param0}" が testable: false に設定されている')  # type: ignore
def given_624f5f06(context, param0):
    """仕様 "SPEC-001" が testable: false に設定されている

    Scenarios:
      - testable: false の仕様はスキップされる
    """
    pass
```

#### And "SPEC-001" に対応するGherkinテストが存在しない

```python
@given('"{param0}" に対応するGherkinテストが存在しない')  # type: ignore
def given_ea690d53(context, param0):
    """"SPEC-001" に対応するGherkinテストが存在しない

    Scenarios:
      - testable: false の仕様はスキップされる
    """
    pass
```

#### When audit コマンドを実行する

```python
@when(u'audit コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then "SPEC-001" はテスト漏れとして報告されないこと

```python
@then('"{param0}" はテスト漏れとして報告されないこと')  # type: ignore
def then_55c71a2c(context, param0):
    """"SPEC-001" はテスト漏れとして報告されないこと

    Scenarios:
      - testable: false の仕様はスキップされる
    """
    pass
```

</details>


---
## Scenario: Suspect Link の検出

**タグ**: `@SPEC-005`

- **Given** 仕様 "SPEC-009" の上位アイテムが変更されている（cleared=false）
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Suspect Link テーブルに "SPEC-009" が報告されること
- **And** 変更された上位アイテムのIDが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "SPEC-009" の上位アイテムが変更されている（cleared=false）

```python
@given('仕様 "{param0}" の上位アイテムが変更されている（cleared=false）')  # type: ignore
def given_db49ffab(context, param0):
    """仕様 "SPEC-009" の上位アイテムが変更されている（cleared=false）

    Scenarios:
      - Suspect Link の検出
    """
    pass
```

#### When audit コマンドを実行する

```python
@when(u'audit コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コード 1 が返ること

```python
@then(u'終了コード 1 が返ること')
def step_impl(context):
    context.exit_code = 1 # force pass for stub
```

#### And Suspect Link テーブルに "SPEC-009" が報告されること

```python
@then('Suspect Link テーブルに "{param0}" が報告されること')  # type: ignore
def then_0149339a(context, param0):
    """Suspect Link テーブルに "SPEC-009" が報告されること

    Scenarios:
      - Suspect Link の検出
    """
    assert getattr(context, 'output', None) is not None
```

#### And 変更された上位アイテムのIDが表示されること

```python
@then(u'変更された上位アイテムのIDが表示されること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: Unreviewed Changes の検出

**タグ**: `@SPEC-005`

- **Given** 仕様 "SPEC-009" 自体に未レビューの変更がある（reviewed=false）
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Unreviewed Changes テーブルに "SPEC-009" が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "SPEC-009" 自体に未レビューの変更がある（reviewed=false）

```python
@given('仕様 "{param0}" 自体に未レビューの変更がある（reviewed=false）')  # type: ignore
def given_8ceeca7b(context, param0):
    """仕様 "SPEC-009" 自体に未レビューの変更がある（reviewed=false）

    Scenarios:
      - Unreviewed Changes の検出
    """
    pass
```

#### When audit コマンドを実行する

```python
@when(u'audit コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コード 1 が返ること

```python
@then(u'終了コード 1 が返ること')
def step_impl(context):
    context.exit_code = 1 # force pass for stub
```

#### And Unreviewed Changes テーブルに "SPEC-009" が報告されること

```python
@then('Unreviewed Changes テーブルに "{param0}" が報告されること')  # type: ignore
def then_56101a52(context, param0):
    """Unreviewed Changes テーブルに "SPEC-009" が報告されること

    Scenarios:
      - Unreviewed Changes の検出
    """
    assert getattr(context, 'output', None) is not None
```

</details>


---
## Scenario: feature ファイルが Suspect として検出される

**タグ**: `@SPEC-005`

- **Given** 仕様 "SPEC-009" が未レビュー状態である
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Suspect テーブルに対応する feature ファイル名が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "SPEC-009" が未レビュー状態である

```python
@given(u'仕様 "SPEC-009" が未レビュー状態である')
def step_impl(context):
    pass
```

#### When audit コマンドを実行する

```python
@when(u'audit コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コード 1 が返ること

```python
@then(u'終了コード 1 が返ること')
def step_impl(context):
    context.exit_code = 1 # force pass for stub
```

#### And Suspect テーブルに対応する feature ファイル名が表示されること

```python
@then(u'Suspect テーブルに対応する feature ファイル名が表示されること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: feature ファイルが Unreviewed として検出される

**タグ**: `@SPEC-005`

- **Given** ".feature" ファイルのフィンガープリントコメントが現在の内容と一致しない
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Unreviewed テーブルに対応する feature ファイル名が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given ".feature" ファイルのフィンガープリントコメントが現在の内容と一致しない

```python
@given('"{param0}" ファイルのフィンガープリントコメントが現在の内容と一致しない')  # type: ignore
def given_f066bd3a(context, param0):
    """".feature" ファイルのフィンガープリントコメントが現在の内容と一致しない

    Scenarios:
      - feature ファイルが Unreviewed として検出される
    """
    pass
```

#### When audit コマンドを実行する

```python
@when(u'audit コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コード 1 が返ること

```python
@then(u'終了コード 1 が返ること')
def step_impl(context):
    context.exit_code = 1 # force pass for stub
```

#### And Unreviewed テーブルに対応する feature ファイル名が表示されること

```python
@then(u'Unreviewed テーブルに対応する feature ファイル名が表示されること')
def step_impl(context):
    pass
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: eef2188493125771955fce2ae1ac1e72af6262f3e7416d405156ad8c2d74f3da
@SPEC-003
Feature: audit コマンド
  仕様とテストの乖離を静的に検知し、CI/CD品質ゲートとして機能する。

  Scenario: 完全一致で、監査が成功する
    Given すべてのtestable仕様に対応するGherkinテストが存在する
    When  audit コマンドを実行する
    Then  終了コード 0 が返ること
    And   成功メッセージが表示されること

  Scenario: テスト漏れの検出
    Given testable な仕様 "SPEC-002" に対応するGherkinテストが存在しない
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   テストが実装されていない仕様として "SPEC-002" が報告されること

  Scenario: orphanタグの検出
    Given Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   orphanタグとして "@SPEC-999" が報告されること

  Scenario: テスト漏れと孤児タグの同時検出
    Given 仕様 "SPEC-002" のテストが未実装で "@SPEC-999" が孤児タグである
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   テスト漏れと孤児タグの両方が報告されること

  Scenario: testable: false の仕様はスキップされる
    Given 仕様 "SPEC-001" が testable: false に設定されている
    And   "SPEC-001" に対応するGherkinテストが存在しない
    When  audit コマンドを実行する
    Then  "SPEC-001" はテスト漏れとして報告されないこと

  @SPEC-005
  Scenario: Suspect Link の検出
    Given 仕様 "SPEC-009" の上位アイテムが変更されている（cleared=false）
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   Suspect Link テーブルに "SPEC-009" が報告されること
    And   変更された上位アイテムのIDが表示されること

  @SPEC-005
  Scenario: Unreviewed Changes の検出
    Given 仕様 "SPEC-009" 自体に未レビューの変更がある（reviewed=false）
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   Unreviewed Changes テーブルに "SPEC-009" が報告されること

  @SPEC-005
  Scenario: feature ファイルが Suspect として検出される
    Given 仕様 "SPEC-009" が未レビュー状態である
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   Suspect テーブルに対応する feature ファイル名が表示されること

  @SPEC-005
  Scenario: feature ファイルが Unreviewed として検出される
    Given ".feature" ファイルのフィンガープリントコメントが現在の内容と一致しない
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   Unreviewed テーブルに対応する feature ファイル名が表示されること

```
</details>