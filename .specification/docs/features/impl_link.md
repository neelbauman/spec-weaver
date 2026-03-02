# Feature: 仕様アイテムと実装ファイルのリンク管理

> 📋 **Unreviewed Changes**: このフィーチャーファイル自体に未レビューの変更があります。レビュー後に `review` コマンドで更新してください。

> ⚠️ **Suspect**: 関連する仕様や他のテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: [SPEC-020](../items/SPEC-020.md)

**タグ**: `@SPEC-017` `@SPEC-018` `@SPEC-019` `@SPEC-020`

**関連アイテム**: [SPEC-017](../items/SPEC-017.md) / [SPEC-018](../items/SPEC-018.md) / [SPEC-019](../items/SPEC-019.md) / [SPEC-020](../items/SPEC-020.md)

DoorstopのYAML impl_files カスタム属性とコードアノテーションを組み合わせて、
  仕様と実装ファイルの双方向トレーサビリティを実現する。

---
## Background

- **Given** Doorstopツリーが初期化されている
- **And** 以下のSPECアイテムが存在する:

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopツリーが初期化されている

```python
@given("Doorstopツリーが初期化されている")  # type: ignore
def given_6df87eb3(context):
    """Doorstopツリーが初期化されている

    Scenarios:
      - (trace.feature Background)
      - (impl_link.feature Background)
    """
    context.repo_root = context.temp_dir / "repo"
    context.repo_root.mkdir(parents=True, exist_ok=True)
    context.feature_dir = context.temp_dir / "features"
    context.feature_dir.mkdir(parents=True, exist_ok=True)
    # 遅延プロジェクト作成用の蓄積リスト
    context._pending_req_items = []
    context._pending_spec_items = []
    # scan / impl_files 読み取り用
    context.target_spec_id = None
    context.impl_files_result = None
    context.scan_result = {}
```

#### And 以下のSPECアイテムが存在する:

```python
@given("以下のSPECアイテムが存在する:")  # type: ignore
def given_14c0b615(context):
    """以下のSPECアイテムが存在する:

    Scenarios:
      - (impl_link.feature Background: ID / Header / impl_files)
      - (trace.feature Background: ID / Header / Status / Links)
    """
    headings = [h.strip() for h in context.table.headings]

    for row in context.table:
        uid = row["ID"].strip()
        header = row.get("Header", "").strip() if "Header" in headings else ""
        item_cfg: dict = {"uid": uid, "header": header, "testable": True}

        if "Status" in headings:
            status = row["Status"].strip()
            if status:
                item_cfg["status"] = status

        if "Links" in headings:
            links_str = row["Links"].strip()
            if links_str:
                item_cfg["links"] = [
                    l.strip() for l in links_str.split(",") if l.strip()
                ]

        if "impl_files" in headings:
            impl_str = row["impl_files"].strip()
            if impl_str:
                item_cfg["extra"] = {"impl_files": [impl_str]}

        context._pending_spec_items.append(item_cfg)

    # SPEC ステップが Background の最後（REQ は既に蓄積済み）なので、ここでプロジェクトを作成する
    documents = []
    req_items = getattr(context, "_pending_req_items", [])
    if req_items:
        documents.append(
            {
                "dir": "reqs",
                "prefix": "REQ",
                "parent": None,
                "items": req_items,
            }
        )
    documents.append(
        {
            "dir": "specs",
            "prefix": "SPEC",
            "parent": "REQ" if req_items else None,
            "items": context._pending_spec_items,
        }
    )
    create_doorstop_project_yaml(context.repo_root, documents)
```

</details>


---
## Scenario: impl_files にリスト形式でファイルパスを記述できる

**タグ**: `@SPEC-017`

- **Given** SPEC-018 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている
- **When** impl_files を読み取る
- **Then** ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-018 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている

```python
@given('SPEC-018 の impl_files に ["{param0}"] が設定されている')  # type: ignore
def given_5b35c4dd(context, param0):
    """SPEC-018 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている

    Scenarios:
      - impl_files にリスト形式でファイルパスを記述できる
    """
    _update_spec_yaml(context, "SPEC-018", "impl_files", [param0])
    context.target_spec_id = "SPEC-018"
```

#### When impl_files を読み取る

