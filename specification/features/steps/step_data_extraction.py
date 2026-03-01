"""behave steps for: データ抽出基盤"""

from __future__ import annotations
import sys
from pathlib import Path
from behave import given, when, then

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _helpers import (
    PROJECT_ROOT,
    create_doorstop_project_api,
    minimal_feature,
    write_feature_file,
)

# --- Doorstop 解析 ---


@given("Doorstopプロジェクトにアクティブな仕様アイテムが存在する")  # type: ignore
def given_a04781e9(context):
    """Doorstopプロジェクトにアクティブな仕様アイテムが存在する

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        req_items=[{"header": "要件A", "testable": False}],
        spec_items=[{"header": "仕様A", "testable": True}],
    )


@when("仕様ID集合を取得する")  # type: ignore
def when_e56707cb(context):
    """仕様ID集合を取得する

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
      - 非アクティブなアイテムの除外
      - テスト不可能な仕様の除外
    """
    from spec_weaver.doorstop import get_specs

    context.value = get_specs(repo_root=context.repo_root)


@then("アクティブかつtestableな仕様IDのみが返されること")  # type: ignore
def then_6823b180(context):
    """アクティブかつtestableな仕様IDのみが返されること

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
    """
    specs = context.value
    assert len(specs) >= 1
    for uid in specs:
        assert not uid.startswith("REQ")


@given("Doorstopプロジェクトに active: false のアイテムが存在する")  # type: ignore
def given_dccca3dc(context):
    """Doorstopプロジェクトに active: false のアイテムが存在する

    Scenarios:
      - 非アクティブなアイテムの除外
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        spec_items=[
            {"header": "アクティブ", "testable": True, "active": True},
            {"header": "非アクティブ", "testable": True, "active": False},
        ],
    )
    context.inactive_uid = "SPEC-002"


@then("非アクティブなアイテムは結果に含まれないこと")  # type: ignore
def then_99bfaa46(context):
    """非アクティブなアイテムは結果に含まれないこと

    Scenarios:
      - 非アクティブなアイテムの除外
    """
    assert context.inactive_uid not in context.value


@given("Doorstopプロジェクトに testable: false のアイテムが存在する")  # type: ignore
def given_d534a041(context):
    """Doorstopプロジェクトに testable: false のアイテムが存在する

    Scenarios:
      - テスト不可能な仕様の除外
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        spec_items=[
            {"header": "テスト可能", "testable": True},
            {"header": "テスト不可", "testable": False},
        ],
    )
    context.nontestable_uid = "SPEC-002"


@then("testable: false のアイテムは結果に含まれないこと")  # type: ignore
def then_f3fad2a6(context):
    """testable: false のアイテムは結果に含まれないこと

    Scenarios:
      - テスト不可能な仕様の除外
    """
    assert context.nontestable_uid not in context.value


@given("DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する")  # type: ignore
def given_7f8e9c65(context):
    """DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        req_items=[{"header": "要件", "testable": True}],
        spec_items=[{"header": "仕様", "testable": True}],
    )


@when('プレフィックス "{prefix}" で仕様ID集合を取得する')  # type: ignore
def when_1d11bcd6(context, prefix):
    """プレフィックス "SPEC" で仕様ID集合を取得する

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    from spec_weaver.doorstop import get_specs

    context.value = get_specs(repo_root=context.repo_root, prefix=prefix)


@then("SPECプレフィックスのアイテムのみが返されること")  # type: ignore
def then_b5f39418(context):
    """SPECプレフィックスのアイテムのみが返されること

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    for uid in context.value:
        assert uid.startswith("SPEC")
    assert any(uid.startswith("SPEC") for uid in context.value)


# --- Gherkin 解析 ---


@given("Gherkin .feature ファイルに @SPEC-001 タグが付与されている")  # type: ignore
def given_b830a393(context):
    """Gherkin .feature ファイルに @SPEC-001 タグが付与されている

    Scenarios:
      - Gherkin ASTからのタグ抽出
    """
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(
        context.feature_dir / "test.feature", minimal_feature("@SPEC-001")
    )


@when("タグ集合を取得する")  # type: ignore
def when_a12b8a55(context):
    """タグ集合を取得する

    Scenarios:
      - Gherkin ASTからのタグ抽出
      - Feature・Scenario両レベルのタグ抽出
      - サブディレクトリ内のfeatureファイルの再帰探索
      - Gherkin構文エラーの検出
    """
    from spec_weaver.gherkin import get_tags

    try:
        context.value = get_tags(features_dir=context.feature_dir)
        context.error = None
    except ValueError as e:
        context.error = e
        context.value = set()


