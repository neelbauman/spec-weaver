# Feature: build コマンド

**タグ**: `@SPEC-004`

**関連アイテム**: [SPEC-004](../items/SPEC-004.md) / [SPEC-005](../items/SPEC-005.md) / [SPEC-009](../items/SPEC-009.md) / [SPEC-014](../items/SPEC-014.md)

Doorstopの仕様データとGherkinテストを統合した
  MkDocsドキュメントサイトを自動生成する。

---
## Scenario: MkDocs設定ファイルの生成

- **Given** DoorstopプロジェクトとGherkin featureファイルが存在する
- **When** build コマンドを実行する
- **Then** 出力ディレクトリに mkdocs.yml が生成されること
- **And** Material テーマが設定されていること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopプロジェクトとGherkin featureファイルが存在する

```python
@given(u'DoorstopプロジェクトとGherkin featureファイルが存在する')
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

#### Then 出力ディレクトリに mkdocs.yml が生成されること

```python
@then(u'出力ディレクトリに mkdocs.yml が生成されること')
def step_impl(context):
    pass
```

#### And Material テーマが設定されていること

```python
@then(u'Material テーマが設定されていること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: 要件一覧ページの生成

- **Given** DoorstopプロジェクトにREQアイテムが存在する
- **When** build コマンドを実行する
- **Then** docs/req.md が生成されること
- **And** 各REQアイテムがテーブル行として含まれること
- **And** 関連仕様への相互リンクが含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopプロジェクトにREQアイテムが存在する

```python
@given(u'DoorstopプロジェクトにREQアイテムが存在する')
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

#### Then docs/req.md が生成されること

```python
@then(u'docs/req.md が生成されること')
def step_impl(context):
    pass
```

#### And 各REQアイテムがテーブル行として含まれること

```python
@then(u'各REQアイテムがテーブル行として含まれること')
def step_impl(context):
    pass
```

#### And 関連仕様への相互リンクが含まれること

```python
@then(u'関連仕様への相互リンクが含まれること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: 仕様一覧ページの生成

- **Given** DoorstopプロジェクトにSPECアイテムが存在する
- **When** build コマンドを実行する
- **Then** docs/spec.md が生成されること
- **And** 各SPECアイテムがテーブル行として含まれること
- **And** 上位要件への相互リンクが含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopプロジェクトにSPECアイテムが存在する

```python
@given(u'DoorstopプロジェクトにSPECアイテムが存在する')
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

#### Then docs/spec.md が生成されること

```python
@then(u'docs/spec.md が生成されること')
def step_impl(context):
    pass
```

#### And 各SPECアイテムがテーブル行として含まれること

```python
@then(u'各SPECアイテムがテーブル行として含まれること')
def step_impl(context):
    pass
```

#### And 上位要件への相互リンクが含まれること

```python
@then(u'上位要件への相互リンクが含まれること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: 個別アイテム詳細ページの生成

- **Given** DoorstopプロジェクトにアイテムとGherkinテストが存在する
- **When** build コマンドを実行する
- **Then** docs/items/ 配下に各アイテムのMarkdownファイルが生成されること
- **And** アイテムの本文が含まれること
- **And** 上位・下位リンクが含まれること
- **And** 対応するテストシナリオのファイルパスと行番号が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopプロジェクトにアイテムとGherkinテストが存在する

```python
@given(u'DoorstopプロジェクトにアイテムとGherkinテストが存在する')
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

#### Then docs/items/ 配下に各アイテムのMarkdownファイルが生成されること

```python
@then(u'docs/items/ 配下に各アイテムのMarkdownファイルが生成されること')
def step_impl(context):
    pass
```

#### And アイテムの本文が含まれること

```python
@then(u'アイテムの本文が含まれること')
def step_impl(context):
    pass
```

#### And 上位・下位リンクが含まれること

```python
@then(u'上位・下位リンクが含まれること')
def step_impl(context):
    pass
```

#### And 対応するテストシナリオのファイルパスと行番号が含まれること

```python
@then(u'対応するテストシナリオのファイルパスと行番号が含まれること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: 一覧テーブルのフィルタリング機能

**タグ**: `@SPEC-009`

- **Given** Doorstopプロジェクトにアイテムが存在する
- **When** build コマンドを実行する
- **Then** 生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること
- **And** ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopプロジェクトにアイテムが存在する

```python
@given(u'Doorstopプロジェクトにアイテムが存在する')
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

#### Then 生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること

```python
@then(u'生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること')
def step_impl(context):
    pass
```

#### And ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること

```python
@then(u'ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: 出力ディレクトリの独立性

- **Given** プロジェクトに既存のドキュメントが存在する
- **When** build コマンドをデフォルト出力先で実行する
- **Then** ".specification" ディレクトリに出力されること
- **And** 既存のドキュメントファイルは変更されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given プロジェクトに既存のドキュメントが存在する

```python
@given(u'プロジェクトに既存のドキュメントが存在する')
def step_impl(context):
    pass
```

#### When build コマンドをデフォルト出力先で実行する

```python
@when(u'build コマンドをデフォルト出力先で実行する')
def step_impl(context):
    res = run_spec_weaver(['build'], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then ".specification" ディレクトリに出力されること

```python
@then('"{param0}" ディレクトリに出力されること')  # type: ignore
def then_32de837a(context, param0):
    """".specification" ディレクトリに出力されること

    Scenarios:
      - 出力ディレクトリの独立性
      - カスタム出力ディレクトリの指定
    """
    pass
```

#### And 既存のドキュメントファイルは変更されないこと

```python
@then(u'既存のドキュメントファイルは変更されないこと')
def step_impl(context):
    pass
```

</details>


---
## Scenario: カスタム出力ディレクトリの指定

- **Given** DoorstopプロジェクトとGherkin featureファイルが存在する
- **When** build コマンドを --out-dir "./custom_docs" で実行する
- **Then** "./custom_docs" ディレクトリに出力されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopプロジェクトとGherkin featureファイルが存在する

```python
@given(u'DoorstopプロジェクトとGherkin featureファイルが存在する')
def step_impl(context):
    pass
```

#### When build コマンドを --out-dir "./custom_docs" で実行する

```python
@when('build コマンドを --out-dir "{param0}" で実行する')  # type: ignore
def when_678e47f6(context, param0):
    """build コマンドを --out-dir "./custom_docs" で実行する

    Scenarios:
      - カスタム出力ディレクトリの指定
    """
    pass
```

#### Then "./custom_docs" ディレクトリに出力されること

```python
@then('"{param0}" ディレクトリに出力されること')  # type: ignore
def then_32de837a(context, param0):
    """".specification" ディレクトリに出力されること

    Scenarios:
      - 出力ディレクトリの独立性
      - カスタム出力ディレクトリの指定
    """
    pass
```

</details>


---
## Scenario: feature MDページへのバックリンク生成

**タグ**: `@SPEC-014`

- **Given** "@SPEC-003" タグを持つ "audit.feature" が存在する
- **When** build コマンドを実行する
- **Then** "docs/features/audit.md" の冒頭に "関連アイテム" セクションが含まれること
- **And** "[SPEC-003](../items/SPEC-003.md)" へのリンクが含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "@SPEC-003" タグを持つ "audit.feature" が存在する

```python
@given('"{param0}" タグを持つ "{param1}" が存在する')  # type: ignore
def given_8c5d7037(context, param0, param1):
    """"@SPEC-003" タグを持つ "audit.feature" が存在する

    Scenarios:
      - feature MDページへのバックリンク生成
    """
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

#### Then "docs/features/audit.md" の冒頭に "関連アイテム" セクションが含まれること

```python
@then('"{param0}" の冒頭に "{param1}" セクションが含まれること')  # type: ignore
def then_dcbe151a(context, param0, param1):
    """"docs/features/audit.md" の冒頭に "関連アイテム" セクションが含まれること

    Scenarios:
      - feature MDページへのバックリンク生成
    """
    pass
```

#### And "[SPEC-003](../items/SPEC-003.md)" へのリンクが含まれること

```python
@then('"{param0}" へのリンクが含まれること')  # type: ignore
def then_3dd5fc62(context, param0):
    """"[SPEC-003](../items/SPEC-003.md)" へのリンクが含まれること

    Scenarios:
      - feature MDページへのバックリンク生成
    """
    pass
```

</details>


---
## Scenario: 複数アイテムを参照するfeatureのバックリンク

**タグ**: `@SPEC-014`

- **Given** "@SPEC-004" と "@SPEC-009" の両タグを持つfeatureが存在する
- **When** build コマンドを実行する
- **Then** 生成されたfeature MDの "関連アイテム" に "SPEC-004" と "SPEC-009" の両方のリンクが含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "@SPEC-004" と "@SPEC-009" の両タグを持つfeatureが存在する

```python
@given('"{param0}" と "{param1}" の両タグを持つfeatureが存在する')  # type: ignore
def given_1d9c057d(context, param0, param1):
    """"@SPEC-004" と "@SPEC-009" の両タグを持つfeatureが存在する

    Scenarios:
      - 複数アイテムを参照するfeatureのバックリンク
    """
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

#### Then 生成されたfeature MDの "関連アイテム" に "SPEC-004" と "SPEC-009" の両方のリンクが含まれること

```python
@then('生成されたfeature MDの "{param0}" に "{param1}" と "{param2}" の両方のリンクが含まれること')  # type: ignore
def then_d670dbfb(context, param0, param1, param2):
    """生成されたfeature MDの "関連アイテム" に "SPEC-004" と "SPEC-009" の両方のリンクが含まれること

    Scenarios:
      - 複数アイテムを参照するfeatureのバックリンク
    """
    pass
```

</details>


---
## Scenario: タグのないfeatureにはバックリンクを表示しない

**タグ**: `@SPEC-014`

- **Given** どのDoorstopアイテムからも参照されていないfeatureが存在する
- **When** build コマンドを実行する
- **Then** 生成されたfeature MDに "関連アイテム" 行が含まれないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given どのDoorstopアイテムからも参照されていないfeatureが存在する

```python
@given(u'どのDoorstopアイテムからも参照されていないfeatureが存在する')
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

#### Then 生成されたfeature MDに "関連アイテム" 行が含まれないこと

```python
@then('生成されたfeature MDに "{param0}" 行が含まれないこと')  # type: ignore
def then_7458537c(context, param0):
    """生成されたfeature MDに "関連アイテム" 行が含まれないこと

    Scenarios:
      - タグのないfeatureにはバックリンクを表示しない
    """
    pass
```

</details>


---
## Scenario: Suspect Link 警告の一覧テーブル表示

**タグ**: `@SPEC-005`

- **Given** アイテムの上位リンク先が変更されている（cleared=false）
- **When** build コマンドを実行する
- **Then** 一覧テーブルの行に "{: .suspect-row }" が適用されていること
- **And** 詳細ページに Suspect Link バナーが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given アイテムの上位リンク先が変更されている（cleared=false）

```python
@given(u'アイテムの上位リンク先が変更されている（cleared=false）')
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

#### Then 一覧テーブルの行に "{: .suspect-row }" が適用されていること

```python
@then('一覧テーブルの行に "{param0}" が適用されていること')  # type: ignore
def then_011c6eae(context, param0):
    """一覧テーブルの行に "{: .suspect-row }" が適用されていること

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
      - Unreviewed Changes 警告の一覧テーブル表示
      - 複合警告の表示
    """
    pass
```

#### And 詳細ページに Suspect Link バナーが表示されること

```python
@then(u'詳細ページに Suspect Link バナーが表示されること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: Unreviewed Changes 警告の一覧テーブル表示

**タグ**: `@SPEC-005`

- **Given** アイテム自体に未レビューの変更がある（reviewed=false）
- **When** build コマンドを実行する
- **Then** 一覧テーブルの行に "{: .unreviewed-row }" が適用されていること
- **And** 詳細ページに Unreviewed Changes バナーが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given アイテム自体に未レビューの変更がある（reviewed=false）

```python
@given(u'アイテム自体に未レビューの変更がある（reviewed=false）')
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

#### Then 一覧テーブルの行に "{: .unreviewed-row }" が適用されていること

```python
@then('一覧テーブルの行に "{param0}" が適用されていること')  # type: ignore
def then_011c6eae(context, param0):
    """一覧テーブルの行に "{: .suspect-row }" が適用されていること

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
      - Unreviewed Changes 警告の一覧テーブル表示
      - 複合警告の表示
    """
    pass
```

#### And 詳細ページに Unreviewed Changes バナーが表示されること

```python
@then(u'詳細ページに Unreviewed Changes バナーが表示されること')
def step_impl(context):
    pass
```

</details>


---
## Scenario: 複合警告の表示

**タグ**: `@SPEC-005`

- **Given** アイテムに Suspect Link と Unreviewed Changes の両方がある
- **When** build コマンドを実行する
- **Then** 一覧テーブルの行に "{: .suspect-row }" が適用されていること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given アイテムに Suspect Link と Unreviewed Changes の両方がある

```python
@given(u'アイテムに Suspect Link と Unreviewed Changes の両方がある')
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

#### Then 一覧テーブルの行に "{: .suspect-row }" が適用されていること

```python
@then('一覧テーブルの行に "{param0}" が適用されていること')  # type: ignore
def then_011c6eae(context, param0):
    """一覧テーブルの行に "{: .suspect-row }" が適用されていること

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
      - Unreviewed Changes 警告の一覧テーブル表示
      - 複合警告の表示
    """
    pass
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: 4d1abc0d24ab84d4b44873ab7fcc439c3e9951bd4046244b1bef9e31f22ac785
@SPEC-004
Feature: build コマンド
  Doorstopの仕様データとGherkinテストを統合した
  MkDocsドキュメントサイトを自動生成する。

  Scenario: MkDocs設定ファイルの生成
    Given DoorstopプロジェクトとGherkin featureファイルが存在する
    When  build コマンドを実行する
    Then  出力ディレクトリに mkdocs.yml が生成されること
    And   Material テーマが設定されていること

  Scenario: 要件一覧ページの生成
    Given DoorstopプロジェクトにREQアイテムが存在する
    When  build コマンドを実行する
    Then  docs/req.md が生成されること
    And   各REQアイテムがテーブル行として含まれること
    And   関連仕様への相互リンクが含まれること

  Scenario: 仕様一覧ページの生成
    Given DoorstopプロジェクトにSPECアイテムが存在する
    When  build コマンドを実行する
    Then  docs/spec.md が生成されること
    And   各SPECアイテムがテーブル行として含まれること
    And   上位要件への相互リンクが含まれること

  Scenario: 個別アイテム詳細ページの生成
    Given DoorstopプロジェクトにアイテムとGherkinテストが存在する
    When  build コマンドを実行する
    Then  docs/items/ 配下に各アイテムのMarkdownファイルが生成されること
    And   アイテムの本文が含まれること
    And   上位・下位リンクが含まれること
    And   対応するテストシナリオのファイルパスと行番号が含まれること

  @SPEC-009
  Scenario: 一覧テーブルのフィルタリング機能
    Given Doorstopプロジェクトにアイテムが存在する
    When  build コマンドを実行する
    Then  生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること
    And   ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること

  Scenario: 出力ディレクトリの独立性
    Given プロジェクトに既存のドキュメントが存在する
    When  build コマンドをデフォルト出力先で実行する
    Then  ".specification" ディレクトリに出力されること
    And   既存のドキュメントファイルは変更されないこと

  Scenario: カスタム出力ディレクトリの指定
    Given DoorstopプロジェクトとGherkin featureファイルが存在する
    When  build コマンドを --out-dir "./custom_docs" で実行する
    Then  "./custom_docs" ディレクトリに出力されること

  @SPEC-014
  Scenario: feature MDページへのバックリンク生成
    Given "@SPEC-003" タグを持つ "audit.feature" が存在する
    When  build コマンドを実行する
    Then  "docs/features/audit.md" の冒頭に "関連アイテム" セクションが含まれること
    And   "[SPEC-003](../items/SPEC-003.md)" へのリンクが含まれること

  @SPEC-014
  Scenario: 複数アイテムを参照するfeatureのバックリンク
    Given "@SPEC-004" と "@SPEC-009" の両タグを持つfeatureが存在する
    When  build コマンドを実行する
    Then  生成されたfeature MDの "関連アイテム" に "SPEC-004" と "SPEC-009" の両方のリンクが含まれること

  @SPEC-014
  Scenario: タグのないfeatureにはバックリンクを表示しない
    Given どのDoorstopアイテムからも参照されていないfeatureが存在する
    When  build コマンドを実行する
    Then  生成されたfeature MDに "関連アイテム" 行が含まれないこと

  @SPEC-005
  Scenario: Suspect Link 警告の一覧テーブル表示
    Given アイテムの上位リンク先が変更されている（cleared=false）
    When  build コマンドを実行する
    Then  一覧テーブルの行に "{: .suspect-row }" が適用されていること
    And   詳細ページに Suspect Link バナーが表示されること

  @SPEC-005
  Scenario: Unreviewed Changes 警告の一覧テーブル表示
    Given アイテム自体に未レビューの変更がある（reviewed=false）
    When  build コマンドを実行する
    Then  一覧テーブルの行に "{: .unreviewed-row }" が適用されていること
    And   詳細ページに Unreviewed Changes バナーが表示されること

  @SPEC-005
  Scenario: 複合警告の表示
    Given アイテムに Suspect Link と Unreviewed Changes の両方がある
    When  build コマンドを実行する
    Then  一覧テーブルの行に "{: .suspect-row }" が適用されていること

```
</details>