```python
@when("impl_files を読み取る")  # type: ignore
def when_1e9b41a9(context):
    """impl_files を読み取る

    Scenarios:
      - impl_files にリスト形式でファイルパスを記述できる
      - impl_files が未設定の場合はリンクなしとして扱われる
    """
    import doorstop

    orig = os.getcwd()
    os.chdir(context.repo_root)
    try:
        tree = doorstop.build()
        item = tree.find_item(str(context.target_spec_id))
        context.impl_files_result = get_ref_files(item)
    finally:
        os.chdir(orig)
```

#### Then ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

```python
@then('ファイルパスのリスト ["{param0}"] が得られること')  # type: ignore
def then_4c08825b(context, param0):
    """ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

    Scenarios:
      - impl_files にリスト形式でファイルパスを記述できる
    """
    assert context.impl_files_result == [param0], (
        f"期待: [{param0!r}]\n実際: {context.impl_files_result}"
    )
```

</details>


---
## Scenario: impl_files が未設定の場合はリンクなしとして扱われる

**タグ**: `@SPEC-017`

- **Given** SPEC-019 の impl_files が未設定である
- **When** impl_files を読み取る
- **Then** 空のリストが返ること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-019 の impl_files が未設定である

```python
@given("SPEC-019 の impl_files が未設定である")  # type: ignore
def given_60f3699e(context):
    """SPEC-019 の impl_files が未設定である

    Scenarios:
      - impl_files が未設定の場合はリンクなしとして扱われる
      - アノテーションがあって impl_files がない場合は警告を報告する
    """
    # Background では SPEC-019 に impl_files が設定されていないため、
    # YAML を更新して impl_files キーを削除する（念のため）
    _update_spec_yaml(context, "SPEC-019", "impl_files", None)
    context.target_spec_id = "SPEC-019"
```

#### When impl_files を読み取る

```python
@when("impl_files を読み取る")  # type: ignore
def when_1e9b41a9(context):
    """impl_files を読み取る

    Scenarios:
      - impl_files にリスト形式でファイルパスを記述できる
      - impl_files が未設定の場合はリンクなしとして扱われる
    """
    import doorstop

    orig = os.getcwd()
    os.chdir(context.repo_root)
    try:
        tree = doorstop.build()
        item = tree.find_item(str(context.target_spec_id))
        context.impl_files_result = get_ref_files(item)
    finally:
        os.chdir(orig)
```

#### Then 空のリストが返ること

```python
@then("空のリストが返ること")  # type: ignore
def then_3cd52b0f(context):
    """空のリストが返ること

    Scenarios:
      - impl_files が未設定の場合はリンクなしとして扱われる
    """
    assert context.impl_files_result == [], (
        f"期待: []\n実際: {context.impl_files_result}"
    )
```

</details>


---
## Scenario: アノテーションのスキャンで仕様IDとファイルの対応を抽出できる

**タグ**: `@SPEC-018`

- **Given** "src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている
- **When** impl-scanner でリポジトリをスキャンする
- **Then** "SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    """ "src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがあって impl_files がない場合は警告を報告する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _create_source_file(
        context, param0, f"{param1}\n# This is a generated test file.\n"
    )
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when("impl-scanner でリポジトリをスキャンする")  # type: ignore
def when_59b7b6ae(context):
    """impl-scanner でリポジトリをスキャンする

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがないファイルはエラーにならない
    """
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.repo_root)
```

#### Then "SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

```python
@then('"{param0}" に対して "{param1}" が紐づくこと')  # type: ignore
def then_6cd9ae6b(context, param0, param1):
    """ "SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
    """
    assert param0 in context.scan_result, (
        f'"{param0}" がスキャン結果にありません: {list(context.scan_result.keys())}'
    )
    # スキャン結果のパスは OS のパス区切り文字を使用する可能性があるため正規化して比較
    found_paths = {str(p).replace("\\", "/") for p in context.scan_result[param0]}
    expected = param1.replace("\\", "/")
    assert expected in found_paths, (
        f'"{param1}" が "{param0}" のスキャン結果にありません: {found_paths}'
    )
