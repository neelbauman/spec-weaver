@SPEC-022
Feature: review コマンド — セマンティックレビュー
  仕様・Gherkin・実装コードの意味的整合性をLLMで検証し、
  実装漏れ・仕様欠落・意味的矛盾を finding として報告する。

  Scenario: 単一アイテムのレビューが実行できる
    Given claudeコマンドが利用可能である
    And 仕様アイテム "SPEC-003" が存在する
    When `spec-weaver review --item SPEC-003 --feature-dir ./specification/features` を実行する
    Then 終了コードが0である
    And 出力にレビュー結果が含まれる

  Scenario: 単一アイテムをJSON形式で出力できる
    Given claudeコマンドが利用可能である
    And 仕様アイテム "SPEC-003" が存在する
    When `spec-weaver review --item SPEC-003 --output json` を実行する
    Then 終了コードが0である
    And 出力が有効なJSONである
    And JSONに "item_id" フィールドが含まれる
    And JSONに "findings" フィールドが含まれる
    And JSONに "summary" フィールドが含まれる

  Scenario: 存在しないアイテムIDを指定するとエラーになる
    When `spec-weaver review --item NOTEXIST-999` を実行する
    Then 終了コードが1である
    And エラーメッセージが表示される

  Scenario: --item と --all は同時に指定できない
    When `spec-weaver review --item SPEC-003 --all` を実行する
    Then 終了コードが2である

  Scenario: --fail-on high でhigh findingがある場合に終了コード1を返す
    Given claudeコマンドが利用可能である
    And レビュー結果に severity "high" のfindingが含まれる
    When `spec-weaver review --item SPEC-003 --fail-on high` を実行する
    Then 終了コードが1である

  Scenario: --fail-on high でhigh findingがない場合に終了コード0を返す
    Given claudeコマンドが利用可能である
    And レビュー結果に severity "high" のfindingが含まれない
    When `spec-weaver review --item SPEC-003 --fail-on high` を実行する
    Then 終了コードが0である

  Scenario: --min-severity medium で low の finding が非表示になる
    Given claudeコマンドが利用可能である
    When `spec-weaver review --item SPEC-003 --min-severity medium` を実行する
    Then 終了コードが0である
    And severity "low" のfindingは出力に含まれない

  Scenario: claudeコマンドが見つからない場合にエラーになる
    Given claudeコマンドが利用不可能である
    When `spec-weaver review --item SPEC-003` を実行する
    Then 終了コードが1である
    And "claude" に関するエラーメッセージが表示される
