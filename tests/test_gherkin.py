import pytest
from spec_weaver.gherkin import get_tag_map, get_tags


def test_get_tags_success(tmp_path):
    # 正常なGherkinファイルを作成
    feature_file = tmp_path / "valid.feature"
    feature_file.write_text("""
@SPEC-001
Feature: User Login
  @SPEC-002
  Scenario: Successful login
    Given a user
    When they login
    Then it works
    """, encoding="utf-8")

    # サブディレクトリにもファイルを作成（再帰探索のテスト）
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    sub_feature = sub_dir / "sub.feature"
    sub_feature.write_text("""
Feature: Sub feature
  @SPEC-003 @other-tag
  Scenario: Sub scenario
    Given something
    """, encoding="utf-8")

    # 実行と検証
    tags = get_tags(tmp_path, prefix="SPEC")

    # SPEC-001 (Feature→Scenario継承), SPEC-002 (Scenario直接), SPEC-003 (Sub-dir) が抽出されるべき
    assert tags == {"SPEC-001", "SPEC-002", "SPEC-003"}
    # @other-tag はプレフィックスが違うため無視されるべき


def test_get_tags_syntax_error(tmp_path):
    # 文法エラーのある（Feature宣言すらない）真に無効なGherkinファイルを作成
    invalid_file = tmp_path / "invalid.feature"
    invalid_file.write_text("""
This is completely invalid Gherkin.
いきなりプレーンテキストを書くことは許されません。
    """, encoding="utf-8")

    # 構文エラー時に ValueError が送出されることを検証
    with pytest.raises(ValueError, match="Gherkin構文エラー"):
        get_tags(tmp_path, prefix="SPEC")


# --- SPEC-021: Gherkinタグ継承（Effective Tags）テスト ---


def test_feature_tag_inherited_by_scenario(tmp_path):
    """
    SPEC-021: Featureレベルのタグのみが付与され、Scenarioにタグがない場合、
    そのScenarioがFeatureタグに紐付けられること。
    """
    (tmp_path / "inherit.feature").write_text("""
@SPEC-100
Feature: 継承テスト Feature
  Scenario: タグなしシナリオ
    Given 何かが存在する
    When  アクションを実行する
    Then  結果が返ること
    """, encoding="utf-8")

    tag_map = get_tag_map(tmp_path, prefixes="SPEC")

    assert "SPEC-100" in tag_map
    scenarios = tag_map["SPEC-100"]
    assert len(scenarios) == 1
    assert scenarios[0]["name"] == "タグなしシナリオ"
    # Featureノードではなく、必ずScenarioキーワードで登録されること（SPEC-021）
    assert scenarios[0]["keyword"] in ("Scenario", "Scenario Outline", "Example")


def test_feature_rule_scenario_multilevel_inheritance(tmp_path):
    """
    SPEC-021: Feature→Rule→Scenarioの多段継承で、
    ScenarioはFeatureタグとRuleタグの両方に紐付けられること。
    """
    (tmp_path / "multilevel.feature").write_text("""
@SPEC-200
Feature: 多段継承テスト

  Rule: ルールレベルの仕様
    @SPEC-210
    Scenario: Rule配下のシナリオ
      Given セットアップ
      When  アクション
      Then  検証
    """, encoding="utf-8")

    tag_map = get_tag_map(tmp_path, prefixes="SPEC")

    # FeatureタグSPEC-200 がRule配下のScenarioに継承されること
    assert "SPEC-200" in tag_map
    assert any(s["name"] == "Rule配下のシナリオ" for s in tag_map["SPEC-200"])

    # RuleタグSPEC-210 も正しく登録されること
    assert "SPEC-210" in tag_map
    assert any(s["name"] == "Rule配下のシナリオ" for s in tag_map["SPEC-210"])


def test_direct_and_inherited_tags_coexist(tmp_path):
    """
    SPEC-021: Scenarioに直接タグがある場合、継承タグと共存して
    Effective Tagsを形成すること（和集合）。
    """
    (tmp_path / "coexist.feature").write_text("""
@SPEC-300
Feature: 直接タグと継承タグの共存テスト

  @SPEC-310
  Scenario: 直接タグ付きシナリオ
    Given 前提
    When  操作
    Then  確認
    """, encoding="utf-8")

    tag_map = get_tag_map(tmp_path, prefixes="SPEC")

    # 継承タグSPEC-300 → シナリオに紐付けられること
    assert "SPEC-300" in tag_map
    assert any(s["name"] == "直接タグ付きシナリオ" for s in tag_map["SPEC-300"])

    # 直接タグSPEC-310 → シナリオに紐付けられること
    assert "SPEC-310" in tag_map
    assert any(s["name"] == "直接タグ付きシナリオ" for s in tag_map["SPEC-310"])


def test_scenario_outline_examples_tags_aggregated(tmp_path):
    """
    SPEC-021: Scenario Outlineの場合、全ExamplesテーブルのタグがEffective Tagsに集約され、
    Scenario Outline自身のタグと合わせて1エントリとして登録されること。
    """
    (tmp_path / "outline.feature").write_text("""
@SPEC-400
Feature: ScenarioOutline Effective Tagsテスト

  @SPEC-410
  Scenario Outline: アウトラインシナリオ
    Given 入力 <値>
    Then  結果 <期待値>

    Examples: 基本ケース
      | 値 | 期待値 |
      | 1  | 2      |

    @SPEC-420
    Examples: 拡張ケース
      | 値 | 期待値 |
      | 5  | 10     |
    """, encoding="utf-8")

    tag_map = get_tag_map(tmp_path, prefixes="SPEC")

    # Feature継承タグSPEC-400 → ScenarioOutlineに紐付けられること
    assert "SPEC-400" in tag_map
    assert any("アウトラインシナリオ" in s["name"] for s in tag_map["SPEC-400"])

    # ScenarioOutline直接タグSPEC-410
    assert "SPEC-410" in tag_map
    assert any("アウトラインシナリオ" in s["name"] for s in tag_map["SPEC-410"])

    # Examplesタグ SPEC-420 → ScenarioOutlineとして集約されること
    assert "SPEC-420" in tag_map
    assert any("アウトラインシナリオ" in s["name"] for s in tag_map["SPEC-420"])


def test_prefix_filter_applied_after_effective_tags(tmp_path):
    """
    SPEC-021: プレフィックスフィルタはEffective Tags算出後に適用されること。
    REQタグをFeatureに、SPECタグをScenarioに付与した場合、
    prefix="SPEC" で取得した場合はSPECタグのみが返されること。
    """
    (tmp_path / "prefix.feature").write_text("""
@REQ-001
Feature: プレフィックスフィルタテスト

  @SPEC-500
  Scenario: SPECタグ付きシナリオ
    Given 前提
    When  操作
    Then  確認
    """, encoding="utf-8")

    tag_map = get_tag_map(tmp_path, prefixes="SPEC")

    # SPEC-500 はフィルタを通過して登録されること
    assert "SPEC-500" in tag_map
    # REQ-001 はフィルタで除外されること
    assert "REQ-001" not in tag_map
