from specification.features.steps._helpers import create_doorstop_project_api, write_feature_file, run_spec_weaver
"""behave steps for: build コマンド"""

from behave import given, when, then, step

# ======================================================================
# Steps
# ======================================================================

@given('DoorstopプロジェクトとGherkin featureファイルが存在する')  # type: ignore
def given_8a7b1a87(context):
    """DoorstopプロジェクトとGherkin featureファイルが存在する

    Scenarios:
      - MkDocs設定ファイルの生成
      - カスタム出力ディレクトリの指定
    """
    raise NotImplementedError('STEP: DoorstopプロジェクトとGherkin featureファイルが存在する')


@then('出力ディレクトリに mkdocs.yml が生成されること')  # type: ignore
def then_453d91c1(context):
    """出力ディレクトリに mkdocs.yml が生成されること

    Scenarios:
      - MkDocs設定ファイルの生成
    """
    raise NotImplementedError('STEP: 出力ディレクトリに mkdocs.yml が生成されること')


@then('Material テーマが設定されていること')  # type: ignore
def then_281c0fa4(context):
    """Material テーマが設定されていること

    Scenarios:
      - MkDocs設定ファイルの生成
    """
    raise NotImplementedError('STEP: Material テーマが設定されていること')


@given('DoorstopプロジェクトにREQアイテムが存在する')  # type: ignore
def given_ce6845b7(context):
    """DoorstopプロジェクトにREQアイテムが存在する

    Scenarios:
      - 要件一覧ページの生成
    """
    raise NotImplementedError('STEP: DoorstopプロジェクトにREQアイテムが存在する')


@then('docs/req.md が生成されること')  # type: ignore
def then_0130d8b7(context):
    """docs/req.md が生成されること

    Scenarios:
      - 要件一覧ページの生成
    """
    raise NotImplementedError('STEP: docs/req.md が生成されること')


@then('各REQアイテムがテーブル行として含まれること')  # type: ignore
def then_2977857a(context):
    """各REQアイテムがテーブル行として含まれること

    Scenarios:
      - 要件一覧ページの生成
    """
    raise NotImplementedError('STEP: 各REQアイテムがテーブル行として含まれること')


@then('関連仕様への相互リンクが含まれること')  # type: ignore
def then_ef9d25c2(context):
    """関連仕様への相互リンクが含まれること

    Scenarios:
      - 要件一覧ページの生成
    """
    raise NotImplementedError('STEP: 関連仕様への相互リンクが含まれること')


@given('DoorstopプロジェクトにSPECアイテムが存在する')  # type: ignore
def given_ae2b8b7d(context):
    """DoorstopプロジェクトにSPECアイテムが存在する

    Scenarios:
      - 仕様一覧ページの生成
      - 一覧テーブルにレビューステータス列が表示されること
    """
    import tempfile
    from pathlib import Path

    tmp_dir = Path(tempfile.mkdtemp())
    context.tmp_dir = tmp_dir

    from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file
    create_doorstop_project_yaml(tmp_dir, [
        {
            "dir": "reqs",
            "prefix": "REQ",
            "parent": None,
            "items": [{"uid": "REQ-001", "header": "要件1", "testable": False}],
        },
        {
            "dir": "specs",
            "prefix": "SPEC",
            "parent": "REQ",
            "items": [{"uid": "SPEC-001", "header": "仕様1", "links": ["REQ-001"]}],
        },
    ])

    features_dir = tmp_dir / "features"
    features_dir.mkdir()
    write_feature_file(
        features_dir / "test.feature",
        "@SPEC-001\nFeature: テスト\n\n  Scenario: S1\n    Given 前提\n    When 操作\n    Then 確認\n",
    )

    out_dir = tmp_dir / "out"
    result = run_spec_weaver(
        ["build", str(features_dir), "--out-dir", str(out_dir)],
        cwd=tmp_dir,
    )
    spec_md = out_dir / "docs" / "spec.md"
    context.spec_md_content = spec_md.read_text(encoding="utf-8") if spec_md.exists() else ""
    context.build_result = result


