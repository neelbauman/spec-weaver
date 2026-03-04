# Feature: 仕様アイテムと実装ファイルのリンク管理

**タグ**: `@TRC-002` `@TRC-003` `@QA-003` `@TRC-004`

**関連アイテム**: [QA-003](../items/QA-003.md) / [TRC-002](../items/TRC-002.md) / [TRC-003](../items/TRC-003.md) / [TRC-004](../items/TRC-004.md)

DoorstopのYAML impl_files カスタム属性とコードアノテーションを組み合わせて、
  仕様と実装ファイルの双方向トレーサビリティを実現する。

---
## Background

- **Given** Doorstopツリーが初期化されている
- **And** 以下のSPECアイテムが存在する:

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopツリーが初期化されている

```python
@given('Doorstopツリーが初期化されている')  # type: ignore
def given_6df87eb3(context):
    """Doorstopツリーが初期化されている

    Scenarios:
      - 
    """
    raise NotImplementedError('STEP: Doorstopツリーが初期化されている')
```

#### And 以下のSPECアイテムが存在する:

```python
@given('以下のSPECアイテムが存在する:')  # type: ignore
def given_14c0b615(context):
    """以下のSPECアイテムが存在する:

    Scenarios:
      - 
    """
    raise NotImplementedError('STEP: 以下のSPECアイテムが存在する:')
```

</details>


---
## Scenario: impl_files にリスト形式でファイルパスを記述できる {: #line-21 }

**タグ**: `@TRC-002`

- **Given** TRC-003 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている
- **When** impl_files を読み取る
- **Then** ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given TRC-003 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている

```python
@given('TRC-003 の impl_files に ["{param0}"] が設定されている')  # type: ignore
def given_5b35c4dd(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "TRC-003", extra={"impl_files": [param0]})
    context.target_spec = "TRC-003"
```

#### When impl_files を読み取る

```python
@when('impl_files を読み取る')  # type: ignore
def when_1e9b41a9(context):
    import doorstop

    from spec_weaver.adapters.impl_scanner import get_ref_files
    tree = doorstop.build(cwd=str(context.temp_dir))
    item = tree.find_item(context.target_spec)
    context.actual_files = get_ref_files(item)
```

#### Then ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

```python
@then('ファイルパスのリスト ["{param0}"] が得られること')  # type: ignore
def then_4c08825b(context, param0):
    assert context.actual_files == [param0], f"Expected [{param0}], got {context.actual_files}"
```

</details>


---
## Scenario: impl_files が文字列形式で記述されている場合は単一要素リストとして解釈される {: #line-27 }

**タグ**: `@TRC-002`

- **Given** TRC-003 の impl_files に "src/spec_weaver/cli.py" が文字列として設定されている
- **When** impl_files を読み取る
- **Then** ファイルパスのリスト ["src/spec_weaver/cli.py"] が得られること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given TRC-003 の impl_files に "src/spec_weaver/cli.py" が文字列として設定されている

```python
@given('TRC-003 の impl_files に "{param0}" が文字列として設定されている')  # type: ignore
def given_254bc1f7(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "TRC-003", extra={"impl_files": param0})
    context.target_spec = "TRC-003"
```

#### When impl_files を読み取る

```python
@when('impl_files を読み取る')  # type: ignore
def when_1e9b41a9(context):
    import doorstop

    from spec_weaver.adapters.impl_scanner import get_ref_files
    tree = doorstop.build(cwd=str(context.temp_dir))
    item = tree.find_item(context.target_spec)
    context.actual_files = get_ref_files(item)
```

#### Then ファイルパスのリスト ["src/spec_weaver/cli.py"] が得られること

```python
@then('ファイルパスのリスト ["{param0}"] が得られること')  # type: ignore
def then_4c08825b(context, param0):
    assert context.actual_files == [param0], f"Expected [{param0}], got {context.actual_files}"
```

</details>


---
## Scenario: impl_files が未設定の場合はリンクなしとして扱われる {: #line-33 }

**タグ**: `@TRC-002`

