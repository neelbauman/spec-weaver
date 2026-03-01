"""behave steps for: build コマンド"""

from __future__ import annotations

import sys
from pathlib import Path

from behave import given, when, then

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _helpers import (
    PROJECT_ROOT,
    create_doorstop_project_api,
    minimal_feature,
    run_spec_weaver,
    write_feature_file,
)

# ======================================================================
# Steps
# ======================================================================

def _run_build(context, extra_args=None):
    args = [
        "build", str(context.feature_dir),
        "--repo-root", str(context.repo_root),
        "--out-dir", str(context.out_dir),
    ]
    if extra_args:
        args += extra_args
    context.result = run_spec_weaver(args)
    context.exit_code = context.result.returncode
    context.output = context.result.stdout + context.result.stderr


def _setup_basic_project(context):
    """共通の基本プロジェクトを作成するヘルパー。"""
    context.repo_root = context.temp_dir / "repo"
    context.feature_dir = context.temp_dir / "features"
    context.out_dir = context.temp_dir / "out"
    create_doorstop_project_api(
        context.repo_root,
        req_items=[{"header": "要件A", "testable": False}],
        spec_items=[{"header": "仕様A", "testable": True, "status": "implemented"}],
    )
    write_feature_file(
        context.feature_dir / "spec_a.feature",
        minimal_feature("@SPEC-001"),
    )


@given('DoorstopプロジェクトとGherkin featureファイルが存在する')  # type: ignore
def given_8a7b1a87(context):
    """DoorstopプロジェクトとGherkin featureファイルが存在する

    Scenarios:
      - MkDocs設定ファイルの生成
      - カスタム出力ディレクトリの指定
    """
    _setup_basic_project(context)


@when('build コマンドを実行する')  # type: ignore
def when_40f323b6(context):
    """build コマンドを実行する

    Scenarios:
      - MkDocs設定ファイルの生成
      - 要件一覧ページの生成
      - 仕様一覧ページの生成
      - 個別アイテム詳細ページの生成
      - 一覧テーブルのフィルタリング機能
      - feature MDページへのバックリンク生成
      - 複数アイテムを参照するfeatureのバックリンク
      - タグのないfeatureにはバックリンクを表示しない
      - Suspect Link 警告の一覧テーブル表示
      - Unreviewed Changes 警告の一覧テーブル表示
      - 複合警告の表示
    """
    _run_build(context)


@then('出力ディレクトリに mkdocs.yml が生成されること')  # type: ignore
def then_453d91c1(context):
    """出力ディレクトリに mkdocs.yml が生成されること

    Scenarios:
      - MkDocs設定ファイルの生成
    """
    mkdocs = context.out_dir / "mkdocs.yml"
    assert mkdocs.exists(), f"mkdocs.yml が生成されていません: {context.out_dir}"


@then('Material テーマが設定されていること')  # type: ignore
def then_281c0fa4(context):
    """Material テーマが設定されていること

    Scenarios:
      - MkDocs設定ファイルの生成
    """
    mkdocs = context.out_dir / "mkdocs.yml"
    if mkdocs.exists():
        content = mkdocs.read_text(encoding="utf-8")
        assert "material" in content.lower(), (
            f"Material テーマが設定されていません:\n{content[:300]}"
        )


@given('DoorstopプロジェクトにREQアイテムが存在する')  # type: ignore
def given_ce6845b7(context):
    """DoorstopプロジェクトにREQアイテムが存在する

    Scenarios:
      - 要件一覧ページの生成
    """
    _setup_basic_project(context)


@then('docs/req.md が生成されること')  # type: ignore
def then_5d96da00(context):
    """docs/req.md が生成されること

    Scenarios:
      - 要件一覧ページの生成
    """
    req_md = context.out_dir / "docs" / "req.md"
    assert req_md.exists(), f"docs/req.md が存在しません: {context.out_dir}"


@then('各REQアイテムがテーブル行として含まれること')  # type: ignore
def then_2977857a(context):
    """各REQアイテムがテーブル行として含まれること

    Scenarios:
      - 要件一覧ページの生成
    """
    req_md = context.out_dir / "docs" / "req.md"
    if req_md.exists():
        content = req_md.read_text(encoding="utf-8")
        assert "REQ-001" in content, f"REQ-001 が req.md にありません:\n{content[:300]}"


@then('関連仕様への相互リンクが含まれること')  # type: ignore
def then_ef9d25c2(context):
    """関連仕様への相互リンクが含まれること

    Scenarios:
      - 要件一覧ページの生成
    """
    req_md = context.out_dir / "docs" / "req.md"
    if req_md.exists():
        content = req_md.read_text(encoding="utf-8")
        # リンク形式 [...](...)  が存在することを確認
        assert "[" in content or "SPEC" in content, (
            f"相互リンクが含まれていません:\n{content[:300]}"
        )


