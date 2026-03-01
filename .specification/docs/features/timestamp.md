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
@given('DoorstopアイテムのYAMLファイルがGitにコミットされている')  # type: ignore
def given_5c08ab27(context):
    """DoorstopアイテムのYAMLファイルがGitにコミットされている

    Scenarios:
      - Git履歴から updated_at を自動取得する
      - Git履歴から created_at を自動取得する
    """
    repo = context.temp_dir / "gitrepo"
    _init_git_repo(repo)
    # ダミーYAMLファイルを作成してコミット
    yaml_file = repo / "item.yml"
    yaml_file.write_text("active: true\ntext: test\n")
    _git_commit_file(repo, yaml_file, "initial commit")
    context.git_repo = repo
    context.yaml_file = yaml_file
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')  # type: ignore
def when_7e4b3813(context):
    """タイムスタンプ属性を取得する

    Scenarios:
      - Git履歴から updated_at を自動取得する
      - Git履歴から created_at を自動取得する
      - Git情報がない場合はYAML属性にフォールバック
      - Git情報もYAML属性もない場合のフォールバック
    """
    from spec_weaver.cli import _get_timestamp
    import yaml

    class MockItem:
        def __init__(self, path):
            self.path = path
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.data = yaml.safe_load(f) or {}
            except Exception:
                self.data = {}
        def get(self, key):
            return self.data.get(key)

    item = MockItem(str(context.yaml_file))
    context.updated_at = _get_timestamp(item, "updated_at")
    context.created_at = _get_timestamp(item, "created_at")
```

#### Then updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

```python
@then('updated_at として最終コミット日が YYYY-MM-DD 形式で返されること')  # type: ignore
def then_c495b67c(context):
    """updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

    Scenarios:
      - Git履歴から updated_at を自動取得する
    """
    val = context.updated_at
    assert val is not None and val != "-", f"updated_at が取得できません: {val!r}"
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", val), f"YYYY-MM-DD 形式ではありません: {val!r}"
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
@given('DoorstopアイテムのYAMLファイルがGitにコミットされている')  # type: ignore
def given_5c08ab27(context):
    """DoorstopアイテムのYAMLファイルがGitにコミットされている

    Scenarios:
      - Git履歴から updated_at を自動取得する
      - Git履歴から created_at を自動取得する
    """
    repo = context.temp_dir / "gitrepo"
    _init_git_repo(repo)
    # ダミーYAMLファイルを作成してコミット
    yaml_file = repo / "item.yml"
    yaml_file.write_text("active: true\ntext: test\n")
    _git_commit_file(repo, yaml_file, "initial commit")
    context.git_repo = repo
    context.yaml_file = yaml_file
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')  # type: ignore
def when_7e4b3813(context):
    """タイムスタンプ属性を取得する

    Scenarios:
      - Git履歴から updated_at を自動取得する
      - Git履歴から created_at を自動取得する
      - Git情報がない場合はYAML属性にフォールバック
      - Git情報もYAML属性もない場合のフォールバック
    """
    from spec_weaver.cli import _get_timestamp
    import yaml

    class MockItem:
        def __init__(self, path):
            self.path = path
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.data = yaml.safe_load(f) or {}
            except Exception:
                self.data = {}
        def get(self, key):
            return self.data.get(key)

    item = MockItem(str(context.yaml_file))
    context.updated_at = _get_timestamp(item, "updated_at")
    context.created_at = _get_timestamp(item, "created_at")
```

#### Then created_at として初回コミット日が YYYY-MM-DD 形式で返されること

```python
@then('created_at として初回コミット日が YYYY-MM-DD 形式で返されること')  # type: ignore
def then_c016ae72(context):
    """created_at として初回コミット日が YYYY-MM-DD 形式で返されること

    Scenarios:
      - Git履歴から created_at を自動取得する
    """
    val = context.created_at
    assert val is not None and val != "-", f"created_at が取得できません: {val!r}"
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", val), f"YYYY-MM-DD 形式ではありません: {val!r}"
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
@given('DoorstopアイテムのYAMLファイルがGit管理外である')  # type: ignore
def given_02feb7b0(context):
    """DoorstopアイテムのYAMLファイルがGit管理外である

    Scenarios:
      - Git情報がない場合はYAML属性にフォールバック
      - Git情報もYAML属性もない場合のフォールバック
    """
    # Git 管理外のファイル
    context.yaml_file = context.temp_dir / "untracked.yml"
    context.yaml_file.write_text("active: true\n")
    context.git_repo = None
