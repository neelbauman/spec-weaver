from specification.features.steps._helpers import create_doorstop_project_api, create_doorstop_project_yaml, write_feature_file, run_spec_weaver
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
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [
                    {"uid": "SPEC-001", "testable": True, "active": True},
                    {"uid": "SPEC-002", "testable": True, "active": True},
                ],
            }
        ],
    )


@when('仕様ID集合を取得する')  # type: ignore
def when_e56707cb(context):
    """仕様ID集合を取得する

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
      - 非アクティブなアイテムの除外
      - テスト不可能な仕様の除外
    """
    from spec_weaver.doorstop import get_specs
    context.spec_ids = get_specs(context.temp_dir, prefix=None)


@then('アクティブかつtestableな仕様IDのみが返されること')  # type: ignore
def then_6823b180(context):
    """アクティブかつtestableな仕様IDのみが返されること

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
    """
    assert "SPEC-001" in context.spec_ids
    assert "SPEC-002" in context.spec_ids


@given('Doorstopプロジェクトに active: false のアイテムが存在する')  # type: ignore
def given_dccca3dc(context):
    """Doorstopプロジェクトに active: false のアイテムが存在する

    Scenarios:
      - 非アクティブなアイテムの除外
    """
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [
                    {"uid": "SPEC-001", "testable": True, "active": True},
                    {"uid": "SPEC-002", "testable": True, "active": False},
                ],
            }
        ],
    )


@then('非アクティブなアイテムは結果に含まれないこと')  # type: ignore
def then_99bfaa46(context):
    """非アクティブなアイテムは結果に含まれないこと

    Scenarios:
      - 非アクティブなアイテムの除外
    """
    assert "SPEC-001" in context.spec_ids
    assert "SPEC-002" not in context.spec_ids


@given('Doorstopプロジェクトに testable: false のアイテムが存在する')  # type: ignore
def given_d534a041(context):
    """Doorstopプロジェクトに testable: false のアイテムが存在する

    Scenarios:
      - テスト不可能な仕様の除外
    """
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [
                    {"uid": "SPEC-001", "testable": True, "active": True},
                    {"uid": "SPEC-002", "testable": False, "active": True},
                ],
            }
        ],
    )


@then('testable: false のアイテムは結果に含まれないこと')  # type: ignore
def then_f3fad2a6(context):
    """testable: false のアイテムは結果に含まれないこと

    Scenarios:
      - テスト不可能な仕様の除外
    """
    assert "SPEC-001" in context.spec_ids
    assert "SPEC-002" not in context.spec_ids


@given('DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する')  # type: ignore
def given_7f8e9c65(context):
    """DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "reqs",
                "prefix": "REQ",
                "items": [{"uid": "REQ-001", "testable": False}],
            },
            {
                "dir": "specs",
                "prefix": "SPEC",
                "parent": "REQ",
                "items": [{"uid": "SPEC-001", "testable": True, "links": ["REQ-001"]}],
            },
        ],
    )


@when('プレフィックス "{param0}" で仕様ID集合を取得する')  # type: ignore
def when_1d11bcd6(context, param0):
    """プレフィックス "SPEC" で仕様ID集合を取得する

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    from spec_weaver.doorstop import get_specs
    context.spec_ids = get_specs(context.temp_dir, prefix=param0)


