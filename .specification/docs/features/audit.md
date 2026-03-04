# Feature: audit コマンド

**関連アイテム**: [QA-001](../items/QA-001.md) / [QA-006](../items/QA-006.md)

仕様とテストの乖離を静的に検知し、CI/CD品質ゲートとして機能する。

---
## Scenario: 完全一致で、監査が成功する {: #line-8 }

- **Given** すべてのtestable仕様に対応するGherkinテストが存在する
- **When** audit コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** 成功メッセージが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given すべてのtestable仕様に対応するGherkinテストが存在する

```python
@given('すべてのtestable仕様に対応するGherkinテストが存在する')  # type: ignore
def given_a7b8516a(context):
    create_doorstop_project_api(
        context.temp_dir,
        req_items=[{"status": "implemented"}],
        spec_items=[{"status": "implemented", "links": ["REQ-001"]}],
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, "@SPEC-001\nFeature: Test\n  Scenario: Test\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr
```

#### Then 終了コード 0 が返ること

```python
@then('終了コード 0 が返ること')  # type: ignore
def then_4f25c571(context):
    """終了コード 0 が返ること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
      - status 未設定のアイテムは "-" と表示される
      - --filter で特定ステータスに絞り込める
      - --filter に一致するアイテムが存在しない場合に通知される
      - レビューステータスと最終更新日が表示される
    """
    assert getattr(context, 'exit_code', 0) == 0
```

#### And 成功メッセージが表示されること

```python
@then('成功メッセージが表示されること')  # type: ignore
def then_f7642361(context):
    assert "完璧です" in context.output or "Success" in context.output
```

</details>


---
## Scenario: テスト漏れの検出 {: #line-14 }

- **Given** testable な仕様 "CORE-001" に対応するGherkinテストが存在しない
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** テストが実装されていない仕様として "CORE-001" が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given testable な仕様 "CORE-001" に対応するGherkinテストが存在しない

```python
@given('testable な仕様 "{param0}" に対応するGherkinテストが存在しない')  # type: ignore
def given_03339ad7(context, param0):
    prefix = param0.split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": True}]
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    assert getattr(context, 'exit_code', 0) == 1, f"Expected exit code 1, but got {context.exit_code}. Output:\n{context.output}"
```

#### And テストが実装されていない仕様として "CORE-001" が報告されること

```python
@then('テストが実装されていない仕様として "{param0}" が報告されること')  # type: ignore
def then_6664aa42(context, param0):
    assert param0 in context.output
```

</details>


---
## Scenario: orphanタグの検出 {: #line-20 }

- **Given** Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** orphanタグとして "@SPEC-999" が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている

```python
@given('Gherkinに仕様書に存在しない "{param0}" タグが含まれている')  # type: ignore
def given_3aa00113(context, param0):
    orphan_prefix = param0.lstrip('@').split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [{"uid": "SPEC-001", "testable": True}]
            },
            {
                "dir": "orphans",
                "prefix": orphan_prefix,
                "parent": "SPEC",
                "items": []
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, f"{param0}\n@SPEC-001\nFeature: Test\n  Scenario: Test\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    assert getattr(context, 'exit_code', 0) == 1, f"Expected exit code 1, but got {context.exit_code}. Output:\n{context.output}"
```

#### And orphanタグとして "@SPEC-999" が報告されること

```python
@then('orphanタグとして "{param0}" が報告されること')  # type: ignore
def then_33c30716(context, param0):
    assert param0 in context.output
```

</details>


---
## Scenario: テスト漏れとorphanタグの同時検出 {: #line-26 }

- **Given** 仕様 "CORE-001" のテストが未実装で "@SPEC-999" がorphanタグである
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** テスト漏れとorphanタグの両方が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "CORE-001" のテストが未実装で "@SPEC-999" がorphanタグである

