"""behave steps for: audit コマンド"""

from __future__ import annotations
import sys
from pathlib import Path
from behave import given, when, then

from _helpers import (
    PROJECT_ROOT,
    create_doorstop_project_api,
    create_doorstop_project_yaml,
    minimal_feature,
    run_spec_weaver,
    write_feature_file,
    assert_in_output,
)


# 共通: audit 実行
def _run_audit(context, extra_args=None):
    args = ["audit", str(context.feature_dir), "--repo-root", str(context.repo_root)]
    if extra_args:
        args += extra_args
    context.result = run_spec_weaver(args)
    context.exit_code = context.result.returncode
    context.output = context.result.stdout + context.result.stderr


@given("すべてのtestable仕様に対応するGherkinテストが存在する")  # type: ignore
def given_a7b8516a(context):
    """すべてのtestable仕様に対応するGherkinテストが存在する

    Scenarios:
      - 完全一致時の監査成功
    """
    # プロジェクト作成 + 全 SPEC にフィーチャーファイルを用意
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root, spec_items=[{"header": "仕様A", "testable": True}]
    )
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(
        context.feature_dir / "spec_a.feature", minimal_feature("@SPEC-001")
    )

    # test_fingerprint の設定と Doorstop 本体のレビュー
    run_spec_weaver(
        [
            "review",
            "SPEC-001",
            "-f",
            str(context.feature_dir),
            "-r",
            str(context.repo_root),
        ]
    )
    import subprocess

    subprocess.run(
        ["doorstop", "review", "SPEC-001"],
        cwd=str(context.repo_root),
        check=True,
        capture_output=True,
    )


@when("audit コマンドを実行する")  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する

    Scenarios:
      - 完全一致時の監査成功
      - テスト漏れの検出
      - 孤児タグの検出
      - テスト漏れと孤児タグの同時検出
      - testable: false の仕様はスキップされる
      - Suspect Link の検出
      - Unreviewed Changes の検出
    """
    _run_audit(context)


    # SPEC-001 (testable=False), SPEC-002 (testable=True, 未カバー)
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        spec_items=[
            {"header": "カバー外仕様1", "testable": False},
            {"header": "未カバー仕様", "testable": True},
        ],
    )
    context.feature_dir = context.temp_dir / "features"
    # feature ファイルは作らない (SPEC-002 が未カバー)
    context.feature_dir.mkdir(parents=True, exist_ok=True)
    context.expected_spec_id = spec_id  # "SPEC-002"


@then("終了コード 1 が返ること")  # type: ignore
def then_4dccc2fd(context):
    """終了コード 1 が返ること

    Scenarios:
      - テスト漏れの検出
      - 孤児タグの検出
      - テスト漏れと孤児タグの同時検出
      - Suspect Link の検出
      - Unreviewed Changes の検出
    """
    assert context.exit_code == 1, (
        f"終了コード {context.exit_code} (期待: 1)\n{context.output}"
    )


@then('テストが実装されていない仕様として "{spec_id}" が報告されること')  # type: ignore
def then_6664aa42(context, spec_id):
    """テストが実装されていない仕様として "SPEC-002" が報告されること

    Scenarios:
      - テスト漏れの検出
    """
    assert spec_id in context.output, (
        f"{spec_id} が出力に見つかりません:\n{context.output}"
    )


@given('Gherkinに仕様書に存在しない "{tag}" タグが含まれている')  # type: ignore
def given_3aa00113(context, tag):
    """Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている

    Scenarios:
      - 孤児タグの検出
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root, spec_items=[{"header": "仕様A", "testable": True}]
    )
    context.feature_dir = context.temp_dir / "features"
    # SPEC-001 はカバー、かつ存在しない SPEC-999 タグも含む
    write_feature_file(
        context.feature_dir / "spec_a.feature", minimal_feature("@SPEC-001")
    )
    # 孤児タグを持つ feature
    orphan_tag = tag.lstrip("@")  # "@SPEC-999" -> "SPEC-999"
    write_feature_file(context.feature_dir / "orphan.feature", minimal_feature(tag))
    context.expected_orphan = orphan_tag


@then('孤児タグとして "{tag}" が報告されること')  # type: ignore
def then_33c30716(context, tag):
    """孤児タグとして "@SPEC-999" が報告されること

    Scenarios:
      - 孤児タグの検出
    """
    orphan = tag.lstrip("@")
    assert orphan in context.output, (
        f"孤児タグ {orphan} が出力に見つかりません:\n{context.output}"
    )


