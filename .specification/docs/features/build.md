# Feature: build コマンド

**タグ**: `@VIS-001`

**関連アイテム**: [QA-001](../items/QA-001.md) / [VIS-001](../items/VIS-001.md) / [VIS-005](../items/VIS-005.md) / [VIS-008](../items/VIS-008.md)

Doorstopの仕様データとGherkinテストを統合した
  MkDocsドキュメントサイトを自動生成する。

---
## Scenario: MkDocs設定ファイルの生成 {: #line-11 }

- **Given** DoorstopプロジェクトとGherkin featureファイルが存在する
- **When** build コマンドを実行する
- **Then** 出力ディレクトリに mkdocs.yml が生成されること
- **And** Material テーマが設定されていること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_build.py", line 18, in given_8a7b1a87
    raise NotImplementedError('STEP: DoorstopプロジェクトとGherkin featureファイルが存在する')
NotImplementedError: STEP: DoorstopプロジェクトとGherkin featureファイルが存在する
```

#### Given DoorstopプロジェクトとGherkin featureファイルが存在する

```python
@given('DoorstopプロジェクトとGherkin featureファイルが存在する')  # type: ignore
def given_8a7b1a87(context):
    """DoorstopプロジェクトとGherkin featureファイルが存在する

    Scenarios:
      - MkDocs設定ファイルの生成
      - カスタム出力ディレクトリの指定
    """
    raise NotImplementedError('STEP: DoorstopプロジェクトとGherkin featureファイルが存在する')
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
@then('出力ディレクトリに mkdocs.yml が生成されること')  # type: ignore
def then_453d91c1(context):
    """出力ディレクトリに mkdocs.yml が生成されること

    Scenarios:
      - MkDocs設定ファイルの生成
    """
    raise NotImplementedError('STEP: 出力ディレクトリに mkdocs.yml が生成されること')
```

#### And Material テーマが設定されていること

```python
@then('Material テーマが設定されていること')  # type: ignore
def then_281c0fa4(context):
    """Material テーマが設定されていること

    Scenarios:
      - MkDocs設定ファイルの生成
    """
    raise NotImplementedError('STEP: Material テーマが設定されていること')
```

</details>


---
## Scenario: 要件一覧ページの生成 {: #line-17 }

- **Given** DoorstopプロジェクトにREQアイテムが存在する
- **When** build コマンドを実行する
- **Then** docs/req.md が生成されること
- **And** 各REQアイテムがテーブル行として含まれること
- **And** 関連仕様への相互リンクが含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_build.py", line 48, in given_ce6845b7
    raise NotImplementedError('STEP: DoorstopプロジェクトにREQアイテムが存在する')
NotImplementedError: STEP: DoorstopプロジェクトにREQアイテムが存在する
```

#### Given DoorstopプロジェクトにREQアイテムが存在する

```python
@given('DoorstopプロジェクトにREQアイテムが存在する')  # type: ignore
def given_ce6845b7(context):
    """DoorstopプロジェクトにREQアイテムが存在する

    Scenarios:
      - 要件一覧ページの生成
    """
    raise NotImplementedError('STEP: DoorstopプロジェクトにREQアイテムが存在する')
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
@then('docs/req.md が生成されること')  # type: ignore
def then_0130d8b7(context):
    """docs/req.md が生成されること

    Scenarios:
      - 要件一覧ページの生成
    """
    raise NotImplementedError('STEP: docs/req.md が生成されること')
```

#### And 各REQアイテムがテーブル行として含まれること

```python
@then('各REQアイテムがテーブル行として含まれること')  # type: ignore
def then_2977857a(context):
    """各REQアイテムがテーブル行として含まれること

    Scenarios:
      - 要件一覧ページの生成
    """
    raise NotImplementedError('STEP: 各REQアイテムがテーブル行として含まれること')
```

#### And 関連仕様への相互リンクが含まれること

```python
@then('関連仕様への相互リンクが含まれること')  # type: ignore
def then_ef9d25c2(context):
    """関連仕様への相互リンクが含まれること

    Scenarios:
      - 要件一覧ページの生成
    """
    raise NotImplementedError('STEP: 関連仕様への相互リンクが含まれること')
```

</details>


---
## Scenario: 仕様一覧ページの生成 {: #line-24 }

