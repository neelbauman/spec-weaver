# Feature: ci コマンド

> ⚠️ **Suspect**: 関連する仕様や他のテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: [REQ-001](../items/REQ-001.md), [REQ-011](../items/REQ-011.md)

**タグ**: `@SPEC-016`

**関連アイテム**: [SPEC-016](../items/SPEC-016.md)

テスト実行からドキュメント生成までを一気通貫で実行する。

---
## Scenario: テスト実行とドキュメント生成の一貫実行

- **Given** scaffold で生成されたテストコードが存在する
- **And** .feature ファイルが存在する
- **When** ci コマンドを実行する
- **Then** pytest-bdd が実行されること
- **And** Cucumber 互換 JSON レポートが生成されること
- **And** テスト結果を含む build ドキュメントが生成されること

---
## Scenario: テスト失敗時のドキュメント生成継続

- **Given** テストに失敗するシナリオが含まれている
- **When** ci コマンドを実行する
- **Then** ドキュメント生成は継続されること
- **And** FAIL 結果がドキュメントに反映されること

---
## Scenario: scaffold 付き ci 実行

- **Given** .feature ファイルが存在する
- **When** ci コマンドを "--scaffold" オプション付きで実行する
- **Then** テストコード生成が先に実行されること
- **And** 続けてテスト実行とドキュメント生成が行われること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When ci コマンドを "--scaffold" オプション付きで実行する

```python
@when('ci コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_ec489531(context, param0):
    """ci コマンドを "--scaffold" オプション付きで実行する

    Scenarios:
      - scaffold 付き ci 実行
    """
    raise NotImplementedError('STEP: ci コマンドを "{param0}" オプション付きで実行する')
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: 283aa0282d1c19b1bc130d2e18405561a84e83c1b6f10a4a382da9597b25529d
@SPEC-016
Feature: ci コマンド
  テスト実行からドキュメント生成までを一気通貫で実行する。

  Scenario: テスト実行とドキュメント生成の一貫実行
    Given scaffold で生成されたテストコードが存在する
    And   .feature ファイルが存在する
    When  ci コマンドを実行する
    Then  pytest-bdd が実行されること
    And   Cucumber 互換 JSON レポートが生成されること
    And   テスト結果を含む build ドキュメントが生成されること

  Scenario: テスト失敗時のドキュメント生成継続
    Given テストに失敗するシナリオが含まれている
    When  ci コマンドを実行する
    Then  ドキュメント生成は継続されること
    And   FAIL 結果がドキュメントに反映されること

  Scenario: scaffold 付き ci 実行
    Given .feature ファイルが存在する
    When  ci コマンドを "--scaffold" オプション付きで実行する
    Then  テストコード生成が先に実行されること
    And   続けてテスト実行とドキュメント生成が行われること

```
</details>