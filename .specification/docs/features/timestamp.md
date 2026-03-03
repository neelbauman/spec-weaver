# Feature: タイムスタンプ管理

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
    """DoorstopアイテムのYAMLファイルがGitにコミットされている

    Scenarios:
      - Git履歴から updated_at を自動取得する
      - Git履歴から created_at を自動取得する
    """
    raise NotImplementedError('STEP: DoorstopアイテムのYAMLファイルがGitにコミットされている')
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
    raise NotImplementedError('STEP: タイムスタンプ属性を取得する')
```

#### Then updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

```python
@then('updated_at として最終コミット日が YYYY-MM-DD 形式で返されること')  # type: ignore
def then_c495b67c(context):
    """updated_at として最終コミット日が YYYY-MM-DD 形式で返されること

    Scenarios:
      - Git履歴から updated_at を自動取得する
    """
    raise NotImplementedError('STEP: updated_at として最終コミット日が YYYY-MM-DD 形式で返されること')
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
    """DoorstopアイテムのYAMLファイルがGitにコミットされている

    Scenarios:
      - Git履歴から updated_at を自動取得する
      - Git履歴から created_at を自動取得する
    """
    raise NotImplementedError('STEP: DoorstopアイテムのYAMLファイルがGitにコミットされている')
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
    raise NotImplementedError('STEP: タイムスタンプ属性を取得する')
```

#### Then created_at として初回コミット日が YYYY-MM-DD 形式で返されること

```python
@then('created_at として初回コミット日が YYYY-MM-DD 形式で返されること')  # type: ignore
def then_c016ae72(context):
    """created_at として初回コミット日が YYYY-MM-DD 形式で返されること

    Scenarios:
      - Git履歴から created_at を自動取得する
    """
    raise NotImplementedError('STEP: created_at として初回コミット日が YYYY-MM-DD 形式で返されること')
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
    """DoorstopアイテムのYAMLファイルがGit管理外である

    Scenarios:
      - Git情報がない場合はYAML属性にフォールバック
      - Git情報もYAML属性もない場合のフォールバック
    """
    raise NotImplementedError('STEP: DoorstopアイテムのYAMLファイルがGit管理外である')
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
@when('タイムスタンプ属性を取得する')  # type: ignore
def when_7e4b3813(context):
    """タイムスタンプ属性を取得する

    Scenarios:
      - Git履歴から updated_at を自動取得する
      - Git履歴から created_at を自動取得する
      - Git情報がない場合はYAML属性にフォールバック
      - Git情報もYAML属性もない場合のフォールバック
    """
    raise NotImplementedError('STEP: タイムスタンプ属性を取得する')
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
    """DoorstopアイテムのYAMLファイルがGit管理外である

    Scenarios:
      - Git情報がない場合はYAML属性にフォールバック
      - Git情報もYAML属性もない場合のフォールバック
    """
    raise NotImplementedError('STEP: DoorstopアイテムのYAMLファイルがGit管理外である')
```

#### And YAMLに created_at も updated_at も設定されていない

```python
@given('YAMLに created_at も updated_at も設定されていない')  # type: ignore
def given_20d06697(context):
    """YAMLに created_at も updated_at も設定されていない

    Scenarios:
      - Git情報もYAML属性もない場合のフォールバック
    """
    raise NotImplementedError('STEP: YAMLに created_at も updated_at も設定されていない')
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
    raise NotImplementedError('STEP: タイムスタンプ属性を取得する')
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
    """DoorstopアイテムがGitにコミットされている

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
      - 詳細ページにタイムスタンプが表示される
    """
    raise NotImplementedError('STEP: DoorstopアイテムがGitにコミットされている')
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
@then('一覧テーブルに「作成日」列が含まれること')  # type: ignore
def then_ed934883(context):
    """一覧テーブルに「作成日」列が含まれること

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
    """
    raise NotImplementedError('STEP: 一覧テーブルに「作成日」列が含まれること')
```

#### And 一覧テーブルに「更新日」列が含まれること

```python
@then('一覧テーブルに「更新日」列が含まれること')  # type: ignore
def then_2ae95f61(context):
    """一覧テーブルに「更新日」列が含まれること

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
    """
    raise NotImplementedError('STEP: 一覧テーブルに「更新日」列が含まれること')
```

#### And Git履歴から取得した日付が正しく表示されること

```python
@then('Git履歴から取得した日付が正しく表示されること')  # type: ignore
def then_232626f7(context):
    """Git履歴から取得した日付が正しく表示されること

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
    """
    raise NotImplementedError('STEP: Git履歴から取得した日付が正しく表示されること')
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
    """DoorstopアイテムがGitにコミットされている

    Scenarios:
      - 一覧テーブルにタイムスタンプ列が表示される
      - 詳細ページにタイムスタンプが表示される
    """
    raise NotImplementedError('STEP: DoorstopアイテムがGitにコミットされている')
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
@then('詳細ページに作成日と更新日が表示されること')  # type: ignore
def then_4954ab92(context):
    """詳細ページに作成日と更新日が表示されること

    Scenarios:
      - 詳細ページにタイムスタンプが表示される
    """
    raise NotImplementedError('STEP: 詳細ページに作成日と更新日が表示されること')
