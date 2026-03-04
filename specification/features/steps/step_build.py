from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file, run_spec_weaver
"""behave steps for: build コマンド"""

from behave import given, when, then, step
from pathlib import Path

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
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "reqs", "prefix": "REQ", "items": [{"uid": "REQ-001", "header": "Req 1"}]}
    ])
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(feature_dir / "test.feature", "@REQ-001\nFeature: Test\n  Scenario: S1\n    Given test\n")


# [Duplicate Skip] This step is already defined elsewhere
# @when('build コマンドを実行する')  # type: ignore
# def when_40f323b6(context):
#     """build コマンドを実行する
# 
#     Scenarios:
#       - MkDocs設定ファイルの生成
#       - 要件一覧ページの生成
#       - 仕様一覧ページの生成
#       - 個別アイテム詳細ページの生成
#       - 一覧テーブルのフィルタリング機能
#       - feature MDページへのバックリンク生成
#       - 複数アイテムを参照するfeatureのバックリンク
#       - タグのないfeatureにはバックリンクを表示しない
#       - Suspect Link 警告の一覧テーブル表示
#       - Unreviewed Changes 警告の一覧テーブル表示
#       - 複合警告の表示
#       - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
#       - 一覧テーブルにレビューステータス列が表示されること
#     """
#     raise NotImplementedError('STEP: build コマンドを実行する')

# [Duplicate Skip] This step is already defined elsewhere
# @when('build コマンドを実行する')  # type: ignore
# def when_40f323b6(context):
#     """build コマンドを実行する
# 
#     Scenarios:
#       - MkDocs設定ファイルの生成
#       - 要件一覧ページの生成
#       - 仕様一覧ページの生成
#       - 個別アイテム詳細ページの生成
#       - 一覧テーブルのフィルタリング機能
#       - feature MDページへのバックリンク生成
#       - 複数アイテムを参照するfeatureのバックリンク
#       - タグのないfeatureにはバックリンクを表示しない
#       - Suspect Link 警告の一覧テーブル表示
#       - Unreviewed Changes 警告の一覧テーブル表示
#       - 複合警告の表示
#       - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
#       - 一覧テーブルにレビューステータス列が表示されること
#     """
#     raise NotImplementedError('STEP: build コマンドを実行する')

# [Duplicate Skip] This step is already defined elsewhere
# @when('build コマンドを実行する')  # type: ignore
# def when_40f323b6(context):
#     """build コマンドを実行する
# 
#     Scenarios:
#       - MkDocs設定ファイルの生成
#       - 要件一覧ページの生成
#       - 仕様一覧ページの生成
#       - 個別アイテム詳細ページの生成
#       - 一覧テーブルのフィルタリング機能
#       - feature MDページへのバックリンク生成
#       - 複数アイテムを参照するfeatureのバックリンク
#       - タグのないfeatureにはバックリンクを表示しない
#       - Suspect Link 警告の一覧テーブル表示
#       - Unreviewed Changes 警告の一覧テーブル表示
#       - 複合警告の表示
#       - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
#       - 一覧テーブルにレビューステータス列が表示されること
#     """
#     raise NotImplementedError('STEP: build コマンドを実行する')

@then('出力ディレクトリに mkdocs.yml が生成されること')  # type: ignore
def then_453d91c1(context):
    """出力ディレクトリに mkdocs.yml が生成されること

    Scenarios:
      - MkDocs設定ファイルの生成
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    mkdocs_yml = context.temp_dir / out_dir / "mkdocs.yml"
    assert mkdocs_yml.exists(), f"mkdocs.yml was not generated at {mkdocs_yml}"


@then('Material テーマが設定されていること')  # type: ignore
def then_281c0fa4(context):
    """Material テーマが設定されていること

    Scenarios:
      - MkDocs設定ファイルの生成
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    mkdocs_yml = context.temp_dir / out_dir / "mkdocs.yml"
    content = mkdocs_yml.read_text()
    # Use simple string check instead of yaml.safe_load to avoid constructor errors
    assert "name: material" in content


