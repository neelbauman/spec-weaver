# spec-weaver-fingerprint: 0c0424f9b232677c9c2cb4b197f3442a1154c7ddfe9307911dad7333a0311c66
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
    Then clear 終了コードが0である
    And "SPEC-003" の YAML に gherkin_fingerprints が書き込まれる

  Scenario: .feature ファイルを指定して複数アイテムの gherkin_fingerprints を一括更新できる
    Given ".feature" ファイルに複数の仕様IDタグが含まれる
    When `spec-weaver clear specification/features/audit.feature --feature-dir ./specification/features` を実行する
    Then clear 終了コードが0である
    And ファイル内の各アイテムの gherkin_fingerprints が更新される
    And 更新件数が表示される

  Scenario: .feature ファイルを指定してファイル自身の suspect 状態も解除できる
    Given ".feature" ファイルが "suspect-with-reviewed" 状態である
    When `spec-weaver clear specification/features/audit.feature --feature-dir ./specification/features` を実行する
    Then clear 終了コードが0である
    And "specification/features/audit.feature" の内部フィンガープリントが最新の Doorstop スタンプで更新される
    And `spec-weaver status` で当該ファイルが "✅ reviewed" となる

  Scenario: 存在しないアイテムIDを指定するとエラーになる
    When `spec-weaver clear SPEC-999 --feature-dir ./specification/features` を実行する
    Then clear 終了コードが1である
    And エラーメッセージが表示される

  Scenario: 紐づくGherkinシナリオが存在しないアイテムを指定するとエラーになる
    Given 仕様アイテム "SPEC-004" が存在する
    And "SPEC-004" に紐づく Gherkin シナリオが存在しない
    When `spec-weaver clear SPEC-004 --feature-dir ./specification/features` を実行する
    Then clear 終了コードが1である
    And 警告メッセージが表示される
