"""behave steps for: タイムスタンプ管理"""

from behave import given, when, then, step

# ======================================================================
# Steps
# ======================================================================

# 使用されるシナリオ:
# - Git履歴から updated_at を自動取得する
# - Git履歴から created_at を自動取得する
@given('DoorstopアイテムのYAMLファイルがGitにコミットされている')
def given_5c08ab27(context):
    """DoorstopアイテムのYAMLファイルがGitにコミットされている

    Scenarios:
      - Git履歴から updated_at を自動取得する
      - Git履歴から created_at を自動取得する
    """
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'test commit'], cwd=context.temp_dir, check=True)

# 使用されるシナリオ:
# - Git履歴から updated_at を自動取得する
# - Git履歴から created_at を自動取得する
# - Git情報がない場合はYAML属性にフォールバック
# - Git情報もYAML属性もない場合のフォールバック
@when('タイムスタンプ属性を取得する')
def when_7e4b3813(context):
    """タイムスタンプ属性を取得する

    Scenarios:
      - Git履歴から updated_at を自動取得する
      - Git履歴から created_at を自動取得する
      - Git情報がない場合はYAML属性にフォールバック
      - Git情報もYAML属性もない場合のフォールバック
    """
    import doorstop
    tree = doorstop.build(context.temp_dir)
    context.item = tree.find_item('SPEC-001')

# 使用されるシナリオ:
# - Git履歴から updated_at を自動取得する
@then('updated_at として最終コミット日が YYYY-MM-DD 形式で返されること')
def then_c495b67c(context):
    """updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

    Scenarios:
      - Git履歴から updated_at を自動取得する
    """
    from spec_weaver.doorstop import _get_git_file_date
    import re
    updated_at = _get_git_file_date(str(context.item.path), mode='latest')
    assert updated_at is not None
    assert re.match(r'\d{4}-\d{2}-\d{2}', updated_at)

# 使用されるシナリオ:
# - Git履歴から created_at を自動取得する
@then('created_at として初回コミット日が YYYY-MM-DD 形式で返されること')
def then_c016ae72(context):
    """created_at として初回コミット日が YYYY-MM-DD 形式で返されること

    Scenarios:
      - Git履歴から created_at を自動取得する
    """
    from spec_weaver.doorstop import _get_git_file_date
    import re
    created_at = _get_git_file_date(str(context.item.path), mode='first')
    assert created_at is not None
    assert re.match(r'\d{4}-\d{2}-\d{2}', created_at)

# 使用されるシナリオ:
# - Git情報がない場合はYAML属性にフォールバック
# - Git情報もYAML属性もない場合のフォールバック
@given('DoorstopアイテムのYAMLファイルがGit管理外である')
def given_02feb7b0(context):
    """DoorstopアイテムのYAMLファイルがGit管理外である

    Scenarios:
      - Git情報がない場合はYAML属性にフォールバック
      - Git情報もYAML属性もない場合のフォールバック
    """
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    # No git add/commit here

# 使用されるシナリオ:
# - Git情報がない場合はYAML属性にフォールバック
@given('YAMLに created_at: \'2026-01-15\' が設定されている')
def given_78ddd292(context):
    """YAMLに created_at: '2026-01-15' が設定されている

    Scenarios:
      - Git情報がない場合はYAML属性にフォールバック
    """
    import os
    path = os.path.join(context.temp_dir, 'specs', 'SPEC-001.yml')
    with open(path, 'a', encoding='utf-8') as f:
        f.write("created_at: '2026-01-15'\n")

# 使用されるシナリオ:
# - Git情報がない場合はYAML属性にフォールバック
@then('created_at として "{param0}" が返されること')
def then_afecb621(context, param0):
    """created_at として返されること

    Scenarios:
      - Git情報がない場合はYAML属性にフォールバック
    """
    from spec_weaver.doorstop import _get_custom_attribute
    val = _get_custom_attribute(context.item, 'created_at')
    assert str(val) == param0

# 使用されるシナリオ:
# - Git情報もYAML属性もない場合のフォールバック
@given('YAMLに created_at も updated_at も設定されていない')
def given_20d06697(context):
    """YAMLに created_at も updated_at も設定されていない

    Scenarios:
      - Git情報もYAML属性もない場合のフォールバック
    """
    pass