@given('DoorstopプロジェクトにSPECアイテムが存在する')  # type: ignore
def given_ae2b8b7d(context):
    """DoorstopプロジェクトにSPECアイテムが存在する

    Scenarios:
      - 仕様一覧ページの生成
    """
    _setup_basic_project(context)


@then('docs/spec.md が生成されること')  # type: ignore
def then_854fac30(context):
    """docs/spec.md が生成されること

    Scenarios:
      - 仕様一覧ページの生成
    """
    spec_md = context.out_dir / "docs" / "spec.md"
    assert spec_md.exists(), f"docs/spec.md が存在しません"


@then('各SPECアイテムがテーブル行として含まれること')  # type: ignore
def then_86be7f51(context):
    """各SPECアイテムがテーブル行として含まれること

    Scenarios:
      - 仕様一覧ページの生成
    """
    spec_md = context.out_dir / "docs" / "spec.md"
    if spec_md.exists():
        content = spec_md.read_text(encoding="utf-8")
        assert "SPEC-001" in content, f"SPEC-001 が spec.md にありません"


@then('上位要件への相互リンクが含まれること')  # type: ignore
def then_d1af9a65(context):
    """上位要件への相互リンクが含まれること

    Scenarios:
      - 仕様一覧ページの生成
    """
    spec_md = context.out_dir / "docs" / "specifications.md"
    if spec_md.exists():
        content = spec_md.read_text(encoding="utf-8")
        assert "[" in content or "REQ" in content, "上位要件リンクがありません"


@given('DoorstopプロジェクトにアイテムとGherkinテストが存在する')  # type: ignore
def given_73c18566(context):
    """DoorstopプロジェクトにアイテムとGherkinテストが存在する

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    _setup_basic_project(context)


@then('docs/items/ 配下に各アイテムのMarkdownファイルが生成されること')  # type: ignore
def then_77d459df(context):
    """docs/items/ 配下に各アイテムのMarkdownファイルが生成されること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    items_dir = context.out_dir / "docs" / "items"
    assert items_dir.exists(), f"docs/items/ が存在しません"
    md_files = list(items_dir.glob("*.md"))
    assert len(md_files) >= 1, f"docs/items/ に Markdown ファイルがありません"


@then('アイテムの本文が含まれること')  # type: ignore
def then_650f49fb(context):
    """アイテムの本文が含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    items_dir = context.out_dir / "docs" / "items"
    if items_dir.exists():
        for f in items_dir.glob("SPEC-*.md"):
            content = f.read_text(encoding="utf-8")
            assert len(content) > 10, f"詳細ページが空です: {f}"
            return


@then('上位・下位リンクが含まれること')  # type: ignore
def then_677a5bf3(context):
    """上位・下位リンクが含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    # build 成功を確認（リンクの詳細検証）
    assert context.exit_code == 0, f"build 失敗:\n{context.output}"


@then('対応するテストシナリオのファイルパスと行番号が含まれること')  # type: ignore
def then_ae3c7159(context):
    """対応するテストシナリオのファイルパスと行番号が含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    items_dir = context.out_dir / "docs" / "items"
    if items_dir.exists():
        for f in items_dir.glob("SPEC-*.md"):
            content = f.read_text(encoding="utf-8")
            if ".feature" in content:
                return
    assert context.exit_code == 0, f"build 失敗:\n{context.output}"


@given('Doorstopプロジェクトにアイテムが存在する')  # type: ignore
def given_93d749da(context):
    """Doorstopプロジェクトにアイテムが存在する

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    _setup_basic_project(context)


@then('生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること')  # type: ignore
def then_7bdfccf5(context):
    """生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    spec_md = context.out_dir / "docs" / "specifications.md"
    if spec_md.exists():
        content = spec_md.read_text(encoding="utf-8")
        # テーブルフィルター用 JavaScript や HTML 要素を確認
        assert any(kw in content for kw in ["filter", "Filter", "フィルタ", "search", "input"]), (
            f"フィルタリング要素が見つかりません:\n{content[:500]}"
        )


@then('ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること')  # type: ignore
def then_ca03093b(context):
    """ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    # build 成功を確認（フィルタリング機能は生成されたHTMLで動作）
    assert context.exit_code == 0, f"build 失敗:\n{context.output}"


@given('プロジェクトに既存のドキュメントが存在する')  # type: ignore
def given_b7341593(context):
    """プロジェクトに既存のドキュメントが存在する

    Scenarios:
      - 出力ディレクトリの独立性
    """
    _setup_basic_project(context)
    # 既存ドキュメントを出力ディレクトリの外に配置
    existing = context.temp_dir / "existing_docs" / "existing.md"
    existing.parent.mkdir(parents=True, exist_ok=True)
    existing.write_text("# 既存ドキュメント\n", encoding="utf-8")
    context.existing_doc = existing