- **Given** DoorstopプロジェクトにSPECアイテムが存在する
- **When** build コマンドを実行する
- **Then** docs/spec.md が生成されること
- **And** 各SPECアイテムがテーブル行として含まれること
- **And** 上位要件への相互リンクが含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_build.py", line 135, in then_9b5808a6
    raise NotImplementedError('STEP: docs/spec.md が生成されること')
NotImplementedError: STEP: docs/spec.md が生成されること
```

#### Given DoorstopプロジェクトにSPECアイテムが存在する

```python
@given('DoorstopプロジェクトにSPECアイテムが存在する')  # type: ignore
def given_ae2b8b7d(context):
    """DoorstopプロジェクトにSPECアイテムが存在する

    Scenarios:
      - 仕様一覧ページの生成
      - 一覧テーブルにレビューステータス列が表示されること
    """
    import tempfile
    from pathlib import Path

    tmp_dir = Path(tempfile.mkdtemp())
    context.tmp_dir = tmp_dir

    from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file
    create_doorstop_project_yaml(tmp_dir, [
        {
            "dir": "reqs",
            "prefix": "REQ",
            "parent": None,
            "items": [{"uid": "REQ-001", "header": "要件1", "testable": False}],
        },
        {
            "dir": "specs",
            "prefix": "SPEC",
            "parent": "REQ",
            "items": [{"uid": "SPEC-001", "header": "仕様1", "links": ["REQ-001"]}],
        },
    ])

    features_dir = tmp_dir / "features"
    features_dir.mkdir()
    write_feature_file(
        features_dir / "test.feature",
        "@SPEC-001\nFeature: テスト\n\n  Scenario: S1\n    Given 前提\n    When 操作\n    Then 確認\n",
    )

    out_dir = tmp_dir / "out"
    result = run_spec_weaver(
        ["build", str(features_dir), "--out-dir", str(out_dir)],
        cwd=tmp_dir,
    )
    spec_md = out_dir / "docs" / "spec.md"
    context.spec_md_content = spec_md.read_text(encoding="utf-8") if spec_md.exists() else ""
    context.build_result = result
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
@then('docs/spec.md が生成されること')  # type: ignore
def then_9b5808a6(context):
    """docs/spec.md が生成されること

    Scenarios:
      - 仕様一覧ページの生成
    """
    raise NotImplementedError('STEP: docs/spec.md が生成されること')
```

#### And 各SPECアイテムがテーブル行として含まれること

```python
@then('各SPECアイテムがテーブル行として含まれること')  # type: ignore
def then_86be7f51(context):
    """各SPECアイテムがテーブル行として含まれること

    Scenarios:
      - 仕様一覧ページの生成
    """
    raise NotImplementedError('STEP: 各SPECアイテムがテーブル行として含まれること')
```

#### And 上位要件への相互リンクが含まれること

```python
@then('上位要件への相互リンクが含まれること')  # type: ignore
def then_d1af9a65(context):
    """上位要件への相互リンクが含まれること

    Scenarios:
      - 仕様一覧ページの生成
    """
    raise NotImplementedError('STEP: 上位要件への相互リンクが含まれること')
```

</details>


---
## Scenario: 個別アイテム詳細ページの生成 {: #line-31 }

- **Given** DoorstopプロジェクトにアイテムとGherkinテストが存在する
- **When** build コマンドを実行する
- **Then** docs/items/ 配下に各アイテムのMarkdownファイルが生成されること
- **And** アイテムの本文が含まれること
- **And** 上位・下位リンクが含まれること
- **And** 対応するテストシナリオのファイルパスと行番号が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_build.py", line 165, in given_73c18566
    raise NotImplementedError('STEP: DoorstopプロジェクトにアイテムとGherkinテストが存在する')
NotImplementedError: STEP: DoorstopプロジェクトにアイテムとGherkinテストが存在する
```

#### Given DoorstopプロジェクトにアイテムとGherkinテストが存在する

```python
@given('DoorstopプロジェクトにアイテムとGherkinテストが存在する')  # type: ignore
def given_73c18566(context):
    """DoorstopプロジェクトにアイテムとGherkinテストが存在する

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    raise NotImplementedError('STEP: DoorstopプロジェクトにアイテムとGherkinテストが存在する')
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
@then('docs/items/ 配下に各アイテムのMarkdownファイルが生成されること')  # type: ignore
def then_77d459df(context):
    """docs/items/ 配下に各アイテムのMarkdownファイルが生成されること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    raise NotImplementedError('STEP: docs/items/ 配下に各アイテムのMarkdownファイルが生成されること')
```