@then('"{spec_id}" がタグ集合に含まれること')  # type: ignore
def then_e8d01468(context, spec_id):
    """ "SPEC-001" がタグ集合に含まれること

    Scenarios:
      - Gherkin ASTからのタグ抽出
    """
    assert spec_id in context.value


@given("Feature レベルと Scenario レベルに異なるSPECタグが付与されている")  # type: ignore
def given_07def24f(context):
    """Feature レベルと Scenario レベルに異なるSPECタグが付与されている

    Scenarios:
      - Feature・Scenario両レベルのタグ抽出
    """
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(
        context.feature_dir / "dual.feature",
        """\
@SPEC-010
Feature: デュアルタグテスト

  @SPEC-011
  Scenario: シナリオレベルのタグ
    Given テスト
    When  実行
    Then  確認
""",
    )


@then("両方のレベルのタグがすべて抽出されること")  # type: ignore
def then_d712dc38(context):
    """両方のレベルのタグがすべて抽出されること

    Scenarios:
      - Feature・Scenario両レベルのタグ抽出
    """
    assert "SPEC-010" in context.value
    assert "SPEC-011" in context.value


@given("サブディレクトリに .feature ファイルが存在する")  # type: ignore
def given_1427ca58(context):
    """サブディレクトリに .feature ファイルが存在する

    Scenarios:
      - サブディレクトリ内のfeatureファイルの再帰探索
    """
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(
        context.feature_dir / "subdir" / "nested.feature", minimal_feature("@SPEC-099")
    )


@then("サブディレクトリ内のタグも含めて抽出されること")  # type: ignore
def then_1c0ec472(context):
    """サブディレクトリ内のタグも含めて抽出されること

    Scenarios:
      - サブディレクトリ内のfeatureファイルの再帰探索
    """
    assert "SPEC-099" in context.value


@given("構文的に不正な .feature ファイルが存在する")  # type: ignore
def given_540458bc(context):
    """構文的に不正な .feature ファイルが存在する

    Scenarios:
      - Gherkin構文エラーの検出
    """
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(
        context.feature_dir / "bad.feature", "この行は Gherkin ではない\n  壊れた構文\n"
    )


@then("ValueError が発生しGherkin構文エラーが報告されること")  # type: ignore
def then_c5d0b4fe(context):
    """ValueError が発生しGherkin構文エラーが報告されること

    Scenarios:
      - Gherkin構文エラーの検出
    """
    assert context.error is not None
    assert isinstance(context.error, ValueError)


# --- Effective Tags ---


@given("Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない")  # type: ignore
def given_630f9d2e(context):
    """Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない

    Scenarios:
      - Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
    """
    context.feature_dir = context.temp_dir / "features"
    context.spec_tag = "SPEC-050"
    write_feature_file(
        context.feature_dir / "inherit.feature",
        """\
@SPEC-050
Feature: タグ継承テスト

  Scenario: タグなしシナリオ
    Given テスト
    When  実行
    Then  確認
""",
    )


@when("タグマップを取得する")  # type: ignore
def when_24daec1e(context):
    """タグマップを取得する

    Scenarios:
      - Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
      - Featureタグを継承したエントリのkeywordはScenarioになる
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    from spec_weaver.gherkin import get_tag_map

    context.value = get_tag_map(context.feature_dir, prefixes={"SPEC", "REQ"})


@then("その仕様タグのエントリにシナリオの情報が紐付けられること")  # type: ignore
def then_2c7421ae(context):
    """その仕様タグのエントリにシナリオの情報が紐付けられること

    Scenarios:
      - Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
    """
    tag_map = context.value
    assert context.spec_tag in tag_map
    assert len(tag_map[context.spec_tag]) >= 1


@given("Feature レベルにのみ仕様タグが付与されている")  # type: ignore
def given_8bed9a12(context):
    """Feature レベルにのみ仕様タグが付与されている

    Scenarios:
      - Featureタグを継承したエントリのkeywordはScenarioになる
    """
    context.feature_dir = context.temp_dir / "features"
    context.spec_tag = "SPEC-051"
    write_feature_file(
        context.feature_dir / "keyword.feature",
        """\
@SPEC-051
Feature: keyword テスト

  Scenario: keyword check
    Given テスト
    When  実行
    Then  確認