```

</details>


---
## Scenario: 1行に複数の仕様IDを記述できる

**タグ**: `@SPEC-018`

- **Given** "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-019, SPEC-020" が記述されている
- **When** impl-scanner でリポジトリをスキャンする
- **Then** "SPEC-019" に対して "src/spec_weaver/cli.py" が紐づくこと
- **And** "SPEC-020" に対して "src/spec_weaver/cli.py" が紐づくこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-019, SPEC-020" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    """ "src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがあって impl_files がない場合は警告を報告する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _create_source_file(
        context, param0, f"{param1}\n# This is a generated test file.\n"
    )
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when("impl-scanner でリポジトリをスキャンする")  # type: ignore
def when_59b7b6ae(context):
    """impl-scanner でリポジトリをスキャンする

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがないファイルはエラーにならない
    """
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.repo_root)
```

#### Then "SPEC-019" に対して "src/spec_weaver/cli.py" が紐づくこと

```python
@then('"{param0}" に対して "{param1}" が紐づくこと')  # type: ignore
def then_6cd9ae6b(context, param0, param1):
    """ "SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
    """
    assert param0 in context.scan_result, (
        f'"{param0}" がスキャン結果にありません: {list(context.scan_result.keys())}'
    )
    # スキャン結果のパスは OS のパス区切り文字を使用する可能性があるため正規化して比較
    found_paths = {str(p).replace("\\", "/") for p in context.scan_result[param0]}
    expected = param1.replace("\\", "/")
    assert expected in found_paths, (
        f'"{param1}" が "{param0}" のスキャン結果にありません: {found_paths}'
    )
```

#### And "SPEC-020" に対して "src/spec_weaver/cli.py" が紐づくこと

```python
@then('"{param0}" に対して "{param1}" が紐づくこと')  # type: ignore
def then_6cd9ae6b(context, param0, param1):
    """ "SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
    """
    assert param0 in context.scan_result, (
        f'"{param0}" がスキャン結果にありません: {list(context.scan_result.keys())}'
    )
    # スキャン結果のパスは OS のパス区切り文字を使用する可能性があるため正規化して比較
    found_paths = {str(p).replace("\\", "/") for p in context.scan_result[param0]}
    expected = param1.replace("\\", "/")
    assert expected in found_paths, (
        f'"{param1}" が "{param0}" のスキャン結果にありません: {found_paths}'
    )
```

</details>


---
## Scenario: --extensions オプションでスキャン対象を絞れる

**タグ**: `@SPEC-018`

- **Given** リポジトリに .py ファイルと .md ファイルが存在する
- **And** .md ファイルの行頭に "# implements: SPEC-018" が記述されている
- **When** --extensions py を指定して impl-scanner でスキャンする
- **Then** .md ファイルは結果に含まれないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given リポジトリに .py ファイルと .md ファイルが存在する

```python
@given("リポジトリに .py ファイルと .md ファイルが存在する")  # type: ignore
def given_6f18a295(context):
    """リポジトリに .py ファイルと .md ファイルが存在する

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    _create_source_file(
        context, "src/dummy.py", "# Python file without annotation\npass\n"
    )
```

#### And .md ファイルの行頭に "# implements: SPEC-018" が記述されている

```python
@given('.md ファイルの行頭に "{param0}" が記述されている')  # type: ignore
def given_d9c1b21a(context, param0):
    """.md ファイルの行頭に "# implements: SPEC-018" が記述されている

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    _create_source_file(context, "docs/annotation.md", f"{param0}\n# Markdown file\n")
    context.md_file_path = "docs/annotation.md"
```

#### When --extensions py を指定して impl-scanner でスキャンする

```python
@when("--extensions py を指定して impl-scanner でスキャンする")  # type: ignore
def when_d61ff5a2(context):
    """--extensions py を指定して impl-scanner でスキャンする

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.repo_root, extensions=["py"])
```

#### Then .md ファイルは結果に含まれないこと

```python
@then(".md ファイルは結果に含まれないこと")  # type: ignore
def then_1e4aee33(context):
    """.md ファイルは結果に含まれないこと

    Scenarios:
      - --extensions オプションでスキャン対象を絞れる
    """
    for spec_id, paths in context.scan_result.items():
        for path_str in paths:
            assert not str(path_str).endswith(".md"), (
                f".md ファイル {path_str!r} がスキャン結果に含まれています"
            )
```

</details>


---
## Scenario: アノテーションがないファイルはエラーにならない

**タグ**: `@SPEC-018`