#### And アイテムの本文が含まれること

```python
@then('アイテムの本文が含まれること')  # type: ignore
def then_650f49fb(context):
    """アイテムの本文が含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    raise NotImplementedError('STEP: アイテムの本文が含まれること')
```

#### And 上位・下位リンクが含まれること

```python
@then('上位・下位リンクが含まれること')  # type: ignore
def then_677a5bf3(context):
    """上位・下位リンクが含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    raise NotImplementedError('STEP: 上位・下位リンクが含まれること')
```

#### And 対応するテストシナリオのファイルパスと行番号が含まれること

```python
@then('対応するテストシナリオのファイルパスと行番号が含まれること')  # type: ignore
def then_ae3c7159(context):
    """対応するテストシナリオのファイルパスと行番号が含まれること

    Scenarios:
      - 個別アイテム詳細ページの生成
    """
    raise NotImplementedError('STEP: 対応するテストシナリオのファイルパスと行番号が含まれること')
```

</details>


---
## Scenario: 一覧テーブルのフィルタリング機能 {: #line-40 }

**タグ**: `@VIS-005`

- **Given** Doorstopプロジェクトにアイテムが存在する
- **When** build コマンドを実行する
- **Then** 生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること
- **And** ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_build.py", line 215, in given_93d749da
    raise NotImplementedError('STEP: Doorstopプロジェクトにアイテムが存在する')
NotImplementedError: STEP: Doorstopプロジェクトにアイテムが存在する
```

#### Given Doorstopプロジェクトにアイテムが存在する

```python
@given('Doorstopプロジェクトにアイテムが存在する')  # type: ignore
def given_93d749da(context):
    """Doorstopプロジェクトにアイテムが存在する

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    raise NotImplementedError('STEP: Doorstopプロジェクトにアイテムが存在する')
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
@then('生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること')  # type: ignore
def then_7bdfccf5(context):
    """生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    raise NotImplementedError('STEP: 生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること')
```

#### And ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること

```python
@then('ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること')  # type: ignore
def then_ca03093b(context):
    """ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること

    Scenarios:
      - 一覧テーブルのフィルタリング機能
    """
    raise NotImplementedError('STEP: ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること')
```

</details>


---
## Scenario: 出力ディレクトリの独立性 {: #line-46 }

- **Given** プロジェクトに既存のドキュメントが存在する
- **When** build コマンドをデフォルト出力先で実行する
- **Then** ".specification" ディレクトリに出力されること
- **And** 既存のドキュメントファイルは変更されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_build.py", line 245, in given_b7341593
    raise NotImplementedError('STEP: プロジェクトに既存のドキュメントが存在する')
NotImplementedError: STEP: プロジェクトに既存のドキュメントが存在する
```

#### Given プロジェクトに既存のドキュメントが存在する

```python
@given('プロジェクトに既存のドキュメントが存在する')  # type: ignore
def given_b7341593(context):
    """プロジェクトに既存のドキュメントが存在する

    Scenarios:
      - 出力ディレクトリの独立性
    """
    raise NotImplementedError('STEP: プロジェクトに既存のドキュメントが存在する')
```

#### When build コマンドをデフォルト出力先で実行する

```python
@when('build コマンドをデフォルト出力先で実行する')  # type: ignore
def when_6f73d51e(context):
    """build コマンドをデフォルト出力先で実行する

    Scenarios:
      - 出力ディレクトリの独立性
    """
    raise NotImplementedError('STEP: build コマンドをデフォルト出力先で実行する')
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
@then('既存のドキュメントファイルは変更されないこと')  # type: ignore
def then_56c968de(context):
    """既存のドキュメントファイルは変更されないこと

    Scenarios:
      - 出力ディレクトリの独立性
    """
    raise NotImplementedError('STEP: 既存のドキュメントファイルは変更されないこと')
```

</details>


---
## Scenario: カスタム出力ディレクトリの指定 {: #line-52 }

- **Given** DoorstopプロジェクトとGherkin featureファイルが存在する
- **When** build コマンドを --out-dir "./custom_docs" で実行する
- **Then** "./custom_docs" ディレクトリに出力されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_build.py", line 18, in given_8a7b1a87
    raise NotImplementedError('STEP: DoorstopプロジェクトとGherkin featureファイルが存在する')
