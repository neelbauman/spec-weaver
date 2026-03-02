# spec-weaver-fingerprint: 291dfce7176f7df3eb4ed27c6363ddfa4bf5196470b040957e8775d85d8a56e4
@SPEC-025
Feature: clear コマンド — Doorstop test_fingerprint 更新
  指定した仕様アイテムまたは .feature ファイル内の全アイテムの
  test_fingerprint を現在の Gherkin 内容のハッシュで更新し、
  Suspect 状態を解除する。

  Scenario: アイテムIDを指定して test_fingerprint を更新できる
    Given 仕様アイテム "SPEC-003" が存在する
    And "SPEC-003" に紐づく Gherkin シナリオが存在する
    When `spec-weaver clear SPEC-003 --feature-dir ./specification/features` を実行する
    Then 終了コードが0である
    And "SPEC-003" の YAML に test_fingerprint が書き込まれる

  Scenario: .feature ファイルを指定して複数アイテムの test_fingerprint を一括更新できる
    Given ".feature" ファイルに複数の仕様IDタグが含まれる
    When `spec-weaver clear specification/features/audit.feature --feature-dir ./specification/features` を実行する
    Then 終了コードが0である
    And ファイル内の各アイテムの test_fingerprint が更新される
    And 更新件数が表示される

  Scenario: 存在しないアイテムIDを指定するとエラーになる
    When `spec-weaver clear SPEC-999 --feature-dir ./specification/features` を実行する
    Then 終了コードが1である
    And エラーメッセージが表示される