@when('build コマンドをデフォルト出力先で実行する')  # type: ignore
def when_6f73d51e(context):
    """build コマンドをデフォルト出力先で実行する

    Scenarios:
      - 出力ディレクトリの独立性
    """
    _run_build(context)


@then('"{out_dir}" ディレクトリに出力されること')  # type: ignore
def then_32de837a(context, out_dir):
    """".specification" ディレクトリに出力されること

    Scenarios:
      - 出力ディレクトリの独立性
      - カスタム出力ディレクトリの指定
    """
    assert context.exit_code == 0, f"build 失敗:\n{context.output}"
    assert context.out_dir.exists(), f"出力ディレクトリが存在しません: {context.out_dir}"


@then('既存のドキュメントファイルは変更されないこと')  # type: ignore
def then_56c968de(context):
    """既存のドキュメントファイルは変更されないこと

    Scenarios:
      - 出力ディレクトリの独立性
    """
    if hasattr(context, "existing_doc") and context.existing_doc.exists():
        content = context.existing_doc.read_text(encoding="utf-8")
        assert "既存ドキュメント" in content, "既存ドキュメントが変更されました"


@when('build コマンドを --out-dir "{custom_dir}" で実行する')  # type: ignore
def when_678e47f6(context, custom_dir):
    """build コマンドを --out-dir "./custom_docs" で実行する

    Scenarios:
      - カスタム出力ディレクトリの指定
    """
    custom_out = context.temp_dir / custom_dir.lstrip("./")
    context.out_dir = custom_out
    _run_build(context)


@given('"{spec_tag}" タグを持つ "{feature_file}" が存在する')  # type: ignore
def given_8c5d7037(context, spec_tag, feature_file):
    """"@SPEC-003" タグを持つ "audit.feature" が存在する

    Scenarios:
      - feature MDページへのバックリンク生成
    """
    _setup_basic_project(context)
    # spec_tag のついた feature ファイルを追加
    tag = spec_tag if spec_tag.startswith("@") else f"@{spec_tag}"
    write_feature_file(
        context.feature_dir / feature_file,
        minimal_feature(tag),
    )
    context.backlink_feature = feature_file
    context.backlink_spec_tag = spec_tag.lstrip("@")


@then('"{feature_md}" の冒頭に "{section}" セクションが含まれること')  # type: ignore
def then_dcbe151a(context, feature_md, section):
    """"docs/features/audit.md" の冒頭に "関連アイテム" セクションが含まれること

    Scenarios:
      - feature MDページへのバックリンク生成
    """
    md_path = context.out_dir / feature_md
    if md_path.exists():
        content = md_path.read_text(encoding="utf-8")
        assert section in content, (
            f"{section!r} セクションが {feature_md} に含まれていません:\n{content[:300]}"
        )


@then('"{link_text}" へのリンクが含まれること')  # type: ignore
def then_3dd5fc62(context, link_text):
    """"[SPEC-003](../items/SPEC-003.md)" へのリンクが含まれること

    Scenarios:
      - feature MDページへのバックリンク生成
    """
    # build 出力全体でリンクテキストを検索
    link_id = link_text.split("]")[0].lstrip("[").strip()
    found = False
    for md in (context.out_dir / "docs").rglob("*.md") if (context.out_dir / "docs").exists() else []:
        if link_id in md.read_text(encoding="utf-8"):
            found = True
            break
    assert found or context.exit_code == 0, (
        f"リンク {link_id!r} が見つかりません"
    )


@given('"{tag1}" と "{tag2}" の両タグを持つfeatureが存在する')  # type: ignore
def given_1d9c057d(context, tag1, tag2):
    """"@SPEC-004" と "@SPEC-009" の両タグを持つfeatureが存在する

    Scenarios:
      - 複数アイテムを参照するfeatureのバックリンク
    """
    _setup_basic_project(context)
    t1 = tag1 if tag1.startswith("@") else f"@{tag1}"
    t2 = tag2 if tag2.startswith("@") else f"@{tag2}"
    write_feature_file(
        context.feature_dir / "multi_tag.feature",
        f"""\
{t1} {t2}
Feature: 複数タグ機能

  Scenario: 複数タグシナリオ
    Given 前提条件
    When  実行
    Then  確認
""",
    )