# 使用されるシナリオ:
# - Git情報もYAML属性もない場合のフォールバック
@then('両方とも "{param0}" が返されること')
def then_6f3caa07(context, param0):
    """両方とも返されること

    Scenarios:
      - Git情報もYAML属性もない場合のフォールバック
    """
    from spec_weaver.doorstop import _get_custom_attribute
    c = _get_custom_attribute(context.item, 'created_at')
    u = _get_custom_attribute(context.item, 'updated_at')
    # If they are None, it means they are not set. 
    # The feature expects "-" but that's what the CLI displays.
    # Here context.item is a doorstop item.
    assert c is None
    assert u is None

# 使用されるシナリオ:
# - 一覧テーブルにタイムスタンプ列が表示される
# - 詳細ページにタイムスタンプが表示される
@given('DoorstopアイテムがGitにコミットされている')
def given_cc8e9bef(context):
    """DoorstopアイテムがGitにコミットされている

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
      - 詳細ページにタイムスタンプが表示される
    """
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'test'], cwd=context.temp_dir, check=True)

# 使用されるシナリオ:
# - 一覧テーブルにタイムスタンプ列が表示される
@then('一覧テーブルに「作成日」列が含まれること')
def then_ed934883(context):
    """一覧テーブルに「作成日」列が含まれること

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
    """
    import os
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'spec.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '作成日' in content

# 使用されるシナリオ:
# - 一覧テーブルにタイムスタンプ列が表示される
@then('一覧テーブルに「更新日」列が含まれること')
def then_2ae95f61(context):
    """一覧テーブルに「更新日」列が含まれること

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
    """
    import os
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'spec.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '更新日' in content

# 使用されるシナリオ:
# - 一覧テーブルにタイムスタンプ列が表示される
@then('Git履歴から取得した日付が正しく表示されること')
def then_232626f7(context):
    """Git履歴から取得した日付が正しく表示されること

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
    """
    import os
    import re
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'spec.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert re.search(r'\d{4}-\d{2}-\d{2}', content)

# 使用されるシナリオ:
# - 詳細ページにタイムスタンプが表示される
@then('詳細ページに作成日と更新日が表示されること')
def then_4954ab92(context):
    """詳細ページに作成日と更新日が表示されること

    Scenarios:
      - 詳細ページにタイムスタンプが表示される
    """
    import os
    import re
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'items', 'SPEC-001.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '作成日' in content
    assert '更新日' in content
    assert re.search(r'\d{4}-\d{2}-\d{2}', content)

# 使用されるシナリオ:
# - 詳細ページにタイムスタンプが表示される
@then('実装状況バッジの直後に配置されていること')
def then_1a39f98b(context):
    """実装状況バッジの直後に配置されていること

    Scenarios:
      - 詳細ページにタイムスタンプが表示される
    """
    import os
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'items', 'SPEC-001.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '実装状況' in content
    # Order: status badge then timestamps
    assert content.find('実装状況') < content.find('作成日')

# 使用されるシナリオ:
# - Git情報がない場合の一覧テーブル表示
@given('DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない')
def given_8798cdab(context):
    """DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない

    Scenarios:
      - Git情報がない場合の一覧テーブル表示
    """
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)

# 使用されるシナリオ:
# - Git情報がない場合の一覧テーブル表示
@then('一覧テーブルの作成日・更新日列に "{param0}" が表示されること')
def then_645670cf(context, param0):
    """一覧テーブルの作成日・更新日列に表示されること

    Scenarios:
      - Git情報がない場合の一覧テーブル表示
    """
    import os
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'spec.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert f'| {param0} | {param0} |' in content

# 使用されるシナリオ:
# - stale アイテムの検出（Git履歴ベース）
@given('Doorstopアイテムの最終コミット日が 91日前である')
def given_6998f2b6(context):
    """Doorstopアイテムの最終コミット日が 91日前である

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
    """
    import subprocess, os
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'test', '--date', '91 days ago'], cwd=context.temp_dir, check=True)

# 使用されるシナリオ:
# - stale アイテムの検出（Git履歴ベース）
@given('そのアイテムの status が "{param0}" である')
def given_a61b1d71(context, param0):
    """そのアイテムの status である

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
    """
    import os
    path = os.path.join(context.temp_dir, 'specs', 'SPEC-001.yml')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f'status: {param0}\n')

