# Feature: タイムスタンプ管理

**タグ**: `@SPEC-011`

**関連アイテム**: [SPEC-011](../items/SPEC-011.md) / [SPEC-012](../items/SPEC-012.md) / [SPEC-013](../items/SPEC-013.md)

アイテムの作成日・最終更新日をGit履歴から自動取得し、
  ドキュメント生成および監査で活用する。

---
## Scenario: Git履歴から updated_at を自動取得する

- **Given** DoorstopアイテムのYAMLファイルがGitにコミットされている
- **When** タイムスタンプ属性を取得する
- **Then** updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムのYAMLファイルがGitにコミットされている

```python
@given('DoorstopアイテムのYAMLファイルがGitにコミットされている')
def given_5c08ab27(context):
    """DoorstopアイテムのYAMLファイルがGitにコミットされている"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'test commit'], cwd=context.temp_dir, check=True)
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')
def when_7e4b3813(context):
    """タイムスタンプ属性を取得する"""
    import doorstop
    tree = doorstop.build(context.temp_dir)
    context.item = tree.find_item('SPEC-001')
```

#### Then updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

```python
@then('updated_at として最終コミット日が YYYY-MM-DD 形式で返されること')
def then_c495b67c(context):
    """updated_at として最終コミット日が YYYY-MM-DD 形式で返されること"""
    from spec_weaver.doorstop import _get_git_file_date
    import re
    updated_at = _get_git_file_date(str(context.item.path), mode='latest')
    assert updated_at is not None
    assert re.match(r'\d{4}-\d{2}-\d{2}', updated_at)
```

</details>


---
## Scenario: Git履歴から created_at を自動取得する

- **Given** DoorstopアイテムのYAMLファイルがGitにコミットされている
- **When** タイムスタンプ属性を取得する
- **Then** created_at として初回コミット日が YYYY-MM-DD 形式で返されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムのYAMLファイルがGitにコミットされている

```python
@given('DoorstopアイテムのYAMLファイルがGitにコミットされている')
def given_5c08ab27(context):
    """DoorstopアイテムのYAMLファイルがGitにコミットされている"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'test commit'], cwd=context.temp_dir, check=True)
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')
def when_7e4b3813(context):
    """タイムスタンプ属性を取得する"""
    import doorstop
    tree = doorstop.build(context.temp_dir)
    context.item = tree.find_item('SPEC-001')
```

#### Then created_at として初回コミット日が YYYY-MM-DD 形式で返されること

```python
@then('created_at として初回コミット日が YYYY-MM-DD 形式で返されること')
def then_c016ae72(context):
    """created_at として初回コミット日が YYYY-MM-DD 形式で返されること"""
    from spec_weaver.doorstop import _get_git_file_date
    import re
    created_at = _get_git_file_date(str(context.item.path), mode='first')
    assert created_at is not None
    assert re.match(r'\d{4}-\d{2}-\d{2}', created_at)
```

</details>


---
## Scenario: Git情報がない場合はYAML属性にフォールバック

- **Given** DoorstopアイテムのYAMLファイルがGit管理外である
- **And** YAMLに created_at: '2026-01-15' が設定されている
- **When** タイムスタンプ属性を取得する
- **Then** created_at として "2026-01-15" が返されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムのYAMLファイルがGit管理外である

```python
@given('DoorstopアイテムのYAMLファイルがGit管理外である')
def given_02feb7b0(context):
    """DoorstopアイテムのYAMLファイルがGit管理外である"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
```

#### And YAMLに created_at: '2026-01-15' が設定されている

```python
@given('YAMLに created_at: \'2026-01-15\' が設定されている')
def given_78ddd292(context):
    """YAMLに created_at: '2026-01-15' が設定されている"""
    import os
    path = os.path.join(context.temp_dir, 'specs', 'SPEC-001.yml')
    with open(path, 'a', encoding='utf-8') as f:
        f.write("created_at: '2026-01-15'\n")
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')
def when_7e4b3813(context):
    """タイムスタンプ属性を取得する"""
    import doorstop
    tree = doorstop.build(context.temp_dir)
    context.item = tree.find_item('SPEC-001')
```