```python
@given('仕様 "{param0}" のテストが未実装で "{param1}" がorphanタグである')  # type: ignore
def given_ffdcf7f2(context, param0, param1):
    prefix = param0.split("-")[0]
    orphan_prefix = param1.lstrip('@').split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": True}]
            },
            {
                "dir": "orphans",
                "prefix": orphan_prefix,
                "parent": prefix,
                "items": []
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, f"{param1}\nFeature: Test\n  Scenario: Test\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    assert getattr(context, 'exit_code', 0) == 1, f"Expected exit code 1, but got {context.exit_code}. Output:\n{context.output}"
```

#### And テスト漏れとorphanタグの両方が報告されること

```python
@then('テスト漏れとorphanタグの両方が報告されること')  # type: ignore
def then_755ec6da(context):
    assert "Untested Specs" in context.output or "テストが実装されていません" in context.output or "テスト漏れ" in context.output or "Missing" in context.output
    assert "Orphaned Tags" in context.output or "orphan" in context.output.lower() or "存在しない仕様" in context.output
```

</details>


---
## Scenario: testable: false の仕様はスキップされる {: #line-32 }

- **Given** 仕様 "SPEC-001" が testable: false に設定されている
- **And** "SPEC-001" に対応するGherkinテストが存在しない
- **When** audit コマンドを実行する
- **Then** "SPEC-001" はテスト漏れとして報告されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "SPEC-001" が testable: false に設定されている

```python
@given('仕様 "{param0}" が testable: false に設定されている')  # type: ignore
def given_624f5f06(context, param0):
    prefix = param0.split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": False}]
            }
        ]
    )
```

#### And "SPEC-001" に対応するGherkinテストが存在しない

```python
@given('"{param0}" に対応するGherkinテストが存在しない')  # type: ignore
def given_ea690d53(context, param0):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr
```

#### Then "SPEC-001" はテスト漏れとして報告されないこと

```python
@then('"{param0}" はテスト漏れとして報告されないこと')  # type: ignore
def then_55c71a2c(context, param0):
    assert param0 not in context.output
```

</details>


---
## Scenario: Suspect Link の検出 {: #line-39 }

**タグ**: `@QA-001`

- **Given** 仕様 "VIS-005" の上位アイテムが変更されている（cleared=false）
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Suspect Link テーブルに "VIS-005" が報告されること
- **And** 変更された上位アイテムのIDが表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "VIS-005" の上位アイテムが変更されている（cleared=false）

```python
@given('仕様 "{param0}" の上位アイテムが変更されている（cleared=false）')  # type: ignore
def given_db49ffab(context, param0):
    prefix = param0.split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "reqs",
                "prefix": "REQ",
                "items": [{"uid": "REQ-001", "testable": False, "text": "Old text"}]
            },
            {
                "dir": "specs",
                "prefix": prefix,
                "parent": "REQ",
                "items": [{"uid": param0, "testable": True, "links": ["REQ-001"]}]
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, f"@{param0}\nFeature: Test\n  Scenario: Test\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)

    req_file = context.temp_dir / "reqs" / "REQ-001.yml"
    with open(req_file, "r") as f_yml:
        content = f_yml.read()
    with open(req_file, "w") as f_yml:
        f_yml.write(content.replace("Old text", "New text"))
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    assert getattr(context, 'exit_code', 0) == 1, f"Expected exit code 1, but got {context.exit_code}. Output:\n{context.output}"
```

#### And Suspect Link テーブルに "VIS-005" が報告されること

```python
@then('Suspect Link テーブルに "{param0}" が報告されること')  # type: ignore
def then_0149339a(context, param0):
    assert param0 in context.output
    assert "Suspect" in context.output or "suspect" in context.output.lower()
```

#### And 変更された上位アイテムのIDが表示されること

```python
@then('変更された上位アイテムのIDが表示されること')  # type: ignore
def then_407500a2(context):
    assert "REQ-001" in context.output
```

</details>


---
## Scenario: Unreviewed Changes の検出 {: #line-47 }

**タグ**: `@QA-001`

