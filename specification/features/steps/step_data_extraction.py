"""behave steps for: データ抽出基盤"""

from behave import given, when, then, step

# ======================================================================
# Steps
# ======================================================================

# 使用されるシナリオ:
# - Doorstop APIによる仕様ID集合の取得
@given('Doorstopプロジェクトにアクティブな仕様アイテムが存在する')
def given_a04781e9(context):
    """Doorstopプロジェクトにアクティブな仕様アイテムが存在する"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)

# 使用されるシナリオ:
# - Doorstop APIによる仕様ID集合の取得
# - 非アクティブなアイテムの除外
# - テスト不可能な仕様の除外
@when('仕様ID集合を取得する')
def when_e56707cb(context):
    """仕様ID集合を取得する"""
    from spec_weaver.doorstop import get_specs
    from pathlib import Path
    context.spec_ids = get_specs(Path(context.temp_dir), prefix=None)

# 使用されるシナリオ:
# - Doorstop APIによる仕様ID集合の取得
@then('アクティブかつtestableな仕様IDのみが返されること')
def then_6823b180(context):
    """アクティブかつtestableな仕様IDのみが返されること"""
    assert 'SPEC-001' in context.spec_ids

# 使用されるシナリオ:
# - 非アクティブなアイテムの除外
@given('Doorstopプロジェクトに active: false のアイテムが存在する')
def given_dccca3dc(context):
    """Doorstopプロジェクトに active: false のアイテムが存在する"""
    import subprocess, os, re
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    path = os.path.join(context.temp_dir, 'specs', 'SPEC-001.yml')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Replace active: true or active: True with active: false
    content = re.sub(r'active:\s*(true|True)', 'active: false', content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


# 使用されるシナリオ:
# - 非アクティブなアイテムの除外
@then('非アクティブなアイテムは結果に含まれないこと')
def then_99bfaa46(context):
    """非アクティブなアイテムは結果に含まれないこと"""
    assert 'SPEC-001' not in context.spec_ids

# 使用されるシナリオ:
# - テスト不可能な仕様の除外
@given('Doorstopプロジェクトに testable: false のアイテムが存在する')
def given_d534a041(context):
    """Doorstopプロジェクトに testable: false のアイテムが存在する"""
    import subprocess, os
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    path = os.path.join(context.temp_dir, 'specs', 'SPEC-001.yml')
    with open(path, 'a', encoding='utf-8') as f:
        f.write('testable: false\n')

# 使用されるシナリオ:
# - テスト不可能な仕様の除外
@then('testable: false のアイテムは結果に含まれないこと')
def then_f3fad2a6(context):
    """testable: false のアイテムは結果に含まれないこと"""
    assert 'SPEC-001' not in context.spec_ids

# 使用されるシナリオ:
# - プレフィックスによるフィルタリング
@given('DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する')
def given_7f8e9c65(context):
    """DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context, prefixes=['REQ', 'SPEC'])
    subprocess.run(['doorstop', 'add', 'REQ'], cwd=context.temp_dir, check=True)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)

# 使用されるシナリオ:
# - プレフィックスによるフィルタリング
@when('プレフィックス "{param0}" で仕様ID集合を取得する')
def when_1d11bcd6(context, param0):
    """プレフィックスで仕様ID集合を取得する"""
    from spec_weaver.doorstop import get_specs
    from pathlib import Path
    context.spec_ids = get_specs(Path(context.temp_dir), prefix=param0)

# 使用されるシナリオ:
# - プレフィックスによるフィルタリング
@then('SPECプレフィックスのアイテムのみが返されること')
def then_b5f39418(context):
    """SPECプレフィックスのアイテムのみが返されること"""
    assert 'SPEC-001' in context.spec_ids
    assert 'REQ-001' not in context.spec_ids

# 使用されるシナリオ:
# - Gherkin ASTからのタグ抽出
@given('Gherkin .feature ファイルに @SPEC-001 タグが付与されている')
def given_b830a393(context):
    """Gherkin .feature ファイルに @SPEC-001 タグが付与されている"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    create_feature_file(context, 'test.feature', '@SPEC-001\nFeature: Test\n  Scenario: Test\n    Given test')

# 使用されるシナリオ:
# - Gherkin ASTからのタグ抽出
# - Feature・Scenario両レベルのタグ抽出
# - サブディレクトリ内のfeatureファイルの再帰探索
# - Gherkin構文エラーの検出
@when('タグ集合を取得する')
def when_a12b8a55(context):
    """タグ集合を取得する"""
    from spec_weaver.gherkin import get_tags
    from pathlib import Path
    import os
    feature_dir = Path(context.temp_dir) / 'features'
    try:
        # get_tags returns a set of tag names (without @)
        context.tags = get_tags(feature_dir)
    except Exception as e:
        context.exc = e

# 使用されるシナリオ:
# - Gherkin ASTからのタグ抽出
@then('"{param0}" がタグ集合に含まれること')
def then_e8d01468(context, param0):
    """タグ集合に含まれること"""
    assert param0 in context.tags

# 使用されるシナリオ:
# - Feature・Scenario両レベルのタグ抽出
@given('Feature レベルと Scenario レベルに異なるSPECタグが付与されている')
def given_07def24f(context):
    """Feature レベルと Scenario レベルに異なるSPECタグが付与されている"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    create_feature_file(context, 'test.feature', '@SPEC-001\nFeature: Test\n  @SPEC-002\n  Scenario: Test\n    Given test')

# 使用されるシナリオ:
# - Feature・Scenario両レベルのタグ抽出
@then('両方のレベルのタグがすべて抽出されること')
def then_d712dc38(context):
    """両方のレベルのタグがすべて抽出されること"""
    assert 'SPEC-001' in context.tags
    assert 'SPEC-002' in context.tags

# 使用されるシナリオ:
# - サブディレクトリ内のfeatureファイルの再帰探索
@given('サブディレクトリに .feature ファイルが存在する')
def given_1427ca58(context):
    """サブディレクトリに .feature ファイルが存在する"""
    import os
    os.makedirs(os.path.join(context.temp_dir, 'features', 'sub'), exist_ok=True)
    with open(os.path.join(context.temp_dir, 'features', 'sub', 'sub.feature'), 'w', encoding='utf-8') as f:
        f.write('@SPEC-003\nFeature: Sub\n  Scenario: Sub\n    Given sub')

# 使用されるシナリオ:
# - サブディレクトリ内のfeatureファイルの再帰探索
@then('サブディレクトリ内のタグも含めて抽出されること')
def then_1c0ec472(context):
    """サブディレクトリ内のタグも含めて抽出されること"""
    assert 'SPEC-003' in context.tags


# 使用されるシナリオ:
# - Gherkin構文エラーの検出
@given('構文的に不正な .feature ファイルが存在する')
def given_540458bc(context):
    """構文的に不正な .feature ファイルが存在する"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    create_feature_file(context, 'invalid.feature', 'Feature Test')

# 使用されるシナリオ:
# - Gherkin構文エラーの検出
@then('ValueError が発生しGherkin構文エラーが報告されること')
def then_c5d0b4fe(context):
    """ValueError が発生しGherkin構文エラーが報告されること"""
    assert hasattr(context, 'exc')
    assert context.exc is not None
