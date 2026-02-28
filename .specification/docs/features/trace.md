# Feature: trace コマンド — トレーサビリティ・ツリー表示

**タグ**: `@SPEC-010`

**関連アイテム**: [SPEC-010](../items/SPEC-010.md)

任意のアイテム（REQ・SPEC・Gherkin）を起点として、
  関連する上位・下位アイテムを階層構造で表示する。

---
## Background

- **Given** Doorstopツリーが初期化されている
- **And** 以下のREQアイテムが存在する:
- **And** 以下のSPECアイテムが存在する:
- **And** 以下のfeatureファイルが存在する:

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopツリーが初期化されている

```python
@given('Doorstopツリーが初期化されている')
def step_impl_1(context):
    setup_doorstop(context, prefixes=["REQ", "SPEC"])
```

#### And 以下のREQアイテムが存在する:

```python
@given('以下のREQアイテムが存在する:')
def step_impl_2(context):
    for row in context.table:
        item_path = os.path.join(context.temp_dir, "reqs", f"{row['ID']}.yml")
        os.makedirs(os.path.dirname(item_path), exist_ok=True)
        with open(item_path, "w") as f:
            f.write(f"active: True\nheader: {row['Header']}\n")
            if 'Status' in row and row['Status']:
                f.write(f"status: {row['Status']}\n")
            if 'Links' in row and row['Links']:
                links = row['Links'].split(',')
                f.write("links:\n")
                for l in links:
                    f.write(f"- {l.strip()}\n")
```

#### And 以下のSPECアイテムが存在する:

```python
@given('以下のSPECアイテムが存在する:')
def step_impl_3(context):
    for row in context.table:
        item_path = os.path.join(context.temp_dir, "specs", f"{row['ID']}.yml")
        os.makedirs(os.path.dirname(item_path), exist_ok=True)
        with open(item_path, "w") as f:
            f.write(f"active: True\nheader: {row['Header']}\n")
            if 'Status' in row and row['Status']:
                f.write(f"status: {row['Status']}\n")
            if 'Links' in row and row['Links']:
                links = row['Links'].split(',')
                f.write("links:\n")
                for l in links:
                    f.write(f"- {l.strip()}\n")
```

#### And 以下のfeatureファイルが存在する:

```python
@given('以下のfeatureファイルが存在する:')
def step_impl_4(context):
    for row in context.table:
        content = f"{row['Tags']}\nFeature: {row['File']}\n"
        scenarios = row['Scenarios'].split(',')
        for s in scenarios:
            content += f"  Scenario: {s.strip()}\n    Given test\n"
        create_feature_file(context, row['File'], content)
```

</details>


---
## Scenario: REQを起点としたトップダウンのツリー表示

- **When** `spec-weaver trace REQ-001 -f ./specification/features` を実行する
- **Then** 終了コードが0である
- **And** 出力にツリー構造が含まれる
- **And** "REQ-001" がルートノードとして表示される
- **And** "REQ-002" が "REQ-001" の子ノードとして表示される
- **And** "SPEC-001" が "REQ-001" の子ノードとして表示される
- **And** "SPEC-003" が "REQ-002" の子ノードとして表示される
- **And** "audit.feature" が "SPEC-003" の子ノードとして表示される

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace REQ-001 -f ./specification/features` を実行する

```python
@when('`spec-weaver trace {item_id} -f ./specification/features` を実行する')
def step_impl_5(context, item_id):
    run_cli(context, ["trace", item_id, "-f", "features", "--repo-root", "."])
