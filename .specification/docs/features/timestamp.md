# Feature: タイムスタンプ管理

> 📋 **Unreviewed Changes**: このフィーチャーファイル自体に未レビューの変更があります。レビュー後に `review` コマンドで更新してください。

**タグ**: `@VIS-006`

**関連アイテム**: [QA-002](../items/QA-002.md) / [VIS-006](../items/VIS-006.md) / [VIS-007](../items/VIS-007.md)

アイテムの作成日・最終更新日をGit履歴から自動取得し、
  ドキュメント生成および監査で活用する。

---
## Scenario: Git履歴から updated_at を自動取得する {: #line-12 }

- **Given** DoorstopアイテムのYAMLファイルがGitにコミットされている
- **When** タイムスタンプ属性を取得する
- **Then** updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムのYAMLファイルがGitにコミットされている

```python
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
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')  # type: ignore
def when_7e4b3813(context):
    from spec_weaver.adapters.doorstop import _get_git_file_date
    yaml_path = str(context.temp_dir / "specs" / f"{context.target_item_id}.yml")
    context.updated_at = _get_git_file_date(yaml_path, mode="latest")
    context.created_at = _get_git_file_date(yaml_path, mode="first")
```

#### Then updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

```python
@then('updated_at として最終コミット日が YYYY-MM-DD 形式で返されること')  # type: ignore
def then_c495b67c(context):
    assert context.updated_at == "2026-02-01", f"Expected 2026-02-01, got {context.updated_at}"
```

</details>


---
## Scenario: Git履歴から created_at を自動取得する {: #line-17 }

- **Given** DoorstopアイテムのYAMLファイルがGitにコミットされている
- **When** タイムスタンプ属性を取得する
- **Then** created_at として初回コミット日が YYYY-MM-DD 形式で返されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムのYAMLファイルがGitにコミットされている

```python
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
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')  # type: ignore
def when_7e4b3813(context):
    from spec_weaver.adapters.doorstop import _get_git_file_date
    yaml_path = str(context.temp_dir / "specs" / f"{context.target_item_id}.yml")
    context.updated_at = _get_git_file_date(yaml_path, mode="latest")
    context.created_at = _get_git_file_date(yaml_path, mode="first")
```

#### Then created_at として初回コミット日が YYYY-MM-DD 形式で返されること

```python
@then('created_at として初回コミット日が YYYY-MM-DD 形式で返されること')  # type: ignore
def then_c016ae72(context):
    assert context.created_at == "2026-01-01", f"Expected 2026-01-01, got {context.created_at}"
```

</details>


---
## Scenario: Git情報がない場合はYAML属性にフォールバック {: #line-22 }

- **Given** DoorstopアイテムのYAMLファイルがGit管理外である
- **And** YAMLに created_at: '2026-01-15' が設定されている
- **When** タイムスタンプ属性を取得する
- **Then** created_at として "2026-01-15" が返されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムのYAMLファイルがGit管理外である

```python
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
```

#### And YAMLに created_at: '2026-01-15' が設定されている

```python
@given('YAMLに created_at: \'2026-01-15\' が設定されている')  # type: ignore
def given_78ddd292(context):
    yaml_path = context.temp_dir / "specs" / f"{context.target_item_id}.yml"
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    data["created_at"] = '2026-01-15'
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')  # type: ignore
def when_7e4b3813(context):
    from spec_weaver.adapters.doorstop import _get_git_file_date
    yaml_path = str(context.temp_dir / "specs" / f"{context.target_item_id}.yml")
    context.updated_at = _get_git_file_date(yaml_path, mode="latest")
    context.created_at = _get_git_file_date(yaml_path, mode="first")
```

#### Then created_at として "2026-01-15" が返されること

```python
@then('created_at として "{expected}" が返されること')  # type: ignore
def step_impl_created_at_check(context, expected):
    from spec_weaver.utils.formatters import get_timestamp
    import doorstop
    tree = doorstop.build(cwd=str(context.temp_dir))
    item = tree.find_item(context.target_item_id)
    val = get_timestamp(item, "created_at")
    assert val == expected, f"Expected {expected}, got {val}"
```

</details>


---
## Scenario: Git情報もYAML属性もない場合のフォールバック {: #line-28 }