NotImplementedError: STEP: DoorstopプロジェクトとGherkin featureファイルが存在する
```

#### Given DoorstopプロジェクトとGherkin featureファイルが存在する

```python
@given('DoorstopプロジェクトとGherkin featureファイルが存在する')  # type: ignore
def given_8a7b1a87(context):
    """DoorstopプロジェクトとGherkin featureファイルが存在する

    Scenarios:
      - MkDocs設定ファイルの生成
      - カスタム出力ディレクトリの指定
    """
    raise NotImplementedError('STEP: DoorstopプロジェクトとGherkin featureファイルが存在する')
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
## Scenario: feature MDページへのバックリンク生成 {: #line-58 }

**タグ**: `@VIS-008`

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
## Scenario: 複数アイテムを参照するfeatureのバックリンク {: #line-65 }

**タグ**: `@VIS-008`

- **Given** "@VIS-001" と "@VIS-005" の両タグを持つfeatureが存在する
- **When** build コマンドを実行する
- **Then** 生成されたfeature MDの "関連アイテム" に "VIS-001" と "VIS-005" の両方のリンクが含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "@VIS-001" と "@VIS-005" の両タグを持つfeatureが存在する

```python
@given('"{param0}" と "{param1}" の両タグを持つfeatureが存在する')  # type: ignore
def given_1d9c057d(context, param0, param1):
    """"@VIS-001" と "@VIS-005" の両タグを持つfeatureが存在する

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

#### Then 生成されたfeature MDの "関連アイテム" に "VIS-001" と "VIS-005" の両方のリンクが含まれること

```python
@then('生成されたfeature MDの "{param0}" に "{param1}" と "{param2}" の両方のリンクが含まれること')  # type: ignore
def then_d670dbfb(context, param0, param1, param2):
    """生成されたfeature MDの "関連アイテム" に "VIS-001" と "VIS-005" の両方のリンクが含まれること

    Scenarios:
      - 複数アイテムを参照するfeatureのバックリンク
    """
    pass
```

</details>


---
## Scenario: タグのないfeatureにはバックリンクを表示しない {: #line-71 }

**タグ**: `@VIS-008`

- **Given** どのDoorstopアイテムからも参照されていないfeatureが存在する
- **When** build コマンドを実行する
- **Then** 生成されたfeature MDに "関連アイテム" 行が含まれないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_build.py", line 346, in given_486efd83
    raise NotImplementedError('STEP: どのDoorstopアイテムからも参照されていないfeatureが存在する')
NotImplementedError: STEP: どのDoorstopアイテムからも参照されていないfeatureが存在する
```

#### Given どのDoorstopアイテムからも参照されていないfeatureが存在する

```python
@given('どのDoorstopアイテムからも参照されていないfeatureが存在する')  # type: ignore
def given_486efd83(context):
    """どのDoorstopアイテムからも参照されていないfeatureが存在する

    Scenarios:
      - タグのないfeatureにはバックリンクを表示しない
    """
    raise NotImplementedError('STEP: どのDoorstopアイテムからも参照されていないfeatureが存在する')
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
## Scenario: Suspect Link 警告の一覧テーブル表示 {: #line-77 }

**タグ**: `@QA-001`

- **Given** アイテムの上位リンク先が変更されている（cleared=false）
- **When** build コマンドを実行する
- **Then** 一覧テーブルの行に "{: .suspect-row }" が適用されていること
- **And** 詳細ページに Suspect Link バナーが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_build.py", line 366, in given_5951291a
    raise NotImplementedError('STEP: アイテムの上位リンク先が変更されている（cleared=false）')
NotImplementedError: STEP: アイテムの上位リンク先が変更されている（cleared=false）
```

#### Given アイテムの上位リンク先が変更されている（cleared=false）

```python
@given('アイテムの上位リンク先が変更されている（cleared=false）')  # type: ignore
def given_5951291a(context):
    """アイテムの上位リンク先が変更されている（cleared=false）

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
    """
    raise NotImplementedError('STEP: アイテムの上位リンク先が変更されている（cleared=false）')
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
@then('詳細ページに Suspect Link バナーが表示されること')  # type: ignore
def then_b9db4871(context):
    """詳細ページに Suspect Link バナーが表示されること

    Scenarios:
      - Suspect Link 警告の一覧テーブル表示
    """
    raise NotImplementedError('STEP: 詳細ページに Suspect Link バナーが表示されること')
```