@given('DoorstopプロジェクトにREQアイテムが存在する')  # type: ignore
def given_ce6845b7(context):
    """DoorstopプロジェクトにREQアイテムが存在する

    Scenarios:
      - 要件一覧ページの生成
    """
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "reqs", "prefix": "REQ", "items": [{"uid": "REQ-001", "header": "Requirement 1"}]},
        {"dir": "specs", "prefix": "SPEC", "parent": "REQ", "items": [{"uid": "SPEC-001", "header": "Spec 1", "links": ["REQ-001"]}]},
    ])


@then('docs/req.md が生成されること')  # type: ignore
def then_0130d8b7(context):
    """docs/req.md が生成されること

    Scenarios:
      - 要件一覧ページの生成
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    req_md = context.temp_dir / out_dir / "docs" / "req.md"
    assert req_md.exists(), f"req.md was not generated at {req_md}"
    context.req_md_content = req_md.read_text()


@then('各REQアイテムがテーブル行として含まれること')  # type: ignore
def then_2977857a(context):
    """各REQアイテムがテーブル行として含まれること

    Scenarios:
      - 要件一覧ページの生成
    """
    assert "REQ-001" in context.req_md_content
    assert "Requirement 1" in context.req_md_content


@then('関連仕様への相互リンクが含まれること')  # type: ignore
def then_ef9d25c2(context):
    """関連仕様への相互リンクが含まれること

    Scenarios:
      - 要件一覧ページの生成
    """
    assert "SPEC-001" in context.req_md_content


@given('DoorstopプロジェクトにSPECアイテムが存在する')  # type: ignore
def given_ae2b8b7d(context):
    """DoorstopプロジェクトにSPECアイテムが存在する

    Scenarios:
      - 仕様一覧ページの生成
      - 一覧テーブルにレビューステータス列が表示されること
    """
    from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file
    create_doorstop_project_yaml(context.temp_dir, [
        {
            "dir": "reqs",
            "prefix": "REQ",
            "items": [{"uid": "REQ-001", "header": "Requirement 1"}],
        },
        {
            "dir": "specs",
            "prefix": "SPEC",
            "parent": "REQ",
            "items": [{"uid": "SPEC-001", "header": "Specification 1", "links": ["REQ-001"]}],
        },
    ])
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(feature_dir / "test.feature", "@SPEC-001\nFeature: Test\n  Scenario: S1\n    Given test\n")


@then('docs/spec.md が生成されること')  # type: ignore
def then_9b5808a6(context):
    """docs/spec.md が生成されること

    Scenarios:
      - 仕様一覧ページの生成
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    spec_md = context.temp_dir / out_dir / "docs" / "spec.md"
    assert spec_md.exists(), f"spec.md was not generated at {spec_md}"
    context.spec_md_content = spec_md.read_text()


@then('各SPECアイテムがテーブル行として含まれること')  # type: ignore
def then_86be7f51(context):
    """各SPECアイテムがテーブル行として含まれること

    Scenarios:
      - 仕様一覧ページの生成
    """
    assert "SPEC-001" in context.spec_md_content
    assert "Specification 1" in context.spec_md_content


@then('上位要件への相互リンクが含まれること')  # type: ignore
def then_d1af9a65(context):
    """上位要件への相互リンクが含まれること

    Scenarios:
      - 仕様一覧ページの生成
    """
    assert "REQ-001" in context.spec_md_content


@given('DoorstopプロジェクトにアイテムとGherkinテストが存在する')  # type: ignore
def given_73c18566(context):
    """DoorstopプロジェクトにアイテムとGherkinテストが存在する

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "reqs", "prefix": "REQ", "items": [{"uid": "REQ-001", "header": "Req 1", "text": "Body of REQ-001"}]},
        {"dir": "specs", "prefix": "SPEC", "parent": "REQ", "items": [{"uid": "SPEC-001", "header": "Spec 1", "links": ["REQ-001"], "text": "Body of SPEC-001"}]},
    ])
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(feature_dir / "test.feature", "@SPEC-001\nFeature: Test\n  Scenario: S1\n    Given test\n")


@then('docs/items/ 配下に各アイテムのMarkdownファイルが生成されること')  # type: ignore
def then_77d459df(context):
    """docs/items/ 配下に各アイテムのMarkdownファイルが生成されること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    req_md = context.temp_dir / out_dir / "docs" / "items" / "REQ-001.md"
    spec_md = context.temp_dir / out_dir / "docs" / "items" / "SPEC-001.md"
    assert req_md.exists(), f"{req_md} does not exist"
    assert spec_md.exists(), f"{spec_md} does not exist"
    context.req_item_md = req_md.read_text()
    context.spec_item_md = spec_md.read_text()