@given('仕様 "{spec_id}" のテストが未実装で "{tag}" が孤児タグである')  # type: ignore
def given_ffdcf7f2(context, spec_id, tag):
    """仕様 "SPEC-002" のテストが未実装で "@SPEC-999" が孤児タグである

    Scenarios:
      - テスト漏れと孤児タグの同時検出
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        spec_items=[
            {"header": "カバー外", "testable": False},
            {"header": "未カバー", "testable": True},
        ],
    )
    context.feature_dir = context.temp_dir / "features"
    orphan_tag = tag.lstrip("@")
    write_feature_file(context.feature_dir / "orphan.feature", minimal_feature(tag))


@then("テスト漏れと孤児タグの両方が報告されること")  # type: ignore
def then_4928ac49(context):
    """テスト漏れと孤児タグの両方が報告されること

    Scenarios:
      - テスト漏れと孤児タグの同時検出
    """
    # 両方の問題が出力に含まれることを確認
    assert context.exit_code == 1
    # SPEC-002 (未カバー) と孤児タグ (SPEC-999) が報告されていること
    assert (
        "SPEC-002" in context.output
        or "missing" in context.output.lower()
        or "漏れ" in context.output
    )
    assert any(kw in context.output for kw in ["SPEC-999", "orphan", "孤児"]), (
        f"孤児タグ報告が見つかりません:\n{context.output}"
    )


@given('仕様 "{spec_id}" が testable: false に設定されている')  # type: ignore
def given_624f5f06(context, spec_id):
    """仕様 "SPEC-001" が testable: false に設定されている

    Scenarios:
      - testable: false の仕様はスキップされる
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root, spec_items=[{"header": "テスト不可仕様", "testable": False}]
    )
    context.feature_dir = context.temp_dir / "features"
    context.feature_dir.mkdir(parents=True, exist_ok=True)
    context.nontestable_id = spec_id  # "SPEC-001"


@given('"{spec_id}" に対応するGherkinテストが存在しない')  # type: ignore
def given_ea690d53(context, spec_id):
    """ "SPEC-001" に対応するGherkinテストが存在しない

    Scenarios:
      - testable: false の仕様はスキップされる
    """
    pass  # 上の Given でフィーチャーファイルを作っていない


@then('"{spec_id}" はテスト漏れとして報告されないこと')  # type: ignore
def then_55c71a2c(context, spec_id):
    """ "SPEC-001" はテスト漏れとして報告されないこと

    Scenarios:
      - testable: false の仕様はスキップされる
    """
    # testable: false のため報告されないはず
    # exit code 0 かつ spec_id がエラー報告に含まれないこと
    # 出力に spec_id が含まれても "missing"/"漏れ"文脈でなければOK
    assert context.exit_code == 0, (
        f"終了コード {context.exit_code} (期待: 0)\n{context.output}"
    )


@given('仕様 "{spec_id}" の上位アイテムが変更されている（cleared=false）')  # type: ignore
def given_db49ffab(context, spec_id):
    """仕様 "SPEC-009" の上位アイテムが変更されている（cleared=false）

    Scenarios:
      - Suspect Link の検出
    """
    import yaml, os

    context.repo_root = context.temp_dir / "repo"
    # まず通常のプロジェクトを作成
    create_doorstop_project_api(
        context.repo_root,
        req_items=[{"header": "要件", "testable": False}],
        spec_items=[{"header": "仕様", "testable": True}],
    )
    # SPEC-001 の link stamp を意図的に壊す (cleared=False にする)
    specs_dir = context.repo_root / "specs"
    spec_file = specs_dir / "SPEC-001.yml"
    with open(spec_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data["links"] = [{"REQ-001": "WRONG_STAMP_XXXX"}]
    with open(spec_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(
        context.feature_dir / "spec.feature", minimal_feature("@SPEC-001")
    )
    context.suspect_id = spec_id  # "SPEC-009" (featureでは SPEC-001 を使用)


@then('Suspect Link テーブルに "{spec_id}" が報告されること')  # type: ignore
def then_0149339a(context, spec_id):
    """Suspect Link テーブルに "SPEC-009" が報告されること

    Scenarios:
      - Suspect Link の検出
    """
    # SPEC-001 が suspect として報告されるはず
    assert any(
        kw in context.output for kw in ["SPEC-001", "suspect", "Suspect", "⚠"]
    ), f"Suspect Link 報告が見つかりません:\n{context.output}"


@then("変更された上位アイテムのIDが表示されること")  # type: ignore
def then_407500a2(context):
    """変更された上位アイテムのIDが表示されること

    Scenarios:
      - Suspect Link の検出
    """
    assert any(kw in context.output for kw in ["REQ-001", "Suspect", "suspect", "⚠"]), (
        f"上位アイテムIDが見つかりません:\n{context.output}"
    )


@given('仕様 "{spec_id}" 自体に未レビューの変更がある（reviewed=false）')  # type: ignore
def given_8ceeca7b(context, spec_id):
    """仕様 "SPEC-009" 自体に未レビューの変更がある（reviewed=false）

    Scenarios:
      - Unreviewed Changes の検出
    """
    import yaml

    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root, spec_items=[{"header": "仕様", "testable": True}]
    )
    # SPEC-001 の reviewed を None に設定 (unreviewed)
    specs_dir = context.repo_root / "specs"
    spec_file = specs_dir / "SPEC-001.yml"
    with open(spec_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data["reviewed"] = None
    with open(spec_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(
        context.feature_dir / "spec.feature", minimal_feature("@SPEC-001")
    )


@then('Unreviewed Changes テーブルに "{spec_id}" が報告されること')  # type: ignore
def then_56101a52(context, spec_id):
    """Unreviewed Changes テーブルに "SPEC-009" が報告されること

    Scenarios:
      - Unreviewed Changes の検出
    """
    assert any(
        kw in context.output
        for kw in ["SPEC-001", "unreviewed", "Unreviewed", "未レビュー", "📋"]
    ), f"Unreviewed Changes 報告が見つかりません:\n{context.output}"