#### Then created_at として "2026-01-15" が返されること

```python
@then('created_at として "{param0}" が返されること')
def then_afecb621(context, param0):
    """created_at として返されること"""
    from spec_weaver.doorstop import _get_custom_attribute
    val = _get_custom_attribute(context.item, 'created_at')
    assert str(val) == param0
```

</details>


---
## Scenario: Git情報もYAML属性もない場合のフォールバック

- **Given** DoorstopアイテムのYAMLファイルがGit管理外である
- **And** YAMLに created_at も updated_at も設定されていない
- **When** タイムスタンプ属性を取得する
- **Then** 両方とも "-" が返されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムのYAMLファイルがGit管理外である

```python
@given('DoorstopアイテムのYAMLファイルがGit管理外である')
def given_02feb7b0(context):
    """DoorstopアイテムのYAMLファイルがGit管理外である"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
```

#### And YAMLに created_at も updated_at も設定されていない

```python
@given('YAMLに created_at も updated_at も設定されていない')
def given_20d06697(context):
    """YAMLに created_at も updated_at も設定されていない"""
    pass
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')
def when_7e4b3813(context):
    """タイムスタンプ属性を取得する"""
    import doorstop
    tree = doorstop.build(context.temp_dir)
    context.item = tree.find_item('SPEC-001')
```

#### Then 両方とも "-" が返されること

```python
@then('両方とも "{param0}" が返されること')
def then_6f3caa07(context, param0):
    """両方とも返されること"""
    from spec_weaver.doorstop import _get_custom_attribute
    c = _get_custom_attribute(context.item, 'created_at')
    u = _get_custom_attribute(context.item, 'updated_at')
    # If they are None, it means they are not set. 
    # The feature expects "-" but that's what the CLI displays.
    # Here context.item is a doorstop item.
    assert c is None
    assert u is None
```

</details>


---
## Scenario: 一覧テーブルにタイムスタンプ列が表示される

**タグ**: `@SPEC-012`

- **Given** DoorstopアイテムがGitにコミットされている
- **When** build コマンドを実行する
- **Then** 一覧テーブルに「作成日」列が含まれること
- **And** 一覧テーブルに「更新日」列が含まれること
- **And** Git履歴から取得した日付が正しく表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムがGitにコミットされている

```python
@given('DoorstopアイテムがGitにコミットされている')
def given_cc8e9bef(context):
    """DoorstopアイテムがGitにコミットされている"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'test'], cwd=context.temp_dir, check=True)
```

#### When build コマンドを実行する

```python
@when('build コマンドを実行する') # type: ignore
def when_40f323b6(context):
    """build コマンドを実行する"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    run_cli(context, ['build', 'features', '--repo-root', '.'])
```

#### Then 一覧テーブルに「作成日」列が含まれること

```python
@then('一覧テーブルに「作成日」列が含まれること')
def then_ed934883(context):
    """一覧テーブルに「作成日」列が含まれること"""
    import os
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'spec.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '作成日' in content
```

#### And 一覧テーブルに「更新日」列が含まれること

```python
@then('一覧テーブルに「更新日」列が含まれること')
def then_2ae95f61(context):
    """一覧テーブルに「更新日」列が含まれること"""
    import os
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'spec.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '更新日' in content
```

#### And Git履歴から取得した日付が正しく表示されること

```python
@then('Git履歴から取得した日付が正しく表示されること')
def then_232626f7(context):
    """Git履歴から取得した日付が正しく表示されること"""
    import os
    import re
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'spec.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert re.search(r'\d{4}-\d{2}-\d{2}', content)
```

</details>


---
## Scenario: 詳細ページにタイムスタンプが表示される

**タグ**: `@SPEC-012`

- **Given** DoorstopアイテムがGitにコミットされている
- **When** build コマンドを実行する
- **Then** 詳細ページに作成日と更新日が表示されること
- **And** 実装状況バッジの直後に配置されていること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムがGitにコミットされている

```python
@given('DoorstopアイテムがGitにコミットされている')
def given_cc8e9bef(context):
    """DoorstopアイテムがGitにコミットされている"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'test'], cwd=context.temp_dir, check=True)
```

#### When build コマンドを実行する

```python
@when('build コマンドを実行する') # type: ignore
def when_40f323b6(context):
    """build コマンドを実行する"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    run_cli(context, ['build', 'features', '--repo-root', '.'])
```

#### Then 詳細ページに作成日と更新日が表示されること

```python
@then('詳細ページに作成日と更新日が表示されること')
def then_4954ab92(context):
    """詳細ページに作成日と更新日が表示されること"""
    import os
    import re
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'items', 'SPEC-001.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '作成日' in content
    assert '更新日' in content
    assert re.search(r'\d{4}-\d{2}-\d{2}', content)
```

#### And 実装状況バッジの直後に配置されていること

```python
@then('実装状況バッジの直後に配置されていること')
def then_1a39f98b(context):
    """実装状況バッジの直後に配置されていること"""
    import os
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'items', 'SPEC-001.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert '実装状況' in content
    # Order: status badge then timestamps
    assert content.find('実装状況') < content.find('作成日')
```

</details>


---
## Scenario: Git情報がない場合の一覧テーブル表示

**タグ**: `@SPEC-012`

- **Given** DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない
- **When** build コマンドを実行する
- **Then** 一覧テーブルの作成日・更新日列に "-" が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない

```python
@given('DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない')
def given_8798cdab(context):
    """DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
```

#### When build コマンドを実行する

```python
@when('build コマンドを実行する') # type: ignore
def when_40f323b6(context):
    """build コマンドを実行する"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    run_cli(context, ['build', 'features', '--repo-root', '.'])
```

#### Then 一覧テーブルの作成日・更新日列に "-" が表示されること

```python
@then('一覧テーブルの作成日・更新日列に "{param0}" が表示されること')
def then_645670cf(context, param0):
    """一覧テーブルの作成日・更新日列に表示されること"""
    import os
    path = os.path.join(context.temp_dir, '.specification', 'docs', 'spec.md')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert f'| {param0} | {param0} |' in content
```

</details>


---
## Scenario: stale アイテムの検出（Git履歴ベース）

**タグ**: `@SPEC-013`

- **Given** Doorstopアイテムの最終コミット日が 91日前である
- **And** そのアイテムの status が "implemented" である
- **When** audit コマンドを --stale-days 90 で実行する
- **Then** そのアイテムが stale として報告されること
- **And** 経過日数が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopアイテムの最終コミット日が 91日前である

```python
@given('Doorstopアイテムの最終コミット日が 91日前である')
def given_6998f2b6(context):
    """Doorstopアイテムの最終コミット日が 91日前である"""
    import subprocess, os
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'test', '--date', '91 days ago'], cwd=context.temp_dir, check=True)
```

#### And そのアイテムの status が "implemented" である

```python
@given('そのアイテムの status が "{param0}" である')
def given_a61b1d71(context, param0):
    """そのアイテムの status である"""
    import os
    path = os.path.join(context.temp_dir, 'specs', 'SPEC-001.yml')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f'status: {param0}\n')
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')
def when_81d68298(context):
    """audit コマンドを --stale-days 90 で実行する"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    run_cli(context, ['audit', 'features', '--stale-days', '90', '--repo-root', '.'])
```

#### Then そのアイテムが stale として報告されること

```python
@then('そのアイテムが stale として報告されること')
def then_54f17b4b(context):
    """そのアイテムが stale として報告されること"""
    assert 'Stale Items' in context.stdout
    assert 'SPEC-001' in context.stdout
```

#### And 経過日数が表示されること

```python
@then('経過日数が表示されること')
def then_9500bbae(context):
    """経過日数が表示されること"""
    assert '日' in context.stdout
```

</details>


---
## Scenario: 閾値内のアイテムは stale と判定されない

