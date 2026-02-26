@SPEC-011
Feature: タイムスタンプ管理
  アイテムの作成日・最終更新日をカスタム属性として管理し、
  ドキュメント生成および監査で活用する。

  # --- カスタム属性の定義と取得 (SPEC-011) ---

  Scenario: created_at 属性の取得
    Given Doorstopアイテムに created_at: '2026-01-15' が設定されている
    When  タイムスタンプ属性を取得する
    Then  created_at として "2026-01-15" が返されること

  Scenario: updated_at 属性の取得
    Given Doorstopアイテムに updated_at: '2026-02-20' が設定されている
    When  タイムスタンプ属性を取得する
    Then  updated_at として "2026-02-20" が返されること

  Scenario: タイムスタンプ未設定時のフォールバック
    Given Doorstopアイテムに created_at も updated_at も設定されていない
    When  タイムスタンプ属性を取得する
    Then  両方とも None が返されること
    And   表示上は "-" となること

  # --- build コマンドへの表示統合 (SPEC-012) ---

  @SPEC-012
  Scenario: 一覧テーブルにタイムスタンプ列が表示される
    Given Doorstopアイテムに created_at と updated_at が設定されている
    When  build コマンドを実行する
    Then  一覧テーブルに「作成日」列が含まれること
    And   一覧テーブルに「更新日」列が含まれること
    And   設定された日付が正しく表示されること

  @SPEC-012
  Scenario: 詳細ページにタイムスタンプが表示される
    Given Doorstopアイテムに created_at と updated_at が設定されている
    When  build コマンドを実行する
    Then  詳細ページに作成日と更新日が表示されること
    And   実装状況バッジの直後に配置されていること

  @SPEC-012
  Scenario: タイムスタンプ未設定時の一覧テーブル表示
    Given Doorstopアイテムに created_at も updated_at も設定されていない
    When  build コマンドを実行する
    Then  一覧テーブルの作成日・更新日列に "-" が表示されること

  # --- 鮮度の監査チェック (SPEC-013) ---

  @SPEC-013
  Scenario: stale アイテムの検出
    Given Doorstopアイテムの updated_at が 91日前の日付である
    And   そのアイテムの status が "implemented" である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムが stale として報告されること
    And   経過日数が表示されること

  @SPEC-013
  Scenario: 閾値内のアイテムは stale と判定されない
    Given Doorstopアイテムの updated_at が 30日前の日付である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @SPEC-013
  Scenario: updated_at 未設定のアイテムは stale 判定の対象外
    Given Doorstopアイテムに updated_at が設定されていない
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @SPEC-013
  Scenario: deprecated アイテムは stale 判定の対象外
    Given Doorstopアイテムの status が "deprecated" である
    And   updated_at が 180日前の日付である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @SPEC-013
  Scenario: --stale-days 0 で鮮度チェックを無効化
    Given Doorstopアイテムの updated_at が 365日前の日付である
    When  audit コマンドを --stale-days 0 で実行する
    Then  stale に関する報告は表示されないこと