- **Given** 仕様 "VIS-005" 自体に未レビューの変更がある（reviewed=false）
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Unreviewed Changes テーブルに "VIS-005" が報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "VIS-005" 自体に未レビューの変更がある（reviewed=false）

```python
@given('仕様 "{param0}" 自体に未レビューの変更がある（reviewed=false）')  # type: ignore
def given_8ceeca7b(context, param0):
    prefix = param0.split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": True, "text": "Old spec text"}]
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, f"@{param0}\nFeature: Test\n  Scenario: Test\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)

    spec_file = context.temp_dir / "specs" / f"{param0}.yml"
    with open(spec_file, "r") as f_yml:
        content = f_yml.read()
    with open(spec_file, "w") as f_yml:
        f_yml.write(content.replace("Old spec text", "New spec text"))
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    assert getattr(context, 'exit_code', 0) == 1, f"Expected exit code 1, but got {context.exit_code}. Output:\n{context.output}"
```

#### And Unreviewed Changes テーブルに "VIS-005" が報告されること

```python
@then('Unreviewed Changes テーブルに "{param0}" が報告されること')  # type: ignore
def then_56101a52(context, param0):
    assert param0 in context.output
    assert "Unreviewed" in context.output or "unreviewed" in context.output.lower()
```

</details>


---
## Scenario: feature ファイルが Unreviewed として検出される {: #line-54 }

**タグ**: `@QA-001`

- **Given** ".feature" ファイルのフィンガープリントコメントが現在の内容と一致しない
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** Unreviewed テーブルに対応する feature ファイル名が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given ".feature" ファイルのフィンガープリントコメントが現在の内容と一致しない

```python
@given('"{param0}" ファイルのフィンガープリントコメントが現在の内容と一致しない')  # type: ignore
def given_f066bd3a(context, param0):
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [{"uid": "SPEC-001", "testable": True}]
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, "@SPEC-001\nFeature: Test\n  Scenario: Old\n    Given old\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)

    with open(f, "r") as f_feat:
        content = f_feat.read()
    with open(f, "w") as f_feat:
        f_feat.write(content.replace("Old", "New").replace("old", "new"))
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    assert getattr(context, 'exit_code', 0) == 1, f"Expected exit code 1, but got {context.exit_code}. Output:\n{context.output}"
```

#### And Unreviewed テーブルに対応する feature ファイル名が表示されること

```python
@then('Unreviewed テーブルに対応する feature ファイル名が表示されること')  # type: ignore
def then_c1e4063b(context):
    assert "test.feature" in context.output
```

</details>


---
## Scenario: behavior-without-gherkin の検出 {: #line-61 }

**タグ**: `@QA-006`

- **Given** 仕様 "VIS-003" が "layer: behavior" かつ "testable: true" に設定されている
- **And** "VIS-003" に対応するGherkinタグが存在しない
- **When** audit コマンドを実行する
- **Then** 終了コード 1 が返ること
- **And** "VIS-003" が behavior-without-gherkin として報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "VIS-003" が "layer: behavior" かつ "testable: true" に設定されている

```python
@given('仕様 "{param0}" が "{param1}" かつ "{param2}" に設定されている')  # type: ignore
def given_d902e872(context, param0, param1, param2):
    # param1 = "layer: behavior", param2 = "testable: true"
    prefix = param0.split("-")[0]
    layer_val = param1.split(":")[1].strip() if ":" in param1 else param1
    testable_val = param2.split(":")[1].strip().lower() != "false" if ":" in param2 else True
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": testable_val, "extra": {"layer": layer_val}}]
            }
        ]
    )
```

#### And "VIS-003" に対応するGherkinタグが存在しない

```python
@given('"{param0}" に対応するGherkinタグが存在しない')  # type: ignore
def given_b9e6bcbc(context, param0):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    # タグなしのfeatureファイルを作成（または何もしない）
    f = feature_dir / "test.feature"
    if not f.exists():
        write_feature_file(f, "Feature: Test\n  Scenario: S1\n    Given test\n")
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr
```

