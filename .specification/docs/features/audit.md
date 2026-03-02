# Feature: audit コマンド

**関連アイテム**: [QA-001](../items/QA-001.md)

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
@given('すべてのtestable仕様に対応するGherkinテストが存在する')  # type: ignore
def given_a7b8516a(context):
    """すべてのtestable仕様に対応するGherkinテストが存在する

    Scenarios:
      - 完全一致で、監査が成功する
    """
    raise NotImplementedError('STEP: すべてのtestable仕様に対応するGherkinテストが存在する')
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する

    Scenarios:
      - 完全一致で、監査が成功する
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - testable: false の仕様はスキップされる
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: audit コマンドを実行する')
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
@then('成功メッセージが表示されること')  # type: ignore
def then_f7642361(context):
    """成功メッセージが表示されること

    Scenarios:
      - 完全一致で、監査が成功する
      - orphanタグの検出
    """
    raise NotImplementedError('STEP: 成功メッセージが表示されること')
```

</details>


---
## Scenario: テスト漏れの検出

- **Given** testable な仕様 "CORE-001" に対応するGherkinテストが存在しない
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** テストが実装されていない仕様として "CORE-001" が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given testable な仕様 "CORE-001" に対応するGherkinテストが存在しない

```python
@given('testable な仕様 "{param0}" に対応するGherkinテストが存在しない')  # type: ignore
def given_03339ad7(context, param0):
    """testable な仕様 "CORE-001" に対応するGherkinテストが存在しない

    Scenarios:
      - テスト漏れの検出
      - テスト漏れとorphanタグの同時検出
    """
    raise NotImplementedError('STEP: testable な仕様 "{param0}" に対応するGherkinテストが存在しない')
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する

    Scenarios:
      - 完全一致で、監査が成功する
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - testable: false の仕様はスキップされる
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: audit コマンドを実行する')
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    """終了コード 1 が返ること

    Scenarios:
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: 終了コード 1 が返ること')
```

#### And テストが実装されていない仕様として "CORE-001" が報告されること

```python
@then('テストが実装されていない仕様として "{param0}" が報告されること')  # type: ignore
def then_6664aa42(context, param0):
    """テストが実装されていない仕様として "CORE-001" が報告されること

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
      - orphanタグの検出
    """
    pass
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する

    Scenarios:
      - 完全一致で、監査が成功する
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - testable: false の仕様はスキップされる
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: audit コマンドを実行する')
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    """終了コード 1 が返ること

    Scenarios:
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: 終了コード 1 が返ること')
```

#### And orphanタグとして "@SPEC-999" が報告されること

```python
@then('orphanタグとして "{param0}" が報告されること')  # type: ignore
def then_33c30716(context, param0):
    """orphanタグとして "@SPEC-999" が報告されること

    Scenarios:
      - orphanタグの検出
    """
    assert getattr(context, 'output', None) is not None
```

</details>


---
## Scenario: テスト漏れとorphanタグの同時検出

- **Given** 仕様 "CORE-001" のテストが未実装で "@SPEC-999" がorphanタグである
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** テスト漏れとorphanタグの両方が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "CORE-001" のテストが未実装で "@SPEC-999" がorphanタグである

```python
@given('仕様 "{param0}" のテストが未実装で "{param1}" がorphanタグである')  # type: ignore
def given_ffdcf7f2(context, param0, param1):
    """仕様 "CORE-001" のテストが未実装で "@SPEC-999" がorphanタグである

    Scenarios:
      - テスト漏れとorphanタグの同時検出
    """
    pass
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する

    Scenarios:
      - 完全一致で、監査が成功する
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - testable: false の仕様はスキップされる
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: audit コマンドを実行する')
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    """終了コード 1 が返ること

    Scenarios:
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: 終了コード 1 が返ること')
```

#### And テスト漏れとorphanタグの両方が報告されること

```python
@then('テスト漏れとorphanタグの両方が報告されること')  # type: ignore
def then_755ec6da(context):
    """テスト漏れとorphanタグの両方が報告されること

    Scenarios:
      - テスト漏れとorphanタグの同時検出
    """
    raise NotImplementedError('STEP: テスト漏れとorphanタグの両方が報告されること')
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
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する

    Scenarios:
      - 完全一致で、監査が成功する
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - testable: false の仕様はスキップされる
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: audit コマンドを実行する')
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

**タグ**: `@QA-001`

- **Given** 仕様 "VIS-005" の上位アイテムが変更されている（cleared=false）
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Suspect Link テーブルに "VIS-005" が報告されること
- **And** 変更された上位アイテムのIDが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "VIS-005" の上位アイテムが変更されている（cleared=false）

```python
@given('仕様 "{param0}" の上位アイテムが変更されている（cleared=false）')  # type: ignore
def given_db49ffab(context, param0):
    """仕様 "VIS-005" の上位アイテムが変更されている（cleared=false）

    Scenarios:
      - Suspect Link の検出
    """
    pass
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する

    Scenarios:
      - 完全一致で、監査が成功する
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - testable: false の仕様はスキップされる
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: audit コマンドを実行する')
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    """終了コード 1 が返ること

    Scenarios:
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: 終了コード 1 が返ること')
```

#### And Suspect Link テーブルに "VIS-005" が報告されること

```python
@then('Suspect Link テーブルに "{param0}" が報告されること')  # type: ignore
def then_0149339a(context, param0):
    """Suspect Link テーブルに "VIS-005" が報告されること

    Scenarios:
      - Suspect Link の検出
    """
    assert getattr(context, 'output', None) is not None