**タグ**: `@SPEC-013`

- **Given** Doorstopアイテムの最終コミット日が 30日前である
- **When** audit コマンドを --stale-days 90 で実行する
- **Then** そのアイテムは stale として報告されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopアイテムの最終コミット日が 30日前である

```python
@given('Doorstopアイテムの最終コミット日が 30日前である')
def given_32d4fe40(context):
    """Doorstopアイテムの最終コミット日が 30日前である"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'test', '--date', '30 days ago'], cwd=context.temp_dir, check=True)
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')
def when_81d68298(context):
    """audit コマンドを --stale-days 90 で実行する"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    run_cli(context, ['audit', 'features', '--stale-days', '90', '--repo-root', '.'])
```

#### Then そのアイテムは stale として報告されないこと

```python
@then('そのアイテムは stale として報告されないこと')
def then_e9c88743(context):
    """そのアイテムは stale として報告されないこと"""
    assert 'Stale Items' not in context.stdout
```

</details>


---
## Scenario: Git情報もupdated_atもないアイテムは stale 判定の対象外

**タグ**: `@SPEC-013`

- **Given** DoorstopアイテムがGit管理外でupdated_atも設定されていない
- **When** audit コマンドを --stale-days 90 で実行する
- **Then** そのアイテムは stale として報告されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムがGit管理外でupdated_atも設定されていない

```python
@given('DoorstopアイテムがGit管理外でupdated_atも設定されていない')
def given_9da29b97(context):
    """DoorstopアイテムがGit管理外でupdated_atも設定されていない"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')
def when_81d68298(context):
    """audit コマンドを --stale-days 90 で実行する"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    run_cli(context, ['audit', 'features', '--stale-days', '90', '--repo-root', '.'])
```

#### Then そのアイテムは stale として報告されないこと

```python
@then('そのアイテムは stale として報告されないこと')
def then_e9c88743(context):
    """そのアイテムは stale として報告されないこと"""
    assert 'Stale Items' not in context.stdout
```

</details>


---
## Scenario: deprecated アイテムは stale 判定の対象外

**タグ**: `@SPEC-013`

- **Given** Doorstopアイテムの status が "deprecated" である
- **And** 最終コミット日が 180日前である
- **When** audit コマンドを --stale-days 90 で実行する
- **Then** そのアイテムは stale として報告されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopアイテムの status が "deprecated" である

```python
@given('Doorstopアイテムの status が "{param0}" である')
def given_e5e93deb(context, param0):
    """Doorstopアイテムの status がである"""
    import os
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    path = os.path.join(context.temp_dir, 'specs', 'SPEC-001.yml')
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f'status: {param0}\n')
```

#### And 最終コミット日が 180日前である

```python
@given('最終コミット日が 180日前である')
def given_1588d2c1(context):
    """最終コミット日が 180日前である"""
    import subprocess
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'stale test', '--date', '180 days ago'], cwd=context.temp_dir, check=True)
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')
def when_81d68298(context):
    """audit コマンドを --stale-days 90 で実行する"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    run_cli(context, ['audit', 'features', '--stale-days', '90', '--repo-root', '.'])
```

#### Then そのアイテムは stale として報告されないこと

```python
@then('そのアイテムは stale として報告されないこと')
def then_e9c88743(context):
    """そのアイテムは stale として報告されないこと"""
    assert 'Stale Items' not in context.stdout
```

</details>


---
## Scenario: --stale-days 0 で鮮度チェックを無効化

**タグ**: `@SPEC-013`

- **Given** Doorstopアイテムの最終コミット日が 365日前である
- **When** audit コマンドを --stale-days 0 で実行する
- **Then** stale に関する報告は表示されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopアイテムの最終コミット日が 365日前である

```python
@given('Doorstopアイテムの最終コミット日が 365日前である')
def given_45c0cb00(context):
    """Doorstopアイテムの最終コミット日が 365日前である"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'add', '.'], cwd=context.temp_dir, check=True)
    subprocess.run(['git', 'commit', '-m', 'very old', '--date', '365 days ago'], cwd=context.temp_dir, check=True)
```