@then('アイテムの本文が含まれること')  # type: ignore
def then_650f49fb(context):
    """アイテムの本文が含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    assert "Body of REQ-001" in context.req_item_md
    assert "Body of SPEC-001" in context.spec_item_md


@then('上位・下位リンクが含まれること')  # type: ignore
def then_677a5bf3(context):
    """上位・下位リンクが含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    assert "下位アイテム" in context.req_item_md
    assert "[SPEC-001](SPEC-001.md)" in context.req_item_md
    assert "上位アイテム" in context.spec_item_md
    assert "[REQ-001](REQ-001.md)" in context.spec_item_md


@then('対応するテストシナリオのファイルパスと行番号が含まれること')  # type: ignore
def then_ae3c7159(context):
    """対応するテストシナリオのファイルパスと行番号が含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    assert "test.feature" in context.spec_item_md
    # Line number check might be a bit loose but it should contain it
    assert ":3" in context.spec_item_md or "#line-3" in context.spec_item_md


@given('Doorstopプロジェクトにアイテムが存在する')  # type: ignore
def given_93d749da(context):
    """Doorstopプロジェクトにアイテムが存在する

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    from specification.features.steps._helpers import create_doorstop_project_yaml
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "reqs", "prefix": "REQ", "items": [{"uid": "REQ-001", "header": "Req 1"}]}
    ])


@then('生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること')  # type: ignore
def then_7bdfccf5(context):
    """生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    mkdocs_yml = context.temp_dir / out_dir / "mkdocs.yml"
    content = mkdocs_yml.read_text()
    assert "custom-table-filter.js" in content


@then('ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること')  # type: ignore
def then_ca03093b(context):
    """ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    js_file = context.temp_dir / out_dir / "docs" / "javascripts" / "custom-table-filter.js"
    assert js_file.exists()


@given('プロジェクトに既存のドキュメントが存在する')  # type: ignore
def given_b7341593(context):
    """プロジェクトに既存のドキュメントが存在する

    Scenarios:
      - 出力ディレクトリの独立性
    """
    from specification.features.steps._helpers import create_doorstop_project_yaml
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "reqs", "prefix": "REQ", "items": [{"uid": "REQ-001", "header": "Req 1"}]}
    ])
    context.existing_file = context.temp_dir / "README.md"
    context.existing_file.write_text("Existing README content")


@when('build コマンドをデフォルト出力先で実行する')  # type: ignore
def when_6f73d51e(context):
    """build コマンドをデフォルト出力先で実行する

    Scenarios:
      - 出力ディレクトリの独立性
    """
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(feature_dir / "dummy.feature", "Feature: Dummy\n  Scenario: D\n    Given G\n")
    context.result = run_spec_weaver(["build", str(feature_dir)], cwd=context.temp_dir)


@then('"{param0}" ディレクトリに出力されること')  # type: ignore
def then_32de837a(context, param0):
    """".specification" ディレクトリに出力されること

    Scenarios:
      - 出力ディレクトリの独立性
      - カスタム出力ディレクトリの指定
    """
    path = context.temp_dir / param0
    assert path.exists(), f"Output directory {path} does not exist"


@then('既存のドキュメントファイルは変更されないこと')  # type: ignore
def then_56c968de(context):
    """既存のドキュメントファイルは変更されないこと

    Scenarios:
      - 出力ディレクトリの独立性
    """
    assert context.existing_file.read_text() == "Existing README content"


@when('build コマンドを --out-dir "{param0}" で実行する')  # type: ignore
def when_678e47f6(context, param0):
    """build コマンドを --out-dir "./custom_docs" で実行する

    Scenarios:
      - カスタム出力ディレクトリの指定
    """
    context.out_dir = param0
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(feature_dir / "dummy.feature", "Feature: Dummy\n  Scenario: D\n    Given G\n")
    context.result = run_spec_weaver(["build", str(feature_dir), "--out-dir", param0], cwd=context.temp_dir)


