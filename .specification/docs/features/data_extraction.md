# Feature: データ抽出基盤

> ⚠️ **Suspect**: 関連する仕様や他のテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: [REQ-001](../items/REQ-001.md), [REQ-002](../items/REQ-002.md), [SPEC-002](../items/SPEC-002.md), [SPEC-021](../items/SPEC-021.md)

**タグ**: `@SPEC-002`

**関連アイテム**: [SPEC-002](../items/SPEC-002.md) / [SPEC-021](../items/SPEC-021.md)

Doorstop と Gherkin から仕様データとテストタグを正確に抽出する。

---
## Scenario: Doorstop APIによる仕様ID集合の取得

- **Given** Doorstopプロジェクトにアクティブな仕様アイテムが存在する
- **When** 仕様ID集合を取得する
- **Then** アクティブかつtestableな仕様IDのみが返されること

---
## Scenario: 非アクティブなアイテムの除外

- **Given** Doorstopプロジェクトに active: false のアイテムが存在する
- **When** 仕様ID集合を取得する
- **Then** 非アクティブなアイテムは結果に含まれないこと

---
## Scenario: テスト不可能な仕様の除外

- **Given** Doorstopプロジェクトに testable: false のアイテムが存在する
- **When** 仕様ID集合を取得する
- **Then** testable: false のアイテムは結果に含まれないこと

---
## Scenario: プレフィックスによるフィルタリング

- **Given** DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する
- **When** プレフィックス "SPEC" で仕様ID集合を取得する
- **Then** SPECプレフィックスのアイテムのみが返されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When プレフィックス "SPEC" で仕様ID集合を取得する

```python
@when('プレフィックス "{param0}" で仕様ID集合を取得する')  # type: ignore
def when_1d11bcd6(context, param0):
    """プレフィックス "SPEC" で仕様ID集合を取得する

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    raise NotImplementedError('STEP: プレフィックス "{param0}" で仕様ID集合を取得する')
```

</details>


---
## Scenario: Gherkin ASTからのタグ抽出

- **Given** Gherkin .feature ファイルに @SPEC-001 タグが付与されている
- **When** タグ集合を取得する
- **Then** "SPEC-001" がタグ集合に含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Then "SPEC-001" がタグ集合に含まれること

```python
@then('"{param0}" がタグ集合に含まれること')  # type: ignore
def then_e8d01468(context, param0):
    """"SPEC-001" がタグ集合に含まれること

    Scenarios:
      - Gherkin ASTからのタグ抽出
    """
    raise NotImplementedError('STEP: "{param0}" がタグ集合に含まれること')
```

</details>


---
## Scenario: Feature・Scenario両レベルのタグ抽出

- **Given** Feature レベルと Scenario レベルに異なるSPECタグが付与されている
- **When** タグ集合を取得する
- **Then** 両方のレベルのタグがすべて抽出されること

---
## Scenario: サブディレクトリ内のfeatureファイルの再帰探索

- **Given** サブディレクトリに .feature ファイルが存在する
- **When** タグ集合を取得する
- **Then** サブディレクトリ内のタグも含めて抽出されること

---
## Scenario: Gherkin構文エラーの検出

- **Given** 構文的に不正な .feature ファイルが存在する
- **When** タグ集合を取得する
- **Then** ValueError が発生しGherkin構文エラーが報告されること


---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: 15d5fb6f482561665a6a41ec38e7d3dff795a95d4f7ab3c2a60a10a322b36fcb
@SPEC-002
Feature: データ抽出基盤
  Doorstop と Gherkin から仕様データとテストタグを正確に抽出する。

  # --- Doorstop解析 ---

  Scenario: Doorstop APIによる仕様ID集合の取得
    Given Doorstopプロジェクトにアクティブな仕様アイテムが存在する
    When  仕様ID集合を取得する
    Then  アクティブかつtestableな仕様IDのみが返されること

  Scenario: 非アクティブなアイテムの除外
    Given Doorstopプロジェクトに active: false のアイテムが存在する
    When  仕様ID集合を取得する
    Then  非アクティブなアイテムは結果に含まれないこと

  Scenario: テスト不可能な仕様の除外
    Given Doorstopプロジェクトに testable: false のアイテムが存在する
    When  仕様ID集合を取得する
    Then  testable: false のアイテムは結果に含まれないこと

  Scenario: プレフィックスによるフィルタリング
    Given DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する
    When  プレフィックス "SPEC" で仕様ID集合を取得する
    Then  SPECプレフィックスのアイテムのみが返されること

  # --- Gherkin解析 ---

  Scenario: Gherkin ASTからのタグ抽出
    Given Gherkin .feature ファイルに @SPEC-001 タグが付与されている
    When  タグ集合を取得する
    Then  "SPEC-001" がタグ集合に含まれること

  Scenario: Feature・Scenario両レベルのタグ抽出
    Given Feature レベルと Scenario レベルに異なるSPECタグが付与されている
    When  タグ集合を取得する
    Then  両方のレベルのタグがすべて抽出されること

  Scenario: サブディレクトリ内のfeatureファイルの再帰探索
    Given サブディレクトリに .feature ファイルが存在する
    When  タグ集合を取得する
    Then  サブディレクトリ内のタグも含めて抽出されること

  Scenario: Gherkin構文エラーの検出
    Given 構文的に不正な .feature ファイルが存在する
    When  タグ集合を取得する
    Then  ValueError が発生しGherkin構文エラーが報告されること

  # --- Gherkinタグ継承（Effective Tags）---

  Rule: Featureレベルのタグは配下のすべてのScenarioに継承される

    @SPEC-021
    Scenario: Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
      Given Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない
      When  タグマップを取得する
      Then  その仕様タグのエントリにシナリオの情報が紐付けられること

    @SPEC-021
    Scenario: Featureタグを継承したエントリのkeywordはScenarioになる
      Given Feature レベルにのみ仕様タグが付与されている
      When  タグマップを取得する
      Then  tag_map エントリの keyword が "Scenario" または "Scenario Outline" であること

    @SPEC-021
    Scenario: Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
      Given Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている
      And   Rule 配下のシナリオにはタグが付いていない
      When  タグマップを取得する
      Then  そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること

    @SPEC-021
    Scenario: シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
      Given Feature レベルに仕様タグ A が付与されている
      And   配下のシナリオに直接 仕様タグ B が付与されている
      When  タグマップを取得する
      Then  そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること

    @SPEC-021
    Scenario: Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
      Given Scenario Outline に仕様タグ A が付与されている
      And   いずれかの Examples テーブルに仕様タグ B が付与されている
      When  タグマップを取得する
      Then  仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること

    @SPEC-021
    Scenario: プレフィックスフィルタはEffective Tags算出後に適用される
      Given Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている
      When  プレフィックス "SPEC" でタグマップを取得する
      Then  "SPEC-001" のみがタグマップに含まれ "REQ-001" は含まれないこと

```
</details>