@then('docs/spec.md が生成されること')  # type: ignore
def then_9b5808a6(context):
    """docs/spec.md が生成されること

    Scenarios:
      - 仕様一覧ページの生成
    """
    raise NotImplementedError('STEP: docs/spec.md が生成されること')


@then('各SPECアイテムがテーブル行として含まれること')  # type: ignore
def then_86be7f51(context):
    """各SPECアイテムがテーブル行として含まれること

    Scenarios:
      - 仕様一覧ページの生成
    """
    raise NotImplementedError('STEP: 各SPECアイテムがテーブル行として含まれること')


@then('上位要件への相互リンクが含まれること')  # type: ignore
def then_d1af9a65(context):
    """上位要件への相互リンクが含まれること

    Scenarios:
      - 仕様一覧ページの生成
    """
    raise NotImplementedError('STEP: 上位要件への相互リンクが含まれること')


@given('DoorstopプロジェクトにアイテムとGherkinテストが存在する')  # type: ignore
def given_73c18566(context):
    """DoorstopプロジェクトにアイテムとGherkinテストが存在する

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    raise NotImplementedError('STEP: DoorstopプロジェクトにアイテムとGherkinテストが存在する')


@then('docs/items/ 配下に各アイテムのMarkdownファイルが生成されること')  # type: ignore
def then_77d459df(context):
    """docs/items/ 配下に各アイテムのMarkdownファイルが生成されること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    raise NotImplementedError('STEP: docs/items/ 配下に各アイテムのMarkdownファイルが生成されること')


@then('アイテムの本文が含まれること')  # type: ignore
def then_650f49fb(context):
    """アイテムの本文が含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    raise NotImplementedError('STEP: アイテムの本文が含まれること')


@then('上位・下位リンクが含まれること')  # type: ignore
def then_677a5bf3(context):
    """上位・下位リンクが含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    raise NotImplementedError('STEP: 上位・下位リンクが含まれること')


@then('対応するテストシナリオのファイルパスと行番号が含まれること')  # type: ignore
def then_ae3c7159(context):
    """対応するテストシナリオのファイルパスと行番号が含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    raise NotImplementedError('STEP: 対応するテストシナリオのファイルパスと行番号が含まれること')


@given('Doorstopプロジェクトにアイテムが存在する')  # type: ignore
def given_93d749da(context):
    """Doorstopプロジェクトにアイテムが存在する

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    raise NotImplementedError('STEP: Doorstopプロジェクトにアイテムが存在する')


@then('生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること')  # type: ignore
def then_7bdfccf5(context):
    """生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    raise NotImplementedError('STEP: 生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること')


@then('ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること')  # type: ignore
def then_ca03093b(context):
    """ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    raise NotImplementedError('STEP: ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること')


@given('プロジェクトに既存のドキュメントが存在する')  # type: ignore
def given_b7341593(context):
    """プロジェクトに既存のドキュメントが存在する

    Scenarios:
      - 出力ディレクトリの独立性
    """
    raise NotImplementedError('STEP: プロジェクトに既存のドキュメントが存在する')


@when('build コマンドをデフォルト出力先で実行する')  # type: ignore
def when_6f73d51e(context):
    """build コマンドをデフォルト出力先で実行する

    Scenarios:
      - 出力ディレクトリの独立性
    """
    raise NotImplementedError('STEP: build コマンドをデフォルト出力先で実行する')


@then('"{param0}" ディレクトリに出力されること')  # type: ignore
def then_32de837a(context, param0):
    """".specification" ディレクトリに出力されること

    Scenarios:
      - 出力ディレクトリの独立性
      - カスタム出力ディレクトリの指定
    """
    pass


@then('既存のドキュメントファイルは変更されないこと')  # type: ignore
def then_56c968de(context):
    """既存のドキュメントファイルは変更されないこと

    Scenarios:
      - 出力ディレクトリの独立性
    """
    raise NotImplementedError('STEP: 既存のドキュメントファイルは変更されないこと')


@when('build コマンドを --out-dir "{param0}" で実行する')  # type: ignore
def when_678e47f6(context, param0):
    """build コマンドを --out-dir "./custom_docs" で実行する

    Scenarios:
      - カスタム出力ディレクトリの指定
    """
    pass