- **Given** "src/spec_weaver/gherkin.py" にアノテーションが存在しない
- **When** impl-scanner でリポジトリをスキャンする
- **Then** エラーが発生しないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/gherkin.py" にアノテーションが存在しない

```python
@given('"{param0}" にアノテーションが存在しない')  # type: ignore
def given_8d04b283(context, param0):
    """ "src/spec_weaver/gherkin.py" にアノテーションが存在しない

    Scenarios:
      - アノテーションがないファイルはエラーにならない
    """
    _create_source_file(context, param0, "# No annotation here\npass\n")
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when("impl-scanner でリポジトリをスキャンする")  # type: ignore
def when_59b7b6ae(context):
    """impl-scanner でリポジトリをスキャンする

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがないファイルはエラーにならない
    """
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.repo_root)
```

#### Then エラーが発生しないこと

```python
@then("エラーが発生しないこと")  # type: ignore
def then_b705ab9f(context):
    """エラーが発生しないこと

    Scenarios:
      - アノテーションがないファイルはエラーにならない
    """
    # scan_result が None でなければスキャンは成功している
    assert context.scan_result is not None, "スキャン中にエラーが発生しました"
```

</details>


---
## Scenario: --check-impl オプションで存在しないファイルへの impl_files を検出する

**タグ**: `@SPEC-019`

- **Given** SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** 終了コードが 1 であること
- **And** "nonexistent.py" が存在しないファイルとして報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

```python
@given('SPEC-019 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_4cea3b9d(context, param0):
    """SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - --check-impl なしでは実装リンク検証は実行されない
    """
    _update_spec_yaml(context, "SPEC-019", "impl_files", [param0])
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    """ "spec-weaver audit --check-impl" を実行する

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - impl_files にあってアノテーションがない場合は警告を報告する
      - アノテーションがあって impl_files がない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _run_cmd(context, param0)
```

#### Then 終了コードが 1 であること

```python
@then("終了コードが 1 であること")  # type: ignore
def then_3783b41c(context):
    """終了コードが 1 であること

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
    """
    assert context.exit_code == 1, (
        f"終了コード {context.exit_code} (期待: 1)\n{context.output}"
    )
```

#### And "nonexistent.py" が存在しないファイルとして報告されること

```python
@then('"{param0}" が存在しないファイルとして報告されること')  # type: ignore
def then_7ef614ad(context, param0):
    """ "nonexistent.py" が存在しないファイルとして報告されること

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
    """
    assert param0 in context.output, (
        f'"{param0}" が存在しないファイルとして報告されていません:\n{context.output}'
    )
```

</details>


---
## Scenario: impl_files にあってアノテーションがない場合は警告を報告する

**タグ**: `@SPEC-019`

- **Given** SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている
- **And** "src/spec_weaver/cli.py" に SPEC-018 のアノテーションが存在しない
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** "SPEC-018 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている

```python
@given('SPEC-018 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    """SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - --show-impl なしでは実装ファイルは表示されない
    """
    _update_spec_yaml(context, "SPEC-018", "impl_files", [param0])
```

#### And "src/spec_weaver/cli.py" に SPEC-018 のアノテーションが存在しない

```python
@given('"{param0}" に SPEC-018 のアノテーションが存在しない')  # type: ignore
def given_d0ba98a0(context, param0):
    """ "src/spec_weaver/cli.py" に SPEC-018 のアノテーションが存在しない

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
    """
    # ファイルを作成するが、SPEC-018 アノテーションは含めない
    _create_source_file(
        context, param0, "# This file has no SPEC-018 annotation\npass\n"
    )
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    """ "spec-weaver audit --check-impl" を実行する

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - impl_files にあってアノテーションがない場合は警告を報告する
      - アノテーションがあって impl_files がない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _run_cmd(context, param0)
```

#### Then "SPEC-018 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

```python
@then('"{param0}" が impl_files のみ（アノテーションなし）として報告されること')  # type: ignore
def then_f76e2a8d(context, param0):
    """ "SPEC-018 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
    """
    # CLI 出力例: "   SPEC-018 → src/spec_weaver/cli.py"
    # param0: "SPEC-018 → src/spec_weaver/cli.py"
    parts = param0.split("→")
    spec_id = parts[0].strip()
    file_path = parts[1].strip() if len(parts) > 1 else ""
    assert spec_id in context.output, (
        f'"{spec_id}" が impl_files のみ（ref-only）セクションにありません:\n{context.output}'
    )
    assert file_path in context.output, (
        f'"{file_path}" が impl_files のみ（ref-only）セクションにありません:\n{context.output}'
    )
```

