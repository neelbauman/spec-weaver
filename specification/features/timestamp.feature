# spec-weaver-fingerprint: da96d085750ad925a01239120c8024c82745d513fe7bcda1e9ba144c448a9023
# spec-weaver-fingerprint-QA-002: pIUDUCm2SbEPeLzmScATm5kxQXhzHgfNLVTet64j5OY=
# spec-weaver-fingerprint-VIS-006: X_KRBM_YhZCFigeGpRMit5ZIjnIx1JMby0egIg10egw=
# spec-weaver-fingerprint-VIS-007: yOFv-Mqqd6cmn9y-BMHTC3-5N_plpH_vbw4UzEypfk8=
@VIS-006
Feature: タイムスタンプ管理
  アイテムの作成日・最終更新日をGit履歴から自動取得し、
  ドキュメント生成および監査で活用する。

  # --- Git履歴からの自動取得 (VIS-006) ---

  Scenario: Git履歴から updated_at を自動取得する
    Given DoorstopアイテムのYAMLファイルがGitにコミットされている
    When  タイムスタンプ属性を取得する
    Then  updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

  Scenario: Git履歴から created_at を自動取得する
    Given DoorstopアイテムのYAMLファイルがGitにコミットされている
    When  タイムスタンプ属性を取得する
    Then  created_at として初回コミット日が YYYY-MM-DD 形式で返されること

  Scenario: Git情報がない場合はYAML属性にフォールバック
    Given DoorstopアイテムのYAMLファイルがGit管理外である
    And   YAMLに created_at: '2026-01-15' が設定されている
    When  タイムスタンプ属性を取得する
    Then  created_at として "2026-01-15" が返されること

  Scenario: Git情報もYAML属性もない場合のフォールバック
    Given DoorstopアイテムのYAMLファイルがGit管理外である
    And   YAMLに created_at も updated_at も設定されていない
    When  タイムスタンプ属性を取得する
    Then  両方とも "-" が返されること

  # --- build コマンドへの表示統合 (VIS-007) ---

  @VIS-007
  Scenario: 一覧テーブルにタイムスタンプ列が表示される
    Given DoorstopアイテムがGitにコミットされている
    When  build コマンドを実行する
    Then  一覧テーブルに「作成日」列が含まれること
    And   一覧テーブルに「更新日」列が含まれること
    And   Git履歴から取得した日付が正しく表示されること

  @VIS-007
  Scenario: 詳細ページにタイムスタンプが表示される
    Given DoorstopアイテムがGitにコミットされている
    When  build コマンドを実行する
    Then  詳細ページに作成日と更新日が表示されること
    And   実装状況バッジの直後に配置されていること

  @VIS-007
  Scenario: Git情報がない場合の一覧テーブル表示
    Given DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない
    When  build コマンドを実行する
    Then  一覧テーブルの作成日・更新日列に "-" が表示されること

  # --- 鮮度の監査チェック (QA-002) ---

  @QA-002
  Scenario: stale アイテムの検出（Git履歴ベース）
    Given Doorstopアイテムの最終コミット日が 91日前である
    And   そのアイテムの status が "implemented" である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムが stale として報告されること
    And   経過日数が表示されること
    And   タイムスタンプ監査の終了コードが 1 であること

  @QA-002
  Scenario: 閾値内のアイテムは stale と判定されない
    Given Doorstopアイテムの最終コミット日が 30日前である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @QA-002
  Scenario: Git情報もupdated_atもないアイテムは stale 判定の対象外
    Given DoorstopアイテムがGit管理外でupdated_atも設定されていない
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @QA-002
  Scenario: deprecated アイテムは stale 判定の対象外
    Given 最終コミット日が 180日前である
    And   Doorstopアイテムの status が "deprecated" である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @QA-002
  Scenario: --stale-days 0 で鮮度チェックを無効化
    Given Doorstopアイテムの最終コミット日が 365日前である
    When  audit コマンドを --stale-days 0 で実行する
    Then  stale に関する報告は表示されないこと
