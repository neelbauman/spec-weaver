@SPEC-015
Feature: scaffold コマンド
  .feature ファイルから behave テストコードの雛形を自動生成・差分マージする。

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

  Scenario: Docstring にシナリオリストを記載
    Given ".feature" ファイルが存在するディレクトリがある
    When  scaffold コマンドを実行する
    Then  各ステップ関数の Docstring に "Scenarios:" セクションが含まれること
    And   そのステップを使用するシナリオ名が列挙されること

  Scenario: 差分マージ（新規ステップ追記）
    Given 出力先に既存のテストファイルが存在する
    And   .feature に既存ファイルにないステップが追加されている
    When  scaffold コマンドをデフォルトオプションで実行する
    Then  既存ファイルに新規ステップのみが追記されること
    And   既存のステップ定義は保持されること
    And   新規ステップは .feature の出現順で挿入されること

  Scenario: 差分なし時のスキップ
    Given 出力先の既存テストファイルが .feature と完全に同期している
    When  scaffold コマンドをデフォルトオプションで実行する
    Then  ファイルへの書き込みは行われないこと
    And   スキップ（差分なし）が表示されること

  Scenario: 既存ファイルの上書き
    Given 出力先に既存のテストファイルが存在する
    When  scaffold コマンドを "--overwrite" オプション付きで実行する
    Then  既存ファイルが上書きされること

  Scenario: Git 未コミット変更の確認プロンプト
    Given 出力先のテストファイルに未コミットの変更がある
    When  scaffold コマンドをデフォルトオプションで実行する
    Then  マージするか確認プロンプトが表示されること
    And   キャンセルするとそのファイルはスキップされること

  Scenario: --force オプションで確認プロンプトをスキップ
    Given 出力先のテストファイルに未コミットの変更がある
    When  scaffold コマンドを "--force" オプション付きで実行する
    Then  確認プロンプトなしでマージが実行されること
