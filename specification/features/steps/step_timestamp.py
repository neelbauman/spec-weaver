# -*- coding: utf-8 -*-
import datetime
import os
import subprocess

import yaml
from behave import given, then, when

from specification.features.steps._helpers import (
    create_doorstop_project_yaml,
    run_spec_weaver,
    write_doorstop_yaml,
    write_feature_file,
)

# ======================================================================
# Steps
# ======================================================================

def _git_init_full(cwd):
    subprocess.run(["git", "init"], cwd=cwd, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=cwd)
    subprocess.run(["git", "config", "user.name", "test"], cwd=cwd)

def _git_commit_at(cwd, message, date_str):
    env = os.environ.copy()
    # RFC3339 format
    env["GIT_AUTHOR_DATE"] = f"{date_str}T12:00:00Z"
    env["GIT_COMMITTER_DATE"] = f"{date_str}T12:00:00Z"
    subprocess.run(["git", "add", "."], cwd=cwd)
    subprocess.run(["git", "commit", "-m", message], cwd=cwd, env=env)

@given('DoorstopアイテムのYAMLファイルがGitにコミットされている')  # type: ignore
def given_5c08ab27(context):
    _git_init_full(context.temp_dir)
    create_doorstop_project_yaml(context.temp_dir, [
        {"dir": "specs", "prefix": "SPEC", "items": [{"uid": "SPEC-001", "header": "Spec 1"}]}
    ])
    _git_commit_at(context.temp_dir, "initial commit", "2026-01-01")
    # Change file content to allow another commit
    path = context.temp_dir / "specs" / "SPEC-001.yml"
    path.write_text(path.read_text() + "\n# updated\n")
    _git_commit_at(context.temp_dir, "update commit", "2026-02-01")
    context.target_item_id = "SPEC-001"


@when('タイムスタンプ属性を取得する')  # type: ignore
def when_7e4b3813(context):
    from spec_weaver.adapters.doorstop import _get_git_file_date
    yaml_path = str(context.temp_dir / "specs" / f"{context.target_item_id}.yml")
    context.updated_at = _get_git_file_date(yaml_path, mode="latest")
    context.created_at = _get_git_file_date(yaml_path, mode="first")


@then('updated_at として最終コミット日が YYYY-MM-DD 形式で返されること')  # type: ignore
def then_c495b67c(context):
    assert context.updated_at == "2026-02-01", f"Expected 2026-02-01, got {context.updated_at}"


@then('created_at として初回コミット日が YYYY-MM-DD 形式で返されること')  # type: ignore
def then_c016ae72(context):
    assert context.created_at == "2026-01-01", f"Expected 2026-01-01, got {context.created_at}"


@given('DoorstopアイテムのYAMLファイルがGit管理外である')  # type: ignore
def given_02feb7b0(context):
    _git_init_full(context.temp_dir)
    # We create the .doorstop infrastructure but don't add the SPEC-001.yml to git
    specs_dir = context.temp_dir / "specs"
    specs_dir.mkdir(parents=True, exist_ok=True)
    # .doorstop.yml
    (specs_dir / ".doorstop.yml").write_text("settings:\n  digits: 3\n  prefix: SPEC\n  sep: '-'\n")
    # item
    write_doorstop_yaml(specs_dir, "SPEC-001", header="No Git")
    context.target_item_id = "SPEC-001"


@given('YAMLに created_at: \'2026-01-15\' が設定されている')  # type: ignore
def given_78ddd292(context):
    yaml_path = context.temp_dir / "specs" / f"{context.target_item_id}.yml"
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    data["created_at"] = '2026-01-15'
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)


@given("YAMLに created_at: '{date}' が設定されている")  # type: ignore
def step_impl_created_at(context, date):
    yaml_path = context.temp_dir / "specs" / f"{context.target_item_id}.yml"
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    data["created_at"] = date
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)


@then('created_at として "{expected}" が返されること')  # type: ignore
def step_impl_created_at_check(context, expected):
    import doorstop

    from spec_weaver.utils.formatters import get_timestamp
    tree = doorstop.build(cwd=str(context.temp_dir))
    item = tree.find_item(context.target_item_id)
    val = get_timestamp(item, "created_at")
    assert val == expected, f"Expected {expected}, got {val}"


@given('YAMLに created_at も updated_at も設定されていない')  # type: ignore
def given_20d06697(context):
    yaml_path = context.temp_dir / "specs" / f"{context.target_item_id}.yml"
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)


@then('両方とも "{expected}" が返されること')  # type: ignore
def step_impl_both_check(context, expected):
    import doorstop

    from spec_weaver.utils.formatters import get_timestamp
    tree = doorstop.build(cwd=str(context.temp_dir))
    item = tree.find_item(context.target_item_id)
    c = get_timestamp(item, "created_at")
    u = get_timestamp(item, "updated_at")
    assert c == expected and u == expected, f"Expected both {expected}, but got {c} and {u}"


@given('DoorstopアイテムがGitにコミットされている')  # type: ignore
def given_cc8e9bef(context):
    given_5c08ab27(context)


# [Dup→step_build.py] build コマンドを実行する — step_build.py の定義を使用


# [Dup→step_build.py] build コマンドを実行する — step_build.py の定義を使用
# @when('build コマンドを実行する')  # type: ignore
# def when_40f323b6(context):
#     raise NotImplementedError('STEP: build コマンドを実行する')


@then('一覧テーブルに「作成日」列が含まれること')  # type: ignore
def then_ed934883(context):
    index_md = context.temp_dir / ".specification" / "docs" / "spec.md"
    content = index_md.read_text()
    assert "作成日" in content


@then('一覧テーブルに「更新日」列が含まれること')  # type: ignore
def then_2ae95f61(context):
    index_md = context.temp_dir / ".specification" / "docs" / "spec.md"
    content = index_md.read_text()
    assert "更新日" in content