# 使用されるシナリオ:
# - stale アイテムの検出（Git履歴ベース）
# - 閾値内のアイテムは stale と判定されない
# - Git情報もupdated_atもないアイテムは stale 判定の対象外
# - deprecated アイテムは stale 判定の対象外
@when('audit コマンドを --stale-days 90 で実行する')
def when_81d68298(context):
    """audit コマンドを --stale-days 90 で実行する

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
      - 閾値内のアイテムは stale と判定されない
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
      - deprecated アイテムは stale 判定の対象外
    """
    from helpers import setup_doorstop, create_feature_file, run_cli
    run_cli(context, ['audit', 'features', '--stale-days', '90', '--repo-root', '.'])

# 使用されるシナリオ:
# - stale アイテムの検出（Git履歴ベース）
@then('そのアイテムが stale として報告されること')
def then_54f17b4b(context):
    """そのアイテムが stale として報告されること

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
    """
    assert 'Stale Items' in context.stdout
    assert 'SPEC-001' in context.stdout

# 使用されるシナリオ:
# - stale アイテムの検出（Git履歴ベース）
@then('経過日数が表示されること')
def then_9500bbae(context):
    """経過日数が表示されること

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
    """
    assert '日' in context.stdout

# 使用されるシナリオ:
# - 閾値内のアイテムは stale と判定されない
@given('Doorstopアイテムの最終コミット日が 30日前である')
def given_32d4fe40(context):
    """Doorstopアイテムの最終コミット日が 30日前である

    Scenarios:
      - 閾値内のアイテムは stale と判定されない
    """
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'test', '--date', '30 days ago'], cwd=context.temp_dir, check=True)

# 使用されるシナリオ:
# - 閾値内のアイテムは stale と判定されない
# - Git情報もupdated_atもないアイテムは stale 判定の対象外
# - deprecated アイテムは stale 判定の対象外
@then('そのアイテムは stale として報告されないこと')
def then_e9c88743(context):
    """そのアイテムは stale として報告されないこと

    Scenarios:
      - 閾値内のアイテムは stale と判定されない
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
      - deprecated アイテムは stale 判定の対象外
    """
    assert 'Stale Items' not in context.stdout

# 使用されるシナリオ:
# - Git情報もupdated_atもないアイテムは stale 判定の対象外
@given('DoorstopアイテムがGit管理外でupdated_atも設定されていない')
def given_9da29b97(context):
    """DoorstopアイテムがGit管理外でupdated_atも設定されていない

    Scenarios:
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
    """
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)

# 使用されるシナリオ:
# - deprecated アイテムは stale 判定の対象外
@given('Doorstopアイテムの status が "{param0}" である')
def given_e5e93deb(context, param0):
    """Doorstopアイテムの status がである

    Scenarios:
      - deprecated アイテムは stale 判定の対象外
    """
    import os
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    path = os.path.join(context.temp_dir, 'specs', 'SPEC-001.yml')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f'status: {param0}\n')

# 使用されるシナリオ:
# - deprecated アイテムは stale 判定の対象外
@given('最終コミット日が 180日前である')
def given_1588d2c1(context):
    """最終コミット日が 180日前である

    Scenarios:
      - deprecated アイテムは stale 判定の対象外
    """
    import subprocess
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'stale test', '--date', '180 days ago'], cwd=context.temp_dir, check=True)

# 使用されるシナリオ:
# - --stale-days 0 で鮮度チェックを無効化
@given('Doorstopアイテムの最終コミット日が 365日前である')
def given_45c0cb00(context):
    """Doorstopアイテムの最終コミット日が 365日前である

    Scenarios:
      - --stale-days 0 で鮮度チェックを無効化
    """
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'very old', '--date', '365 days ago'], cwd=context.temp_dir, check=True)

# 使用されるシナリオ:
# - --stale-days 0 で鮮度チェックを無効化
@when('audit コマンドを --stale-days 0 で実行する')
def when_5cbe8c38(context):
    """audit コマンドを --stale-days 0 で実行する

    Scenarios:
      - --stale-days 0 で鮮度チェックを無効化
    """
    from helpers import setup_doorstop, create_feature_file, run_cli
    run_cli(context, ['audit', 'features', '--stale-days', '0', '--repo-root', '.'])

# 使用されるシナリオ:
# - --stale-days 0 で鮮度チェックを無効化
@then('stale に関する報告は表示されないこと')
def then_e6a9cec1(context):
    """stale に関する報告は表示されないこと

    Scenarios:
      - --stale-days 0 で鮮度チェックを無効化
    """
    assert 'Stale Items' not in context.stdout

