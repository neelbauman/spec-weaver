# Feature: audit コマンド

**タグ**: `@SPEC-003`

**関連アイテム**: [SPEC-003](../items/SPEC-003.md) / [SPEC-005](../items/SPEC-005.md)

仕様とテストの乖離を静的に検知し、CI/CD品質ゲートとして機能する。

---
## Scenario: 完全一致時の監査成功

- **Given** すべてのtestable仕様に対応するGherkinテストが存在する
- **When** audit コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** 成功メッセージが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Then 終了コード 0 が返ること

```python
@then('終了コード {code:d} が返ること')
def then_exit_code(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

</details>


---
## Scenario: テスト漏れの検出

- **Given** testable な仕様 "SPEC-002" に対応するGherkinテストが存在しない
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** テストが実装されていない仕様として "SPEC-002" が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Then 終了コード 1 が返ること

```python
@then('終了コード {code:d} が返ること')
def then_exit_code(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

</details>


---
## Scenario: 孤児タグの検出

- **Given** Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** 孤児タグとして "@SPEC-999" が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Then 終了コード 1 が返ること

```python
@then('終了コード {code:d} が返ること')
def then_exit_code(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

</details>


---
## Scenario: テスト漏れと孤児タグの同時検出

- **Given** 仕様 "SPEC-002" のテストが未実装で "@SPEC-999" が孤児タグである
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** テスト漏れと孤児タグの両方が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Then 終了コード 1 が返ること

```python
@then('終了コード {code:d} が返ること')
def then_exit_code(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

</details>


---
## Scenario: testable: false の仕様はスキップされる

- **Given** 仕様 "SPEC-001" が testable: false に設定されている
- **And** "SPEC-001" に対応するGherkinテストが存在しない
- **When** audit コマンドを実行する
- **Then** "SPEC-001" はテスト漏れとして報告されないこと

---
## Scenario: Suspect Link の検出

**タグ**: `@SPEC-005`

- **Given** 仕様 "SPEC-009" の上位アイテムが変更されている（cleared=false）
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Suspect Link テーブルに "SPEC-009" が報告されること
- **And** 変更された上位アイテムのIDが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Then 終了コード 1 が返ること

```python
@then('終了コード {code:d} が返ること')
def then_exit_code(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
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

#### Then 終了コード 1 が返ること

```python
@then('終了コード {code:d} が返ること')
def then_exit_code(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
@SPEC-003
Feature: audit コマンド
  仕様とテストの乖離を静的に検知し、CI/CD品質ゲートとして機能する。

  Scenario: 完全一致時の監査成功
    Given すべてのtestable仕様に対応するGherkinテストが存在する
    When  audit コマンドを実行する
    Then  終了コード 0 が返ること
    And   成功メッセージが表示されること

  Scenario: テスト漏れの検出
    Given testable な仕様 "SPEC-002" に対応するGherkinテストが存在しない
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   テストが実装されていない仕様として "SPEC-002" が報告されること

  Scenario: 孤児タグの検出
    Given Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   孤児タグとして "@SPEC-999" が報告されること

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

```
</details>