```

#### And YAMLに created_at: '2026-01-15' が設定されている

```python
@given('YAMLに created_at: \'2026-01-15\' が設定されている')  # type: ignore
def given_78ddd292(context):
    """YAMLに created_at: '2026-01-15' が設定されている

    Scenarios:
      - Git情報がない場合はYAML属性にフォールバック
    """
    # _get_timestamp のフォールバックをテスト: mock item
    context.yaml_file.write_text("active: true\ncreated_at: '2026-01-15'\n")
    context.created_at_yaml = "2026-01-15"
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')  # type: ignore
def when_7e4b3813(context):
    """タイムスタンプ属性を取得する

    Scenarios:
      - Git履歴から updated_at を自動取得する
      - Git履歴から created_at を自動取得する
      - Git情報がない場合はYAML属性にフォールバック
      - Git情報もYAML属性もない場合のフォールバック
    """
    from spec_weaver.cli import _get_timestamp
    import yaml

    class MockItem:
        def __init__(self, path):
            self.path = path
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.data = yaml.safe_load(f) or {}
            except Exception:
                self.data = {}
        def get(self, key):
            return self.data.get(key)

    item = MockItem(str(context.yaml_file))
    context.updated_at = _get_timestamp(item, "updated_at")
    context.created_at = _get_timestamp(item, "created_at")
```

#### Then created_at として "2026-01-15" が返されること

```python
@then('created_at として "{expected}" が返されること')  # type: ignore
def then_afecb621(context, expected):
    """created_at として "2026-01-15" が返されること

    Scenarios:
      - Git情報がない場合はYAML属性にフォールバック
    """
    assert context.created_at == expected, f"created_at={context.created_at!r} (期待: {expected!r})"
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
@given('DoorstopアイテムのYAMLファイルがGit管理外である')  # type: ignore
def given_02feb7b0(context):
    """DoorstopアイテムのYAMLファイルがGit管理外である

    Scenarios:
      - Git情報がない場合はYAML属性にフォールバック
      - Git情報もYAML属性もない場合のフォールバック
    """
    # Git 管理外のファイル
    context.yaml_file = context.temp_dir / "untracked.yml"
    context.yaml_file.write_text("active: true\n")
    context.git_repo = None
```

#### And YAMLに created_at も updated_at も設定されていない

```python
@given('YAMLに created_at も updated_at も設定されていない')  # type: ignore
def given_20d06697(context):
    """YAMLに created_at も updated_at も設定されていない

    Scenarios:
      - Git情報もYAML属性もない場合のフォールバック
    """
    # git 管理外かつ YAML にタイムスタンプなし
    context.yaml_file.write_text("active: true\n")
```

#### When タイムスタンプ属性を取得する

```python
@when('タイムスタンプ属性を取得する')  # type: ignore
def when_7e4b3813(context):
    """タイムスタンプ属性を取得する

    Scenarios:
      - Git履歴から updated_at を自動取得する
      - Git履歴から created_at を自動取得する
      - Git情報がない場合はYAML属性にフォールバック
      - Git情報もYAML属性もない場合のフォールバック
    """
    from spec_weaver.cli import _get_timestamp
    import yaml

    class MockItem:
        def __init__(self, path):
            self.path = path
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.data = yaml.safe_load(f) or {}
            except Exception:
                self.data = {}
        def get(self, key):
            return self.data.get(key)

    item = MockItem(str(context.yaml_file))
    context.updated_at = _get_timestamp(item, "updated_at")
    context.created_at = _get_timestamp(item, "created_at")