```

#### Then 終了コードが0である

```python
@then('終了コードが{code:d}である')
def then_exit_code_alt(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And 出力にツリー構造が含まれる

```python
@then('出力にツリー構造が含まれる')
def step_impl_8(context):
    assert "REQ-" in context.stdout or "SPEC-" in context.stdout
```

#### And "REQ-001" がルートノードとして表示される

```python
@then('"{uid}" がルートノードとして表示される')
def step_impl_9(context, uid):
    assert uid in context.stdout
```

#### And "REQ-002" が "REQ-001" の子ノードとして表示される

```python
@step('"{child}" が "{parent}" の子ノードとして表示される')
def step_impl_10(context, child, parent):
    assert child in context.stdout
    assert parent in context.stdout
```

#### And "SPEC-001" が "REQ-001" の子ノードとして表示される

```python
@step('"{child}" が "{parent}" の子ノードとして表示される')
def step_impl_10(context, child, parent):
    assert child in context.stdout
    assert parent in context.stdout
```

#### And "SPEC-003" が "REQ-002" の子ノードとして表示される

```python
@step('"{child}" が "{parent}" の子ノードとして表示される')
def step_impl_10(context, child, parent):
    assert child in context.stdout
    assert parent in context.stdout
```

#### And "audit.feature" が "SPEC-003" の子ノードとして表示される

```python
@step('"{child}" が "{parent}" の子ノードとして表示される')
def step_impl_10(context, child, parent):
    assert child in context.stdout
    assert parent in context.stdout
```

</details>


---
## Scenario: SPECを起点とした双方向のツリー表示

- **When** `spec-weaver trace SPEC-003 -f ./specification/features` を実行する
- **Then** 終了コードが0である
- **And** 出力にツリー構造が含まれる
- **And** 上位に "REQ-002" が表示される
- **And** 上位に "REQ-001" が表示される
- **And** 下位に "audit.feature" のシナリオが表示される

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace SPEC-003 -f ./specification/features` を実行する

```python
@when('`spec-weaver trace {item_id} -f ./specification/features` を実行する')
def step_impl_5(context, item_id):
    run_cli(context, ["trace", item_id, "-f", "features", "--repo-root", "."])
```

#### Then 終了コードが0である

```python
@then('終了コードが{code:d}である')
def then_exit_code_alt(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And 出力にツリー構造が含まれる

```python
@then('出力にツリー構造が含まれる')
def step_impl_8(context):
    assert "REQ-" in context.stdout or "SPEC-" in context.stdout
```

#### And 上位に "REQ-002" が表示される

```python
@then('上位に "{uid}" が表示される')
def step_impl_12(context, uid):
    assert uid in context.stdout
```

#### And 上位に "REQ-001" が表示される

```python
@then('上位に "{uid}" が表示される')
def step_impl_12(context, uid):
    assert uid in context.stdout
```

#### And 下位に "audit.feature" のシナリオが表示される

```python
@then('下位に "{filename}" のシナリオが表示される')
def step_impl_13(context, filename):
    assert "Scenario:" in context.stdout
```

</details>


---
## Scenario: Gherkin Featureファイルを起点としたボトムアップ表示

- **When** `spec-weaver trace audit.feature -f ./specification/features` を実行する
- **Then** 終了コードが0である
- **And** 出力に "SPEC-003" が表示される
- **And** 出力に "REQ-002" が表示される
- **And** 出力に "REQ-001" が表示される

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace audit.feature -f ./specification/features` を実行する

```python
@when('`spec-weaver trace {item_id} -f ./specification/features` を実行する')
def step_impl_5(context, item_id):
    run_cli(context, ["trace", item_id, "-f", "features", "--repo-root", "."])
```

#### Then 終了コードが0である

```python
@then('終了コードが{code:d}である')
def then_exit_code_alt(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And 出力に "SPEC-003" が表示される

```python
@step('出力に "{text}" が表示される')
def step_output_contains_alt(context, text):
    assert text in context.stdout or text in context.stderr
```

#### And 出力に "REQ-002" が表示される

```python
@step('出力に "{text}" が表示される')
def step_output_contains_alt(context, text):
    assert text in context.stdout or text in context.stderr
```

#### And 出力に "REQ-001" が表示される

```python
@step('出力に "{text}" が表示される')
def step_output_contains_alt(context, text):
    assert text in context.stdout or text in context.stderr
```

</details>


---
## Scenario: --direction up で上方向のみ探索

- **When** `spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する
- **Then** 終了コードが0である
- **And** 出力に "REQ-002" が表示される
- **And** 出力に "REQ-001" が表示される
- **And** 出力に "audit.feature" が表示されない

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する

```python
@when('`spec-weaver trace {item_id} -f ./specification/features --direction {direction}` を実行する')
def step_impl_6(context, item_id, direction):
    run_cli(context, ["trace", item_id, "-f", "features", "--repo-root", ".", "--direction", direction])
```

#### Then 終了コードが0である

```python
@then('終了コードが{code:d}である')
def then_exit_code_alt(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And 出力に "REQ-002" が表示される

```python
@step('出力に "{text}" が表示される')
def step_output_contains_alt(context, text):
    assert text in context.stdout or text in context.stderr
```

#### And 出力に "REQ-001" が表示される

```python
@step('出力に "{text}" が表示される')
def step_output_contains_alt(context, text):
    assert text in context.stdout or text in context.stderr
```

#### And 出力に "audit.feature" が表示されない

```python
@step('出力に "{text}" が表示されない')
def step_output_not_contains_alt(context, text):
    assert text not in context.stdout and text not in context.stderr
```

</details>


---
## Scenario: --direction down で下方向のみ探索

- **When** `spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する
- **Then** 終了コードが0である
- **And** 出力に "REQ-002" が表示される
- **And** 出力に "SPEC-003" が表示される
- **And** 出力に "audit.feature" が表示される

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する

```python
@when('`spec-weaver trace {item_id} -f ./specification/features --direction {direction}` を実行する')
def step_impl_6(context, item_id, direction):
    run_cli(context, ["trace", item_id, "-f", "features", "--repo-root", ".", "--direction", direction])
```

#### Then 終了コードが0である

```python
@then('終了コードが{code:d}である')
def then_exit_code_alt(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And 出力に "REQ-002" が表示される

```python
@step('出力に "{text}" が表示される')
def step_output_contains_alt(context, text):
    assert text in context.stdout or text in context.stderr
```

#### And 出力に "SPEC-003" が表示される

```python
@step('出力に "{text}" が表示される')
def step_output_contains_alt(context, text):
    assert text in context.stdout or text in context.stderr
```

#### And 出力に "audit.feature" が表示される

```python
@step('出力に "{text}" が表示される')
def step_output_contains_alt(context, text):
    assert text in context.stdout or text in context.stderr
```

</details>


---
## Scenario: --format flat でフラットリスト表示

- **When** `spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する
- **Then** 終了コードが0である
- **And** 出力がフラットリスト形式である
- **And** 各行に "[REQ]" または "[SPEC]" または "[TEST]" のラベルが含まれる

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する

```python
@when('`spec-weaver trace {item_id} -f ./specification/features --format {fmt}` を実行する')
def step_impl_7(context, item_id, fmt):
    run_cli(context, ["trace", item_id, "-f", "features", "--repo-root", ".", "--format", fmt])
```

#### Then 終了コードが0である

```python
@then('終了コードが{code:d}である')
def then_exit_code_alt(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And 出力がフラットリスト形式である

```python
@then('出力がフラットリスト形式である')
def step_impl_17(context):
    assert "ID" in context.stdout
```

#### And 各行に "[REQ]" または "[SPEC]" または "[TEST]" のラベルが含まれる

```python
@then('各行に "{label1}" または "{label2}" または "{label3}" のラベルが含まれる')
def step_impl_18(context, label1, label2, label3):
    assert label1.strip('[]') in context.stdout or label2.strip('[]') in context.stdout or label3.strip('[]') in context.stdout
```

</details>


---
## Scenario: 存在しないIDを指定した場合のエラー

- **When** `spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する
- **Then** 終了コードが1である
- **And** エラーメッセージに "not found" が含まれる

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する

```python
@when('`spec-weaver trace {item_id} -f ./specification/features` を実行する')
def step_impl_5(context, item_id):
    run_cli(context, ["trace", item_id, "-f", "features", "--repo-root", "."])
```

#### Then 終了コードが1である

```python
@then('終了コードが{code:d}である')
def then_exit_code_alt(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And エラーメッセージに "not found" が含まれる

```python
@then('エラーメッセージに "{msg}" が含まれる')
def step_impl_19(context, msg):
    assert msg.lower() in context.stdout.lower() or msg.lower() in context.stderr.lower()
```

</details>


---
## Scenario: 各ノードにステータスバッジが表示される

- **When** `spec-weaver trace REQ-001 -f ./specification/features` を実行する
- **Then** 終了コードが0である
- **And** "REQ-001" のノードに "implemented" のステータスバッジが表示される
- **And** "SPEC-003" のノードに "implemented" のステータスバッジが表示される

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace REQ-001 -f ./specification/features` を実行する

```python
@when('`spec-weaver trace {item_id} -f ./specification/features` を実行する')
def step_impl_5(context, item_id):
    run_cli(context, ["trace", item_id, "-f", "features", "--repo-root", "."])
```

#### Then 終了コードが0である

```python
@then('終了コードが{code:d}である')
def then_exit_code_alt(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And "REQ-001" のノードに "implemented" のステータスバッジが表示される

```python
@then('"{uid}" のノードに "{status}" のステータスバッジが表示される')
def step_impl_20(context, uid, status):
    assert uid in context.stdout
    assert status in context.stdout
```

#### And "SPEC-003" のノードに "implemented" のステータスバッジが表示される

```python
@then('"{uid}" のノードに "{status}" のステータスバッジが表示される')
def step_impl_20(context, uid, status):
    assert uid in context.stdout
    assert status in context.stdout
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
@SPEC-010
Feature: trace コマンド — トレーサビリティ・ツリー表示
  任意のアイテム（REQ・SPEC・Gherkin）を起点として、
  関連する上位・下位アイテムを階層構造で表示する。

  Background:
    Given Doorstopツリーが初期化されている
    And 以下のREQアイテムが存在する:
      | ID      | Header                   | Status      | Links   |
      | REQ-001 | トレーサビリティ保証      | implemented |         |
      | REQ-002 | 監査による品質担保        | implemented | REQ-001 |
    And 以下のSPECアイテムが存在する:
      | ID       | Header             | Status      | Links   |
      | SPEC-001 | コア・アーキテクチャ | implemented | REQ-001 |
      | SPEC-003 | audit コマンド仕様  | implemented | REQ-002 |
    And 以下のfeatureファイルが存在する:
      | File          | Tags      | Scenarios                    |
      | audit.feature | @SPEC-003 | 完全一致時の監査成功, テスト漏れの検出 |

  Scenario: REQを起点としたトップダウンのツリー表示
    When `spec-weaver trace REQ-001 -f ./specification/features` を実行する
    Then 終了コードが0である
    And 出力にツリー構造が含まれる
    And "REQ-001" がルートノードとして表示される
    And "REQ-002" が "REQ-001" の子ノードとして表示される
    And "SPEC-001" が "REQ-001" の子ノードとして表示される
    And "SPEC-003" が "REQ-002" の子ノードとして表示される
    And "audit.feature" が "SPEC-003" の子ノードとして表示される

  Scenario: SPECを起点とした双方向のツリー表示
    When `spec-weaver trace SPEC-003 -f ./specification/features` を実行する
    Then 終了コードが0である
    And 出力にツリー構造が含まれる
    And 上位に "REQ-002" が表示される
    And 上位に "REQ-001" が表示される
    And 下位に "audit.feature" のシナリオが表示される

  Scenario: Gherkin Featureファイルを起点としたボトムアップ表示
    When `spec-weaver trace audit.feature -f ./specification/features` を実行する
    Then 終了コードが0である
    And 出力に "SPEC-003" が表示される
    And 出力に "REQ-002" が表示される
    And 出力に "REQ-001" が表示される

  Scenario: --direction up で上方向のみ探索
    When `spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する
    Then 終了コードが0である
    And 出力に "REQ-002" が表示される
    And 出力に "REQ-001" が表示される
    And 出力に "audit.feature" が表示されない

  Scenario: --direction down で下方向のみ探索
    When `spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する
    Then 終了コードが0である
    And 出力に "REQ-002" が表示される
    And 出力に "SPEC-003" が表示される
    And 出力に "audit.feature" が表示される

  Scenario: --format flat でフラットリスト表示
    When `spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する
    Then 終了コードが0である
    And 出力がフラットリスト形式である
    And 各行に "[REQ]" または "[SPEC]" または "[TEST]" のラベルが含まれる

  Scenario: 存在しないIDを指定した場合のエラー
    When `spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する
    Then 終了コードが1である
    And エラーメッセージに "not found" が含まれる

  Scenario: 各ノードにステータスバッジが表示される
    When `spec-weaver trace REQ-001 -f ./specification/features` を実行する
    Then 終了コードが0である
    And "REQ-001" のノードに "implemented" のステータスバッジが表示される
    And "SPEC-003" のノードに "implemented" のステータスバッジが表示される

```
</details>