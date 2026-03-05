@CORE-003
Feature: AST解析結果の同期とCLIフレンドリー化 (Sync Command)
  仕様と実装・テストの紐づけ情報をDoorstopのYAMLファイルに直接書き込むことで、
  grepやjqなどの標準CLIツールから容易に検索・集計できる「CLIフレンドリー」な状態を実現する。

  Background:
    Given Sync用Doorstopツリーが初期化されている

  Scenario: spec-weaver sync コマンドで feature_files が同期される
    Given "specification/features/sample.feature" に "@SPEC-001" タグを持つシナリオが存在する
    When "spec-weaver sync --feature-dir specification/features" を実行する（sync用）
    Then "SPEC-001" のYAMLファイルに "feature_files" 属性が追加されること
    And その属性に "specification/features/sample.feature" が含まれること

  Scenario: spec-weaver sync コマンドで scanned_impl_files が同期される
    Given "src/sample.py" に "# implements: SPEC-002" アノテーションが存在する
    When "spec-weaver sync" を実行する（sync用）
    Then "SPEC-002" のYAMLファイルに "scanned_impl_files" 属性が追加されること
    And その属性に "src/sample.py" が含まれること