""",
    )


@then('tag_map エントリの keyword が "{kw1}" または "{kw2}" であること')  # type: ignore
def then_92430f3a(context, kw1, kw2):
    """tag_map エントリの keyword が "Scenario" または "Scenario Outline" であること

    Scenarios:
      - Featureタグを継承したエントリのkeywordはScenarioになる
    """
    for entry in context.value.get(context.spec_tag, []):
        assert entry["keyword"] in (kw1, kw2)


@given("Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている")  # type: ignore
def given_5a96b103(context):
    """Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    context.feature_dir = context.temp_dir / "features"
    context.spec_tag_feature = "SPEC-060"
    context.spec_tag_rule = "SPEC-061"
    write_feature_file(
        context.feature_dir / "multilvl.feature",
        """\
@SPEC-060
Feature: 多段継承テスト

  @SPEC-061
  Rule: ルール

    Scenario: ルール配下シナリオ
      Given テスト
      When  実行
      Then  確認
""",
    )


@given("Rule 配下のシナリオにはタグが付いていない")  # type: ignore
def given_b89243df(context):
    """Rule 配下のシナリオにはタグが付いていない

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    pass  # 上の Given で設定済み


@then("そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること")  # type: ignore
def then_769bc618(context):
    """そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    tag_map = context.value
    assert context.spec_tag_feature in tag_map
    assert context.spec_tag_rule in tag_map


@given("Feature レベルに仕様タグ A が付与されている")  # type: ignore
def given_2ea31132(context):
    """Feature レベルに仕様タグ A が付与されている

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    context.feature_dir = context.temp_dir / "features"
    context.spec_tag_a = "SPEC-070"
    context.spec_tag_b = "SPEC-071"
    write_feature_file(
        context.feature_dir / "coexist.feature",
        """\
@SPEC-070
Feature: タグ共存テスト

  @SPEC-071
  Scenario: 両タグ保有シナリオ
    Given テスト
    When  実行
    Then  確認
""",
    )


@given("配下のシナリオに直接 仕様タグ B が付与されている")  # type: ignore
def given_07eca074(context):
    """配下のシナリオに直接 仕様タグ B が付与されている

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    pass  # 上の Given で設定済み


@then("そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること")  # type: ignore
def then_4386e28c(context):
    """そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    tag_map = context.value
    assert context.spec_tag_a in tag_map
    assert context.spec_tag_b in tag_map


@given("Scenario Outline に仕様タグ A が付与されている")  # type: ignore
def given_c475ab28(context):
    """Scenario Outline に仕様タグ A が付与されている

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    context.feature_dir = context.temp_dir / "features"
    context.spec_tag_a = "SPEC-080"
    context.spec_tag_b = "SPEC-081"
    write_feature_file(
        context.feature_dir / "outline.feature",
        """\
Feature: Outline テスト

  @SPEC-080
  Scenario Outline: アウトライン
    Given <item>

    @SPEC-081
    Examples: タグ付き例
      | item |
      | val1 |
""",
    )


@given("いずれかの Examples テーブルに仕様タグ B が付与されている")  # type: ignore
def given_224c4b5d(context):
    """いずれかの Examples テーブルに仕様タグ B が付与されている

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    pass  # 上の Given で設定済み


@then("仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること")  # type: ignore
def then_f65c91e7(context):
    """仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    tag_map = context.value
    assert context.spec_tag_a in tag_map
    assert context.spec_tag_b in tag_map


@given("Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている")  # type: ignore
def given_8f7f4921(context):
    """Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(
        context.feature_dir / "filter.feature",
        """\
@REQ-001
Feature: フィルタテスト

  @SPEC-001
  Scenario: フィルタシナリオ
    Given テスト
    When  実行
    Then  確認
""",
    )


@when('プレフィックス "{prefix}" でタグマップを取得する')  # type: ignore
def when_1bf4e117(context, prefix):
    """プレフィックス "SPEC" でタグマップを取得する

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    from spec_weaver.gherkin import get_tag_map

    context.value = get_tag_map(context.feature_dir, prefixes=prefix)


@then('"{uid1}" のみがタグマップに含まれ "{uid2}" は含まれないこと')  # type: ignore
def then_237adb2e(context, uid1, uid2):
    """ "SPEC-001" のみがタグマップに含まれ "REQ-001" は含まれないこと

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    tag_map = context.value
    assert uid1 in tag_map
    assert uid2 not in tag_map