</details>


---
## Scenario: Unreviewed Changes 警告の一覧テーブル表示 {: #line-84 }

**タグ**: `@QA-001`

- **Given** アイテム自体に未レビューの変更がある（reviewed=false）
- **When** build コマンドを実行する
- **Then** 一覧テーブルの行に "{: .unreviewed-row }" が適用されていること
- **And** 詳細ページに Unreviewed Changes バナーが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_build.py", line 398, in given_60830b9f
    raise NotImplementedError('STEP: アイテム自体に未レビューの変更がある（reviewed=false）')
NotImplementedError: STEP: アイテム自体に未レビューの変更がある（reviewed=false）
```

#### Given アイテム自体に未レビューの変更がある（reviewed=false）

```python
@given('アイテム自体に未レビューの変更がある（reviewed=false）')  # type: ignore
def given_60830b9f(context):
    """アイテム自体に未レビューの変更がある（reviewed=false）

    Scenarios:
      - Unreviewed Changes 警告の一覧テーブル表示
    """
    raise NotImplementedError('STEP: アイテム自体に未レビューの変更がある（reviewed=false）')
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
@then('詳細ページに Unreviewed Changes バナーが表示されること')  # type: ignore
def then_e1fe71d4(context):
    """詳細ページに Unreviewed Changes バナーが表示されること

    Scenarios:
      - Unreviewed Changes 警告の一覧テーブル表示
    """
    raise NotImplementedError('STEP: 詳細ページに Unreviewed Changes バナーが表示されること')
```

</details>


---
## Scenario: 複合警告の表示 {: #line-91 }

**タグ**: `@QA-001`

- **Given** アイテムに Suspect Link と Unreviewed Changes の両方がある
- **When** build コマンドを実行する
- **Then** 一覧テーブルの行に "{: .suspect-row }" が適用されていること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### 📋 Execution Log (Failure)

```text
Traceback (most recent call last):
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/model.py", line 1991, in run
    match.run(runner.context)
    ~~~~~~~~~^^^^^^^^^^^^^^^^
  File "/home/adelie/projects/spec-weaver/.venv/lib/python3.14/site-packages/behave/matchers.py", line 105, in run
    self.func(context, *args, **kwargs)
    ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "specification/features/steps/step_build.py", line 418, in given_89f3d16e
    raise NotImplementedError('STEP: アイテムに Suspect Link と Unreviewed Changes の両方がある')
NotImplementedError: STEP: アイテムに Suspect Link と Unreviewed Changes の両方がある
```

#### Given アイテムに Suspect Link と Unreviewed Changes の両方がある

```python
@given('アイテムに Suspect Link と Unreviewed Changes の両方がある')  # type: ignore
def given_89f3d16e(context):
    """アイテムに Suspect Link と Unreviewed Changes の両方がある

    Scenarios:
      - 複合警告の表示
    """
    raise NotImplementedError('STEP: アイテムに Suspect Link と Unreviewed Changes の両方がある')
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
## Scenario: 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること {: #line-96 }

- **Given** 2つのシナリオを持つfeatureファイルにタグで紐づいたSPECアイテムが存在する
- **When** build コマンドを実行する
- **Then** 一覧テーブルの Gherkinカバレッジ列に "🟢 2" が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 2つのシナリオを持つfeatureファイルにタグで紐づいたSPECアイテムが存在する