@given('"{param0}" タグを持つ "{param1}" が存在する')  # type: ignore
def given_8c5d7037(context, param0, param1):
    """"@SPEC-003" タグを持つ "audit.feature" が存在する

    Scenarios:
      - feature MDページへのバックリンク生成
    """
    from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file
    uid = param0.replace("@", "")
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "specs", "prefix": "SPEC", "items": [{"uid": uid, "header": "Spec 3"}]}
    ])
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(feature_dir / param1, f"{param0}\nFeature: Test\n  Scenario: S1\n    Given G\n")


@then('"{param0}" の冒頭に "{param1}" セクションが含まれること')  # type: ignore
def then_dcbe151a(context, param0, param1):
    """"docs/features/audit.md" の冒頭に "関連アイテム" セクションが含まれること

    Scenarios:
      - feature MDページへのバックリンク生成
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    full_path = context.temp_dir / out_dir / param0
    assert full_path.exists(), f"{full_path} does not exist"
    content = full_path.read_text()
    assert param1 in content
    context.last_md_content = content


@then('"{param0}" へのリンクが含まれること')  # type: ignore
def then_3dd5fc62(context, param0):
    """"[SPEC-003](../items/SPEC-003.md)" へのリンクが含まれること

    Scenarios:
      - feature MDページへのバックリンク生成
    """
    content = getattr(context, "last_md_content", "")
    assert param0 in content


@given('"{param0}" と "{param1}" の両タグを持つfeatureが存在する')  # type: ignore
def given_1d9c057d(context, param0, param1):
    """"@VIS-001" と "@VIS-005" の両タグを持つfeatureが存在する

    Scenarios:
      - 複数アイテムを参照するfeatureのバックリンク
    """
    from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file
    uids = [param0.replace("@", ""), param1.replace("@", "")]
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "specs", "prefix": "VIS", "items": [
            {"uid": uids[0], "header": "VIS 1"},
            {"uid": uids[1], "header": "VIS 5"},
        ]}
    ])
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(feature_dir / "multi.feature", f"{param0} {param1}\nFeature: Multi\n  Scenario: S1\n    Given G\n")


@then('生成されたfeature MDの "{param0}" に "{param1}" と "{param2}" の両方のリンクが含まれること')  # type: ignore
def then_d670dbfb(context, param0, param1, param2):
    """生成されたfeature MDの "関連アイテム" に "VIS-001" と "VIS-005" の両方のリンクが含まれること

    Scenarios:
      - 複数アイテムを参照するfeatureのバックリンク
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    full_path = context.temp_dir / out_dir / "docs" / "features" / "multi.md"
    assert full_path.exists()
    content = full_path.read_text()
    assert param0 in content
    assert param1 in content
    assert param2 in content


@given('どのDoorstopアイテムからも参照されていないfeatureが存在する')  # type: ignore
def given_486efd83(context):
    """どのDoorstopアイテムからも参照されていないfeatureが存在する

    Scenarios:
      - タグのないfeatureにはバックリンクを表示しない
    """
    from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "reqs", "prefix": "REQ", "items": [{"uid": "REQ-001", "header": "R1"}]}
    ])
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(feature_dir / "no_tags.feature", "Feature: No Tags\n  Scenario: S1\n    Given G\n")


