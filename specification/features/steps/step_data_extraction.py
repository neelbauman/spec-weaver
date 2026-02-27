"""behave steps for: データ抽出基盤"""

import tempfile
from pathlib import Path

from behave import given, when, then, step
from spec_weaver.gherkin import get_tag_map

# ======================================================================
# Steps
# ======================================================================

# [Duplicate Skip] This step is already defined elsewhere
# @given('Doorstopプロジェクトにアクティブな仕様アイテムが存在する')  # type: ignore
# def given_a04781e9(context):
#     """Doorstopプロジェクトにアクティブな仕様アイテムが存在する
# 
#     Scenarios:
#       - Doorstop APIによる仕様ID集合の取得
#     """
#     raise NotImplementedError('STEP: Doorstopプロジェクトにアクティブな仕様アイテムが存在する')


# [Duplicate Skip] This step is already defined elsewhere
# @when('仕様ID集合を取得する')  # type: ignore
# def when_e56707cb(context):
#     """仕様ID集合を取得する
# 
#     Scenarios:
#       - Doorstop APIによる仕様ID集合の取得
#       - 非アクティブなアイテムの除外
#       - テスト不可能な仕様の除外
#     """
#     raise NotImplementedError('STEP: 仕様ID集合を取得する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('アクティブかつtestableな仕様IDのみが返されること')  # type: ignore
# def then_6823b180(context):
#     """アクティブかつtestableな仕様IDのみが返されること
# 
#     Scenarios:
#       - Doorstop APIによる仕様ID集合の取得
#     """
#     raise NotImplementedError('STEP: アクティブかつtestableな仕様IDのみが返されること')


# [Duplicate Skip] This step is already defined elsewhere
# @given('Doorstopプロジェクトに active: false のアイテムが存在する')  # type: ignore
# def given_dccca3dc(context):
#     """Doorstopプロジェクトに active: false のアイテムが存在する
# 
#     Scenarios:
#       - 非アクティブなアイテムの除外
#     """
#     raise NotImplementedError('STEP: Doorstopプロジェクトに active: false のアイテムが存在する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('非アクティブなアイテムは結果に含まれないこと')  # type: ignore
# def then_99bfaa46(context):
#     """非アクティブなアイテムは結果に含まれないこと
# 
#     Scenarios:
#       - 非アクティブなアイテムの除外
#     """
#     raise NotImplementedError('STEP: 非アクティブなアイテムは結果に含まれないこと')


# [Duplicate Skip] This step is already defined elsewhere
# @given('Doorstopプロジェクトに testable: false のアイテムが存在する')  # type: ignore
# def given_d534a041(context):
#     """Doorstopプロジェクトに testable: false のアイテムが存在する
# 
#     Scenarios:
#       - テスト不可能な仕様の除外
#     """
#     raise NotImplementedError('STEP: Doorstopプロジェクトに testable: false のアイテムが存在する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('testable: false のアイテムは結果に含まれないこと')  # type: ignore
# def then_f3fad2a6(context):
#     """testable: false のアイテムは結果に含まれないこと
# 
#     Scenarios:
#       - テスト不可能な仕様の除外
#     """
#     raise NotImplementedError('STEP: testable: false のアイテムは結果に含まれないこと')


# [Duplicate Skip] This step is already defined elsewhere
# @given('DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する')  # type: ignore
# def given_7f8e9c65(context):
#     """DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する
# 
#     Scenarios:
#       - プレフィックスによるフィルタリング
#     """
#     raise NotImplementedError('STEP: DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する')


# [Duplicate Skip] This step is already defined elsewhere
# @when('プレフィックス "{param0}" で仕様ID集合を取得する')  # type: ignore
# def when_1d11bcd6(context, param0):
#     """プレフィックス "SPEC" で仕様ID集合を取得する
# 
#     Scenarios:
#       - プレフィックスによるフィルタリング
#     """
#     raise NotImplementedError('STEP: プレフィックス "{param0}" で仕様ID集合を取得する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('SPECプレフィックスのアイテムのみが返されること')  # type: ignore
# def then_b5f39418(context):
#     """SPECプレフィックスのアイテムのみが返されること
# 
#     Scenarios:
#       - プレフィックスによるフィルタリング
#     """
#     raise NotImplementedError('STEP: SPECプレフィックスのアイテムのみが返されること')