- **Given** QA-003 の impl_files が未設定である
- **When** impl_files を読み取る
- **Then** 空のリストが返ること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given QA-003 の impl_files が未設定である

```python
@given('QA-003 の impl_files が未設定である')  # type: ignore
def given_60f3699e(context):
    write_doorstop_yaml(context.temp_dir / "specs", "QA-003")
    context.target_spec = "QA-003"
```

#### When impl_files を読み取る

```python
@when('impl_files を読み取る')  # type: ignore
def when_1e9b41a9(context):
    import doorstop

    from spec_weaver.adapters.impl_scanner import get_ref_files
    tree = doorstop.build(cwd=str(context.temp_dir))
    item = tree.find_item(context.target_spec)
    context.actual_files = get_ref_files(item)
```

#### Then 空のリストが返ること

```python
@then('空のリストが返ること')  # type: ignore
def then_3cd52b0f(context):
    assert context.actual_files == [], f"Expected [], got {context.actual_files}"
```

</details>


---
## Scenario: アノテーションのスキャンで仕様IDとファイルの対応を抽出できる {: #line-41 }

**タグ**: `@TRC-003`

- **Given** "src/spec_weaver/impl_scanner.py" の行頭に "# implements: TRC-003" が記述されている
- **When** impl-scanner でリポジトリをスキャンする
- **Then** "TRC-003" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/impl_scanner.py" の行頭に "# implements: TRC-003" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{param1}\n")
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when('impl-scanner でリポジトリをスキャンする')  # type: ignore
def when_59b7b6ae(context):
    from spec_weaver.adapters.impl_scanner import ImplScanner
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.temp_dir)
```

#### Then "TRC-003" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

```python
@then('"{param0}" に対して "{param1}" が紐づくこと')  # type: ignore
def then_6cd9ae6b(context, param0, param1):
    assert param0 in context.scan_result, f"{param0} not found in scan result"
    assert param1 in context.scan_result[param0], f"{param1} not linked to {param0}"
```

</details>


---
## Scenario: 1行に複数の仕様IDを記述できる {: #line-47 }

**タグ**: `@TRC-003`

- **Given** "src/spec_weaver/cli.py" の行頭に "# implements: QA-003, TRC-004" が記述されている
- **When** impl-scanner でリポジトリをスキャンする
- **Then** "QA-003" に対して "src/spec_weaver/cli.py" が紐づくこと
- **And** "TRC-004" に対して "src/spec_weaver/cli.py" が紐づくこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/cli.py" の行頭に "# implements: QA-003, TRC-004" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{param1}\n")
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when('impl-scanner でリポジトリをスキャンする')  # type: ignore
def when_59b7b6ae(context):
    from spec_weaver.adapters.impl_scanner import ImplScanner
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.temp_dir)
```

#### Then "QA-003" に対して "src/spec_weaver/cli.py" が紐づくこと

```python
@then('"{param0}" に対して "{param1}" が紐づくこと')  # type: ignore
def then_6cd9ae6b(context, param0, param1):
    assert param0 in context.scan_result, f"{param0} not found in scan result"
    assert param1 in context.scan_result[param0], f"{param1} not linked to {param0}"
```

#### And "TRC-004" に対して "src/spec_weaver/cli.py" が紐づくこと

```python
@then('"{param0}" に対して "{param1}" が紐づくこと')  # type: ignore
def then_6cd9ae6b(context, param0, param1):
    assert param0 in context.scan_result, f"{param0} not found in scan result"
    assert param1 in context.scan_result[param0], f"{param1} not linked to {param0}"
```

</details>


---
## Scenario: --extensions オプションでスキャン対象を絞れる {: #line-54 }

**タグ**: `@TRC-003`

- **Given** リポジトリに .py ファイルと .md ファイルが存在する
- **And** .md ファイルの行頭に "# implements: TRC-003" が記述されている
- **When** --extensions py を指定して impl-scanner でスキャンする
- **Then** .md ファイルは結果に含まれないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given リポジトリに .py ファイルと .md ファイルが存在する