#### Then 終了コード 1 が返ること

```python
@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    assert getattr(context, 'exit_code', 0) == 1, f"Expected exit code 1, but got {context.exit_code}. Output:\n{context.output}"
```

#### And "VIS-003" が behavior-without-gherkin として報告されること

```python
@then('"{param0}" が behavior-without-gherkin として報告されること')  # type: ignore
def then_0a2ef35f(context, param0):
    assert param0 in context.output, f"Expected {param0} in output:\n{context.output}"
    assert "behavior-without-gherkin" in context.output.lower() or "Behavior Without Gherkin" in context.output, \
        f"Expected 'Behavior Without Gherkin' section in output:\n{context.output}"
```

</details>


---
## Scenario: architecture-with-gherkin の検出（警告） {: #line-69 }

**タグ**: `@QA-006`

- **Given** 仕様 "CORE-001" が "layer: architecture" に設定されている
- **And** "CORE-001" に対応するGherkinタグが存在する
- **When** audit コマンドを実行する
- **Then** "CORE-001" が architecture-with-gherkin として警告表示されること
- **And** architecture-with-gherkin は終了コードに影響しないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 仕様 "CORE-001" が "layer: architecture" に設定されている

```python
@given('仕様 "{param0}" が "{param1}" に設定されている')  # type: ignore
def given_802bb420(context, param0, param1):
    # param1 = "layer: architecture"
    prefix = param0.split("-")[0]
    layer_val = param1.split(":")[1].strip() if ":" in param1 else param1
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": True, "extra": {"layer": layer_val}}]
            }
        ]
    )
```

#### And "CORE-001" に対応するGherkinタグが存在する

```python
@given('"{param0}" に対応するGherkinタグが存在する')  # type: ignore
def given_25d0a3d0(context, param0):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, f"@{param0}\nFeature: Test\n  Scenario: S1\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr
```

#### Then "CORE-001" が architecture-with-gherkin として警告表示されること

```python
@then('"{param0}" が architecture-with-gherkin として警告表示されること')  # type: ignore
def then_c994e63b(context, param0):
    assert param0 in context.output, f"Expected {param0} in output:\n{context.output}"
    assert "architecture-with-gherkin" in context.output.lower() or "Architecture With Gherkin" in context.output, \
        f"Expected 'Architecture With Gherkin' section in output:\n{context.output}"
```

#### And architecture-with-gherkin は終了コードに影響しないこと

```python
@then('architecture-with-gherkin は終了コードに影響しないこと')  # type: ignore
def then_9b9cd278(context):
    assert getattr(context, 'exit_code', 1) == 0, \
        f"Expected exit code 0 (architecture-with-gherkin is warning only), got {context.exit_code}. Output:\n{context.output}"
```

</details>


---
## Scenario: layer-unset の通知（情報） {: #line-77 }

**タグ**: `@QA-006`

- **Given** アクティブかつ "testable: true" の仕様に "layer" 属性が設定されていない
- **When** audit コマンドを実行する
- **Then** 当該仕様IDが layer-unset として情報表示されること
- **And** layer-unset は終了コードに影響しないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given アクティブかつ "testable: true" の仕様に "layer" 属性が設定されていない

```python
@given('アクティブかつ "{param0}" の仕様に "{param1}" 属性が設定されていない')  # type: ignore
def given_b00764d8(context, param0, param1):
    # param0 = "testable: true", param1 = "layer"
    # layer 属性なし・testable: true のアイテムを作成し、対応するGherkinタグも用意する（untested_specs を避けるため）
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [{"uid": "SPEC-001", "testable": True}]  # layer なし
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, "@SPEC-001\nFeature: Test\n  Scenario: S1\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)
```

#### When audit コマンドを実行する

```python
@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr
```

#### Then 当該仕様IDが layer-unset として情報表示されること