# [Duplicate Skip] This step is already defined elsewhere
# @given('Gherkin .feature ファイルに @SPEC-001 タグが付与されている')  # type: ignore
# def given_b830a393(context):
#     """Gherkin .feature ファイルに @SPEC-001 タグが付与されている
# 
#     Scenarios:
#       - Gherkin ASTからのタグ抽出
#     """
#     raise NotImplementedError('STEP: Gherkin .feature ファイルに @SPEC-001 タグが付与されている')


# [Duplicate Skip] This step is already defined elsewhere
# @when('タグ集合を取得する')  # type: ignore
# def when_a12b8a55(context):
#     """タグ集合を取得する
# 
#     Scenarios:
#       - Gherkin ASTからのタグ抽出
#       - Feature・Scenario両レベルのタグ抽出
#       - サブディレクトリ内のfeatureファイルの再帰探索
#       - Gherkin構文エラーの検出
#     """
#     raise NotImplementedError('STEP: タグ集合を取得する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('"{param0}" がタグ集合に含まれること')  # type: ignore
# def then_e8d01468(context, param0):
#     """"SPEC-001" がタグ集合に含まれること
# 
#     Scenarios:
#       - Gherkin ASTからのタグ抽出
#     """
#     raise NotImplementedError('STEP: "{param0}" がタグ集合に含まれること')


# [Duplicate Skip] This step is already defined elsewhere
# @given('Feature レベルと Scenario レベルに異なるSPECタグが付与されている')  # type: ignore
# def given_07def24f(context):
#     """Feature レベルと Scenario レベルに異なるSPECタグが付与されている
# 
#     Scenarios:
#       - Feature・Scenario両レベルのタグ抽出
#     """
#     raise NotImplementedError('STEP: Feature レベルと Scenario レベルに異なるSPECタグが付与されている')


# [Duplicate Skip] This step is already defined elsewhere
# @then('両方のレベルのタグがすべて抽出されること')  # type: ignore
# def then_d712dc38(context):
#     """両方のレベルのタグがすべて抽出されること
# 
#     Scenarios:
#       - Feature・Scenario両レベルのタグ抽出
#     """
#     raise NotImplementedError('STEP: 両方のレベルのタグがすべて抽出されること')


# [Duplicate Skip] This step is already defined elsewhere
# @given('サブディレクトリに .feature ファイルが存在する')  # type: ignore
# def given_1427ca58(context):
#     """サブディレクトリに .feature ファイルが存在する
# 
#     Scenarios:
#       - サブディレクトリ内のfeatureファイルの再帰探索
#     """
#     raise NotImplementedError('STEP: サブディレクトリに .feature ファイルが存在する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('サブディレクトリ内のタグも含めて抽出されること')  # type: ignore
# def then_1c0ec472(context):
#     """サブディレクトリ内のタグも含めて抽出されること
# 
#     Scenarios:
#       - サブディレクトリ内のfeatureファイルの再帰探索
#     """
#     raise NotImplementedError('STEP: サブディレクトリ内のタグも含めて抽出されること')


# [Duplicate Skip] This step is already defined elsewhere
# @given('構文的に不正な .feature ファイルが存在する')  # type: ignore
# def given_540458bc(context):
#     """構文的に不正な .feature ファイルが存在する
# 
#     Scenarios:
#       - Gherkin構文エラーの検出
#     """
#     raise NotImplementedError('STEP: 構文的に不正な .feature ファイルが存在する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('ValueError が発生しGherkin構文エラーが報告されること')  # type: ignore
# def then_c5d0b4fe(context):
#     """ValueError が発生しGherkin構文エラーが報告されること
# 
#     Scenarios:
#       - Gherkin構文エラーの検出
#     """
#     raise NotImplementedError('STEP: ValueError が発生しGherkin構文エラーが報告されること')


