@SPEC-024
Feature: review コマンド — Gherkin フィンガープリント更新と Doorstop レビュー
  指定した仕様アイテムまたは .feature ファイルの Gherkin フィンガープリントを
  更新し、doorstop review を自動実行してレビュー済み状態にする。
  Gherkin シナリオが存在しないアイテム（testable: false など）は
  doorstop review のみ実行する。

  Scenario: アイテムIDを指定してフィンガープリントを更新できる
    Given 仕様アイテム "SPEC-003" が存在する
    And "SPEC-003" に紐づく Gherkin シナリオが存在する
    When `spec-weaver review SPEC-003 --feature-dir ./specification/features` を実行する
    Then 終了コードが0である
    And "SPEC-003" の YAML に test_fingerprint が書き込まれる
    And Doorstop のレビューが自動実行される

  Scenario: .feature ファイルを指定して複数アイテムをまとめて更新できる
    Given ".feature" ファイルに複数の仕様IDタグが含まれる
    When `spec-weaver review specification/features/audit.feature --feature-dir ./specification/features` を実行する
    Then 終了コードが0である
    And ファイル内の各アイテムの test_fingerprint が更新される
    And 更新件数が表示される

  Scenario: Gherkin シナリオが存在しないアイテムは doorstop review のみ実行される
    Given 仕様アイテム "REQ-013" が存在する
    And "REQ-013" に紐づく Gherkin シナリオが存在しない
    When `spec-weaver review REQ-013 --feature-dir ./specification/features` を実行する
    Then 終了コードが0である
    And Doorstop のレビューが自動実行される

  Scenario: 存在しないアイテムIDを指定するとエラーになる
    When `spec-weaver review SPEC-999` を実行する
    Then 終了コードが1である
    And エラーメッセージが表示される