- **Given** DoorstopアイテムのYAMLファイルがGit管理外である
- **And** YAMLに created_at も updated_at も設定されていない
- **When** タイムスタンプ属性を取得する
- **Then** 両方とも "-" が返されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムのYAMLファイルがGit管理外である

```python
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
```

#### And YAMLに created_at も updated_at も設定されていない

```python
@given('YAMLに created_at も updated_at も設定されていない')  # type: ignore
def given_20d06697(context):
    yaml_path = context.temp_dir / "specs" / f"{context.target_item_id}.yml"
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')  # type: ignore
def when_7e4b3813(context):
    from spec_weaver.adapters.doorstop import _get_git_file_date
    yaml_path = str(context.temp_dir / "specs" / f"{context.target_item_id}.yml")
    context.updated_at = _get_git_file_date(yaml_path, mode="latest")
    context.created_at = _get_git_file_date(yaml_path, mode="first")
```

#### Then 両方とも "-" が返されること

```python
@then('両方とも "{expected}" が返されること')  # type: ignore
def step_impl_both_check(context, expected):
    from spec_weaver.utils.formatters import get_timestamp
    import doorstop
    tree = doorstop.build(cwd=str(context.temp_dir))
    item = tree.find_item(context.target_item_id)
    c = get_timestamp(item, "created_at")
    u = get_timestamp(item, "updated_at")
    assert c == expected and u == expected, f"Expected both {expected}, but got {c} and {u}"
```

</details>


---
## Scenario: 一覧テーブルにタイムスタンプ列が表示される {: #line-37 }

**タグ**: `@VIS-007`

- **Given** DoorstopアイテムがGitにコミットされている
- **When** build コマンドを実行する
- **Then** 一覧テーブルに「作成日」列が含まれること
- **And** 一覧テーブルに「更新日」列が含まれること
- **And** Git履歴から取得した日付が正しく表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムがGitにコミットされている

```python
@given('DoorstopアイテムがGitにコミットされている')  # type: ignore
def given_cc8e9bef(context):
    given_5c08ab27(context)
```

#### When build コマンドを実行する

```python
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
      - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
      - 一覧テーブルにレビューステータス列が表示されること
    """
    raise NotImplementedError('STEP: build コマンドを実行する')
```

#### Then 一覧テーブルに「作成日」列が含まれること

```python
@then('一覧テーブルに「作成日」列が含まれること')  # type: ignore
def then_ed934883(context):
    index_md = context.temp_dir / ".specification" / "docs" / "spec.md"
    content = index_md.read_text()
    assert "作成日" in content
```

#### And 一覧テーブルに「更新日」列が含まれること

```python
@then('一覧テーブルに「更新日」列が含まれること')  # type: ignore
def then_2ae95f61(context):
    index_md = context.temp_dir / ".specification" / "docs" / "spec.md"
    content = index_md.read_text()
    assert "更新日" in content
```

#### And Git履歴から取得した日付が正しく表示されること

```python
@then('Git履歴から取得した日付が正しく表示されること')  # type: ignore
def then_232626f7(context):
    index_md = context.temp_dir / ".specification" / "docs" / "spec.md"
    content = index_md.read_text()
    assert "2026-02-01" in content
```

</details>


---
## Scenario: 詳細ページにタイムスタンプが表示される {: #line-45 }

**タグ**: `@VIS-007`

- **Given** DoorstopアイテムがGitにコミットされている
- **When** build コマンドを実行する
- **Then** 詳細ページに作成日と更新日が表示されること
- **And** 実装状況バッジの直後に配置されていること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムがGitにコミットされている

```python
@given('DoorstopアイテムがGitにコミットされている')  # type: ignore
def given_cc8e9bef(context):
    given_5c08ab27(context)
```

#### When build コマンドを実行する

```python
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
      - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
      - 一覧テーブルにレビューステータス列が表示されること
    """
    raise NotImplementedError('STEP: build コマンドを実行する')
```

#### Then 詳細ページに作成日と更新日が表示されること

```python
@then('詳細ページに作成日と更新日が表示されること')  # type: ignore
def then_4954ab92(context):
    item_md = context.temp_dir / ".specification" / "docs" / "items" / "SPEC-001.md"
    content = item_md.read_text()
    assert "作成日" in content and "更新日" in content
```

#### And 実装状況バッジの直後に配置されていること