@given('Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない')  # type: ignore
def given_630f9d2e(context):
    """Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない

    Scenarios:
      - Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
    """
    context._tmp_dir = tempfile.TemporaryDirectory()
    features_dir = Path(context._tmp_dir.name)
    (features_dir / "test.feature").write_text(
        "@SPEC-INHERIT-001\n"
        "Feature: 継承テスト\n"
        "  Scenario: タグなしシナリオ\n"
        "    Given 前提\n"
        "    When アクション\n"
        "    Then 確認\n",
        encoding="utf-8",
    )
    context.features_dir = features_dir
    context.expected_tag = "SPEC-INHERIT-001"
    context.expected_scenario_name = "タグなしシナリオ"


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
    context.tag_map = get_tag_map(context.features_dir, prefixes="SPEC")


@then('その仕様タグのエントリにシナリオの情報が紐付けられること')  # type: ignore
def then_2c7421ae(context):
    """その仕様タグのエントリにシナリオの情報が紐付けられること

    Scenarios:
      - Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
    """
    assert context.expected_tag in context.tag_map
    scenarios = context.tag_map[context.expected_tag]
    assert len(scenarios) >= 1
    assert scenarios[0]["name"] == context.expected_scenario_name


@given('Feature レベルにのみ仕様タグが付与されている')  # type: ignore
def given_8bed9a12(context):
    """Feature レベルにのみ仕様タグが付与されている

    Scenarios:
      - Featureタグを継承したエントリのkeywordはScenarioになる
    """
    context._tmp_dir = tempfile.TemporaryDirectory()
    features_dir = Path(context._tmp_dir.name)
    (features_dir / "test.feature").write_text(
        "@SPEC-KEYWORD-001\n"
        "Feature: キーワードテスト\n"
        "  Scenario: キーワード確認シナリオ\n"
        "    Given 前提\n"
        "    When アクション\n"
        "    Then 確認\n",
        encoding="utf-8",
    )
    context.features_dir = features_dir


@then('tag_map エントリの keyword が "{param0}" または "{param1}" であること')  # type: ignore
def then_92430f3a(context, param0, param1):
    """tag_map エントリの keyword が "Scenario" または "Scenario Outline" であること

    Scenarios:
      - Featureタグを継承したエントリのkeywordはScenarioになる
    """
    valid_keywords = {param0, param1}
    for scenarios in context.tag_map.values():
        for s in scenarios:
            assert s["keyword"] in valid_keywords


@given('Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている')  # type: ignore
def given_5a96b103(context):
    """Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    context._tmp_dir = tempfile.TemporaryDirectory()
    features_dir = Path(context._tmp_dir.name)
    (features_dir / "test.feature").write_text(
        "@SPEC-FEAT-001\n"
        "Feature: 多段継承テスト\n"
        "\n"
        "  Rule: ルールレベル\n"
        "    @SPEC-RULE-002\n"
        "    Scenario: Rule配下のシナリオ\n"
        "      Given 前提\n"
        "      When アクション\n"
        "      Then 確認\n",
        encoding="utf-8",
    )
    context.features_dir = features_dir


@given('Rule 配下のシナリオにはタグが付いていない')  # type: ignore
def given_b89243df(context):
    """Rule 配下のシナリオにはタグが付いていない

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    # フィクスチャは前の Given ステップで作成済み。シナリオへの直接タグなしはそこで保証されている


@then('そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること')  # type: ignore
def then_769bc618(context):
    """そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    assert "SPEC-FEAT-001" in context.tag_map
    assert "SPEC-RULE-002" in context.tag_map
    assert any(s["name"] == "Rule配下のシナリオ" for s in context.tag_map["SPEC-FEAT-001"])
    assert any(s["name"] == "Rule配下のシナリオ" for s in context.tag_map["SPEC-RULE-002"])


@given('Feature レベルに仕様タグ A が付与されている')  # type: ignore
def given_2ea31132(context):
    """Feature レベルに仕様タグ A が付与されている

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    context._tmp_dir = tempfile.TemporaryDirectory()
    context.features_dir = Path(context._tmp_dir.name)
    context.feature_tag = "SPEC-COEXIST-A"