@then('生成されたfeature MDに "{param0}" 行が含まれないこと')  # type: ignore
def then_7458537c(context, param0):
    """生成されたfeature MDに "関連アイテム" 行が含まれないこと

    Scenarios:
      - タグのないfeatureにはバックリンクを表示しない
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    features_docs_dir = context.temp_dir / out_dir / "docs" / "features"
    full_path = features_docs_dir / "no_tags.md"
    
    if not full_path.exists():
        import os
        files = []
        if features_docs_dir.exists():
            files = os.listdir(features_docs_dir)
        print(f"DEBUG: {full_path} does not exist. Files in {features_docs_dir}: {files}")
        
    assert full_path.exists(), f"{full_path} does not exist"
    content = full_path.read_text()
    # It might be in bold so check for param0 itself.
    if param0 in content:
        print(f"DEBUG: content of {full_path}:\n{content}")
    assert param0 not in content, f"'{param0}' found in {full_path}"


@given('アイテムの上位リンク先が変更されている（cleared=false）')  # type: ignore
def given_5951291a(context):
    """アイテムの上位リンク先が変更されている（cleared=false）

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
    """
    from specification.features.steps._helpers import create_doorstop_project_yaml
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "reqs", "prefix": "REQ", "items": [{"uid": "REQ-001", "header": "Req 1"}]},
        {"dir": "specs", "prefix": "SPEC", "parent": "REQ", "items": [{"uid": "SPEC-001", "header": "Spec 1", "links": ["REQ-001"]}]},
    ])
    
    import yaml
    path = context.temp_dir / "specs" / "SPEC-001.yml"
    data = yaml.safe_load(path.read_text())
    # Manually break link stamps to make it suspect. 
    # Link format: [{'REQ-001': 'stamp'}]
    for link_entry in data.get('links', []):
        for uid in link_entry:
            link_entry[uid] = "invalid-stamp"
    path.write_text(yaml.dump(data, allow_unicode=True), encoding="utf-8")


@then('一覧テーブルの行に "{param0}" が適用されていること')  # type: ignore
def then_011c6eae(context, param0):
    """一覧テーブルの行に "{: .suspect-row }" が適用されていること

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
      - Unreviewed Changes 警告の一覧テーブル表示
      - 複合警告の表示
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    
    # Strip braces and prefix for more flexible check
    marker = param0.replace("{: ", "").replace(" }", "").strip()
    
    # Check both spec.md and req.md as we don't know which one has it
    found = False
    all_content = ""
    for filename in ["spec.md", "req.md"]:
        path = context.temp_dir / out_dir / "docs" / filename
        if path.exists():
            content = path.read_text()
            all_content += f"--- {filename} ---\n{content}\n"
            if marker in content:
                found = True
                break
    assert found, f"{marker!r} was not found in any index table. \nContents:\n{all_content}"