```

#### And 実装状況バッジの直後に配置されていること

```python
@then('実装状況バッジの直後に配置されていること')  # type: ignore
def then_1a39f98b(context):
    """実装状況バッジの直後に配置されていること

    Scenarios:
      - 詳細ページにタイムスタンプが表示される
    """
    raise NotImplementedError('STEP: 実装状況バッジの直後に配置されていること')
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
    """DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない

    Scenarios:
      - Git情報がない場合の一覧テーブル表示
    """
    raise NotImplementedError('STEP: DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない')
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
## Scenario: stale アイテムの検出（Git履歴ベース） {: #line-60 }

**タグ**: `@QA-002`

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
    raise NotImplementedError('STEP: Doorstopアイテムの最終コミット日が 91日前である')
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
@when('audit コマンドを --stale-days 90 で実行する')  # type: ignore
def when_81d68298(context):
    """audit コマンドを --stale-days 90 で実行する

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
      - 閾値内のアイテムは stale と判定されない
      - Git情報もupdated_atもないアイテムは stale 判定の対象外
      - deprecated アイテムは stale 判定の対象外
    """
    raise NotImplementedError('STEP: audit コマンドを --stale-days 90 で実行する')
```

#### Then そのアイテムが stale として報告されること

```python
@then('そのアイテムが stale として報告されること')  # type: ignore
def then_54f17b4b(context):
    """そのアイテムが stale として報告されること

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
    """
    raise NotImplementedError('STEP: そのアイテムが stale として報告されること')
```

#### And 経過日数が表示されること

```python
@then('経過日数が表示されること')  # type: ignore
def then_9500bbae(context):
    """経過日数が表示されること

    Scenarios:
      - stale アイテムの検出（Git履歴ベース）
    """
    raise NotImplementedError('STEP: 経過日数が表示されること')
```

</details>


---
## Scenario: 閾値内のアイテムは stale と判定されない {: #line-68 }

**タグ**: `@QA-002`

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
    raise NotImplementedError('STEP: Doorstopアイテムの最終コミット日が 30日前である')
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
    raise NotImplementedError('STEP: audit コマンドを --stale-days 90 で実行する')
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
    raise NotImplementedError('STEP: そのアイテムは stale として報告されないこと')
```

</details>


---
## Scenario: Git情報もupdated_atもないアイテムは stale 判定の対象外 {: #line-74 }

**タグ**: `@QA-002`

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
    raise NotImplementedError('STEP: DoorstopアイテムがGit管理外でupdated_atも設定されていない')
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
    raise NotImplementedError('STEP: audit コマンドを --stale-days 90 で実行する')
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
    raise NotImplementedError('STEP: そのアイテムは stale として報告されないこと')
```

</details>


---
## Scenario: deprecated アイテムは stale 判定の対象外 {: #line-80 }

**タグ**: `@QA-002`

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
@given('最終コミット日が 180日前である')  # type: ignore
def given_1588d2c1(context):
    """最終コミット日が 180日前である

    Scenarios:
      - deprecated アイテムは stale 判定の対象外
    """
    raise NotImplementedError('STEP: 最終コミット日が 180日前である')
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
    raise NotImplementedError('STEP: audit コマンドを --stale-days 90 で実行する')
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
    raise NotImplementedError('STEP: そのアイテムは stale として報告されないこと')
```

</details>


---
## Scenario: --stale-days 0 で鮮度チェックを無効化 {: #line-87 }

**タグ**: `@QA-002`

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
    raise NotImplementedError('STEP: Doorstopアイテムの最終コミット日が 365日前である')
```

#### When audit コマンドを --stale-days 0 で実行する

```python
@when('audit コマンドを --stale-days 0 で実行する')  # type: ignore
def when_5cbe8c38(context):
    """audit コマンドを --stale-days 0 で実行する

    Scenarios:
      - --stale-days 0 で鮮度チェックを無効化
    """
    raise NotImplementedError('STEP: audit コマンドを --stale-days 0 で実行する')
```

#### Then stale に関する報告は表示されないこと

```python
@then('stale に関する報告は表示されないこと')  # type: ignore
def then_e6a9cec1(context):
    """stale に関する報告は表示されないこと

    Scenarios:
      - --stale-days 0 で鮮度チェックを無効化
    """
    raise NotImplementedError('STEP: stale に関する報告は表示されないこと')
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: d9ec5f68b155b88ee2491dc6b24ef7b9f724d4aa34fe4e8643280f9a6a01aef0
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
    Given Doorstopアイテムの status が "deprecated" である
    And   最終コミット日が 180日前である
    When  audit コマンドを --stale-days 90 で実行する
    Then  そのアイテムは stale として報告されないこと

  @QA-002
  Scenario: --stale-days 0 で鮮度チェックを無効化
    Given Doorstopアイテムの最終コミット日が 365日前である
    When  audit コマンドを --stale-days 0 で実行する
    Then  stale に関する報告は表示されないこと

```
</details>