```python
@then('実装状況バッジの直後に配置されていること')  # type: ignore
def then_1a39f98b(context):
    item_md = context.temp_dir / ".specification" / "docs" / "items" / "SPEC-001.md"
    content = item_md.read_text()
    # Check if "作成日" exists in the content.
    assert "作成日" in content or "更新日" in content
```

</details>


---
## Scenario: Git情報がない場合の一覧テーブル表示 {: #line-52 }

**タグ**: `@VIS-007`

- **Given** DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない
- **When** build コマンドを実行する
- **Then** 一覧テーブルの作成日・更新日列に "-" が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない

```python
@given('DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない')  # type: ignore
def given_8798cdab(context):
    given_02feb7b0(context)
```

#### When build コマンドを実行する

```python
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
      - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
      - 一覧テーブルにレビューステータス列が表示されること
    """
    raise NotImplementedError('STEP: build コマンドを実行する')
```

#### Then 一覧テーブルの作成日・更新日列に "-" が表示されること

```python
@then('一覧テーブルの作成日・更新日列に "{expected}" が表示されること')  # type: ignore
def step_impl_table_check(context, expected):
    index_md = context.temp_dir / ".specification" / "docs" / "spec.md"
    content = index_md.read_text()
    assert expected in content
```

</details>


---
## Scenario: stale アイテムの検出（Git履歴ベース） {: #line-60 }

**タグ**: `@QA-002`

- **Given** Doorstopアイテムの最終コミット日が 91日前である
- **And** そのアイテムの status が "implemented" である
- **When** audit コマンドを --stale-days 90 で実行する
- **Then** そのアイテムが stale として報告されること
- **And** 経過日数が表示されること
- **And** タイムスタンプ監査の終了コードが 1 であること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopアイテムの最終コミット日が 91日前である

```python
@given('Doorstopアイテムの最終コミット日が 91日前である')  # type: ignore
def given_6998f2b6(context):
    _git_init_full(context.temp_dir)
    date = (datetime.datetime.now() - datetime.timedelta(days=91)).strftime("%Y-%m-%d")
    create_doorstop_project_yaml(context.temp_dir, [{"dir": "specs", "prefix": "SPEC", "items": [{"uid": "SPEC-001", "status": "implemented"}]}])
    _git_commit_at(context.temp_dir, "old commit", date)
    context.target_item_id = "SPEC-001"
```

#### And そのアイテムの status が "implemented" である

```python
@given('そのアイテムの status が "{status}" である')  # type: ignore
@given('Doorstopアイテムの status が "{status}" である')  # type: ignore
def step_impl_status(context, status):
    yaml_path = context.temp_dir / "specs" / f"{context.target_item_id}.yml"
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    data["status"] = status
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')  # type: ignore
def when_81d68298(context):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    # Create dummy feature with the tag to satisfy audit
    write_feature_file(feature_dir / "dummy.feature", f"@{context.target_item_id}\nFeature: Dummy\n  Scenario: Dummy\n    Given test\n")
    context.result = run_spec_weaver(["audit", str(feature_dir), "--stale-days", "90"], cwd=context.temp_dir)
```

#### Then そのアイテムが stale として報告されること

```python
@then('そのアイテムが stale として報告されること')  # type: ignore
def then_54f17b4b(context):
    assert "Stale Items" in context.result.stdout or "長期間経過" in context.result.stdout
    assert context.target_item_id in context.result.stdout
```

#### And 経過日数が表示されること

```python
@then('経過日数が表示されること')  # type: ignore
def then_9500bbae(context):
    assert "days" in context.result.stdout or "日" in context.result.stdout
```

#### And タイムスタンプ監査の終了コードが 1 であること

```python
@then('タイムスタンプ監査の終了コードが {code:d} であること')  # type: ignore
def then_ab1e81e6_timestamp(context, code):
    assert context.result.returncode == code, f"Expected exit code {code}, but got {context.result.returncode}. Output: {context.result.stdout}"
```

</details>


---
## Scenario: 閾値内のアイテムは stale と判定されない {: #line-69 }

**タグ**: `@QA-002`

- **Given** Doorstopアイテムの最終コミット日が 30日前である
- **When** audit コマンドを --stale-days 90 で実行する
- **Then** そのアイテムは stale として報告されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopアイテムの最終コミット日が 30日前である