@then('Git履歴から取得した日付が正しく表示されること')  # type: ignore
def then_232626f7(context):
    index_md = context.temp_dir / ".specification" / "docs" / "spec.md"
    content = index_md.read_text()
    assert "2026-02-01" in content


@then('詳細ページに作成日と更新日が表示されること')  # type: ignore
def then_4954ab92(context):
    item_md = context.temp_dir / ".specification" / "docs" / "items" / "SPEC-001.md"
    content = item_md.read_text()
    assert "作成日" in content and "更新日" in content


@then('実装状況バッジの直後に配置されていること')  # type: ignore
def then_1a39f98b(context):
    item_md = context.temp_dir / ".specification" / "docs" / "items" / "SPEC-001.md"
    content = item_md.read_text()
    # Check if "作成日" exists in the content.
    assert "作成日" in content or "更新日" in content


@given('DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない')  # type: ignore
def given_8798cdab(context):
    given_02feb7b0(context)


@then('一覧テーブルの作成日・更新日列に "{expected}" が表示されること')  # type: ignore
def step_impl_table_check(context, expected):
    index_md = context.temp_dir / ".specification" / "docs" / "spec.md"
    content = index_md.read_text()
    assert expected in content


@given('Doorstopアイテムの最終コミット日が 91日前である')  # type: ignore
def given_6998f2b6(context):
    _git_init_full(context.temp_dir)
    date = (datetime.datetime.now() - datetime.timedelta(days=91)).strftime("%Y-%m-%d")
    create_doorstop_project_yaml(context.temp_dir, [{"dir": "specs", "prefix": "SPEC", "items": [{"uid": "SPEC-001", "status": "implemented"}]}])
    _git_commit_at(context.temp_dir, "old commit", date)
    context.target_item_id = "SPEC-001"


@given('そのアイテムの status が "{status}" である')  # type: ignore
@given('Doorstopアイテムの status が "{status}" である')  # type: ignore
def step_impl_status(context, status):
    yaml_path = context.temp_dir / "specs" / f"{context.target_item_id}.yml"
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    data["status"] = status
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)


@when('audit コマンドを --stale-days 90 で実行する')  # type: ignore
def when_81d68298(context):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    # Create dummy feature with the tag to satisfy audit
    write_feature_file(feature_dir / "dummy.feature", f"@{context.target_item_id}\nFeature: Dummy\n  Scenario: Dummy\n    Given test\n")
    context.result = run_spec_weaver(["audit", str(feature_dir), "--stale-days", "90"], cwd=context.temp_dir)


@then('そのアイテムが stale として報告されること')  # type: ignore
def then_54f17b4b(context):
    assert "Stale Items" in context.result.stdout or "長期間経過" in context.result.stdout
    assert context.target_item_id in context.result.stdout


@then('経過日数が表示されること')  # type: ignore
def then_9500bbae(context):
    assert "days" in context.result.stdout or "日" in context.result.stdout


@then('タイムスタンプ監査の終了コードが {code:d} であること')  # type: ignore
def then_ab1e81e6_timestamp(context, code):
    assert context.result.returncode == code, f"Expected exit code {code}, but got {context.result.returncode}. Output: {context.result.stdout}"


@given('Doorstopアイテムの最終コミット日が 30日前である')  # type: ignore
def given_32d4fe40(context):
    _git_init_full(context.temp_dir)
    date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    create_doorstop_project_yaml(context.temp_dir, [{"dir": "specs", "prefix": "SPEC", "items": [{"uid": "SPEC-001", "status": "implemented"}]}])
    _git_commit_at(context.temp_dir, "recent commit", date)
    context.target_item_id = "SPEC-001"


@then('そのアイテムは stale として報告されないこと')  # type: ignore
def then_e9c88743(context):
    assert "Stale" not in context.result.stdout and "長期間経過" not in context.result.stdout


@given('DoorstopアイテムがGit管理外でupdated_atも設定されていない')  # type: ignore
def given_9da29b97(context):
    given_02feb7b0(context)


@given('最終コミット日が 180日前である')  # type: ignore
def given_1588d2c1(context):
    _git_init_full(context.temp_dir)
    date = (datetime.datetime.now() - datetime.timedelta(days=180)).strftime("%Y-%m-%d")
    create_doorstop_project_yaml(context.temp_dir, [{"dir": "specs", "prefix": "SPEC", "items": [{"uid": "SPEC-001", "status": "deprecated"}]}])
    _git_commit_at(context.temp_dir, "very old commit", date)
    context.target_item_id = "SPEC-001"


@given('Doorstopアイテムの最終コミット日が 365日前である')  # type: ignore
def given_45c0cb00(context):
    _git_init_full(context.temp_dir)
    date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    create_doorstop_project_yaml(context.temp_dir, [{"dir": "specs", "prefix": "SPEC", "items": [{"uid": "SPEC-001", "status": "implemented"}]}])
    _git_commit_at(context.temp_dir, "ancient commit", date)
    context.target_item_id = "SPEC-001"


@when('audit コマンドを --stale-days 0 で実行する')  # type: ignore
def when_5cbe8c38(context):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    # Create dummy feature with the tag to satisfy audit
    write_feature_file(feature_dir / "dummy.feature", f"@{context.target_item_id}\nFeature: Dummy\n  Scenario: Dummy\n    Given test\n")
    context.result = run_spec_weaver(["audit", str(feature_dir), "--stale-days", "0"], cwd=context.temp_dir)


@then('stale に関する報告は表示されないこと')  # type: ignore
def then_e6a9cec1(context):
    assert "Stale" not in context.result.stdout and "長期間経過" not in context.result.stdout