</details>


---
## Scenario: アノテーションがあって impl_files がない場合は警告を報告する

**タグ**: `@SPEC-019`

- **Given** "src/spec_weaver/gherkin.py" の行頭に "# implements: SPEC-019" が記述されている
- **And** SPEC-019 の impl_files が未設定である
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** "SPEC-019 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/gherkin.py" の行頭に "# implements: SPEC-019" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    """ "src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがあって impl_files がない場合は警告を報告する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _create_source_file(
        context, param0, f"{param1}\n# This is a generated test file.\n"
    )
```

#### And SPEC-019 の impl_files が未設定である

```python
@given("SPEC-019 の impl_files が未設定である")  # type: ignore
def given_60f3699e(context):
    """SPEC-019 の impl_files が未設定である

    Scenarios:
      - impl_files が未設定の場合はリンクなしとして扱われる
      - アノテーションがあって impl_files がない場合は警告を報告する
    """
    # Background では SPEC-019 に impl_files が設定されていないため、
    # YAML を更新して impl_files キーを削除する（念のため）
    _update_spec_yaml(context, "SPEC-019", "impl_files", None)
    context.target_spec_id = "SPEC-019"
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    """ "spec-weaver audit --check-impl" を実行する

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - impl_files にあってアノテーションがない場合は警告を報告する
      - アノテーションがあって impl_files がない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _run_cmd(context, param0)
```

#### Then "SPEC-019 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

```python
@then('"{param0}" がアノテーションのみ（impl_files なし）として報告されること')  # type: ignore
def then_7fa51a4f(context, param0):
    """ "SPEC-019 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

    Scenarios:
      - アノテーションがあって impl_files がない場合は警告を報告する
    """
    # CLI 出力例: "   SPEC-019 ← src/spec_weaver/gherkin.py"
    # param0: "SPEC-019 ← src/spec_weaver/gherkin.py"
    parts = param0.split("←")
    spec_id = parts[0].strip()
    file_path = parts[1].strip() if len(parts) > 1 else ""
    assert spec_id in context.output, (
        f'"{spec_id}" がアノテーションのみ（annotation-only）セクションにありません:\n{context.output}'
    )
    assert file_path in context.output, (
        f'"{file_path}" がアノテーションのみ（annotation-only）セクションにありません:\n{context.output}'
    )