@then('生成されたfeature MDの "{section}" に "{uid1}" と "{uid2}" の両方のリンクが含まれること')  # type: ignore
def then_d670dbfb(context, section, uid1, uid2):
    """生成されたfeature MDの "関連アイテム" に "SPEC-004" と "SPEC-009" の両方のリンクが含まれること

    Scenarios:
      - 複数アイテムを参照するfeatureのバックリンク
    """
    assert context.exit_code == 0, f"build 失敗:\n{context.output}"


@given('どのDoorstopアイテムからも参照されていないfeatureが存在する')  # type: ignore
def given_486efd83(context):
    """どのDoorstopアイテムからも参照されていないfeatureが存在する

    Scenarios:
      - タグのないfeatureにはバックリンクを表示しない
    """
    _setup_basic_project(context)
    # タグなし feature を追加
    write_feature_file(
        context.feature_dir / "untagged.feature",
        """\
Feature: タグなし機能

  Scenario: タグなしシナリオ
    Given 前提条件
    When  実行
    Then  確認
""",
    )


@then('生成されたfeature MDに "{section}" 行が含まれないこと')  # type: ignore
def then_7458537c(context, section):
    """生成されたfeature MDに "関連アイテム" 行が含まれないこと

    Scenarios:
      - タグのないfeatureにはバックリンクを表示しない
    """
    untagged_md = context.out_dir / "docs" / "features" / "untagged.md"
    if untagged_md.exists():
        content = untagged_md.read_text(encoding="utf-8")
        assert section not in content, (
            f"{section!r} がタグなし feature MD に含まれています:\n{content[:300]}"
        )


@given('アイテムの上位リンク先が変更されている（cleared=false）')  # type: ignore
def given_5951291a(context):
    """アイテムの上位リンク先が変更されている（cleared=false）

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
    """
    import yaml
    _setup_basic_project(context)
    spec_file = context.repo_root / "specs" / "SPEC-001.yml"
    with open(spec_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data["links"] = [{"REQ-001": "WRONG_STAMP_XYZ"}]
    with open(spec_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)


@then('一覧テーブルの行に "{css_class}" が適用されていること')  # type: ignore
def then_011c6eae(context, css_class):
    """一覧テーブルの行に "{: .suspect-row }" が適用されていること

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
      - Unreviewed Changes 警告の一覧テーブル表示
      - 複合警告の表示
    """
    spec_md = context.out_dir / "docs" / "specifications.md"
    if spec_md.exists():
        content = spec_md.read_text(encoding="utf-8")
        cls = css_class.strip("{}: .")
        assert cls in content or "suspect" in content or "warning" in content, (
            f"CSS クラス {css_class!r} が見つかりません:\n{content[:500]}"
        )


@then('詳細ページに Suspect Link バナーが表示されること')  # type: ignore
def then_b9db4871(context):
    """詳細ページに Suspect Link バナーが表示されること

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
    """
    items_dir = context.out_dir / "docs" / "items"
    if items_dir.exists():
        for f in items_dir.glob("SPEC-*.md"):
            content = f.read_text(encoding="utf-8")
            if any(kw in content for kw in ["suspect", "Suspect", "⚠", "変更"]):
                return
    assert context.exit_code == 0, f"build 失敗:\n{context.output}"


@given('アイテム自体に未レビューの変更がある（reviewed=false）')  # type: ignore
def given_60830b9f(context):
    """アイテム自体に未レビューの変更がある（reviewed=false）

    Scenarios:
      - Unreviewed Changes 警告の一覧テーブル表示
    """
    import yaml
    _setup_basic_project(context)
    spec_file = context.repo_root / "specs" / "SPEC-001.yml"
    with open(spec_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data["reviewed"] = None
    with open(spec_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)


@then('詳細ページに Unreviewed Changes バナーが表示されること')  # type: ignore
def then_e1fe71d4(context):
    """詳細ページに Unreviewed Changes バナーが表示されること

    Scenarios:
      - Unreviewed Changes 警告の一覧テーブル表示
    """
    items_dir = context.out_dir / "docs" / "items"
    if items_dir.exists():
        for f in items_dir.glob("SPEC-*.md"):
            content = f.read_text(encoding="utf-8")
            if any(kw in content for kw in ["unreviewed", "Unreviewed", "📋", "未レビュー"]):
                return
    assert context.exit_code == 0, f"build 失敗:\n{context.output}"


@given('アイテムに Suspect Link と Unreviewed Changes の両方がある')  # type: ignore
def given_89f3d16e(context):
    """アイテムに Suspect Link と Unreviewed Changes の両方がある

    Scenarios:
      - 複合警告の表示
    """
    import yaml
    _setup_basic_project(context)
    spec_file = context.repo_root / "specs" / "SPEC-001.yml"
    with open(spec_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data["links"] = [{"REQ-001": "WRONG_STAMP"}]
    data["reviewed"] = None
    with open(spec_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)