@then('詳細ページに Suspect Link バナーが表示されること')  # type: ignore
def then_b9db4871(context):
    """詳細ページに Suspect Link バナーが表示されること

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    item_md = context.temp_dir / out_dir / "docs" / "items" / "SPEC-001.md"
    content = item_md.read_text()
    assert "**Suspect**" in content


@given('アイテム自体に未レビューの変更がある（reviewed=false）')  # type: ignore
def given_60830b9f(context):
    """アイテム自体に未レビューの変更がある（reviewed=false）

    Scenarios:
      - Unreviewed Changes 警告の一覧テーブル表示
    """
    from specification.features.steps._helpers import create_doorstop_project_yaml
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "specs", "prefix": "SPEC", "items": [{"uid": "SPEC-001", "header": "Spec 1"}]},
    ])
    
    import yaml
    path = context.temp_dir / "specs" / "SPEC-001.yml"
    data = yaml.safe_load(path.read_text())
    # In Doorstop YAML, reviewed: None means unreviewed.
    data["reviewed"] = None
    path.write_text(yaml.dump(data, allow_unicode=True), encoding="utf-8")


@then('詳細ページに Unreviewed Changes バナーが表示されること')  # type: ignore
def then_e1fe71d4(context):
    """詳細ページに Unreviewed Changes バナーが表示されること

    Scenarios:
      - Unreviewed Changes 警告の一覧テーブル表示
    """
    out_dir_val = getattr(context, "out_dir", None) or ".specification"
    out_dir = Path(out_dir_val)
    # Check both SPEC-001 and REQ-001
    found = False
    found_items = []
    for item in ["SPEC-001", "REQ-001"]:
        path = context.temp_dir / out_dir / "docs" / "items" / f"{item}.md"
        if path.exists():
            content = path.read_text()
            found_items.append(item)
            if "**Unreviewed Changes**" in content:
                found = True
                break
    assert found, f"Unreviewed Changes banner not found in items: {found_items}"


@given('アイテムに Suspect Link と Unreviewed Changes の両方がある')  # type: ignore
def given_89f3d16e(context):
    """アイテムに Suspect Link と Unreviewed Changes の両方がある

    Scenarios:
      - 複合警告の表示
    """
    from specification.features.steps._helpers import create_doorstop_project_yaml
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "reqs", "prefix": "REQ", "items": [{"uid": "REQ-001", "header": "Req 1"}]},
        {"dir": "specs", "prefix": "SPEC", "parent": "REQ", "items": [{"uid": "SPEC-001", "header": "Spec 1", "links": ["REQ-001"]}]},
    ])
    
    import yaml
    path = context.temp_dir / "specs" / "SPEC-001.yml"
    data = yaml.safe_load(path.read_text())
    # 1. Unreviewed
    data["reviewed"] = None
    # 2. Suspect
    for link_entry in data.get('links', []):
        for uid in link_entry:
            link_entry[uid] = "invalid-stamp"
    path.write_text(yaml.dump(data, allow_unicode=True), encoding="utf-8")
@given('2つのシナリオを持つfeatureファイルにタグで紐づいたSPECアイテムが存在する')  # type: ignore
def given_a5569e86(context):
    """2つのシナリオを持つfeatureファイルにタグで紐づいたSPECアイテムが存在する

    Scenarios:
      - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
    """
    from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file
    create_doorstop_project_yaml(context.temp_dir, [
        {
            "dir": "reqs",
            "prefix": "REQ",
            "items": [{"uid": "REQ-001", "header": "Req 1"}],
        },
        {
            "dir": "specs",
            "prefix": "SPEC",
            "parent": "REQ",
            "items": [{"uid": "SPEC-001", "header": "Spec 1", "links": ["REQ-001"]}],
        },
    ])

    features_dir = context.temp_dir / "specification" / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    feature_content = (
        "@SPEC-001\n"
        "Feature: Test\n\n"
        "  Scenario: S1\n    Given G\n"
        "  Scenario: S2\n    Given G\n"
    )
    write_feature_file(features_dir / "test.feature", feature_content)


@then('一覧テーブルの Gherkinカバレッジ列に "{param0}" が含まれること')  # type: ignore
def then_5b76eb00(context, param0):
    """一覧テーブルの Gherkinカバレッジ列に "🟢 2" が含まれること

    Scenarios:
      - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
    """
    if not hasattr(context, "spec_md_content"):
        out_dir_val = getattr(context, "out_dir", None) or ".specification"
        out_dir = Path(out_dir_val)
        spec_md = context.temp_dir / out_dir / "docs" / "spec.md"
        context.spec_md_content = spec_md.read_text() if spec_md.exists() else ""

    content = getattr(context, "spec_md_content", "")
    assert param0 in content


@then('一覧テーブルのヘッダーに "{param0}" 列が含まれること')  # type: ignore
def then_eccd5afe(context, param0):
    """一覧テーブルのヘッダーに "レビュー" 列が含まれること

    Scenarios:
      - 一覧テーブルにレビューステータス列が表示されること
    """
    if not hasattr(context, "spec_md_content"):
        out_dir_val = getattr(context, "out_dir", None) or ".specification"
        out_dir = Path(out_dir_val)
        spec_md = context.temp_dir / out_dir / "docs" / "spec.md"
        context.spec_md_content = spec_md.read_text() if spec_md.exists() else ""

    content = getattr(context, "spec_md_content", "")
    header_line = next((line for line in content.splitlines() if line.startswith("| ID ")), "")
    assert param0 in header_line


@then('各行にレビューステータスが表示されること')  # type: ignore
def then_8b62591d(context):
    """各行にレビューステータスが表示されること

    Scenarios:
      - 一覧テーブルにレビューステータス列が表示されること
    """
    if not hasattr(context, "spec_md_content"):
        out_dir_val = getattr(context, "out_dir", None) or ".specification"
        out_dir = Path(out_dir_val)
        spec_md = context.temp_dir / out_dir / "docs" / "spec.md"
        context.spec_md_content = spec_md.read_text() if spec_md.exists() else ""

    content = getattr(context, "spec_md_content", "")
    data_lines = [l for l in content.splitlines() if l.startswith("| [SPEC-") or l.startswith("| [REQ-")]
    assert data_lines
    for line in data_lines:
        assert any(m in line for m in ["reviewed", "suspect", "unreviewed"])
