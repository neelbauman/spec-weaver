# spec-weaver-fingerprint: e72e52f1a09100e944312ac3edc505de44b43c24c963f1b696b64e2f90d45824
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

  Scenario: テスト漏れとorphanタグの同時検出
    Given 仕様 "SPEC-002" のテストが未実装で "@SPEC-999" がorphanタグである
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   テスト漏れとorphanタグの両方が報告されること

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
