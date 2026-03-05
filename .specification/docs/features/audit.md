# Feature: audit コマンド

**関連アイテム**: [QA-001](../items/QA-001.md) / [QA-006](../items/QA-006.md)

仕様とテストの乖離を静的に検知し、CI/CD品質ゲートとして機能する。

---
## Scenario: 完全一致で、監査が成功する {: #line-8 }

- **Given** すべてのtestable仕様に対応するGherkinテストが存在する
- **When** audit コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** 成功メッセージが表示されること

---
## Scenario: テスト漏れの検出 {: #line-14 }

- **Given** testable な仕様 "CORE-001" に対応するGherkinテストが存在しない
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** テストが実装されていない仕様として "CORE-001" が報告されること

---
## Scenario: orphanタグの検出 {: #line-20 }

- **Given** Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** orphanタグとして "@SPEC-999" が報告されること

---
## Scenario: テスト漏れとorphanタグの同時検出 {: #line-26 }

- **Given** 仕様 "CORE-001" のテストが未実装で "@SPEC-999" がorphanタグである
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** テスト漏れとorphanタグの両方が報告されること

---
## Scenario: testable: false の仕様はスキップされる {: #line-32 }

- **Given** 仕様 "SPEC-001" が testable: false に設定されている
- **And** "SPEC-001" に対応するGherkinテストが存在しない
- **When** audit コマンドを実行する
- **Then** "SPEC-001" はテスト漏れとして報告されないこと

---
## Scenario: Suspect Link の検出 {: #line-39 }

**タグ**: `@QA-001`

- **Given** 仕様 "VIS-005" の上位アイテムが変更されている（cleared=false）
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Suspect Link テーブルに "VIS-005" が報告されること
- **And** 変更された上位アイテムのIDが表示されること

---
## Scenario: Unreviewed Changes の検出 {: #line-47 }

**タグ**: `@QA-001`

- **Given** 仕様 "VIS-005" 自体に未レビューの変更がある（reviewed=false）
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Unreviewed Changes テーブルに "VIS-005" が報告されること

---
## Scenario: feature ファイルが Unreviewed として検出される {: #line-54 }

**タグ**: `@QA-001`

- **Given** ".feature" ファイルのフィンガープリントコメントが現在の内容と一致しない
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Unreviewed テーブルに対応する feature ファイル名が表示されること

---
## Scenario: behavior-without-gherkin の検出 {: #line-61 }

**タグ**: `@QA-006`

- **Given** 仕様 "VIS-003" が "layer: behavior" かつ "testable: true" に設定されている
- **And** "VIS-003" に対応するGherkinタグが存在しない
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** "VIS-003" が behavior-without-gherkin として報告されること

---
## Scenario: architecture-with-gherkin の検出（警告） {: #line-69 }

**タグ**: `@QA-006`

- **Given** 仕様 "CORE-001" が "layer: architecture" に設定されている
- **And** "CORE-001" に対応するGherkinタグが存在する
- **When** audit コマンドを実行する
- **Then** "CORE-001" が architecture-with-gherkin として警告表示されること
- **And** architecture-with-gherkin は終了コードに影響しないこと

---
## Scenario: layer-unset の通知（情報） {: #line-77 }

**タグ**: `@QA-006`

- **Given** アクティブかつ "testable: true" の仕様に "layer" 属性が設定されていない
- **When** audit コマンドを実行する
- **Then** 当該仕様IDが layer-unset として情報表示されること
- **And** layer-unset は終了コードに影響しないこと


---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: bcdfb25f894f72de41a0499a31984a64e890c1f9500c0c309c6ae9961f990c95
# spec-weaver-fingerprint-QA-001: IVjwbWJI8Xga_1LFrHA_SqnpsZ_-MHzjo-w7D9zwEYE=
# spec-weaver-fingerprint-QA-006: IQO1lBdAvEzVzJofPO_jiIFF1WjLNsCMUhlLQTXCk6A=

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

  @QA-006
  Scenario: behavior-without-gherkin の検出
    Given 仕様 "VIS-003" が "layer: behavior" かつ "testable: true" に設定されている
    And   "VIS-003" に対応するGherkinタグが存在しない
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   "VIS-003" が behavior-without-gherkin として報告されること

  @QA-006
  Scenario: architecture-with-gherkin の検出（警告）
    Given 仕様 "CORE-001" が "layer: architecture" に設定されている
    And   "CORE-001" に対応するGherkinタグが存在する
    When  audit コマンドを実行する
    Then  "CORE-001" が architecture-with-gherkin として警告表示されること
    And   architecture-with-gherkin は終了コードに影響しないこと

  @QA-006
  Scenario: layer-unset の通知（情報）
    Given アクティブかつ "testable: true" の仕様に "layer" 属性が設定されていない
    When  audit コマンドを実行する
    Then  当該仕様IDが layer-unset として情報表示されること
    And   layer-unset は終了コードに影響しないこと

```
</details>