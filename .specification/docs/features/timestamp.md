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
@given(u'DoorstopアイテムのYAMLファイルがGitにコミットされている')
def step_impl(context):
    pass
```

#### When タイムスタンプ属性を取得する

```python
@when(u'タイムスタンプ属性を取得する')
def step_impl(context):
    pass
```

#### Then updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

```python
@then(u'updated_at として最終コミット日が YYYY-MM-DD 形式で返されること')
def step_impl(context):
    pass
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
@given(u'DoorstopアイテムのYAMLファイルがGitにコミットされている')
def step_impl(context):
    pass
```

#### When タイムスタンプ属性を取得する

```python
@when(u'タイムスタンプ属性を取得する')
def step_impl(context):
    pass
```

#### Then created_at として初回コミット日が YYYY-MM-DD 形式で返されること

```python
@then(u'created_at として初回コミット日が YYYY-MM-DD 形式で返されること')
def step_impl(context):
    pass
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
@given(u'DoorstopアイテムのYAMLファイルがGit管理外である')
def step_impl(context):
    pass
```

#### And YAMLに created_at: '2026-01-15' が設定されている

```python
@given('YAMLに created_at: \'2026-01-15\' が設定されている')  # type: ignore
def given_78ddd292(context):
    """YAMLに created_at: '2026-01-15' が設定されている

    Scenarios:
      - Git情報がない場合はYAML属性にフォールバック
    """
    pass
```

#### When タイムスタンプ属性を取得する

```python
@when(u'タイムスタンプ属性を取得する')
def step_impl(context):
    pass
```

#### Then created_at として "2026-01-15" が返されること

```python
@then('created_at として "{param0}" が返されること')  # type: ignore
def then_afecb621(context, param0):
    """created_at として "2026-01-15" が返されること

    Scenarios:
      - Git情報がない場合はYAML属性にフォールバック
    """
    pass
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
@given(u'DoorstopアイテムのYAMLファイルがGit管理外である')
def step_impl(context):
    pass
```

#### And YAMLに created_at も updated_at も設定されていない

```python
@given(u'YAMLに created_at も updated_at も設定されていない')
def step_impl(context):
    pass
```

#### When タイムスタンプ属性を取得する

```python
@when(u'タイムスタンプ属性を取得する')
def step_impl(context):
    pass
```

#### Then 両方とも "-" が返されること

```python
@then('両方とも "{param0}" が返されること')  # type: ignore
def then_6f3caa07(context, param0):
    """両方とも "-" が返されること

    Scenarios:
      - Git情報もYAML属性もない場合のフォールバック
    """
    pass
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
@given(u'DoorstopアイテムがGitにコミットされている')
def step_impl(context):
    pass
```

#### When build コマンドを実行する

```python
@when('build コマンドを実行する')  # type: ignore
def when_40f323b6(context):
    """build コマンドを実行する

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
      - 詳細ページにタイムスタンプが表示される
      - Git情報がない場合の一覧テーブル表示
    """
    pass
```

#### Then 一覧テーブルに「作成日」列が含まれること

```python
@then(u'一覧テーブルに「作成日」列が含まれること')
def step_impl(context):
    pass
```

#### And 一覧テーブルに「更新日」列が含まれること

```python
@then(u'一覧テーブルに「更新日」列が含まれること')
def step_impl(context):
    pass
```

#### And Git履歴から取得した日付が正しく表示されること

```python
@then(u'Git履歴から取得した日付が正しく表示されること')
def step_impl(context):
    pass
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
@given(u'DoorstopアイテムがGitにコミットされている')
def step_impl(context):
    pass
```

#### When build コマンドを実行する

```python
@when('build コマンドを実行する')  # type: ignore
def when_40f323b6(context):
    """build コマンドを実行する

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
      - 詳細ページにタイムスタンプが表示される
      - Git情報がない場合の一覧テーブル表示
    """
    pass
```

#### Then 詳細ページに作成日と更新日が表示されること

```python
@then(u'詳細ページに作成日と更新日が表示されること')
def step_impl(context):
    pass
```

#### And 実装状況バッジの直後に配置されていること

```python
@then(u'実装状況バッジの直後に配置されていること')
def step_impl(context):
    pass
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
@given(u'DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない')
def step_impl(context):
    pass
```

#### When build コマンドを実行する

```python
@when('build コマンドを実行する')  # type: ignore
def when_40f323b6(context):
    """build コマンドを実行する

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
      - 詳細ページにタイムスタンプが表示される
      - Git情報がない場合の一覧テーブル表示
    """
    pass
```

#### Then 一覧テーブルの作成日・更新日列に "-" が表示されること

```python
@then('一覧テーブルの作成日・更新日列に "{param0}" が表示されること')  # type: ignore
def then_645670cf(context, param0):
    """一覧テーブルの作成日・更新日列に "-" が表示されること

    Scenarios:
      - Git情報がない場合の一覧テーブル表示
    """
    assert getattr(context, 'output', None) is not None
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
@given(u'Doorstopアイテムの最終コミット日が 91日前である')
def step_impl(context):
    pass
```

#### And そのアイテムの status が "implemented" である

```python
@given('そのアイテムの status が "{param0}" である')  # type: ignore
def given_a61b1d71(context, param0):
    """そのアイテムの status が "implemented" である

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
    """
    pass
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when(u'audit コマンドを --stale-days 90 で実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then そのアイテムが stale として報告されること

```python
@then(u'そのアイテムが stale として報告されること')
def step_impl(context):
    pass
```

#### And 経過日数が表示されること

```python
@then(u'経過日数が表示されること')
def step_impl(context):
    pass
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
@given(u'Doorstopアイテムの最終コミット日が 30日前である')
def step_impl(context):
    pass
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when(u'audit コマンドを --stale-days 90 で実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then そのアイテムは stale として報告されないこと

```python
@then(u'そのアイテムは stale として報告されないこと')
def step_impl(context):
    pass
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
@given(u'DoorstopアイテムがGit管理外でupdated_atも設定されていない')
def step_impl(context):
    pass
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when(u'audit コマンドを --stale-days 90 で実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then そのアイテムは stale として報告されないこと

```python
@then(u'そのアイテムは stale として報告されないこと')
def step_impl(context):
    pass
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
@given('Doorstopアイテムの status が "{param0}" である')  # type: ignore
def given_e5e93deb(context, param0):
    """Doorstopアイテムの status が "deprecated" である

    Scenarios:
      - deprecated アイテムは stale 判定の対象外
    """
    pass
```

#### And 最終コミット日が 180日前である

```python
@given(u'最終コミット日が 180日前である')
def step_impl(context):
    pass
```

#### When audit コマンドを --stale-days 90 で実行する

```python
@when(u'audit コマンドを --stale-days 90 で実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then そのアイテムは stale として報告されないこと

```python
@then(u'そのアイテムは stale として報告されないこと')
def step_impl(context):
    pass
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
@given(u'Doorstopアイテムの最終コミット日が 365日前である')
def step_impl(context):
    pass
```

#### When audit コマンドを --stale-days 0 で実行する

```python
@when(u'audit コマンドを --stale-days 0 で実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then stale に関する報告は表示されないこと

```python
@then(u'stale に関する報告は表示されないこと')
def step_impl(context):
    pass
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: d9ec5f68b155b88ee2491dc6b24ef7b9f724d4aa34fe4e8643280f9a6a01aef0
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