```python
@given('リポジトリに .py ファイルと .md ファイルが存在する')  # type: ignore
def given_6f18a295(context):
    py_path = context.temp_dir / "test.py"
    py_path.write_text("# implements: TRC-003\n")
    context.py_path = "test.py"
    md_path = context.temp_dir / "test.md"
    md_path.write_text("# implements: TRC-003\n")
    context.md_path = "test.md"
```

#### And .md ファイルの行頭に "# implements: TRC-003" が記述されている

```python
@given('.md ファイルの行頭に "{param0}" が記述されている')  # type: ignore
def given_d9c1b21a(context, param0):
    pass # Done in the previous step
```

#### When --extensions py を指定して impl-scanner でスキャンする

```python
@when('--extensions py を指定して impl-scanner でスキャンする')  # type: ignore
def when_d61ff5a2(context):
    from spec_weaver.adapters.impl_scanner import ImplScanner
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.temp_dir, extensions=["py"])
```

#### Then .md ファイルは結果に含まれないこと

```python
@then('.md ファイルは結果に含まれないこと')  # type: ignore
def then_1e4aee33(context):
    for files in context.scan_result.values():
        assert not any(f.endswith(".md") for f in files)
```

</details>


---
## Scenario: アノテーションがないファイルはエラーにならない {: #line-61 }

**タグ**: `@TRC-003`

- **Given** "src/spec_weaver/gherkin.py" にアノテーションが存在しない
- **When** impl-scanner でリポジトリをスキャンする
- **Then** エラーが発生しないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/gherkin.py" にアノテーションが存在しない

```python
@given('"{param0}" にアノテーションが存在しない')  # type: ignore
def given_8d04b283(context, param0):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("def no_annotation(): pass\n")
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when('impl-scanner でリポジトリをスキャンする')  # type: ignore
def when_59b7b6ae(context):
    from spec_weaver.adapters.impl_scanner import ImplScanner
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.temp_dir)
```

#### Then エラーが発生しないこと

```python
@then('エラーが発生しないこと')  # type: ignore
def then_b705ab9f(context):
    assert True
```

</details>


---
## Scenario: .gitignore 相当のパターンは除外対象となる {: #line-67 }

**タグ**: `@TRC-003`

- **Given** ".git/ignored_file.py" の行頭に "# implements: TRC-003" が記述されている
- **When** impl-scanner でリポジトリをスキャンする
- **Then** ".git/ignored_file.py" は結果に含まれないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given ".git/ignored_file.py" の行頭に "# implements: TRC-003" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{param1}\n")
```

#### When impl-scanner でリポジトリをスキャンする

```python
@when('impl-scanner でリポジトリをスキャンする')  # type: ignore
def when_59b7b6ae(context):
    from spec_weaver.adapters.impl_scanner import ImplScanner
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.temp_dir)
```

#### Then ".git/ignored_file.py" は結果に含まれないこと

```python
@then('"{param0}" は結果に含まれないこと')  # type: ignore
def then_9ee20369(context, param0):
    for files in context.scan_result.values():
        assert param0 not in files
```

</details>


---
## Scenario: --check-impl オプションで存在しないファイルへの impl_files を検出する {: #line-75 }

**タグ**: `@QA-003`

- **Given** QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** 終了コードが 1 であること
- **And** "nonexistent.py" が存在しないファイルとして報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

```python
@given('QA-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_4cea3b9d(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "QA-003", extra={"impl_files": param0})
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    import shlex
    args = shlex.split(param0)
    if args[0] == "spec-weaver":
        args = args[1:]
    if args[0] == "audit" and len(args) == 2:  # audit --check-impl
        features_dir = context.temp_dir / "specification" / "features"
        features_dir.mkdir(parents=True, exist_ok=True)
        args.append(str(features_dir))
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)

    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 終了コードが 1 であること

```python
@then('終了コードが 1 であること')  # type: ignore
def then_3783b41c(context):
    assert context.result.returncode == 1, f"Expected 1, got {context.result.returncode}\n{context.result.stderr}"
```

