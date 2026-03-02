# spec-weaver-fingerprint: 9a459b73e608b26276d27ad6be826dfdafb28b176f6b7c528b2240a313da2bac
# spec-weaver-fingerprint-QA-001: IVjwbWJI8Xga_1LFrHA_SqnpsZ_-MHzjo-w7D9zwEYE=
# spec-weaver-fingerprint-VIS-001: vS8HMajMu_ierl6Dvv5xBk1dtLB30WMIGR7OIcwtLdk=
# spec-weaver-fingerprint-VIS-005: cnyg43CeR6DlR-nhO8_IOS6ZTbkaQoU6UoJyLvsS-JY=
# spec-weaver-fingerprint-VIS-008: 7sf3VezCdcJHKBaReMXoTyez2UxrlkvvZ8PvQBGdcA8=
@VIS-001
Feature: build コマンド
  Doorstopの仕様データとGherkinテストを統合した
  MkDocsドキュメントサイトを自動生成する。

  Scenario: MkDocs設定ファイルの生成
    Given DoorstopプロジェクトとGherkin featureファイルが存在する
    When  build コマンドを実行する
    Then  出力ディレクトリに mkdocs.yml が生成されること
    And   Material テーマが設定されていること

  Scenario: 要件一覧ページの生成
    Given DoorstopプロジェクトにREQアイテムが存在する
    When  build コマンドを実行する
    Then  docs/req.md が生成されること
    And   各REQアイテムがテーブル行として含まれること
    And   関連仕様への相互リンクが含まれること

  Scenario: 仕様一覧ページの生成
    Given DoorstopプロジェクトにSPECアイテムが存在する
    When  build コマンドを実行する
    Then  docs/spec.md が生成されること
    And   各SPECアイテムがテーブル行として含まれること
    And   上位要件への相互リンクが含まれること

  Scenario: 個別アイテム詳細ページの生成
    Given DoorstopプロジェクトにアイテムとGherkinテストが存在する
    When  build コマンドを実行する
    Then  docs/items/ 配下に各アイテムのMarkdownファイルが生成されること
    And   アイテムの本文が含まれること
    And   上位・下位リンクが含まれること
    And   対応するテストシナリオのファイルパスと行番号が含まれること

  @VIS-005
  Scenario: 一覧テーブルのフィルタリング機能
    Given Doorstopプロジェクトにアイテムが存在する
    When  build コマンドを実行する
    Then  生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること
    And   ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること

  Scenario: 出力ディレクトリの独立性
    Given プロジェクトに既存のドキュメントが存在する
    When  build コマンドをデフォルト出力先で実行する
    Then  ".specification" ディレクトリに出力されること
    And   既存のドキュメントファイルは変更されないこと

  Scenario: カスタム出力ディレクトリの指定
    Given DoorstopプロジェクトとGherkin featureファイルが存在する
    When  build コマンドを --out-dir "./custom_docs" で実行する
    Then  "./custom_docs" ディレクトリに出力されること

  @VIS-008
  Scenario: feature MDページへのバックリンク生成
    Given "@SPEC-003" タグを持つ "audit.feature" が存在する
    When  build コマンドを実行する
    Then  "docs/features/audit.md" の冒頭に "関連アイテム" セクションが含まれること
    And   "[SPEC-003](../items/SPEC-003.md)" へのリンクが含まれること

  @VIS-008
  Scenario: 複数アイテムを参照するfeatureのバックリンク
    Given "@VIS-001" と "@VIS-005" の両タグを持つfeatureが存在する
    When  build コマンドを実行する
    Then  生成されたfeature MDの "関連アイテム" に "VIS-001" と "VIS-005" の両方のリンクが含まれること

  @VIS-008
  Scenario: タグのないfeatureにはバックリンクを表示しない
    Given どのDoorstopアイテムからも参照されていないfeatureが存在する
    When  build コマンドを実行する
    Then  生成されたfeature MDに "関連アイテム" 行が含まれないこと

  @QA-001
  Scenario: Suspect Link 警告の一覧テーブル表示
    Given アイテムの上位リンク先が変更されている（cleared=false）
    When  build コマンドを実行する
    Then  一覧テーブルの行に "{: .suspect-row }" が適用されていること
    And   詳細ページに Suspect Link バナーが表示されること

  @QA-001
  Scenario: Unreviewed Changes 警告の一覧テーブル表示
    Given アイテム自体に未レビューの変更がある（reviewed=false）
    When  build コマンドを実行する
    Then  一覧テーブルの行に "{: .unreviewed-row }" が適用されていること
    And   詳細ページに Unreviewed Changes バナーが表示されること

  @QA-001
  Scenario: 複合警告の表示
    Given アイテムに Suspect Link と Unreviewed Changes の両方がある
    When  build コマンドを実行する
    Then  一覧テーブルの行に "{: .suspect-row }" が適用されていること

  Scenario: 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
    Given 2つのシナリオを持つfeatureファイルにタグで紐づいたSPECアイテムが存在する
    When  build コマンドを実行する
    Then  一覧テーブルの Gherkinカバレッジ列に "🟢 2" が含まれること

  Scenario: 一覧テーブルにレビューステータス列が表示されること
    Given DoorstopプロジェクトにSPECアイテムが存在する
    When  build コマンドを実行する
    Then  一覧テーブルのヘッダーに "レビュー" 列が含まれること
    And   各行にレビューステータスが表示されること