@then('SPECプレフィックスのアイテムのみが返されること')  # type: ignore
def then_b5f39418(context):
    """SPECプレフィックスのアイテムのみが返されること

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    assert all(uid.startswith("SPEC") for uid in context.spec_ids), (
        f"SPEC以外のIDが含まれています: {context.spec_ids}"
    )
    assert "SPEC-001" in context.spec_ids


@given('Gherkin .feature ファイルに @SPEC-001 タグが付与されている')  # type: ignore
def given_b830a393(context):
    """Gherkin .feature ファイルに @SPEC-001 タグが付与されている

    Scenarios:
      - Gherkin ASTからのタグ抽出
    """
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        feature_dir / "test.feature",
        "@SPEC-001\nFeature: Test\n  Scenario: S1\n    Given test\n",
    )
    context.feature_dir = feature_dir


@when('タグ集合を取得する')  # type: ignore
def when_a12b8a55(context):
    """タグ集合を取得する

    Scenarios:
      - Gherkin ASTからのタグ抽出
      - Feature・Scenario両レベルのタグ抽出
      - サブディレクトリ内のfeatureファイルの再帰探索
      - Gherkin構文エラーの検出
    """
    from spec_weaver.adapters.gherkin import get_tag_map
    try:
        tag_map = get_tag_map(context.feature_dir, context.temp_dir, {"SPEC", "REQ", "CORE"})
        context.tag_ids = set(tag_map.keys())
        context.tag_error = None
    except ValueError as e:
        context.tag_ids = set()
        context.tag_error = e


@then('"{param0}" がタグ集合に含まれること')  # type: ignore
def then_e8d01468(context, param0):
    """"SPEC-001" がタグ集合に含まれること

    Scenarios:
      - Gherkin ASTからのタグ抽出
    """
    assert param0 in context.tag_ids, f"{param0} がタグ集合に含まれていません。タグ: {context.tag_ids}"


@given('Feature レベルと Scenario レベルに異なるSPECタグが付与されている')  # type: ignore
def given_07def24f(context):
    """Feature レベルと Scenario レベルに異なるSPECタグが付与されている

    Scenarios:
      - Feature・Scenario両レベルのタグ抽出
    """
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        feature_dir / "test.feature",
        "@SPEC-001\nFeature: Test\n\n  @SPEC-002\n  Scenario: S1\n    Given test\n",
    )
    context.feature_dir = feature_dir


@then('両方のレベルのタグがすべて抽出されること')  # type: ignore
def then_d712dc38(context):
    """両方のレベルのタグがすべて抽出されること

    Scenarios:
      - Feature・Scenario両レベルのタグ抽出
    """
    assert "SPEC-001" in context.tag_ids, f"SPEC-001 がタグ集合に含まれていません: {context.tag_ids}"
    assert "SPEC-002" in context.tag_ids, f"SPEC-002 がタグ集合に含まれていません: {context.tag_ids}"


@given('サブディレクトリに .feature ファイルが存在する')  # type: ignore
def given_1427ca58(context):
    """サブディレクトリに .feature ファイルが存在する

    Scenarios:
      - サブディレクトリ内のfeatureファイルの再帰探索
    """
    feature_dir = context.temp_dir / "features"
    subdir = feature_dir / "sub"
    subdir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        subdir / "sub.feature",
        "@SPEC-010\nFeature: SubTest\n  Scenario: S1\n    Given test\n",
    )
    context.feature_dir = feature_dir


@then('サブディレクトリ内のタグも含めて抽出されること')  # type: ignore
def then_1c0ec472(context):
    """サブディレクトリ内のタグも含めて抽出されること

    Scenarios:
      - サブディレクトリ内のfeatureファイルの再帰探索
    """
    assert "SPEC-010" in context.tag_ids, f"SPEC-010 がタグ集合に含まれていません: {context.tag_ids}"


@given('構文的に不正な .feature ファイルが存在する')  # type: ignore
def given_540458bc(context):
    """構文的に不正な .feature ファイルが存在する

    Scenarios:
      - Gherkin構文エラーの検出
    """
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    # 不正なGherkin構文（Feature キーワードなし、インデント誤り等）
    (feature_dir / "broken.feature").write_text(
        "This is not valid gherkin\n  And there is no feature keyword\n    Invalid stuff\n",
        encoding="utf-8",
    )
    context.feature_dir = feature_dir


@then('ValueError が発生しGherkin構文エラーが報告されること')  # type: ignore
def then_c5d0b4fe(context):
    """ValueError が発生しGherkin構文エラーが報告されること

    Scenarios:
      - Gherkin構文エラーの検出
    """
    assert context.tag_error is not None, "ValueError が発生しませんでした"
    assert isinstance(context.tag_error, ValueError), f"ValueError ではなく {type(context.tag_error)} が発生しました"


# --- Gherkinタグ継承（Effective Tags）---

@given('Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない')  # type: ignore
def given_630f9d2e(context):
    """Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない

    Scenarios:
      - Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
    """
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        feature_dir / "test.feature",
        "@SPEC-001\nFeature: Test\n\n  Scenario: シナリオA\n    Given test\n    When action\n    Then verify\n",
    )
    context.feature_dir = feature_dir


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
    from spec_weaver.adapters.gherkin import get_tag_map
    context.tag_map = get_tag_map(context.feature_dir, context.temp_dir, {"SPEC", "REQ", "CORE"})


@then('その仕様タグのエントリにシナリオの情報が紐付けられること')  # type: ignore
def then_2c7421ae(context):
    """その仕様タグのエントリにシナリオの情報が紐付けられること

    Scenarios:
      - Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
    """
    assert "SPEC-001" in context.tag_map, f"SPEC-001 がタグマップに含まれていません: {list(context.tag_map.keys())}"
    entries = context.tag_map["SPEC-001"]
    assert len(entries) > 0, "SPEC-001 のエントリが空です"
    assert entries[0].get("name"), "シナリオ名が設定されていません"


@given('Feature レベルにのみ仕様タグが付与されている')  # type: ignore
def given_8bed9a12(context):
    """Feature レベルにのみ仕様タグが付与されている

    Scenarios:
      - Featureタグを継承したエントリのkeywordはScenarioになる
    """
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        feature_dir / "test.feature",
        "@SPEC-001\nFeature: Test\n\n  Scenario: シナリオA\n    Given test\n",
    )
    context.feature_dir = feature_dir


@then('tag_map エントリの keyword が "{param0}" または "{param1}" であること')  # type: ignore
def then_92430f3a(context, param0, param1):
    """tag_map エントリの keyword が "Scenario" または "Scenario Outline" であること

    Scenarios:
      - Featureタグを継承したエントリのkeywordはScenarioになる
    """
    entries = context.tag_map.get("SPEC-001", [])
    assert len(entries) > 0, "SPEC-001 のエントリが空です"
    for entry in entries:
        assert entry.get("keyword") in (param0, param1), (
            f"keyword が '{param0}' または '{param1}' ではありません: {entry.get('keyword')}"
        )


@given('Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている')  # type: ignore
def given_5a96b103(context):
    """Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        feature_dir / "test.feature",
        "@SPEC-001\nFeature: Test\n\n  @SPEC-002\n  Rule: Some Rule\n\n    Scenario: シナリオA\n      Given test\n",
    )
    context.feature_dir = feature_dir