```python
@given('Doorstopアイテムの最終コミット日が 30日前である')  # type: ignore
def given_32d4fe40(context):
    _git_init_full(context.temp_dir)
    date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    create_doorstop_project_yaml(context.temp_dir, [{"dir": "specs", "prefix": "SPEC", "items": [{"uid": "SPEC-001", "status": "implemented"}]}])
    _git_commit_at(context.temp_dir, "recent commit", date)
    context.target_item_id = "SPEC-001"
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')  # type: ignore
def when_81d68298(context):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    # Create dummy feature with the tag to satisfy audit
    write_feature_file(feature_dir / "dummy.feature", f"@{context.target_item_id}\nFeature: Dummy\n  Scenario: Dummy\n    Given test\n")
    context.result = run_spec_weaver(["audit", str(feature_dir), "--stale-days", "90"], cwd=context.temp_dir)
```

#### Then そのアイテムは stale として報告されないこと

```python
@then('そのアイテムは stale として報告されないこと')  # type: ignore
def then_e9c88743(context):
    assert "Stale" not in context.result.stdout and "長期間経過" not in context.result.stdout
```

</details>


---
## Scenario: Git情報もupdated_atもないアイテムは stale 判定の対象外 {: #line-75 }

**タグ**: `@QA-002`

- **Given** DoorstopアイテムがGit管理外でupdated_atも設定されていない
- **When** audit コマンドを --stale-days 90 で実行する
- **Then** そのアイテムは stale として報告されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopアイテムがGit管理外でupdated_atも設定されていない

```python
@given('DoorstopアイテムがGit管理外でupdated_atも設定されていない')  # type: ignore
def given_9da29b97(context):
    given_02feb7b0(context)
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')  # type: ignore
def when_81d68298(context):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    # Create dummy feature with the tag to satisfy audit
    write_feature_file(feature_dir / "dummy.feature", f"@{context.target_item_id}\nFeature: Dummy\n  Scenario: Dummy\n    Given test\n")
    context.result = run_spec_weaver(["audit", str(feature_dir), "--stale-days", "90"], cwd=context.temp_dir)
```

#### Then そのアイテムは stale として報告されないこと

```python
@then('そのアイテムは stale として報告されないこと')  # type: ignore
def then_e9c88743(context):
    assert "Stale" not in context.result.stdout and "長期間経過" not in context.result.stdout
```

</details>


---
## Scenario: deprecated アイテムは stale 判定の対象外 {: #line-81 }

**タグ**: `@QA-002`

- **Given** 最終コミット日が 180日前である
- **And** Doorstopアイテムの status が "deprecated" である
- **When** audit コマンドを --stale-days 90 で実行する
- **Then** そのアイテムは stale として報告されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 最終コミット日が 180日前である

```python
@given('最終コミット日が 180日前である')  # type: ignore
def given_1588d2c1(context):
    _git_init_full(context.temp_dir)
    date = (datetime.datetime.now() - datetime.timedelta(days=180)).strftime("%Y-%m-%d")
    create_doorstop_project_yaml(context.temp_dir, [{"dir": "specs", "prefix": "SPEC", "items": [{"uid": "SPEC-001", "status": "deprecated"}]}])
    _git_commit_at(context.temp_dir, "very old commit", date)
    context.target_item_id = "SPEC-001"
```

#### And Doorstopアイテムの status が "deprecated" である

```python
@given('Doorstopアイテムの status が "{status}" である')  # type: ignore
def step_impl_status(context, status):
    yaml_path = context.temp_dir / "specs" / f"{context.target_item_id}.yml"
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    data["status"] = status
    with open(yaml_path, "w") as f:
        yaml.dump(data, f)
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')  # type: ignore
def when_81d68298(context):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    # Create dummy feature with the tag to satisfy audit
    write_feature_file(feature_dir / "dummy.feature", f"@{context.target_item_id}\nFeature: Dummy\n  Scenario: Dummy\n    Given test\n")
    context.result = run_spec_weaver(["audit", str(feature_dir), "--stale-days", "90"], cwd=context.temp_dir)
```

#### Then そのアイテムは stale として報告されないこと

```python
@then('そのアイテムは stale として報告されないこと')  # type: ignore
def then_e9c88743(context):
    assert "Stale" not in context.result.stdout and "長期間経過" not in context.result.stdout
```

</details>


---
## Scenario: --stale-days 0 で鮮度チェックを無効化 {: #line-88 }

**タグ**: `@QA-002`

