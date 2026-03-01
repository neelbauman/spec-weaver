"""behave steps for: データ抽出基盤"""

from behave import given, when, then, step

# ======================================================================
# Steps
# ======================================================================

@given('Doorstopプロジェクトにアクティブな仕様アイテムが存在する')  # type: ignore
def given_a04781e9(context):
    """Doorstopプロジェクトにアクティブな仕様アイテムが存在する

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
    """
    raise NotImplementedError('STEP: Doorstopプロジェクトにアクティブな仕様アイテムが存在する')


@when('仕様ID集合を取得する')  # type: ignore
def when_e56707cb(context):
    """仕様ID集合を取得する

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
      - 非アクティブなアイテムの除外
      - テスト不可能な仕様の除外
    """
    raise NotImplementedError('STEP: 仕様ID集合を取得する')


@then('アクティブかつtestableな仕様IDのみが返されること')  # type: ignore
def then_6823b180(context):
    """アクティブかつtestableな仕様IDのみが返されること

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
    """
    raise NotImplementedError('STEP: アクティブかつtestableな仕様IDのみが返されること')


@given('Doorstopプロジェクトに active: false のアイテムが存在する')  # type: ignore
def given_dccca3dc(context):
    """Doorstopプロジェクトに active: false のアイテムが存在する

    Scenarios:
      - 非アクティブなアイテムの除外
    """
    raise NotImplementedError('STEP: Doorstopプロジェクトに active: false のアイテムが存在する')


@then('非アクティブなアイテムは結果に含まれないこと')  # type: ignore
def then_99bfaa46(context):
    """非アクティブなアイテムは結果に含まれないこと

    Scenarios:
      - 非アクティブなアイテムの除外
    """
    raise NotImplementedError('STEP: 非アクティブなアイテムは結果に含まれないこと')


@given('Doorstopプロジェクトに testable: false のアイテムが存在する')  # type: ignore
def given_d534a041(context):
    """Doorstopプロジェクトに testable: false のアイテムが存在する

    Scenarios:
      - テスト不可能な仕様の除外
    """
    raise NotImplementedError('STEP: Doorstopプロジェクトに testable: false のアイテムが存在する')


@then('testable: false のアイテムは結果に含まれないこと')  # type: ignore
def then_f3fad2a6(context):
    """testable: false のアイテムは結果に含まれないこと

    Scenarios:
      - テスト不可能な仕様の除外
    """
    raise NotImplementedError('STEP: testable: false のアイテムは結果に含まれないこと')


@given('DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する')  # type: ignore
def given_7f8e9c65(context):
    """DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    raise NotImplementedError('STEP: DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する')


@when('プレフィックス "{param0}" で仕様ID集合を取得する')  # type: ignore
def when_1d11bcd6(context, param0):
    """プレフィックス "SPEC" で仕様ID集合を取得する

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    raise NotImplementedError('STEP: プレフィックス "{param0}" で仕様ID集合を取得する')


@then('SPECプレフィックスのアイテムのみが返されること')  # type: ignore
def then_b5f39418(context):
    """SPECプレフィックスのアイテムのみが返されること

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    raise NotImplementedError('STEP: SPECプレフィックスのアイテムのみが返されること')


@given('Gherkin .feature ファイルに @SPEC-001 タグが付与されている')  # type: ignore
def given_b830a393(context):
    """Gherkin .feature ファイルに @SPEC-001 タグが付与されている

    Scenarios:
      - Gherkin ASTからのタグ抽出
    """
    raise NotImplementedError('STEP: Gherkin .feature ファイルに @SPEC-001 タグが付与されている')


@when('タグ集合を取得する')  # type: ignore
def when_a12b8a55(context):
    """タグ集合を取得する

    Scenarios:
      - Gherkin ASTからのタグ抽出
      - Feature・Scenario両レベルのタグ抽出
      - サブディレクトリ内のfeatureファイルの再帰探索
      - Gherkin構文エラーの検出
    """
    raise NotImplementedError('STEP: タグ集合を取得する')


@then('"{param0}" がタグ集合に含まれること')  # type: ignore
def then_e8d01468(context, param0):
    """"SPEC-001" がタグ集合に含まれること

    Scenarios:
      - Gherkin ASTからのタグ抽出
    """
    raise NotImplementedError('STEP: "{param0}" がタグ集合に含まれること')


@given('Feature レベルと Scenario レベルに異なるSPECタグが付与されている')  # type: ignore
def given_07def24f(context):
    """Feature レベルと Scenario レベルに異なるSPECタグが付与されている

    Scenarios:
      - Feature・Scenario両レベルのタグ抽出
    """
    raise NotImplementedError('STEP: Feature レベルと Scenario レベルに異なるSPECタグが付与されている')


@then('両方のレベルのタグがすべて抽出されること')  # type: ignore
def then_d712dc38(context):
    """両方のレベルのタグがすべて抽出されること

    Scenarios:
      - Feature・Scenario両レベルのタグ抽出
    """
    raise NotImplementedError('STEP: 両方のレベルのタグがすべて抽出されること')


@given('サブディレクトリに .feature ファイルが存在する')  # type: ignore
def given_1427ca58(context):
    """サブディレクトリに .feature ファイルが存在する

    Scenarios:
      - サブディレクトリ内のfeatureファイルの再帰探索
    """
    raise NotImplementedError('STEP: サブディレクトリに .feature ファイルが存在する')


@then('サブディレクトリ内のタグも含めて抽出されること')  # type: ignore
def then_1c0ec472(context):
    """サブディレクトリ内のタグも含めて抽出されること

    Scenarios:
      - サブディレクトリ内のfeatureファイルの再帰探索
    """
    raise NotImplementedError('STEP: サブディレクトリ内のタグも含めて抽出されること')


@given('構文的に不正な .feature ファイルが存在する')  # type: ignore
def given_540458bc(context):
    """構文的に不正な .feature ファイルが存在する

    Scenarios:
      - Gherkin構文エラーの検出
    """
    raise NotImplementedError('STEP: 構文的に不正な .feature ファイルが存在する')


@then('ValueError が発生しGherkin構文エラーが報告されること')  # type: ignore
def then_c5d0b4fe(context):
    """ValueError が発生しGherkin構文エラーが報告されること

    Scenarios:
      - Gherkin構文エラーの検出
    """
    raise NotImplementedError('STEP: ValueError が発生しGherkin構文エラーが報告されること')


@given('Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない')  # type: ignore
def given_630f9d2e(context):
    """Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない

    Scenarios:
      - Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
    """
    raise NotImplementedError('STEP: Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない')


@when('タグマップを取得する')  # type: ignore
def when_24daec1e(context):
    """タグマップを取得する

    Scenarios:
      - Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
      - Featureタグを継承したエントリのkeywordはScenarioになる
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    raise NotImplementedError('STEP: タグマップを取得する')