@given('Rule 配下のシナリオにはタグが付いていない')  # type: ignore
def given_b89243df(context):
    """Rule 配下のシナリオにはタグが付いていない

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    # Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている で設定済み
    pass


@then('そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること')  # type: ignore
def then_769bc618(context):
    """そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること

    Scenarios:
      - Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
    """
    assert "SPEC-001" in context.tag_map, f"SPEC-001 がタグマップに含まれていません: {list(context.tag_map.keys())}"
    assert "SPEC-002" in context.tag_map, f"SPEC-002 がタグマップに含まれていません: {list(context.tag_map.keys())}"


@given('Feature レベルに仕様タグ A が付与されている')  # type: ignore
def given_2ea31132(context):
    """Feature レベルに仕様タグ A が付与されている

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    # feature_dir は given_07eca074 で設定する
    context._tag_a = "SPEC-010"
    context._tag_b = "SPEC-011"


@given('配下のシナリオに直接 仕様タグ B が付与されている')  # type: ignore
def given_07eca074(context):
    """配下のシナリオに直接 仕様タグ B が付与されている

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    tag_a = getattr(context, '_tag_a', 'SPEC-010')
    tag_b = getattr(context, '_tag_b', 'SPEC-011')
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        feature_dir / "test.feature",
        f"@{tag_a}\nFeature: Test\n\n  @{tag_b}\n  Scenario: シナリオA\n    Given test\n",
    )
    context.feature_dir = feature_dir


@then('そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること')  # type: ignore
def then_4386e28c(context):
    """そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること

    Scenarios:
      - シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
    """
    tag_a = getattr(context, '_tag_a', 'SPEC-010')
    tag_b = getattr(context, '_tag_b', 'SPEC-011')
    assert tag_a in context.tag_map, f"{tag_a} がタグマップに含まれていません: {list(context.tag_map.keys())}"
    assert tag_b in context.tag_map, f"{tag_b} がタグマップに含まれていません: {list(context.tag_map.keys())}"


@given('Scenario Outline に仕様タグ A が付与されている')  # type: ignore
def given_c475ab28(context):
    """Scenario Outline に仕様タグ A が付与されている

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    context._outline_tag_a = "SPEC-020"
    context._outline_tag_b = "SPEC-021"


@given('いずれかの Examples テーブルに仕様タグ B が付与されている')  # type: ignore
def given_224c4b5d(context):
    """いずれかの Examples テーブルに仕様タグ B が付与されている

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    tag_a = getattr(context, '_outline_tag_a', 'SPEC-020')
    tag_b = getattr(context, '_outline_tag_b', 'SPEC-021')
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        feature_dir / "test.feature",
        f"@{tag_a}\nFeature: Test\n\n  Scenario Outline: アウトライン\n    Given <param>\n\n  @{tag_b}\n  Examples: ケースB\n    | param |\n    | val1  |\n",
    )
    context.feature_dir = feature_dir


@then('仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること')  # type: ignore
def then_f65c91e7(context):
    """仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること

    Scenarios:
      - Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
    """
    tag_a = getattr(context, '_outline_tag_a', 'SPEC-020')
    tag_b = getattr(context, '_outline_tag_b', 'SPEC-021')
    assert tag_a in context.tag_map, f"{tag_a} がタグマップに含まれていません: {list(context.tag_map.keys())}"
    assert tag_b in context.tag_map, f"{tag_b} がタグマップに含まれていません: {list(context.tag_map.keys())}"


@given('Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている')  # type: ignore
def given_8f7f4921(context):
    """Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        feature_dir / "test.feature",
        "@REQ-001\nFeature: Test\n\n  @SPEC-001\n  Scenario: シナリオA\n    Given test\n",
    )
    context.feature_dir = feature_dir


@when('プレフィックス "{param0}" でタグマップを取得する')  # type: ignore
def when_1bf4e117(context, param0):
    """プレフィックス "SPEC" でタグマップを取得する

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    from spec_weaver.adapters.gherkin import get_tag_map
    context.tag_map = get_tag_map(context.feature_dir, context.temp_dir, {param0})


@then('"{param0}" のみがタグマップに含まれ "{param1}" は含まれないこと')  # type: ignore
def then_abc12345(context, param0, param1):
    """"SPEC-001" のみがタグマップに含まれ "REQ-001" は含まれないこと

    Scenarios:
      - プレフィックスフィルタはEffective Tags算出後に適用される
    """
    assert param0 in context.tag_map, f"{param0} がタグマップに含まれていません: {list(context.tag_map.keys())}"
    assert param1 not in context.tag_map, f"{param1} がタグマップに含まれています（含まれないはず）: {list(context.tag_map.keys())}"