```

</details>


---
## Scenario: --check-impl なしでは実装リンク検証は実行されない

**タグ**: `@SPEC-019`

- **Given** SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
- **When** 通常の "spec-weaver audit" を実行する（--check-impl なし）
- **Then** 実装ファイルリンクのセクションが出力されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

```python
@given('SPEC-019 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_4cea3b9d(context, param0):
    """SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - --check-impl なしでは実装リンク検証は実行されない
    """
    _update_spec_yaml(context, "SPEC-019", "impl_files", [param0])
```

#### When 通常の "spec-weaver audit" を実行する（--check-impl なし）

```python
@when('通常の "{param0}" を実行する（--check-impl なし）')  # type: ignore
def when_6a6c02d8(context, param0):
    """通常の "spec-weaver audit" を実行する（--check-impl なし）

    Scenarios:
      - --check-impl なしでは実装リンク検証は実行されない
    """
    _run_cmd(context, param0)
```

#### Then 実装ファイルリンクのセクションが出力されないこと

```python
@then("実装ファイルリンクのセクションが出力されないこと")  # type: ignore
def then_70e4e0dc(context):
    """実装ファイルリンクのセクションが出力されないこと

    Scenarios:
      - --check-impl なしでは実装リンク検証は実行されない
    """
    # --check-impl なしでは "🔗 実装ファイルリンクの検証" セクションが出力されない
    impl_section_keywords = ["実装ファイルリンクの検証", "🔗", "check-impl"]
    assert not any(kw in context.output for kw in impl_section_keywords), (
        f"実装ファイルリンクのセクションが誤って出力されています:\n{context.output}"
    )
```

</details>


---
## Scenario: --show-impl オプションで trace ツリーに実装ファイルを表示する

**タグ**: `@SPEC-020`

- **Given** SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
- **When** "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する
- **Then** 出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている

```python
@given('SPEC-018 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    """SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - --show-impl なしでは実装ファイルは表示されない
    """
    _update_spec_yaml(context, "SPEC-018", "impl_files", [param0])
```

#### When "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    """ "spec-weaver audit --check-impl" を実行する

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - impl_files にあってアノテーションがない場合は警告を報告する
      - アノテーションがあって impl_files がない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _run_cmd(context, param0)
```

#### Then 出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

```python
@then('出力ツリーに "{param0}" が含まれること')  # type: ignore
def then_2c56e82a(context, param0):
    """出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

    Scenarios:
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    assert param0 in context.output, (
        f'出力ツリーに "{param0}" が含まれていません:\n{context.output}'
    )
```

</details>


---
## Scenario: アノテーション由来のファイルも trace ツリーに表示される

**タグ**: `@SPEC-020`

- **Given** "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-018" が記述されている
- **And** SPEC-018 の impl_files が未設定である
- **When** "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する
- **Then** 出力ツリーに "src/spec_weaver/cli.py" が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-018" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    """ "src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている

    Scenarios:
      - アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
      - 1行に複数の仕様IDを記述できる
      - アノテーションがあって impl_files がない場合は警告を報告する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _create_source_file(
        context, param0, f"{param1}\n# This is a generated test file.\n"
    )
```

#### And SPEC-018 の impl_files が未設定である

```python
@given("SPEC-018 の impl_files が未設定である")  # type: ignore
def given_c11ed496(context):
    """SPEC-018 の impl_files が未設定である

    Scenarios:
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _update_spec_yaml(context, "SPEC-018", "impl_files", None)
```

#### When "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    """ "spec-weaver audit --check-impl" を実行する

    Scenarios:
      - --check-impl オプションで存在しないファイルへの impl_files を検出する
      - impl_files にあってアノテーションがない場合は警告を報告する
      - アノテーションがあって impl_files がない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    _run_cmd(context, param0)
```

#### Then 出力ツリーに "src/spec_weaver/cli.py" が含まれること

```python
@then('出力ツリーに "{param0}" が含まれること')  # type: ignore
def then_2c56e82a(context, param0):
    """出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

    Scenarios:
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - アノテーション由来のファイルも trace ツリーに表示される
    """
    assert param0 in context.output, (
        f'出力ツリーに "{param0}" が含まれていません:\n{context.output}'
    )
```

</details>


---
## Scenario: --show-impl なしでは実装ファイルは表示されない

**タグ**: `@SPEC-020`

- **Given** SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
- **When** "spec-weaver trace SPEC-018 -f ./specification/features" を実行する（--show-impl なし）
- **Then** 出力ツリーに "impl_scanner.py" が含まれないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている

```python
@given('SPEC-018 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    """SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている

    Scenarios:
      - impl_files にあってアノテーションがない場合は警告を報告する
      - --show-impl オプションで trace ツリーに実装ファイルを表示する
      - --show-impl なしでは実装ファイルは表示されない
    """
    _update_spec_yaml(context, "SPEC-018", "impl_files", [param0])
```

#### When "spec-weaver trace SPEC-018 -f ./specification/features" を実行する（--show-impl なし）

```python
@when('"{param0}" を実行する（--show-impl なし）')  # type: ignore
def when_dfb07a47(context, param0):
    """ "spec-weaver trace SPEC-018 -f ./specification/features" を実行する（--show-impl なし）

    Scenarios:
      - --show-impl なしでは実装ファイルは表示されない
    """
    _run_cmd(context, param0)
```

#### Then 出力ツリーに "impl_scanner.py" が含まれないこと

```python
@then('出力ツリーに "{param0}" が含まれないこと')  # type: ignore
def then_35df9926(context, param0):
    """出力ツリーに "impl_scanner.py" が含まれないこと

    Scenarios:
      - --show-impl なしでは実装ファイルは表示されない
    """
    assert param0 not in context.output, (
        f'出力ツリーに "{param0}" が含まれています（含まれないべき）:\n{context.output}'
    )
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
@SPEC-017 @SPEC-018 @SPEC-019 @SPEC-020
Feature: 仕様アイテムと実装ファイルのリンク管理
  DoorstopのYAML impl_files カスタム属性とコードアノテーションを組み合わせて、
  仕様と実装ファイルの双方向トレーサビリティを実現する。

  Background:
    Given Doorstopツリーが初期化されている
    And 以下のSPECアイテムが存在する:
      | ID       | Header             | impl_files                       |
      | SPEC-018 | アノテーションスキャン | src/spec_weaver/impl_scanner.py |
      | SPEC-019 | audit拡張          |                                  |

  # ---- SPEC-017: impl_files カスタム属性 ----

  @SPEC-017
  Scenario: impl_files にリスト形式でファイルパスを記述できる
    Given SPEC-018 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている
    When impl_files を読み取る
    Then ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

  @SPEC-017
  Scenario: impl_files が未設定の場合はリンクなしとして扱われる
    Given SPEC-019 の impl_files が未設定である
    When impl_files を読み取る
    Then 空のリストが返ること

  # ---- SPEC-018: アノテーションスキャン ----

  @SPEC-018
  Scenario: アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
    Given "src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている
    When impl-scanner でリポジトリをスキャンする
    Then "SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

  @SPEC-018
  Scenario: 1行に複数の仕様IDを記述できる
    Given "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-019, SPEC-020" が記述されている
    When impl-scanner でリポジトリをスキャンする
    Then "SPEC-019" に対して "src/spec_weaver/cli.py" が紐づくこと
    And  "SPEC-020" に対して "src/spec_weaver/cli.py" が紐づくこと

  @SPEC-018
  Scenario: --extensions オプションでスキャン対象を絞れる
    Given リポジトリに .py ファイルと .md ファイルが存在する
    And .md ファイルの行頭に "# implements: SPEC-018" が記述されている
    When --extensions py を指定して impl-scanner でスキャンする
    Then .md ファイルは結果に含まれないこと

  @SPEC-018
  Scenario: アノテーションがないファイルはエラーにならない
    Given "src/spec_weaver/gherkin.py" にアノテーションが存在しない
    When impl-scanner でリポジトリをスキャンする
    Then エラーが発生しないこと

  # ---- SPEC-019: audit 拡張 ----

  @SPEC-019
  Scenario: --check-impl オプションで存在しないファイルへの impl_files を検出する
    Given SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
    When "spec-weaver audit --check-impl" を実行する
    Then 終了コードが 1 であること
    And  "nonexistent.py" が存在しないファイルとして報告されること

  @SPEC-019
  Scenario: impl_files にあってアノテーションがない場合は警告を報告する
    Given SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている
    And "src/spec_weaver/cli.py" に SPEC-018 のアノテーションが存在しない
    When "spec-weaver audit --check-impl" を実行する
    Then "SPEC-018 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

  @SPEC-019
  Scenario: アノテーションがあって impl_files がない場合は警告を報告する
    Given "src/spec_weaver/gherkin.py" の行頭に "# implements: SPEC-019" が記述されている
    And SPEC-019 の impl_files が未設定である
    When "spec-weaver audit --check-impl" を実行する
    Then "SPEC-019 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

  @SPEC-019
  Scenario: --check-impl なしでは実装リンク検証は実行されない
    Given SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
    When 通常の "spec-weaver audit" を実行する（--check-impl なし）
    Then 実装ファイルリンクのセクションが出力されないこと

  # ---- SPEC-020: trace 拡張 ----

  @SPEC-020
  Scenario: --show-impl オプションで trace ツリーに実装ファイルを表示する
    Given SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
    When "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する
    Then 出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること

  @SPEC-020
  Scenario: アノテーション由来のファイルも trace ツリーに表示される
    Given "src/spec_weaver/cli.py" の行頭に "# implements: SPEC-018" が記述されている
    And SPEC-018 の impl_files が未設定である
    When "spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する
    Then 出力ツリーに "src/spec_weaver/cli.py" が含まれること

  @SPEC-020
  Scenario: --show-impl なしでは実装ファイルは表示されない
    Given SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
    When "spec-weaver trace SPEC-018 -f ./specification/features" を実行する（--show-impl なし）
    Then 出力ツリーに "impl_scanner.py" が含まれないこと

```
</details>