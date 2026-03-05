@QA-004
Feature: review コマンド — Doorstop アイテムのエディタ確認レビュー
  Doorstop アイテムを指定し、suspect の原因となった関連アイテムをエディタで開いて確認した上で
  reviewed スタンプを更新する。

  Scenario: アイテムIDを指定してエディタが起動しレビュー済みになる
    Given Doorstop アイテム "QA-001" が存在する
    And エディタが利用可能である
    When `spec-weaver review QA-001` を実行する
    Then review 終了コードが0である
    And エディタが起動した
    And "QA-001" が reviewed 状態になる

  Scenario: suspect な場合に原因アイテムがエディタで開かれる
    Given Doorstop アイテム "QA-001" が suspect 状態である
    And 親アイテムに git 差分が存在する
    And エディタが利用可能である
    When `spec-weaver review QA-001` を実行する
    Then review 終了コードが0である
    And エディタが対象 YAML と関連アイテムの分割表示で起動した

  Scenario: --no-edit でエディタなしでレビューできる
    Given Doorstop アイテム "QA-001" が存在する
    When `spec-weaver review QA-001 --no-edit` を実行する
    Then review 終了コードが0である
    And エディタが起動しない
    And "QA-001" が reviewed 状態になる

  Scenario: 存在しないアイテムIDを指定するとエラーになる
    When `spec-weaver review NONEXISTENT-999` を実行する
    Then review 終了コードが1である
    And review エラーメッセージが表示される

  Scenario: エディタが見つからない場合はエラーになる
    Given Doorstop アイテム "QA-001" が存在する
    And エディタが利用不可能である
    When `spec-weaver review QA-001` を実行する
    Then review 終了コードが1である
    And review エラーメッセージが表示される

  Scenario: エディタが非ゼロ終了するとエラーになる
    Given Doorstop アイテム "QA-001" が存在する
    And エディタが非ゼロ終了コードを返す
    When `spec-weaver review QA-001` を実行する
    Then review 終了コードが1である
    And review エラーメッセージが表示される

  Scenario: --all で全 Doorstop アイテムを一括レビューできる（エディタなし）
    Given 複数のアクティブな Doorstop アイテムが存在する
    When `spec-weaver review --all` を実行する
    Then review 終了コードが0である
    And エディタが起動しない
    And アクティブな全 Doorstop アイテムがレビュー済みになる

  Scenario: --all と対象IDを同時に指定するとエラーになる
    When `spec-weaver review --all QA-001` を実行する
    Then review 終了コードが1である
    And review エラーメッセージが表示される

  Scenario: 引数も --all も指定しないとエラーになる
    When `spec-weaver review` を引数なしで実行する
    Then review 終了コードが1である
    And review エラーメッセージが表示される