#### And "nonexistent.py" が存在しないファイルとして報告されること

```python
@then('"{param0}" が存在しないファイルとして報告されること')  # type: ignore
def then_7ef614ad(context, param0):
    assert param0 in context.result.stdout or param0 in context.result.stderr
```

</details>


---
## Scenario: impl_files にあってアノテーションがない場合は警告を報告する {: #line-82 }

**タグ**: `@QA-003`

- **Given** TRC-003 の impl_files に "src/spec_weaver/cli.py" が設定されている
- **And** "src/spec_weaver/cli.py" に TRC-003 のアノテーションが存在しない
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** "TRC-003 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given TRC-003 の impl_files に "src/spec_weaver/cli.py" が設定されている

```python
@given('TRC-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "TRC-003", extra={"impl_files": param0})
```

#### And "src/spec_weaver/cli.py" に TRC-003 のアノテーションが存在しない

```python
@given('"{param0}" に TRC-003 のアノテーションが存在しない')  # type: ignore
def given_d0ba98a0(context, param0):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("def no_annotation(): pass\n")
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    import shlex
    args = shlex.split(param0)
    if args[0] == "spec-weaver":
        args = args[1:]
    if args[0] == "audit" and len(args) == 2:  # audit --check-impl
        features_dir = context.temp_dir / "specification" / "features"
        features_dir.mkdir(parents=True, exist_ok=True)
        args.append(str(features_dir))
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)

    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then "TRC-003 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

```python
@then('"{param0}" が impl_files のみ（アノテーションなし）として報告されること')  # type: ignore
def then_f76e2a8d(context, param0):
    out = context.result.stdout + context.result.stderr
    assert param0 in out, f"Expected '{param0}' in output. Actual output:\n{out}"
```

</details>


---
## Scenario: アノテーションがあって impl_files がない場合は警告を報告する {: #line-89 }

**タグ**: `@QA-003`

- **Given** "src/spec_weaver/gherkin.py" の行頭に "# implements: QA-003" が記述されている
- **And** QA-003 の impl_files が未設定である
- **When** "spec-weaver audit --check-impl" を実行する
- **Then** "QA-003 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/gherkin.py" の行頭に "# implements: QA-003" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{param1}\n")
```

#### And QA-003 の impl_files が未設定である

```python
@given('QA-003 の impl_files が未設定である')  # type: ignore
def given_60f3699e(context):
    write_doorstop_yaml(context.temp_dir / "specs", "QA-003")
    context.target_spec = "QA-003"
```

#### When "spec-weaver audit --check-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    import shlex
    args = shlex.split(param0)
    if args[0] == "spec-weaver":
        args = args[1:]
    if args[0] == "audit" and len(args) == 2:  # audit --check-impl
        features_dir = context.temp_dir / "specification" / "features"
        features_dir.mkdir(parents=True, exist_ok=True)
        args.append(str(features_dir))
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)

    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then "QA-003 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

```python
@then('"{param0}" がアノテーションのみ（impl_files なし）として報告されること')  # type: ignore
def then_7fa51a4f(context, param0):
    out = context.result.stdout + context.result.stderr
    assert param0 in out, f"Expected '{param0}' in output. Actual output:\n{out}"
```

</details>


---
## Scenario: --check-impl なしでは実装リンク検証は実行されない {: #line-96 }

**タグ**: `@QA-003`

- **Given** QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
- **When** 通常の "spec-weaver audit" を実行する（--check-impl なし）
- **Then** 実装ファイルリンクのセクションが出力されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

```python
@given('QA-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_4cea3b9d(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "QA-003", extra={"impl_files": param0})
```

#### When 通常の "spec-weaver audit" を実行する（--check-impl なし）