@given('"{param0}" タグを持つ "{param1}" が存在する')  # type: ignore
def given_8c5d7037(context, param0, param1):
    """"@SPEC-003" タグを持つ "audit.feature" が存在する

    Scenarios:
      - feature MDページへのバックリンク生成
    """
    pass


@then('"{param0}" の冒頭に "{param1}" セクションが含まれること')  # type: ignore
def then_dcbe151a(context, param0, param1):
    """"docs/features/audit.md" の冒頭に "関連アイテム" セクションが含まれること

    Scenarios:
      - feature MDページへのバックリンク生成
    """
    pass


@then('"{param0}" へのリンクが含まれること')  # type: ignore
def then_3dd5fc62(context, param0):
    """"[SPEC-003](../items/SPEC-003.md)" へのリンクが含まれること

    Scenarios:
      - feature MDページへのバックリンク生成
    """
    pass


@given('"{param0}" と "{param1}" の両タグを持つfeatureが存在する')  # type: ignore
def given_1d9c057d(context, param0, param1):
    """"@VIS-001" と "@VIS-005" の両タグを持つfeatureが存在する

    Scenarios:
      - 複数アイテムを参照するfeatureのバックリンク
    """
    pass


@then('生成されたfeature MDの "{param0}" に "{param1}" と "{param2}" の両方のリンクが含まれること')  # type: ignore
def then_d670dbfb(context, param0, param1, param2):
    """生成されたfeature MDの "関連アイテム" に "VIS-001" と "VIS-005" の両方のリンクが含まれること

    Scenarios:
      - 複数アイテムを参照するfeatureのバックリンク
    """
    pass


@given('どのDoorstopアイテムからも参照されていないfeatureが存在する')  # type: ignore
def given_486efd83(context):
    """どのDoorstopアイテムからも参照されていないfeatureが存在する

    Scenarios:
      - タグのないfeatureにはバックリンクを表示しない
    """
    raise NotImplementedError('STEP: どのDoorstopアイテムからも参照されていないfeatureが存在する')


@then('生成されたfeature MDに "{param0}" 行が含まれないこと')  # type: ignore
def then_7458537c(context, param0):
    """生成されたfeature MDに "関連アイテム" 行が含まれないこと

    Scenarios:
      - タグのないfeatureにはバックリンクを表示しない
    """
    pass


@given('アイテムの上位リンク先が変更されている（cleared=false）')  # type: ignore
def given_5951291a(context):
    """アイテムの上位リンク先が変更されている（cleared=false）

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
    """
    raise NotImplementedError('STEP: アイテムの上位リンク先が変更されている（cleared=false）')


@then('一覧テーブルの行に "{param0}" が適用されていること')  # type: ignore
def then_011c6eae(context, param0):
    """一覧テーブルの行に "{: .suspect-row }" が適用されていること

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
      - Unreviewed Changes 警告の一覧テーブル表示
      - 複合警告の表示
    """
    pass


@then('詳細ページに Suspect Link バナーが表示されること')  # type: ignore
def then_b9db4871(context):
    """詳細ページに Suspect Link バナーが表示されること

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
    """
    raise NotImplementedError('STEP: 詳細ページに Suspect Link バナーが表示されること')


@given('アイテム自体に未レビューの変更がある（reviewed=false）')  # type: ignore
def given_60830b9f(context):
    """アイテム自体に未レビューの変更がある（reviewed=false）

    Scenarios:
      - Unreviewed Changes 警告の一覧テーブル表示
    """
    raise NotImplementedError('STEP: アイテム自体に未レビューの変更がある（reviewed=false）')


@then('詳細ページに Unreviewed Changes バナーが表示されること')  # type: ignore
def then_e1fe71d4(context):
    """詳細ページに Unreviewed Changes バナーが表示されること

    Scenarios:
      - Unreviewed Changes 警告の一覧テーブル表示
    """
    raise NotImplementedError('STEP: 詳細ページに Unreviewed Changes バナーが表示されること')