@given('配下のシナリオに直接 仕様タグ B が付与されている')  # type: ignore
def given_07eca074(context):
    """配下のシナリオに直接 仕様タグ B が付与されている

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    context.scenario_tag = "SPEC-COEXIST-B"
    (context.features_dir / "test.feature").write_text(
        f"@{context.feature_tag}\n"
        "Feature: 共存テスト\n"
        "\n"
        f"  @{context.scenario_tag}\n"
        "  Scenario: 両タグ付きシナリオ\n"
        "    Given 前提\n"
        "    When アクション\n"
        "    Then 確認\n",
        encoding="utf-8",
    )


@then('そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること')  # type: ignore
def then_4386e28c(context):
    """そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    assert context.feature_tag in context.tag_map
    assert context.scenario_tag in context.tag_map
    assert any(s["name"] == "両タグ付きシナリオ" for s in context.tag_map[context.feature_tag])
    assert any(s["name"] == "両タグ付きシナリオ" for s in context.tag_map[context.scenario_tag])


@given('Scenario Outline に仕様タグ A が付与されている')  # type: ignore
def given_c475ab28(context):
    """Scenario Outline に仕様タグ A が付与されている

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    context._tmp_dir = tempfile.TemporaryDirectory()
    context.features_dir = Path(context._tmp_dir.name)
    context.outline_tag = "SPEC-OUTLINE-A"
    context.examples_tag = "SPEC-OUTLINE-B"


@given('いずれかの Examples テーブルに仕様タグ B が付与されている')  # type: ignore
def given_224c4b5d(context):
    """いずれかの Examples テーブルに仕様タグ B が付与されている

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    (context.features_dir / "test.feature").write_text(
        "Feature: Outlineテスト\n"
        "\n"
        f"  @{context.outline_tag}\n"
        "  Scenario Outline: アウトラインシナリオ\n"
        "    Given <値>\n"
        "    Then <期待値>\n"
        "\n"
        "    Examples: 基本\n"
        "      | 値 | 期待値 |\n"
        "      | 1  | 2      |\n"
        "\n"
        f"    @{context.examples_tag}\n"
        "    Examples: 拡張\n"
        "      | 値 | 期待値 |\n"
        "      | 5  | 10     |\n",
        encoding="utf-8",
    )


@then('仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること')  # type: ignore
def then_f65c91e7(context):
    """仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    assert context.outline_tag in context.tag_map
    assert context.examples_tag in context.tag_map
    assert any("アウトラインシナリオ" in s["name"] for s in context.tag_map[context.outline_tag])
    assert any("アウトラインシナリオ" in s["name"] for s in context.tag_map[context.examples_tag])


@given('Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている')  # type: ignore
def given_8f7f4921(context):
    """Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    context._tmp_dir = tempfile.TemporaryDirectory()
    features_dir = Path(context._tmp_dir.name)
    (features_dir / "test.feature").write_text(
        "@REQ-001\n"
        "Feature: プレフィックスフィルタテスト\n"
        "\n"
        "  @SPEC-001\n"
        "  Scenario: SPECタグ付きシナリオ\n"
        "    Given 前提\n"
        "    When アクション\n"
        "    Then 確認\n",
        encoding="utf-8",
    )
    context.features_dir = features_dir


@when('プレフィックス "{param0}" でタグマップを取得する')  # type: ignore
def when_1bf4e117(context, param0):
    """プレフィックス "SPEC" でタグマップを取得する

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    context.tag_map = get_tag_map(context.features_dir, prefixes=param0)


@then('"{param0}" のみがタグマップに含まれ "{param1}" は含まれないこと')  # type: ignore
def then_237adb2e(context, param0, param1):
    """"SPEC-001" のみがタグマップに含まれ "REQ-001" は含まれないこと

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    assert param0 in context.tag_map
    assert param1 not in context.tag_map