```python
@when('通常の "{param0}" を実行する（--check-impl なし）')  # type: ignore
def when_6a6c02d8(context, param0):
    import shlex
    args = shlex.split(param0)
    if args[0] == "spec-weaver":
        args = args[1:]
    
    if args[0] == "audit":
        features_dir = context.temp_dir / "specification" / "features"
        features_dir.mkdir(parents=True, exist_ok=True)
        args.append(str(features_dir))
        
    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 実装ファイルリンクのセクションが出力されないこと

```python
@then('実装ファイルリンクのセクションが出力されないこと')  # type: ignore
def then_70e4e0dc(context):
    out = context.result.stdout + context.result.stderr
    assert "Broken impl_files refs" not in out and "Annotation only" not in out
```

</details>


---
## Scenario: --show-impl オプションで trace ツリーに実装ファイルを表示する {: #line-104 }

**タグ**: `@TRC-004`

- **Given** TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
- **And** "src/spec_weaver/impl_scanner.py" が存在する
- **When** "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
- **Then** 出力ツリーに "📁 src/spec_weaver/impl_scanner.py" が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている

```python
@given('TRC-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "TRC-003", extra={"impl_files": param0})
```

#### And "src/spec_weaver/impl_scanner.py" が存在する

```python
@given('"{param0}" が存在する')  # type: ignore
def given_file_exists(context, param0):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("")
```

#### When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    import shlex
    args = shlex.split(param0)
    if args[0] == "spec-weaver":
        args = args[1:]
    if args[0] == "audit" and len(args) == 2:  # audit --check-impl
        features_dir = context.temp_dir / "specification" / "features"
        features_dir.mkdir(parents=True, exist_ok=True)
        args.append(str(features_dir))
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)

    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 出力ツリーに "📁 src/spec_weaver/impl_scanner.py" が含まれること

```python
@then('出力ツリーに "{param0}" が含まれること')  # type: ignore
def then_2c56e82a(context, param0):
    out = context.result.stdout + context.result.stderr
    assert param0 in out, f"Expected '{param0}' in output. Actual output:\n{out}"
```

</details>


---
## Scenario: アノテーション由来のファイルも trace ツリーに表示される {: #line-111 }

**タグ**: `@TRC-004`

- **Given** "src/spec_weaver/cli.py" の行頭に "# implements: TRC-003" が記述されている
- **And** TRC-003 の impl_files が未設定である
- **When** "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
- **Then** 出力ツリーに "📝 src/spec_weaver/cli.py" が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given "src/spec_weaver/cli.py" の行頭に "# implements: TRC-003" が記述されている

```python
@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{param1}\n")
```

#### And TRC-003 の impl_files が未設定である

```python
@given('TRC-003 の impl_files が未設定である')  # type: ignore
def given_c11ed496(context):
    write_doorstop_yaml(context.temp_dir / "specs", "TRC-003")
```

#### When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    import shlex
    args = shlex.split(param0)
    if args[0] == "spec-weaver":
        args = args[1:]
    if args[0] == "audit" and len(args) == 2:  # audit --check-impl
        features_dir = context.temp_dir / "specification" / "features"
        features_dir.mkdir(parents=True, exist_ok=True)
        args.append(str(features_dir))
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)

    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 出力ツリーに "📝 src/spec_weaver/cli.py" が含まれること

```python
@then('出力ツリーに "{param0}" が含まれること')  # type: ignore
def then_2c56e82a(context, param0):
    out = context.result.stdout + context.result.stderr
    assert param0 in out, f"Expected '{param0}' in output. Actual output:\n{out}"
```

</details>


---
## Scenario: 存在しないファイルはエラーアイコンとともに表示される {: #line-118 }

**タグ**: `@TRC-004`

- **Given** TRC-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
- **When** "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
- **Then** 出力ツリーに "❌ src/spec_weaver/nonexistent.py (not found)" が含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given TRC-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている

```python
@given('TRC-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "TRC-003", extra={"impl_files": param0})
```

#### When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する

```python
@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    import shlex
    args = shlex.split(param0)
    if args[0] == "spec-weaver":
        args = args[1:]
    if args[0] == "audit" and len(args) == 2:  # audit --check-impl
        features_dir = context.temp_dir / "specification" / "features"
        features_dir.mkdir(parents=True, exist_ok=True)
        args.append(str(features_dir))
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)

    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 出力ツリーに "❌ src/spec_weaver/nonexistent.py (not found)" が含まれること

```python
@then('出力ツリーに "{param0}" が含まれること')  # type: ignore
def then_2c56e82a(context, param0):
    out = context.result.stdout + context.result.stderr
    assert param0 in out, f"Expected '{param0}' in output. Actual output:\n{out}"
```

</details>


---
## Scenario: --show-impl なしでは実装ファイルは表示されない {: #line-124 }

**タグ**: `@TRC-004`

- **Given** TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
- **When** "spec-weaver trace TRC-003 -f ./specification/features" を実行する（--show-impl なし）
- **Then** 出力ツリーに "impl_scanner.py" が含まれないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている

```python
@given('TRC-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "TRC-003", extra={"impl_files": param0})
```

#### When "spec-weaver trace TRC-003 -f ./specification/features" を実行する（--show-impl なし）

```python
@when('"{param0}" を実行する（--show-impl なし）')  # type: ignore
def when_dfb07a47(context, param0):
    import shlex
    args = shlex.split(param0)
    if args[0] == "spec-weaver":
        args = args[1:]
    
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
            
    context.result = run_spec_weaver(args, cwd=context.temp_dir)
```

#### Then 出力ツリーに "impl_scanner.py" が含まれないこと

```python
@then('出力ツリーに "{param0}" が含まれないこと')  # type: ignore
def then_35df9926(context, param0):
    out = context.result.stdout + context.result.stderr
    assert param0 not in out, f"Expected {param0} not to be in output"
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: 72d891bd698202f2c4859359036d7db09d23a01dd78d84d7552bd4e87d60c401
# spec-weaver-fingerprint-QA-003: R7lU5c_GYfAMywWH7ga7C5bNWLi0BcEk_ct5FCCzLOg=
# spec-weaver-fingerprint-TRC-002: A_AtKMCuxp1mjop9_YlIvCzI6ZPuUN_Vmxm3-69zK6A=
# spec-weaver-fingerprint-TRC-003: HejBnkVVAXr50mezShqlLJuFqDQgnm2Ll2xq1IrX7wY=
# spec-weaver-fingerprint-TRC-004: taSaPJAOYmNABY3Fq9QzpfuL400jN9dj2MpQSufRkT8=
@TRC-002 @TRC-003 @QA-003 @TRC-004
Feature: 仕様アイテムと実装ファイルのリンク管理
  DoorstopのYAML impl_files カスタム属性とコードアノテーションを組み合わせて、
  仕様と実装ファイルの双方向トレーサビリティを実現する。

  Background:
    Given Doorstopツリーが初期化されている
    And 以下のSPECアイテムが存在する:
      | ID       | Header             | impl_files                       |
      | TRC-003 | アノテーションスキャン | src/spec_weaver/impl_scanner.py |
      | QA-003 | audit拡張          |                                  |

  # ---- TRC-002: impl_files カスタム属性 ----

  @TRC-002
  Scenario: impl_files にリスト形式でファイルパスを記述できる
    Given TRC-003 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている
    When impl_files を読み取る
    Then ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること

  @TRC-002
  Scenario: impl_files が文字列形式で記述されている場合は単一要素リストとして解釈される
    Given TRC-003 の impl_files に "src/spec_weaver/cli.py" が文字列として設定されている
    When impl_files を読み取る
    Then ファイルパスのリスト ["src/spec_weaver/cli.py"] が得られること

  @TRC-002
  Scenario: impl_files が未設定の場合はリンクなしとして扱われる
    Given QA-003 の impl_files が未設定である
    When impl_files を読み取る
    Then 空のリストが返ること

  # ---- TRC-003: アノテーションスキャン ----

  @TRC-003
  Scenario: アノテーションのスキャンで仕様IDとファイルの対応を抽出できる
    Given "src/spec_weaver/impl_scanner.py" の行頭に "# implements: TRC-003" が記述されている
    When impl-scanner でリポジトリをスキャンする
    Then "TRC-003" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと

  @TRC-003
  Scenario: 1行に複数の仕様IDを記述できる
    Given "src/spec_weaver/cli.py" の行頭に "# implements: QA-003, TRC-004" が記述されている
    When impl-scanner でリポジトリをスキャンする
    Then "QA-003" に対して "src/spec_weaver/cli.py" が紐づくこと
    And  "TRC-004" に対して "src/spec_weaver/cli.py" が紐づくこと

  @TRC-003
  Scenario: --extensions オプションでスキャン対象を絞れる
    Given リポジトリに .py ファイルと .md ファイルが存在する
    And .md ファイルの行頭に "# implements: TRC-003" が記述されている
    When --extensions py を指定して impl-scanner でスキャンする
    Then .md ファイルは結果に含まれないこと

  @TRC-003
  Scenario: アノテーションがないファイルはエラーにならない
    Given "src/spec_weaver/gherkin.py" にアノテーションが存在しない
    When impl-scanner でリポジトリをスキャンする
    Then エラーが発生しないこと

  @TRC-003
  Scenario: .gitignore 相当のパターンは除外対象となる
    Given ".git/ignored_file.py" の行頭に "# implements: TRC-003" が記述されている
    When impl-scanner でリポジトリをスキャンする
    Then ".git/ignored_file.py" は結果に含まれないこと

  # ---- QA-003: audit 拡張 ----

  @QA-003
  Scenario: --check-impl オプションで存在しないファイルへの impl_files を検出する
    Given QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
    When "spec-weaver audit --check-impl" を実行する
    Then 終了コードが 1 であること
    And  "nonexistent.py" が存在しないファイルとして報告されること

  @QA-003
  Scenario: impl_files にあってアノテーションがない場合は警告を報告する
    Given TRC-003 の impl_files に "src/spec_weaver/cli.py" が設定されている
    And "src/spec_weaver/cli.py" に TRC-003 のアノテーションが存在しない
    When "spec-weaver audit --check-impl" を実行する
    Then "TRC-003 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること

  @QA-003
  Scenario: アノテーションがあって impl_files がない場合は警告を報告する
    Given "src/spec_weaver/gherkin.py" の行頭に "# implements: QA-003" が記述されている
    And QA-003 の impl_files が未設定である
    When "spec-weaver audit --check-impl" を実行する
    Then "QA-003 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること

  @QA-003
  Scenario: --check-impl なしでは実装リンク検証は実行されない
    Given QA-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
    When 通常の "spec-weaver audit" を実行する（--check-impl なし）
    Then 実装ファイルリンクのセクションが出力されないこと

  # ---- TRC-004: trace 拡張 ----

  @TRC-004
  Scenario: --show-impl オプションで trace ツリーに実装ファイルを表示する
    Given TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
    And "src/spec_weaver/impl_scanner.py" が存在する
    When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
    Then 出力ツリーに "📁 src/spec_weaver/impl_scanner.py" が含まれること

  @TRC-004
  Scenario: アノテーション由来のファイルも trace ツリーに表示される
    Given "src/spec_weaver/cli.py" の行頭に "# implements: TRC-003" が記述されている
    And TRC-003 の impl_files が未設定である
    When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
    Then 出力ツリーに "📝 src/spec_weaver/cli.py" が含まれること

  @TRC-004
  Scenario: 存在しないファイルはエラーアイコンとともに表示される
    Given TRC-003 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている
    When "spec-weaver trace TRC-003 -f ./specification/features --show-impl" を実行する
    Then 出力ツリーに "❌ src/spec_weaver/nonexistent.py (not found)" が含まれること

  @TRC-004
  Scenario: --show-impl なしでは実装ファイルは表示されない
    Given TRC-003 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている
    When "spec-weaver trace TRC-003 -f ./specification/features" を実行する（--show-impl なし）
    Then 出力ツリーに "impl_scanner.py" が含まれないこと

```
</details>