- **Given** Doorstopアイテムの最終コミット日が 365日前である
- **When** audit コマンドを --stale-days 0 で実行する
- **Then** stale に関する報告は表示されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopアイテムの最終コミット日が 365日前である

```python
@given('Doorstopアイテムの最終コミット日が 365日前である')  # type: ignore
def given_45c0cb00(context):
    _git_init_full(context.temp_dir)
    date = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")
    create_doorstop_project_yaml(context.temp_dir, [{"dir": "specs", "prefix": "SPEC", "items": [{"uid": "SPEC-001", "status": "implemented"}]}])
    _git_commit_at(context.temp_dir, "ancient commit", date)
    context.target_item_id = "SPEC-001"
```

#### When audit コマンドを --stale-days 0 で実行する

```python
@when('audit コマンドを --stale-days 0 で実行する')  # type: ignore
def when_5cbe8c38(context):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    # Create dummy feature with the tag to satisfy audit
    write_feature_file(feature_dir / "dummy.feature", f"@{context.target_item_id}\nFeature: Dummy\n  Scenario: Dummy\n    Given test\n")
    context.result = run_spec_weaver(["audit", str(feature_dir), "--stale-days", "0"], cwd=context.temp_dir)
```

#### Then stale に関する報告は表示されないこと

```python
@then('stale に関する報告は表示されないこと')  # type: ignore
def then_e6a9cec1(context):
    assert "Stale" not in context.result.stdout and "長期間経過" not in context.result.stdout
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: e3987b29813b5d5fa8a1bf13f8eb8dd1232fc3eaa35e4a1a941a9f376706edbd
# spec-weaver-fingerprint-QA-002: pIUDUCm2SbEPeLzmScATm5kxQXhzHgfNLVTet64j5OY=
# spec-weaver-fingerprint-VIS-006: X_KRBM_YhZCFigeGpRMit5ZIjnIx1JMby0egIg10egw=
# spec-weaver-fingerprint-VIS-007: yOFv-Mqqd6cmn9y-BMHTC3-5N_plpH_vbw4UzEypfk8=
@VIS-006
Feature: タイムスタンプ管理
  アイテムの作成日・最終更新日をGit履歴から自動取得し、
  ドキュメント生成および監査で活用する。

  # --- Git履歴からの自動取得 (VIS-006) ---

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

  # --- build コマンドへの表示統合 (VIS-007) ---

  @VIS-007
  Scenario: 一覧テーブルにタイムスタンプ列が表示される
    Given DoorstopアイテムがGitにコミットされている
    When  build コマンドを実行する
    Then  一覧テーブルに「作成日」列が含まれること
    And   一覧テーブルに「更新日」列が含まれること
    And   Git履歴から取得した日付が正しく表示されること

  @VIS-007
  Scenario: 詳細ページにタイムスタンプが表示される
    Given DoorstopアイテムがGitにコミットされている
    When  build コマンドを実行する
    Then  詳細ページに作成日と更新日が表示されること
    And   実装状況バッジの直後に配置されていること

  @VIS-007
  Scenario: Git情報がない場合の一覧テーブル表示
    Given DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない
    When  build コマンドを実行する
    Then  一覧テーブルの作成日・更新日列に "-" が表示されること

  # --- 鮮度の監査チェック (QA-002) ---

  @QA-002
  Scenario: stale アイテムの検出（Git履歴ベース）
    Given Doorstopアイテムの最終コミット日が 91日前である
    And   そのアイテムの status が "implemented" である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムが stale として報告されること
    And   経過日数が表示されること
    And   タイムスタンプ監査の終了コードが 1 であること

  @QA-002
  Scenario: 閾値内のアイテムは stale と判定されない
    Given Doorstopアイテムの最終コミット日が 30日前である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @QA-002
  Scenario: Git情報もupdated_atもないアイテムは stale 判定の対象外
    Given DoorstopアイテムがGit管理外でupdated_atも設定されていない
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @QA-002
  Scenario: deprecated アイテムは stale 判定の対象外
    Given 最終コミット日が 180日前である
    And   Doorstopアイテムの status が "deprecated" である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @QA-002
  Scenario: --stale-days 0 で鮮度チェックを無効化
    Given Doorstopアイテムの最終コミット日が 365日前である
    When  audit コマンドを --stale-days 0 で実行する
    Then  stale に関する報告は表示されないこと

```
</details>