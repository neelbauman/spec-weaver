# spec-weaver-fingerprint: 747a067a366f71279c1117cac9de1de2defd17db0b57a350b3806f514bd482a0
# spec-weaver-fingerprint-SPEC-007: T6XuJu67Dj1RDLYHNeLzVkenP67ky6zNbqcs-ubwpzY=
@SPEC-007
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
