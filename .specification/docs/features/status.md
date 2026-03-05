# Feature: status コマンド

**タグ**: `@VIS-003`

**関連アイテム**: [VIS-003](../items/VIS-003.md)

REQ・SPECの実装ステータスをRichテーブル形式で一覧表示する。

---
## Scenario: 全アイテムのステータスを一覧表示する {: #line-7 }

- **Given** REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている
- **When** status コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** REQ-001 が "draft" バッジとともに表示されること
- **And** SPEC-001 が "implemented" バッジとともに表示されること

---
## Scenario: status 未設定のアイテムは "-" と表示される {: #line-14 }

- **Given** SPEC-001 に status フィールドが設定されていない
- **When** status コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** SPEC-001 の実装状況が "-" と表示されること

---
## Scenario: --filter で特定ステータスに絞り込める {: #line-20 }

- **Given** REQ-001 が status: implemented、REQ-002 が status: draft に設定されている
- **When** status コマンドを "--filter implemented" オプション付きで実行する
- **Then** 終了コード 0 が返ること
- **And** REQ-001 が表示されること
- **And** REQ-002 は表示されないこと

---
## Scenario: --filter に一致するアイテムが存在しない場合に通知される {: #line-27 }

- **Given** すべてのアイテムの status が "draft" に設定されている
- **When** status コマンドを "--filter implemented" オプション付きで実行する
- **Then** 終了コード 0 が返ること
- **And** 一致するアイテムが見つからなかった旨が表示されること

---
## Scenario: レビューステータスと最終更新日が表示される {: #line-33 }

- **Given** Doorstopのアイテムが存在する
- **When** status コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** レビューステータス列が表示されること
- **And** 最終更新日列が表示されること

---
## Scenario: buildコマンドで生成されるドキュメントに実装状況が反映される {: #line-40 }

- **Given** SPEC-001 が status: implemented に設定されている
- **When** build コマンドを実行する
- **Then** 一覧ページの実装状況列にバッジが表示されること
- **And** 詳細ページの本文に "**実装状況**: ✅ implemented" が表示されること


---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: ec3fe7950dd3bd4c3bd04815b3820a604d3148298794bacbf50928c87945fd64
# spec-weaver-fingerprint-VIS-003: vkjlHhlge0Un5uAGQCyff68rJGP3jp7vGCvSQVAsuNM=
@VIS-003
Feature: status コマンド
  REQ・SPECの実装ステータスをRichテーブル形式で一覧表示する。

  Scenario: 全アイテムのステータスを一覧表示する
    Given REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている
    When  status コマンドを実行する
    Then  終了コード 0 が返ること
    And   REQ-001 が "draft" バッジとともに表示されること
    And   SPEC-001 が "implemented" バッジとともに表示されること

  Scenario: status 未設定のアイテムは "-" と表示される
    Given SPEC-001 に status フィールドが設定されていない
    When  status コマンドを実行する
    Then  終了コード 0 が返ること
    And   SPEC-001 の実装状況が "-" と表示されること

  Scenario: --filter で特定ステータスに絞り込める
    Given REQ-001 が status: implemented、REQ-002 が status: draft に設定されている
    When  status コマンドを "--filter implemented" オプション付きで実行する
    Then  終了コード 0 が返ること
    And   REQ-001 が表示されること
    And   REQ-002 は表示されないこと

  Scenario: --filter に一致するアイテムが存在しない場合に通知される
    Given すべてのアイテムの status が "draft" に設定されている
    When  status コマンドを "--filter implemented" オプション付きで実行する
    Then  終了コード 0 が返ること
    And   一致するアイテムが見つからなかった旨が表示されること

  Scenario: レビューステータスと最終更新日が表示される
    Given Doorstopのアイテムが存在する
    When  status コマンドを実行する
    Then  終了コード 0 が返ること
    And   レビューステータス列が表示されること
    And   最終更新日列が表示されること

  Scenario: buildコマンドで生成されるドキュメントに実装状況が反映される
    Given SPEC-001 が status: implemented に設定されている
    When  build コマンドを実行する
    Then  一覧ページの実装状況列にバッジが表示されること
    And   詳細ページの本文に "**実装状況**: ✅ implemented" が表示されること

```
</details>