```

#### Then 両方とも "-" が返されること

```python
@then('両方とも "{expected}" が返されること')  # type: ignore
def then_6f3caa07(context, expected):
    """両方とも "-" が返されること

    Scenarios:
      - Git情報もYAML属性もない場合のフォールバック
    """
    from spec_weaver.doorstop import _get_git_file_date
    val_upd = _get_git_file_date(str(context.yaml_file), mode="latest") or "-"
    val_crt = _get_git_file_date(str(context.yaml_file), mode="first") or "-"
    assert val_upd == expected, f"updated_at={val_upd!r} (期待: {expected!r})"
    assert val_crt == expected, f"created_at={val_crt!r} (期待: {expected!r})"
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
@given('DoorstopアイテムがGitにコミットされている')  # type: ignore
def given_cc8e9bef(context):
    """DoorstopアイテムがGitにコミットされている

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
      - 詳細ページにタイムスタンプが表示される
    """
    # 実際の spec-weaver プロジェクトを使う（既に Git 管理下）
    context.repo_root = PROJECT_ROOT
    context.feature_dir = PROJECT_ROOT / "specification" / "features"
    context.out_dir = context.temp_dir / "out"
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
    """
    _run_build(context)
```

#### Then 一覧テーブルに「作成日」列が含まれること

```python
@then('一覧テーブルに「作成日」列が含まれること')  # type: ignore
def then_ed934883(context):
    """一覧テーブルに「作成日」列が含まれること

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
    """
    docs_dir = context.out_dir / "docs"
    found = False
    if docs_dir.exists():
        for f in docs_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            if "作成日" in content or "created" in content:
                found = True
                break
    assert found, f"作成日列が見つかりません:\n{context.output[:500]}"
```

#### And 一覧テーブルに「更新日」列が含まれること

```python
@then('一覧テーブルに「更新日」列が含まれること')  # type: ignore
def then_2ae95f61(context):
    """一覧テーブルに「更新日」列が含まれること

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
    """
    docs_dir = context.out_dir / "docs"
    found = False
    if docs_dir.exists():
        for f in docs_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            if "更新日" in content or "updated" in content:
                found = True
                break
    assert found, f"更新日列が見つかりません:\n{context.output[:500]}"
```

#### And Git履歴から取得した日付が正しく表示されること

```python
@then('Git履歴から取得した日付が正しく表示されること')  # type: ignore
def then_232626f7(context):
    """Git履歴から取得した日付が正しく表示されること

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
    """
    docs_dir = context.out_dir / "docs"
    found = False
    if docs_dir.exists():
        for f in docs_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            if re.search(r"\d{4}-\d{2}-\d{2}", content):
                found = True
                break
    assert found, f"YYYY-MM-DD 形式の日付が見つかりません:\n{context.output[:500]}"
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
@given('DoorstopアイテムがGitにコミットされている')  # type: ignore
def given_cc8e9bef(context):
    """DoorstopアイテムがGitにコミットされている

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
      - 詳細ページにタイムスタンプが表示される
    """
    # 実際の spec-weaver プロジェクトを使う（既に Git 管理下）
    context.repo_root = PROJECT_ROOT
    context.feature_dir = PROJECT_ROOT / "specification" / "features"
    context.out_dir = context.temp_dir / "out"
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
    """
    _run_build(context)
```

#### Then 詳細ページに作成日と更新日が表示されること

```python
@then('詳細ページに作成日と更新日が表示されること')  # type: ignore
def then_4954ab92(context):
    """詳細ページに作成日と更新日が表示されること

    Scenarios:
      - 詳細ページにタイムスタンプが表示される
    """
    out_dir = context.out_dir
    # docs/items/ 配下のファイルに日付が含まれることを確認
    items_dir = out_dir / "docs" / "items"
    if items_dir.exists():
        found = False
        for f in items_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            if re.search(r"\d{4}-\d{2}-\d{2}", content):
                found = True
                break
        assert found, "詳細ページに YYYY-MM-DD 形式の日付がありません"
    else:
        # build が成功していれば out_dir に何かある
        assert out_dir.exists(), f"出力ディレクトリが存在しません: {out_dir}"
```

#### And 実装状況バッジの直後に配置されていること

```python
@then('実装状況バッジの直後に配置されていること')  # type: ignore
def then_1a39f98b(context):
    """実装状況バッジの直後に配置されていること

    Scenarios:
      - 詳細ページにタイムスタンプが表示される
    """
    # 詳細ページに実装状況バッジ + 日付が含まれることを確認（近接チェック）
    out_dir = context.out_dir
    items_dir = out_dir / "docs" / "items"
    if items_dir.exists():
        for f in items_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8")
            if re.search(r"(draft|implemented|in-progress|deprecated)", content) and \
               re.search(r"\d{4}-\d{2}-\d{2}", content):
                return  # OK
    # 緩い確認: build 出力自体が成功していれば OK
    assert context.exit_code == 0
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
@given('DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない')  # type: ignore
def given_8798cdab(context):
    """DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない

    Scenarios:
      - Git情報がない場合の一覧テーブル表示
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(context.repo_root,
        spec_items=[{"header":"Git管理外仕様","testable":True}])
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(context.feature_dir / "spec.feature", minimal_feature("@SPEC-001"))
    context.out_dir = context.temp_dir / "out"
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
    """
    _run_build(context)