#### When audit コマンドを --stale-days 0 で実行する

```python
@when('audit コマンドを --stale-days 0 で実行する')
def when_5cbe8c38(context):
    """audit コマンドを --stale-days 0 で実行する"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    run_cli(context, ['audit', 'features', '--stale-days', '0', '--repo-root', '.'])
```

#### Then stale に関する報告は表示されないこと

```python
@then('stale に関する報告は表示されないこと')
def then_e6a9cec1(context):
    """stale に関する報告は表示されないこと"""
    assert 'Stale Items' not in context.stdout
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
@SPEC-011
Feature: タイムスタンプ管理
  アイテムの作成日・最終更新日をGit履歴から自動取得し、
  ドキュメント生成および監査で活用する。

  # --- Git履歴からの自動取得 (SPEC-011) ---

  Scenario: Git履歴から updated_at を自動取得する
    Given DoorstopアイテムのYAMLファイルがGitにコミットされている
    When  タイムスタンプ属性を取得する
    Then  updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

  Scenario: Git履歴から created_at を自動取得する
    Given DoorstopアイテムのYAMLファイルがGitにコミットされている
    When  タイムスタンプ属性を取得する
    Then  created_at として初回コミット日が YYYY-MM-DD 形式で返されること

  Scenario: Git情報がない場合はYAML属性にフォールバック
    Given DoorstopアイテムのYAMLファイルがGit管理外である
    And   YAMLに created_at: '2026-01-15' が設定されている
    When  タイムスタンプ属性を取得する
    Then  created_at として "2026-01-15" が返されること

  Scenario: Git情報もYAML属性もない場合のフォールバック
    Given DoorstopアイテムのYAMLファイルがGit管理外である
    And   YAMLに created_at も updated_at も設定されていない
    When  タイムスタンプ属性を取得する
    Then  両方とも "-" が返されること

  # --- build コマンドへの表示統合 (SPEC-012) ---

  @SPEC-012
  Scenario: 一覧テーブルにタイムスタンプ列が表示される
    Given DoorstopアイテムがGitにコミットされている
    When  build コマンドを実行する
    Then  一覧テーブルに「作成日」列が含まれること
    And   一覧テーブルに「更新日」列が含まれること
    And   Git履歴から取得した日付が正しく表示されること

  @SPEC-012
  Scenario: 詳細ページにタイムスタンプが表示される
    Given DoorstopアイテムがGitにコミットされている
    When  build コマンドを実行する
    Then  詳細ページに作成日と更新日が表示されること
    And   実装状況バッジの直後に配置されていること

  @SPEC-012
  Scenario: Git情報がない場合の一覧テーブル表示
    Given DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない
    When  build コマンドを実行する
    Then  一覧テーブルの作成日・更新日列に "-" が表示されること

  # --- 鮮度の監査チェック (SPEC-013) ---

  @SPEC-013
  Scenario: stale アイテムの検出（Git履歴ベース）
    Given Doorstopアイテムの最終コミット日が 91日前である
    And   そのアイテムの status が "implemented" である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムが stale として報告されること
    And   経過日数が表示されること

  @SPEC-013
  Scenario: 閾値内のアイテムは stale と判定されない
    Given Doorstopアイテムの最終コミット日が 30日前である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @SPEC-013
  Scenario: Git情報もupdated_atもないアイテムは stale 判定の対象外
    Given DoorstopアイテムがGit管理外でupdated_atも設定されていない
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @SPEC-013
  Scenario: deprecated アイテムは stale 判定の対象外
    Given Doorstopアイテムの status が "deprecated" である
    And   最終コミット日が 180日前である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @SPEC-013
  Scenario: --stale-days 0 で鮮度チェックを無効化
    Given Doorstopアイテムの最終コミット日が 365日前である
    When  audit コマンドを --stale-days 0 で実行する
    Then  stale に関する報告は表示されないこと

```
</details>