```python
@then('当該仕様IDが layer-unset として情報表示されること')  # type: ignore
def then_7b421936(context):
    assert "SPEC-001" in context.output, f"Expected SPEC-001 in output:\n{context.output}"
    assert "layer-unset" in context.output.lower() or "Layer Unset" in context.output, \
        f"Expected 'Layer Unset' section in output:\n{context.output}"
```

#### And layer-unset は終了コードに影響しないこと

```python
@then('layer-unset は終了コードに影響しないこと')  # type: ignore
def then_8cfff823(context):
    assert getattr(context, 'exit_code', 1) == 0, \
        f"Expected exit code 0 (layer-unset is info only), got {context.exit_code}. Output:\n{context.output}"
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: bcdfb25f894f72de41a0499a31984a64e890c1f9500c0c309c6ae9961f990c95
# spec-weaver-fingerprint-QA-001: IVjwbWJI8Xga_1LFrHA_SqnpsZ_-MHzjo-w7D9zwEYE=
# spec-weaver-fingerprint-QA-006: IQO1lBdAvEzVzJofPO_jiIFF1WjLNsCMUhlLQTXCk6A=

Feature: audit コマンド
  仕様とテストの乖離を静的に検知し、CI/CD品質ゲートとして機能する。

  Scenario: 完全一致で、監査が成功する
    Given すべてのtestable仕様に対応するGherkinテストが存在する
    When  audit コマンドを実行する
    Then  終了コード 0 が返ること
    And   成功メッセージが表示されること

  Scenario: テスト漏れの検出
    Given testable な仕様 "CORE-001" に対応するGherkinテストが存在しない
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   テストが実装されていない仕様として "CORE-001" が報告されること

  Scenario: orphanタグの検出
    Given Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   orphanタグとして "@SPEC-999" が報告されること

  Scenario: テスト漏れとorphanタグの同時検出
    Given 仕様 "CORE-001" のテストが未実装で "@SPEC-999" がorphanタグである
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   テスト漏れとorphanタグの両方が報告されること

  Scenario: testable: false の仕様はスキップされる
    Given 仕様 "SPEC-001" が testable: false に設定されている
    And   "SPEC-001" に対応するGherkinテストが存在しない
    When  audit コマンドを実行する
    Then  "SPEC-001" はテスト漏れとして報告されないこと

  @QA-001
  Scenario: Suspect Link の検出
    Given 仕様 "VIS-005" の上位アイテムが変更されている（cleared=false）
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   Suspect Link テーブルに "VIS-005" が報告されること
    And   変更された上位アイテムのIDが表示されること

  @QA-001
  Scenario: Unreviewed Changes の検出
    Given 仕様 "VIS-005" 自体に未レビューの変更がある（reviewed=false）
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   Unreviewed Changes テーブルに "VIS-005" が報告されること

  @QA-001
  Scenario: feature ファイルが Unreviewed として検出される
    Given ".feature" ファイルのフィンガープリントコメントが現在の内容と一致しない
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   Unreviewed テーブルに対応する feature ファイル名が表示されること

  @QA-006
  Scenario: behavior-without-gherkin の検出
    Given 仕様 "VIS-003" が "layer: behavior" かつ "testable: true" に設定されている
    And   "VIS-003" に対応するGherkinタグが存在しない
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
    And   "VIS-003" が behavior-without-gherkin として報告されること

  @QA-006
  Scenario: architecture-with-gherkin の検出（警告）
    Given 仕様 "CORE-001" が "layer: architecture" に設定されている
    And   "CORE-001" に対応するGherkinタグが存在する
    When  audit コマンドを実行する
    Then  "CORE-001" が architecture-with-gherkin として警告表示されること
    And   architecture-with-gherkin は終了コードに影響しないこと

  @QA-006
  Scenario: layer-unset の通知（情報）
    Given アクティブかつ "testable: true" の仕様に "layer" 属性が設定されていない
    When  audit コマンドを実行する
    Then  当該仕様IDが layer-unset として情報表示されること
    And   layer-unset は終了コードに影響しないこと

```
</details>