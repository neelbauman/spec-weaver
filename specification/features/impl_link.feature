# spec-weaver-fingerprint: b811f33b65429d4bb62aa6ed1e234420882eb37e2a3270541e5030282efd3be7
# spec-weaver-fingerprint-QA-003: R7lU5c_GYfAMywWH7ga7C5bNWLi0BcEk_ct5FCCzLOg=
# spec-weaver-fingerprint-TRC-002: CsNYG2kwoAL2aGQ4OMJZPbq_BdQL1XO9mD52BES64WU=
# spec-weaver-fingerprint-TRC-003: HejBnkVVAXr50mezShqlLJuFqDQgnm2Ll2xq1IrX7wY=
# spec-weaver-fingerprint-TRC-004: taSaPJAOYmNABY3Fq9QzpfuL400jN9dj2MpQSufRkT8=
@TRC-002 @TRC-003 @QA-003 @TRC-004
Feature: 仕様アイテムと実装ファイルのリンク管理
  DoorstopのYAML impl_files カスタム属性とコードアノテーションを組み合わせて、
  仕様と実装ファイルの双方向トレーサビリティを実現する。

  Background:
    Given Doorstopツリーが初期化されている
    And 以下のSPECアイテムが存在する:
      | ID       | Header             | impl_files                       |
      | TRC-003 | アノテーションスキャン | src/spec_weaver/impl_scanner.py |
      | QA-003 | audit拡張          |                                  |

  # ---- TRC-002: impl_files カスタム属性 ----

  @TRC-002
  Scenario: impl_files にリスト形式でファイルパスを記述できる
    Given TRC-003 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている
    When impl_files を読み取る
    Then ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

  @TRC-002
  Scenario: impl_files が未設定の場合はリンクなしとして扱われる
    Given QA-003 の impl_files が未設定である
    When impl_files を読み取る
    Then 空のリストが返ること

  # ---- TRC-003: アノテーションスキャン ----

  @TRC-003
  Scenario: アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
    Given "src/spec_weaver/impl_scanner.py" の行頭に "# implements: TRC-003" が記述されている
    When impl-scanner でリポジトリをスキャンする
    Then "TRC-003" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

  @TRC-003
  Scenario: 1行に複数の仕様IDを記述できる
    Given "src/spec_weaver/cli.py" の行頭に "# implements: QA-003, TRC-004" が記述されている
    When impl-scanner でリポジトリをスキャンする
    Then "QA-003" に対して "src/spec_weaver/cli.py" が紐づくこと
    And  "TRC-004" に対して "src/spec_weaver/cli.py" が紐づくこと

  @TRC-003
  Scenario: --extensions オプションでスキャン対象を絞れる
    Given リポジトリに .py ファイルと .md ファイルが存在する
    And .md ファイルの行頭に "# implements: TRC-003" が記述されている
    When --extensions py を指定して impl-scanner でスキャンする
    Then .md ファイルは結果に含まれないこと

  @TRC-003
  Scenario: アノテーションがないファイルはエラーにならない
    Given "src/spec_weaver/gherkin.py" にアノテーションが存在しない
    When impl-scanner でリポジトリをスキャンする
    Then エラーが発生しないこと

  # ---- QA-003: audit 拡張 ----

  @QA-003
  Scenario: --check-impl オプションで存在しないファイルへの impl_files を検出する
    Given QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
    When "spec-weaver audit --check-impl" を実行する
    Then 終了コードが 1 であること
    And  "nonexistent.py" が存在しないファイルとして報告されること

  @QA-003
  Scenario: impl_files にあってアノテーションがない場合は警告を報告する
    Given TRC-003 の impl_files に "src/spec_weaver/cli.py" が設定されている
    And "src/spec_weaver/cli.py" に TRC-003 のアノテーションが存在しない
    When "spec-weaver audit --check-impl" を実行する
    Then "TRC-003 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

  @QA-003
  Scenario: アノテーションがあって impl_files がない場合は警告を報告する
    Given "src/spec_weaver/gherkin.py" の行頭に "# implements: QA-003" が記述されている
    And QA-003 の impl_files が未設定である
    When "spec-weaver audit --check-impl" を実行する
    Then "QA-003 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

  @QA-003
  Scenario: --check-impl なしでは実装リンク検証は実行されない
    Given QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
    When 通常の "spec-weaver audit" を実行する（--check-impl なし）
    Then 実装ファイルリンクのセクションが出力されないこと

  # ---- TRC-004: trace 拡張 ----

  @TRC-004
  Scenario: --show-impl オプションで trace ツリーに実装ファイルを表示する
    Given TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
    When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
    Then 出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

  @TRC-004
  Scenario: アノテーション由来のファイルも trace ツリーに表示される
    Given "src/spec_weaver/cli.py" の行頭に "# implements: TRC-003" が記述されている
    And TRC-003 の impl_files が未設定である
    When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
    Then 出力ツリーに "src/spec_weaver/cli.py" が含まれること

  @TRC-004
  Scenario: --show-impl なしでは実装ファイルは表示されない
    Given TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
    When "spec-weaver trace TRC-003 -f ./specification/features" を実行する（--show-impl なし）
    Then 出力ツリーに "impl_scanner.py" が含まれないこと