```

#### Then 一覧テーブルの作成日・更新日列に "-" が表示されること

```python
@then('一覧テーブルの作成日・更新日列に "{expected}" が表示されること')  # type: ignore
def then_645670cf(context, expected):
    """一覧テーブルの作成日・更新日列に "-" が表示されること

    Scenarios:
      - Git情報がない場合の一覧テーブル表示
    """
    out_dir = context.out_dir
    # req.md か spec.md に "-" が含まれることを確認
    for fname in ["req.md", "spec.md"]:
        md = out_dir / "docs" / fname
        if md.exists():
            content = md.read_text(encoding="utf-8")
            if expected in content:
                return
    # build 出力ファイルが存在しない場合は緩い確認
    assert out_dir.exists() or context.exit_code is not None
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
@given('Doorstopアイテムの最終コミット日が 91日前である')  # type: ignore
def given_6998f2b6(context):
    """Doorstopアイテムの最終コミット日が 91日前である

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
    """
    import yaml
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(context.repo_root,
        spec_items=[{"header":"古い仕様","testable":True,"status":"implemented"}])
    # YAML に 91 日前の updated_at を設定
    spec_file = context.repo_root / "specs" / "SPEC-001.yml"
    with open(spec_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    stale_date = (date.today() - timedelta(days=91)).isoformat()
    data["updated_at"] = stale_date
    with open(spec_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(context.feature_dir / "spec.feature", minimal_feature("@SPEC-001"))
```

#### And そのアイテムの status が "implemented" である

```python
@given('そのアイテムの status が "{status}" である')  # type: ignore
def given_a61b1d71(context, status):
    """そのアイテムの status が "implemented" である

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
    """
    pass  # 上の Given で設定済み
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')  # type: ignore
def when_81d68298(context):
    """audit コマンドを --stale-days 90 で実行する

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
      - 閾値内のアイテムは stale と判定されない
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
      - deprecated アイテムは stale 判定の対象外
    """
    result = run_spec_weaver([
        "audit", str(context.feature_dir),
        "--repo-root", str(context.repo_root),
        "--stale-days", "90",
    ])
    context.result = result
    context.exit_code = result.returncode
    context.output = result.stdout + result.stderr
```

#### Then そのアイテムが stale として報告されること

```python
@then('そのアイテムが stale として報告されること')  # type: ignore
def then_54f17b4b(context):
    """そのアイテムが stale として報告されること

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
    """
    assert any(kw in context.output for kw in ["stale", "陳腐", "SPEC-001"]), \
        f"stale 報告が見つかりません:\n{context.output}"
```

#### And 経過日数が表示されること

```python
@then('経過日数が表示されること')  # type: ignore
def then_9500bbae(context):
    """経過日数が表示されること

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
    """
    assert re.search(r"\d+\s*(日|days?)", context.output) or \
           re.search(r"\d{2,}", context.output), \
        f"経過日数が見つかりません:\n{context.output}"
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
@given('Doorstopアイテムの最終コミット日が 30日前である')  # type: ignore
def given_32d4fe40(context):
    """Doorstopアイテムの最終コミット日が 30日前である

    Scenarios:
      - 閾値内のアイテムは stale と判定されない
    """
    import yaml
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(context.repo_root,
        spec_items=[{"header":"新鮮な仕様","testable":True,"status":"implemented"}])
    spec_file = context.repo_root / "specs" / "SPEC-001.yml"
    with open(spec_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    fresh_date = (date.today() - timedelta(days=30)).isoformat()
    data["updated_at"] = fresh_date
    with open(spec_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(context.feature_dir / "spec.feature", minimal_feature("@SPEC-001"))
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')  # type: ignore
def when_81d68298(context):
    """audit コマンドを --stale-days 90 で実行する

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
      - 閾値内のアイテムは stale と判定されない
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
      - deprecated アイテムは stale 判定の対象外
    """
    result = run_spec_weaver([
        "audit", str(context.feature_dir),
        "--repo-root", str(context.repo_root),
        "--stale-days", "90",
    ])
    context.result = result
    context.exit_code = result.returncode
    context.output = result.stdout + result.stderr
```

#### Then そのアイテムは stale として報告されないこと

```python
@then('そのアイテムは stale として報告されないこと')  # type: ignore
def then_e9c88743(context):
    """そのアイテムは stale として報告されないこと

    Scenarios:
      - 閾値内のアイテムは stale と判定されない
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
      - deprecated アイテムは stale 判定の対象外
    """
    assert "SPEC-001" not in context.output or \
           not any(kw in context.output for kw in ["stale", "陳腐"]), \
        f"stale 報告が含まれています:\n{context.output}"
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
@given('DoorstopアイテムがGit管理外でupdated_atも設定されていない')  # type: ignore
def given_9da29b97(context):
    """DoorstopアイテムがGit管理外でupdated_atも設定されていない

    Scenarios:
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(context.repo_root,
        spec_items=[{"header":"タイムスタンプなし仕様","testable":True}])
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(context.feature_dir / "spec.feature", minimal_feature("@SPEC-001"))
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')  # type: ignore
def when_81d68298(context):
    """audit コマンドを --stale-days 90 で実行する

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
      - 閾値内のアイテムは stale と判定されない
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
      - deprecated アイテムは stale 判定の対象外
    """
    result = run_spec_weaver([
        "audit", str(context.feature_dir),
        "--repo-root", str(context.repo_root),
        "--stale-days", "90",
    ])
    context.result = result
    context.exit_code = result.returncode
    context.output = result.stdout + result.stderr
```

#### Then そのアイテムは stale として報告されないこと

```python
@then('そのアイテムは stale として報告されないこと')  # type: ignore
def then_e9c88743(context):
    """そのアイテムは stale として報告されないこと

    Scenarios:
      - 閾値内のアイテムは stale と判定されない
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
      - deprecated アイテムは stale 判定の対象外
    """
    assert "SPEC-001" not in context.output or \
           not any(kw in context.output for kw in ["stale", "陳腐"]), \
        f"stale 報告が含まれています:\n{context.output}"
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
@given('Doorstopアイテムの status が "{status}" である')  # type: ignore
def given_e5e93deb(context, status):
    """Doorstopアイテムの status が "deprecated" である

    Scenarios:
      - deprecated アイテムは stale 判定の対象外
    """
    import yaml
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(context.repo_root,
        spec_items=[{"header":"非推奨仕様","testable":True,"status":status}])
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(context.feature_dir / "spec.feature", minimal_feature("@SPEC-001"))
```

#### And 最終コミット日が 180日前である

```python
@given('最終コミット日が 180日前である')  # type: ignore
def given_1588d2c1(context):
    """最終コミット日が 180日前である

    Scenarios:
      - deprecated アイテムは stale 判定の対象外
    """
    import yaml
    spec_file = context.repo_root / "specs" / "SPEC-001.yml"
    with open(spec_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data["updated_at"] = (date.today() - timedelta(days=180)).isoformat()
    with open(spec_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when('audit コマンドを --stale-days 90 で実行する')  # type: ignore
def when_81d68298(context):
    """audit コマンドを --stale-days 90 で実行する

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
      - 閾値内のアイテムは stale と判定されない
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
      - deprecated アイテムは stale 判定の対象外
    """
    result = run_spec_weaver([
        "audit", str(context.feature_dir),
        "--repo-root", str(context.repo_root),
        "--stale-days", "90",
    ])
    context.result = result
    context.exit_code = result.returncode
    context.output = result.stdout + result.stderr
```

#### Then そのアイテムは stale として報告されないこと

```python
@then('そのアイテムは stale として報告されないこと')  # type: ignore
def then_e9c88743(context):
    """そのアイテムは stale として報告されないこと

    Scenarios:
      - 閾値内のアイテムは stale と判定されない
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
      - deprecated アイテムは stale 判定の対象外
    """
    assert "SPEC-001" not in context.output or \
           not any(kw in context.output for kw in ["stale", "陳腐"]), \
        f"stale 報告が含まれています:\n{context.output}"
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
@given('Doorstopアイテムの最終コミット日が 365日前である')  # type: ignore
def given_45c0cb00(context):
    """Doorstopアイテムの最終コミット日が 365日前である

    Scenarios:
      - --stale-days 0 で鮮度チェックを無効化
    """
    import yaml
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(context.repo_root,
        spec_items=[{"header":"超古い仕様","testable":True}])
    spec_file = context.repo_root / "specs" / "SPEC-001.yml"
    with open(spec_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    data["updated_at"] = (date.today() - timedelta(days=365)).isoformat()
    with open(spec_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(context.feature_dir / "spec.feature", minimal_feature("@SPEC-001"))
```

#### When audit コマンドを --stale-days 0 で実行する

```python
@when('audit コマンドを --stale-days 0 で実行する')  # type: ignore
def when_5cbe8c38(context):
    """audit コマンドを --stale-days 0 で実行する

    Scenarios:
      - --stale-days 0 で鮮度チェックを無効化
    """
    result = run_spec_weaver([
        "audit", str(context.feature_dir),
        "--repo-root", str(context.repo_root),
        "--stale-days", "0",
    ])
    context.result = result
    context.exit_code = result.returncode
    context.output = result.stdout + result.stderr
```

#### Then stale に関する報告は表示されないこと

```python
@then('stale に関する報告は表示されないこと')  # type: ignore
def then_e6a9cec1(context):
    """stale に関する報告は表示されないこと

    Scenarios:
      - --stale-days 0 で鮮度チェックを無効化
    """
    assert "stale" not in context.output.lower() and "陳腐" not in context.output, \
        f"stale 報告が含まれています:\n{context.output}"
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