@given('アイテムに Suspect Link と Unreviewed Changes の両方がある')  # type: ignore
def given_89f3d16e(context):
    """アイテムに Suspect Link と Unreviewed Changes の両方がある

    Scenarios:
      - 複合警告の表示
    """
    raise NotImplementedError('STEP: アイテムに Suspect Link と Unreviewed Changes の両方がある')
@given('2つのシナリオを持つfeatureファイルにタグで紐づいたSPECアイテムが存在する')  # type: ignore
def given_a5569e86(context):
    """2つのシナリオを持つfeatureファイルにタグで紐づいたSPECアイテムが存在する

    Scenarios:
      - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
    """
    import tempfile
    from pathlib import Path

    tmp_dir = Path(tempfile.mkdtemp())
    context.tmp_dir = tmp_dir

    from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file
    create_doorstop_project_yaml(tmp_dir, [
        {
            "dir": "reqs",
            "prefix": "REQ",
            "parent": None,
            "items": [{"uid": "REQ-001", "header": "要件1", "testable": False}],
        },
        {
            "dir": "specs",
            "prefix": "SPEC",
            "parent": "REQ",
            "items": [{"uid": "SPEC-001", "header": "仕様1", "links": ["REQ-001"]}],
        },
    ])

    features_dir = tmp_dir / "features"
    features_dir.mkdir()
    feature_content = (
        "@SPEC-001\n"
        "Feature: テスト用フィーチャー\n\n"
        "  Scenario: シナリオその1\n"
        "    Given 前提\n"
        "    When  操作\n"
        "    Then  確認\n\n"
        "  Scenario: シナリオその2\n"
        "    Given 前提2\n"
        "    When  操作2\n"
        "    Then  確認2\n"
    )
    write_feature_file(features_dir / "test.feature", feature_content)

    out_dir = tmp_dir / "out"
    result = run_spec_weaver(
        ["build", str(features_dir), "--out-dir", str(out_dir)],
        cwd=tmp_dir,
    )
    spec_md = out_dir / "docs" / "spec.md"
    context.spec_md_content = spec_md.read_text(encoding="utf-8") if spec_md.exists() else ""
    context.build_result = result


@then('一覧テーブルの Gherkinカバレッジ列に "{param0}" が含まれること')  # type: ignore
def then_5b76eb00(context, param0):
    """一覧テーブルの Gherkinカバレッジ列に "🟢 2" が含まれること

    Scenarios:
      - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
    """
    content = getattr(context, "spec_md_content", "")
    assert param0 in content, (
        f"期待文字列 {param0!r} が spec.md に見つかりません。\n"
        f"spec.md:\n{content[:2000]}"
    )


@then('一覧テーブルのヘッダーに "{param0}" 列が含まれること')  # type: ignore
def then_eccd5afe(context, param0):
    """一覧テーブルのヘッダーに "レビュー" 列が含まれること

    Scenarios:
      - 一覧テーブルにレビューステータス列が表示されること
    """
    content = getattr(context, "spec_md_content", "")
    # ヘッダー行（| ID | タイトル | ... | レビュー | ... |）を確認
    header_line = next(
        (line for line in content.splitlines() if line.startswith("| ID ")), ""
    )
    assert param0 in header_line, (
        f"ヘッダー行に {param0!r} が見つかりません。\nヘッダー行: {header_line!r}"
    )


@then('各行にレビューステータスが表示されること')  # type: ignore
def then_8b62591d(context):
    """各行にレビューステータスが表示されること

    Scenarios:
      - 一覧テーブルにレビューステータス列が表示されること
    """
    content = getattr(context, "spec_md_content", "")
    # データ行（| SPEC-... | で始まる行）にレビューステータス文字列が含まれることを確認
    data_lines = [
        line for line in content.splitlines()
        if line.startswith("| [SPEC-") or line.startswith("| [REQ-")
    ]
    assert data_lines, "spec.md にデータ行が見つかりません。"
    for line in data_lines:
        has_review = any(marker in line for marker in ["reviewed", "suspect", "unreviewed"])
        assert has_review, f"データ行にレビューステータスが含まれません: {line!r}"