```

#### And 変更された上位アイテムのIDが表示されること

```python
@then('変更された上位アイテムのIDが表示されること')  # type: ignore
def then_407500a2(context):
    """変更された上位アイテムのIDが表示されること

    Scenarios:
      - Suspect Link の検出
    """
    raise NotImplementedError('STEP: 変更された上位アイテムのIDが表示されること')
```

</details>


---
## Scenario: Unreviewed Changes の検出

**タグ**: `@QA-001`

- **Given** 仕様 "VIS-005" 自体に未レビューの変更がある（reviewed=false）
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Unreviewed Changes テーブルに "VIS-005" が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "VIS-005" 自体に未レビューの変更がある（reviewed=false）

```python
@given('仕様 "{param0}" 自体に未レビューの変更がある（reviewed=false）')  # type: ignore
def given_8ceeca7b(context, param0):
    """仕様 "VIS-005" 自体に未レビューの変更がある（reviewed=false）

    Scenarios:
      - Unreviewed Changes の検出
    """
    pass
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する

    Scenarios:
      - 完全一致で、監査が成功する
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - testable: false の仕様はスキップされる
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: audit コマンドを実行する')
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    """終了コード 1 が返ること

    Scenarios:
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: 終了コード 1 が返ること')
```

#### And Unreviewed Changes テーブルに "VIS-005" が報告されること

```python
@then('Unreviewed Changes テーブルに "{param0}" が報告されること')  # type: ignore
def then_56101a52(context, param0):
    """Unreviewed Changes テーブルに "VIS-005" が報告されること

    Scenarios:
      - Unreviewed Changes の検出
    """
    assert getattr(context, 'output', None) is not None
```

</details>


---
## Scenario: feature ファイルが Unreviewed として検出される

**タグ**: `@QA-001`

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
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する

    Scenarios:
      - 完全一致で、監査が成功する
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - testable: false の仕様はスキップされる
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: audit コマンドを実行する')
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    """終了コード 1 が返ること

    Scenarios:
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: 終了コード 1 が返ること')
```

#### And Unreviewed テーブルに対応する feature ファイル名が表示されること

```python
@then('Unreviewed テーブルに対応する feature ファイル名が表示されること')  # type: ignore
def then_c1e4063b(context):
    """Unreviewed テーブルに対応する feature ファイル名が表示されること

    Scenarios:
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: Unreviewed テーブルに対応する feature ファイル名が表示されること')
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: 482d0d3cc0550cd81612f7b5482ced1e27599656a96356d22af44921e893edd1
# spec-weaver-fingerprint-QA-001: IVjwbWJI8Xga_1LFrHA_SqnpsZ_-MHzjo-w7D9zwEYE=

Feature: audit コマンド
  仕様とテストの乖離を静的に検知し、CI/CD品質ゲートとして機能する。

  Scenario: 完全一致で、監査が成功する
    Given すべてのtestable仕様に対応するGherkinテストが存在する
    When  audit コマンドを実行する
    Then  終了コード 0 が返ること
    And   成功メッセージが表示されること

  Scenario: テスト漏れの検出
    Given testable な仕様 "CORE-001" に対応するGherkinテストが存在しない
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   テストが実装されていない仕様として "CORE-001" が報告されること

  Scenario: orphanタグの検出
    Given Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   orphanタグとして "@SPEC-999" が報告されること

  Scenario: テスト漏れとorphanタグの同時検出
    Given 仕様 "CORE-001" のテストが未実装で "@SPEC-999" がorphanタグである
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   テスト漏れとorphanタグの両方が報告されること

  Scenario: testable: false の仕様はスキップされる
    Given 仕様 "SPEC-001" が testable: false に設定されている
    And   "SPEC-001" に対応するGherkinテストが存在しない
    When  audit コマンドを実行する
    Then  "SPEC-001" はテスト漏れとして報告されないこと

  @QA-001
  Scenario: Suspect Link の検出
    Given 仕様 "VIS-005" の上位アイテムが変更されている（cleared=false）
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   Suspect Link テーブルに "VIS-005" が報告されること
    And   変更された上位アイテムのIDが表示されること

  @QA-001
  Scenario: Unreviewed Changes の検出
    Given 仕様 "VIS-005" 自体に未レビューの変更がある（reviewed=false）
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   Unreviewed Changes テーブルに "VIS-005" が報告されること


  @QA-001
  Scenario: feature ファイルが Unreviewed として検出される
    Given ".feature" ファイルのフィンガープリントコメントが現在の内容と一致しない
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   Unreviewed テーブルに対応する feature ファイル名が表示されること

```
</details>