```python
@given('2つのシナリオを持つfeatureファイルにタグで紐づいたSPECアイテムが存在する')  # type: ignore
def given_a5569e86(context):
    """2つのシナリオを持つfeatureファイルにタグで紐づいたSPECアイテムが存在する

    Scenarios:
      - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
    """
    import tempfile
    from pathlib import Path

    tmp_dir = Path(tempfile.mkdtemp())
    context.tmp_dir = tmp_dir

    from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file
    create_doorstop_project_yaml(tmp_dir, [
        {
            "dir": "reqs",
            "prefix": "REQ",
            "parent": None,
            "items": [{"uid": "REQ-001", "header": "要件1", "testable": False}],
        },
        {
            "dir": "specs",
            "prefix": "SPEC",
            "parent": "REQ",
            "items": [{"uid": "SPEC-001", "header": "仕様1", "links": ["REQ-001"]}],
        },
    ])

    features_dir = tmp_dir / "features"
    features_dir.mkdir()
    feature_content = (
        "@SPEC-001\n"
        "Feature: テスト用フィーチャー\n\n"
        "  Scenario: シナリオその1\n"
        "    Given 前提\n"
        "    When  操作\n"
        "    Then  確認\n\n"
        "  Scenario: シナリオその2\n"
        "    Given 前提2\n"
        "    When  操作2\n"
        "    Then  確認2\n"
    )
    write_feature_file(features_dir / "test.feature", feature_content)

    out_dir = tmp_dir / "out"
    result = run_spec_weaver(
        ["build", str(features_dir), "--out-dir", str(out_dir)],
        cwd=tmp_dir,
    )
    spec_md = out_dir / "docs" / "spec.md"
    context.spec_md_content = spec_md.read_text(encoding="utf-8") if spec_md.exists() else ""
    context.build_result = result
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

#### Then 一覧テーブルの Gherkinカバレッジ列に "🟢 2" が含まれること

```python
@then('一覧テーブルの Gherkinカバレッジ列に "{param0}" が含まれること')  # type: ignore
def then_5b76eb00(context, param0):
    """一覧テーブルの Gherkinカバレッジ列に "🟢 2" が含まれること

    Scenarios:
      - 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
    """
    content = getattr(context, "spec_md_content", "")
    assert param0 in content, (
        f"期待文字列 {param0!r} が spec.md に見つかりません。\n"
        f"spec.md:\n{content[:2000]}"
    )
```

</details>


---
## Scenario: 一覧テーブルにレビューステータス列が表示されること {: #line-101 }

- **Given** DoorstopプロジェクトにSPECアイテムが存在する
- **When** build コマンドを実行する
- **Then** 一覧テーブルのヘッダーに "レビュー" 列が含まれること
- **And** 各行にレビューステータスが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopプロジェクトにSPECアイテムが存在する

```python
@given('DoorstopプロジェクトにSPECアイテムが存在する')  # type: ignore
def given_ae2b8b7d(context):
    """DoorstopプロジェクトにSPECアイテムが存在する

    Scenarios:
      - 仕様一覧ページの生成
      - 一覧テーブルにレビューステータス列が表示されること
    """
    import tempfile
    from pathlib import Path

    tmp_dir = Path(tempfile.mkdtemp())
    context.tmp_dir = tmp_dir

    from specification.features.steps._helpers import create_doorstop_project_yaml, write_feature_file
    create_doorstop_project_yaml(tmp_dir, [
        {
            "dir": "reqs",
            "prefix": "REQ",
            "parent": None,
            "items": [{"uid": "REQ-001", "header": "要件1", "testable": False}],
        },
        {
            "dir": "specs",
            "prefix": "SPEC",
            "parent": "REQ",
            "items": [{"uid": "SPEC-001", "header": "仕様1", "links": ["REQ-001"]}],
        },
    ])

    features_dir = tmp_dir / "features"
    features_dir.mkdir()
    write_feature_file(
        features_dir / "test.feature",
        "@SPEC-001\nFeature: テスト\n\n  Scenario: S1\n    Given 前提\n    When 操作\n    Then 確認\n",
    )

    out_dir = tmp_dir / "out"
    result = run_spec_weaver(
        ["build", str(features_dir), "--out-dir", str(out_dir)],
        cwd=tmp_dir,
    )
    spec_md = out_dir / "docs" / "spec.md"
    context.spec_md_content = spec_md.read_text(encoding="utf-8") if spec_md.exists() else ""
    context.build_result = result
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

#### Then 一覧テーブルのヘッダーに "レビュー" 列が含まれること

```python
@then('一覧テーブルのヘッダーに "{param0}" 列が含まれること')  # type: ignore
def then_eccd5afe(context, param0):
    """一覧テーブルのヘッダーに "レビュー" 列が含まれること

    Scenarios:
      - 一覧テーブルにレビューステータス列が表示されること
    """
    content = getattr(context, "spec_md_content", "")
    # ヘッダー行（| ID | タイトル | ... | レビュー | ... |）を確認
    header_line = next(
        (line for line in content.splitlines() if line.startswith("| ID ")), ""
    )
    assert param0 in header_line, (
        f"ヘッダー行に {param0!r} が見つかりません。\nヘッダー行: {header_line!r}"
    )
```

