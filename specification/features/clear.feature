@QA-005
Feature: clear コマンド — Doorstop gherkin_fingerprints エディタ確認更新
  Doorstop アイテムを指定し、変更のあった Gherkin ファイルをエディタで開いて確認した上で
  gherkin_fingerprints を更新し Suspect 状態を解除する。

  Scenario: アイテムIDを指定してエディタが起動し gherkin_fingerprints が更新される
    Given 仕様アイテム "QA-001" が存在する
    And "QA-001" に紐づく Gherkin シナリオが存在する
    And エディタが利用可能である
    When `spec-weaver clear QA-001` を実行する
    Then clear 終了コードが0である
    And エディタが起動した
    And "QA-001" の YAML に gherkin_fingerprints が書き込まれる

  Scenario: --no-edit でエディタなしでクリアできる
    Given 仕様アイテム "QA-001" が存在する
    And "QA-001" に紐づく Gherkin シナリオが存在する
    When `spec-weaver clear QA-001 --no-edit` を実行する
    Then clear 終了コードが0である
    And エディタが起動しない
    And "QA-001" の YAML に gherkin_fingerprints が書き込まれる

  Scenario: 存在しないアイテムIDを指定するとエラーになる
    When `spec-weaver clear NONEXISTENT-999` を実行する
    Then clear 終了コードが1である
    And エラーメッセージが表示される

  Scenario: 紐づくGherkinシナリオが存在しないアイテムを指定するとエラーになる
    Given 仕様アイテム "QA-001" が存在する
    And "QA-001" に紐づく Gherkin シナリオが存在しない
    When `spec-weaver clear QA-001` を実行する
    Then clear 終了コードが1である
    And 警告メッセージが表示される

  Scenario: 未レビューアイテムはクリアできない
    Given あるアイテムが "unreviewed" 状態である
    When そのアイテム ID で `spec-weaver clear` を実行する
    Then clear 終了コードが1である
    And エラーメッセージが表示される

  Scenario: エディタが見つからない場合はエラーになる
    Given 仕様アイテム "QA-001" が存在する
    And "QA-001" に紐づく Gherkin シナリオが存在する
    And エディタが利用不可能である
    When `spec-weaver clear QA-001` を実行する
    Then clear 終了コードが1である
    And エラーメッセージが表示される

  Scenario: エディタが非ゼロ終了するとエラーになる
    Given 仕様アイテム "QA-001" が存在する
    And "QA-001" に紐づく Gherkin シナリオが存在する
    And エディタが非ゼロ終了コードを返す
    When `spec-weaver clear QA-001` を実行する
    Then clear 終了コードが1である
    And エラーメッセージが表示される

  Scenario: --all で全アイテムの gherkin_fingerprints を一括更新できる（エディタなし）
    Given gherkin_fingerprints が不一致のアイテムが複数存在する
    When `spec-weaver clear --all` を実行する
    Then clear 終了コードが0である
    And エディタが起動しない
    And 各アイテムの gherkin_fingerprints が更新される

  Scenario: --all で未レビューアイテムはスキップされ警告が出る
    Given あるアイテムが "unreviewed" 状態である
    When `spec-weaver clear --all` を実行する
    Then clear 終了コードが0である
    And 未レビューアイテムに対して警告メッセージが表示される

  Scenario: --all と対象IDを同時に指定するとエラーになる
    When `spec-weaver clear --all QA-001` を実行する
    Then clear 終了コードが1である
    And エラーメッセージが表示される
