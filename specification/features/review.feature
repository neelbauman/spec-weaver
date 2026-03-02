@SPEC-024
Feature: review コマンド — Gherkin フィンガープリント更新
  指定した仕様アイテムまたは .feature ファイルの Gherkin フィンガープリントを
  更新し、Gherkin 側の「レビュー済み」状態を記録する。

  Scenario: アイテムIDを指定してフィンガープリントを更新できる
    Given 仕様アイテム "SPEC-003" が存在する
    And "SPEC-003" に紐づく Gherkin シナリオが存在する
    When `spec-weaver review SPEC-003 --feature-dir ./specification/features` を実行する
    Then 終了コードが0である
    And "SPEC-003" の YAML に test_fingerprint が書き込まれる
    And 次のアクションとして "doorstop review SPEC-003" が案内される

  Scenario: .feature ファイルを指定して複数アイテムをまとめて更新できる
    Given ".feature" ファイルに複数の仕様IDタグが含まれる
    When `spec-weaver review specification/features/audit.feature --feature-dir ./specification/features` を実行する
    Then 終了コードが0である
    And ファイル内の各アイテムの test_fingerprint が更新される
    And 更新件数が表示される

  Scenario: 紐づく Gherkin シナリオが存在しないアイテムを指定するとエラーになる
    When `spec-weaver review SPEC-999` を実行する
    Then 終了コードが1である
    And 警告メッセージが表示される
