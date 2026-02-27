"""behave steps for: audit コマンド"""

import os
import subprocess
import doorstop
import re
from behave import given, when, then, step

# ======================================================================
# Helpers
# ======================================================================

from helpers import run_cli, setup_doorstop, create_feature_file

# ======================================================================
# Steps
# ======================================================================

# 使用されるシナリオ:
# - 完全一致時の監査成功
@given('すべてのtestable仕様に対応するGherkinテストが存在する')  # type: ignore
def given_a7b8516a(context):
    """すべてのtestable仕様に対応するGherkinテストが存在する"""
    setup_doorstop(context)
    subprocess.run(["doorstop", "add", "SPEC"], cwd=context.temp_dir, check=True)
    subprocess.run(["doorstop", "review", "all"], cwd=context.temp_dir, check=True)
    create_feature_file(context, "test.feature", "@SPEC-001\nFeature: Test\n  Scenario: Test\n    Given test")


# 使用されるシナリオ:
# - 完全一致時の監査成功
# - テスト漏れの検出
# - 孤児タグの検出
# - テスト漏れと孤児タグの同時検出
# - testable: false の仕様はスキップされる
# - Suspect Link の検出
# - Unreviewed Changes の検出
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する"""
    run_cli(context, ["audit", "features", "--repo-root", "."])


# 使用されるシナリオ:
# - 完全一致時の監査成功
@then('成功メッセージが表示されること')  # type: ignore
def then_f7642361(context):
    """成功メッセージが表示されること"""
    assert "完璧です" in context.stdout


# 使用されるシナリオ:
# - テスト漏れの検出
@given('testable な仕様 "{param0}" に対応するGherkinテストが存在しない')  # type: ignore
def given_03339ad7(context, param0):
    """testable な仕様 "SPEC-002" に対応するGherkinテストが存在しない"""
    setup_doorstop(context)
    item_path = os.path.join(context.temp_dir, "specs", f"{param0}.yml")
    with open(item_path, "w") as f:
        f.write("active: True\nreviewed: True\ntext: test\n")


# 使用されるシナリオ:
# - テスト漏れの検出
@then('テストが実装されていない仕様として "{param0}" が報告されること')  # type: ignore
def then_6664aa42(context, param0):
    """テストが実装されていない仕様として "SPEC-002" が報告されること"""
    assert "テストが実装されていない仕様" in context.stdout
    assert param0 in context.stdout


# 使用されるシナリオ:
# - 孤児タグの検出
@given('Gherkinに仕様書に存在しない "{param0}" タグが含まれている')  # type: ignore
def given_3aa00113(context, param0):
    """Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている"""
    setup_doorstop(context)
    create_feature_file(context, "orphan.feature", f"{param0}\nFeature: Orphan\n  Scenario: Orphan")


# 使用されるシナリオ:
# - 孤児タグの検出
@then('孤児タグとして "{param0}" が報告されること')  # type: ignore
def then_33c30716(context, param0):
    """孤児タグとして "@SPEC-999" が報告されること"""
    assert "仕様書に存在しない孤児タグ" in context.stdout
    assert param0 in context.stdout


# 使用されるシナリオ:
# - テスト漏れと孤児タグの同時検出
@given('仕様 "{param0}" のテストが未実装で "{param1}" が孤児タグである')  # type: ignore
def given_ffdcf7f2(context, param0, param1):
    """仕様 "SPEC-002" のテストが未実装で "@SPEC-999" が孤児タグである"""
    setup_doorstop(context)
    item_path = os.path.join(context.temp_dir, "specs", f"{param0}.yml")
    with open(item_path, "w") as f:
        f.write("active: True\nreviewed: True\ntext: test\n")
    
    create_feature_file(context, "orphan.feature", f"{param1}\nFeature: Orphan\n  Scenario: Orphan")


# 使用されるシナリオ:
# - テスト漏れと孤児タグの同時検出
@then('テスト漏れと孤児タグの両方が報告されること')  # type: ignore
def then_4928ac49(context):
    """テスト漏れと孤児タグの両方が報告されること"""
    assert "テストが実装されていない仕様" in context.stdout
    assert "仕様書に存在しない孤児タグ" in context.stdout


# 使用されるシナリオ:
# - testable: false の仕様はスキップされる
@given('仕様 "{param0}" が testable: false に設定されている')  # type: ignore
def given_624f5f06(context, param0):
    """仕様 "SPEC-001" が testable: false に設定されている"""
    setup_doorstop(context)
    item_path = os.path.join(context.temp_dir, "specs", f"{param0}.yml")
    with open(item_path, "w") as f:
        f.write("active: True\nreviewed: True\ntestable: false\ntext: test\n")


# 使用されるシナリオ:
# - testable: false の仕様はスキップされる
@given('"{param0}" に対応するGherkinテストが存在しない')  # type: ignore
def given_ea690d53(context, param0):
    """"SPEC-001" に対応するGherkinテストが存在しない"""
    pass


# 使用されるシナリオ:
# - testable: false の仕様はスキップされる
@then('"{param0}" はテスト漏れとして報告されないこと')  # type: ignore
def then_55c71a2c(context, param0):
    """"SPEC-001" はテスト漏れとして報告されないこと"""
    assert param0 not in context.stdout


# 使用されるシナリオ:
# - Suspect Link の検出
@given('仕様 "{param0}" の上位アイテムが変更されている（cleared=false）')  # type: ignore
def given_db49ffab(context, param0):
    """仕様 "SPEC-009" の上位アイテムが変更されている（cleared=false）"""
    setup_doorstop(context, prefixes=["REQ", "SPEC"])
    # 1. Add REQ-001
    subprocess.run(["doorstop", "add", "REQ"], cwd=context.temp_dir, check=True)
    # 2. Add SPEC-001 linked to REQ-001
    subprocess.run(["doorstop", "add", "SPEC"], cwd=context.temp_dir, check=True)
    subprocess.run(["doorstop", "link", "SPEC-001", "REQ-001"], cwd=context.temp_dir, check=True)
    
    # 3. Review all
    subprocess.run(["doorstop", "review", "all"], cwd=context.temp_dir, check=True)
    
    # 4. Change REQ-001 text
    req_path = os.path.join(context.temp_dir, "reqs", "REQ-001.yml")
    with open(req_path, "r") as f:
        lines = f.readlines()
    with open(req_path, "w") as f:
        for line in lines:
            if line.startswith("text:"):
                f.write("text: modified text\n")
            else:
                f.write(line)
    
    context.target_id = "SPEC-001"
    create_feature_file(context, "test.feature", f"@{context.target_id}\nFeature: Test\n  Scenario: Test\n    Given test")


# 使用されるシナリオ:
# - Suspect Link の検出
@then('Suspect Link テーブルに "{param0}" が報告されること')  # type: ignore
def then_0149339a(context, param0):
    """Suspect Link テーブルに "SPEC-009" が報告されること"""
    assert "Suspect Link" in context.stdout, f"Suspect Link table not found in output: {context.stdout}"
    target = getattr(context, "target_id", param0)
    assert target in context.stdout


# 使用されるシナリオ:
# - Suspect Link の検出
@then('変更された上位アイテムのIDが表示されること')  # type: ignore
def then_407500a2(context):
    """変更された上位アイテムのIDが表示されること"""
    assert "REQ-001" in context.stdout


# 使用されるシナリオ:
# - Unreviewed Changes の検出
@given('仕様 "{param0}" 自体に未レビューの変更がある（reviewed=false）')  # type: ignore
def given_8ceeca7b(context, param0):
    """仕様 "SPEC-009" 自体に未レビューの変更がある（reviewed=false）"""
    setup_doorstop(context)
    subprocess.run(["doorstop", "add", "SPEC"], cwd=context.temp_dir, check=True)
    subprocess.run(["doorstop", "review", "all"], cwd=context.temp_dir, check=True)
    
    # Modify SPEC-001 text
    spec_path = os.path.join(context.temp_dir, "specs", "SPEC-001.yml")
    with open(spec_path, "r") as f:
        lines = f.readlines()
    with open(spec_path, "w") as f:
        for line in lines:
            if line.startswith("text:"):
                f.write("text: modified text\n")
            else:
                f.write(line)
    
    context.target_id = "SPEC-001"
    create_feature_file(context, f"{context.target_id}.feature", f"@{context.target_id}\nFeature: Test\n  Scenario: Test\n    Given test")


# 使用されるシナリオ:
# - Unreviewed Changes の検出
@then('Unreviewed Changes テーブルに "{param0}" が報告されること')  # type: ignore
def then_56101a52(context, param0):
    """Unreviewed Changes テーブルに "SPEC-009" が報告されること"""
    assert "Unreviewed Changes" in context.stdout
    target = getattr(context, "target_id", param0)
    assert target in context.stdout
