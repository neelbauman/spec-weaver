# spec-weaver-fingerprint: 0485ebf45bbfa6feb6378a9f8817c7e3d53c0edbabe17b04d89fd7632c47e816
# spec-weaver-fingerprint-QA-005: sF4bXqVCp0C7Q2T3NpRXT26Hdj_FTb7yqGfcnXQcYkU=
@QA-005
Feature: clear コマンド — Doorstop gherkin_fingerprints 更新
  指定した仕様アイテムまたは .feature ファイル内の全アイテムの
  gherkin_fingerprints を現在の Gherkin 内容のハッシュで更新し、
  Suspect 状態を解除する。

  Scenario: アイテムIDを指定して gherkin_fingerprints を更新できる
    Given 仕様アイテム "SPEC-003" が存在する
    And "SPEC-003" に紐づく Gherkin シナリオが存在する
    When `spec-weaver clear SPEC-003 --feature-dir ./specification/features` を実行する
    Then 終了コードが0である
    And "SPEC-003" の YAML に gherkin_fingerprints が書き込まれる

  Scenario: .feature ファイルを指定して複数アイテムの gherkin_fingerprints を一括更新できる
    Given ".feature" ファイルに複数の仕様IDタグが含まれる
    When `spec-weaver clear specification/features/audit.feature --feature-dir ./specification/features` を実行する
    Then 終了コードが0である
    And ファイル内の各アイテムの gherkin_fingerprints が更新される
    And 更新件数が表示される

  Scenario: 存在しないアイテムIDを指定するとエラーになる
    When `spec-weaver clear SPEC-999 --feature-dir ./specification/features` を実行する
    Then 終了コードが1である
    And エラーメッセージが表示される
