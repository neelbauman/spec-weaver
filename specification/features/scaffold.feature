@SPEC-015
Feature: scaffold コマンド
  .feature ファイルから behave テストコードの雛形を自動生成する。

  Scenario: 基本的なテストコード生成
    Given ".feature" ファイルが存在するディレクトリがある
    When  scaffold コマンドを実行する
    Then  各 .feature に対応する "step_<stem>.py" が生成されること
    And   各ステップに "@given", "@when", "@then" デコレータ付き関数が含まれること

  Scenario: ハッシュベースの関数名生成
    Given 日本語のシナリオ名を持つ .feature ファイルがある
    When  scaffold コマンドを実行する
    Then  生成されたステップ関数名が ASCII 文字のみで構成されること
    And   関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること
    And   docstring にオリジナルのステップ文が記載されること

  Scenario: ステップ関数の生成と重複排除
    Given 複数のシナリオで同一のステップ文が使用されている
    When  scaffold コマンドを実行する
    Then  同一ステップに対する関数は1回のみ生成されること

  Scenario: 既存ファイルのスキップ
    Given 出力先に既存のテストファイルが存在する
    When  scaffold コマンドをデフォルトオプションで実行する
    Then  既存ファイルはスキップされること
    And   スキップされた旨の警告が表示されること

  Scenario: 既存ファイルの上書き
    Given 出力先に既存のテストファイルが存在する
    When  scaffold コマンドを "--overwrite" オプション付きで実行する
    Then  既存ファイルが上書きされること