@then('その仕様タグのエントリにシナリオの情報が紐付けられること')  # type: ignore
def then_2c7421ae(context):
    """その仕様タグのエントリにシナリオの情報が紐付けられること

    Scenarios:
      - Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
    """
    raise NotImplementedError('STEP: その仕様タグのエントリにシナリオの情報が紐付けられること')


@given('Feature レベルにのみ仕様タグが付与されている')  # type: ignore
def given_8bed9a12(context):
    """Feature レベルにのみ仕様タグが付与されている

    Scenarios:
      - Featureタグを継承したエントリのkeywordはScenarioになる
    """
    raise NotImplementedError('STEP: Feature レベルにのみ仕様タグが付与されている')


@then('tag_map エントリの keyword が "{param0}" または "{param1}" であること')  # type: ignore
def then_92430f3a(context, param0, param1):
    """tag_map エントリの keyword が "Scenario" または "Scenario Outline" であること

    Scenarios:
      - Featureタグを継承したエントリのkeywordはScenarioになる
    """
    raise NotImplementedError('STEP: tag_map エントリの keyword が "{param0}" または "{param1}" であること')


@given('Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている')  # type: ignore
def given_5a96b103(context):
    """Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    raise NotImplementedError('STEP: Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている')


@given('Rule 配下のシナリオにはタグが付いていない')  # type: ignore
def given_b89243df(context):
    """Rule 配下のシナリオにはタグが付いていない

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    raise NotImplementedError('STEP: Rule 配下のシナリオにはタグが付いていない')


@then('そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること')  # type: ignore
def then_769bc618(context):
    """そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    raise NotImplementedError('STEP: そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること')


@given('Feature レベルに仕様タグ A が付与されている')  # type: ignore
def given_2ea31132(context):
    """Feature レベルに仕様タグ A が付与されている

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    raise NotImplementedError('STEP: Feature レベルに仕様タグ A が付与されている')


@given('配下のシナリオに直接 仕様タグ B が付与されている')  # type: ignore
def given_07eca074(context):
    """配下のシナリオに直接 仕様タグ B が付与されている

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    raise NotImplementedError('STEP: 配下のシナリオに直接 仕様タグ B が付与されている')


@then('そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること')  # type: ignore
def then_4386e28c(context):
    """そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    raise NotImplementedError('STEP: そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること')


@given('Scenario Outline に仕様タグ A が付与されている')  # type: ignore
def given_c475ab28(context):
    """Scenario Outline に仕様タグ A が付与されている

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    raise NotImplementedError('STEP: Scenario Outline に仕様タグ A が付与されている')


@given('いずれかの Examples テーブルに仕様タグ B が付与されている')  # type: ignore
def given_224c4b5d(context):
    """いずれかの Examples テーブルに仕様タグ B が付与されている

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    raise NotImplementedError('STEP: いずれかの Examples テーブルに仕様タグ B が付与されている')


@then('仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること')  # type: ignore
def then_f65c91e7(context):
    """仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    raise NotImplementedError('STEP: 仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること')


@given('Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている')  # type: ignore
def given_8f7f4921(context):
    """Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    raise NotImplementedError('STEP: Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている')


@when('プレフィックス "{param0}" でタグマップを取得する')  # type: ignore
def when_1bf4e117(context, param0):
    """プレフィックス "SPEC" でタグマップを取得する

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    raise NotImplementedError('STEP: プレフィックス "{param0}" でタグマップを取得する')


@then('"{param0}" のみがタグマップに含まれ "{param1}" は含まれないこと')  # type: ignore
def then_237adb2e(context, param0, param1):
    """"SPEC-001" のみがタグマップに含まれ "REQ-001" は含まれないこと

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    raise NotImplementedError('STEP: "{param0}" のみがタグマップに含まれ "{param1}" は含まれないこと')