#### And 各行にレビューステータスが表示されること

```python
@then('各行にレビューステータスが表示されること')  # type: ignore
def then_8b62591d(context):
    """各行にレビューステータスが表示されること

    Scenarios:
      - 一覧テーブルにレビューステータス列が表示されること
    """
    content = getattr(context, "spec_md_content", "")
    # データ行（| SPEC-... | で始まる行）にレビューステータス文字列が含まれることを確認
    data_lines = [
        line for line in content.splitlines()
        if line.startswith("| [SPEC-") or line.startswith("| [REQ-")
    ]
    assert data_lines, "spec.md にデータ行が見つかりません。"
    for line in data_lines:
        has_review = any(marker in line for marker in ["reviewed", "suspect", "unreviewed"])
        assert has_review, f"データ行にレビューステータスが含まれません: {line!r}"
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: 9a459b73e608b26276d27ad6be826dfdafb28b176f6b7c528b2240a313da2bac
# spec-weaver-fingerprint-QA-001: IVjwbWJI8Xga_1LFrHA_SqnpsZ_-MHzjo-w7D9zwEYE=
# spec-weaver-fingerprint-VIS-001: vS8HMajMu_ierl6Dvv5xBk1dtLB30WMIGR7OIcwtLdk=
# spec-weaver-fingerprint-VIS-005: cnyg43CeR6DlR-nhO8_IOS6ZTbkaQoU6UoJyLvsS-JY=
# spec-weaver-fingerprint-VIS-008: 7sf3VezCdcJHKBaReMXoTyez2UxrlkvvZ8PvQBGdcA8=
@VIS-001
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

  @VIS-005
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

  @VIS-008
  Scenario: feature MDページへのバックリンク生成
    Given "@SPEC-003" タグを持つ "audit.feature" が存在する
    When  build コマンドを実行する
    Then  "docs/features/audit.md" の冒頭に "関連アイテム" セクションが含まれること
    And   "[SPEC-003](../items/SPEC-003.md)" へのリンクが含まれること

  @VIS-008
  Scenario: 複数アイテムを参照するfeatureのバックリンク
    Given "@VIS-001" と "@VIS-005" の両タグを持つfeatureが存在する
    When  build コマンドを実行する
    Then  生成されたfeature MDの "関連アイテム" に "VIS-001" と "VIS-005" の両方のリンクが含まれること

  @VIS-008
  Scenario: タグのないfeatureにはバックリンクを表示しない
    Given どのDoorstopアイテムからも参照されていないfeatureが存在する
    When  build コマンドを実行する
    Then  生成されたfeature MDに "関連アイテム" 行が含まれないこと

  @QA-001
  Scenario: Suspect Link 警告の一覧テーブル表示
    Given アイテムの上位リンク先が変更されている（cleared=false）
    When  build コマンドを実行する
    Then  一覧テーブルの行に "{: .suspect-row }" が適用されていること
    And   詳細ページに Suspect Link バナーが表示されること

  @QA-001
  Scenario: Unreviewed Changes 警告の一覧テーブル表示
    Given アイテム自体に未レビューの変更がある（reviewed=false）
    When  build コマンドを実行する
    Then  一覧テーブルの行に "{: .unreviewed-row }" が適用されていること
    And   詳細ページに Unreviewed Changes バナーが表示されること

  @QA-001
  Scenario: 複合警告の表示
    Given アイテムに Suspect Link と Unreviewed Changes の両方がある
    When  build コマンドを実行する
    Then  一覧テーブルの行に "{: .suspect-row }" が適用されていること

  Scenario: 一覧テーブルのGherkinカバレッジ列はシナリオ数を表示すること
    Given 2つのシナリオを持つfeatureファイルにタグで紐づいたSPECアイテムが存在する
    When  build コマンドを実行する
    Then  一覧テーブルの Gherkinカバレッジ列に "🟢 2" が含まれること

  Scenario: 一覧テーブルにレビューステータス列が表示されること
    Given DoorstopプロジェクトにSPECアイテムが存在する
    When  build コマンドを実行する
    Then  一覧テーブルのヘッダーに "レビュー" 列が含まれること
    And   各行にレビューステータスが表示されること

```
</details>