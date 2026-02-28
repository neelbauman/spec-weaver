# Feature: status コマンド

**タグ**: `@SPEC-007`

**関連アイテム**: [SPEC-007](../items/SPEC-007.md)

REQ・SPECの実装ステータスをRichテーブル形式で一覧表示する。

---
## Scenario: 全アイテムのステータスを一覧表示する

- **Given** REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている
- **When** status コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** REQ-001 が "draft" バッジとともに表示されること
- **And** SPEC-001 が "implemented" バッジとともに表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている

```python
@given('REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている')
def step_impl_1(context):
    setup_doorstop(context, prefixes=["REQ", "SPEC"])
    add_item_manual(context, "REQ", "REQ-001", "draft")
    add_item_manual(context, "SPEC", "SPEC-001", "implemented")
```

#### When status コマンドを実行する

```python
@when('status コマンドを実行する')
def step_impl_2(context):
    run_cli(context, ["status", "--repo-root", "."])
```

#### Then 終了コード 0 が返ること

```python
@then('終了コード {code:d} が返ること')
def then_exit_code(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And REQ-001 が "draft" バッジとともに表示されること

```python
@then('REQ-001 が "draft" バッジとともに表示されること')
def step_impl_4(context):
    assert "REQ-001" in context.stdout
    assert "draft" in context.stdout
```

#### And SPEC-001 が "implemented" バッジとともに表示されること

```python
@then('SPEC-001 が "implemented" バッジとともに表示されること')
def step_impl_5(context):
    assert "SPEC-001" in context.stdout
    assert "implemented" in context.stdout
```

</details>


---
## Scenario: status 未設定のアイテムは "-" と表示される

- **Given** SPEC-001 に status フィールドが設定されていない
- **When** status コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** SPEC-001 の実装状況が "-" と表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-001 に status フィールドが設定されていない

```python
@given('SPEC-001 に status フィールドが設定されていない')
def step_impl_6(context):
    setup_doorstop(context, prefixes=["SPEC"])
    add_item_manual(context, "SPEC", "SPEC-001", status=None)
```

#### When status コマンドを実行する

```python
@when('status コマンドを実行する')
def step_impl_2(context):
    run_cli(context, ["status", "--repo-root", "."])
```

#### Then 終了コード 0 が返ること

```python
@then('終了コード {code:d} が返ること')
def then_exit_code(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And SPEC-001 の実装状況が "-" と表示されること

```python
@then('SPEC-001 の実装状況が "-" と表示されること')
def step_impl_7(context):
    for line in context.stdout.splitlines():
        if "SPEC-001" in line:
            assert "-" in line
            return
    assert False
```

</details>


---
## Scenario: --filter で特定ステータスに絞り込める

- **Given** REQ-001 が status: implemented、REQ-002 が status: draft に設定されている
- **When** status コマンドを "--filter implemented" オプション付きで実行する
- **Then** 終了コード 0 が返ること
- **And** REQ-001 が表示されること
- **And** REQ-002 は表示されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given REQ-001 が status: implemented、REQ-002 が status: draft に設定されている

```python
@given('REQ-001 が status: implemented、REQ-002 が status: draft に設定されている')
def step_impl_8(context):
    setup_doorstop(context, prefixes=["REQ"])
    add_item_manual(context, "REQ", "REQ-001", "implemented")
    add_item_manual(context, "REQ", "REQ-002", "draft")
```

#### When status コマンドを "--filter implemented" オプション付きで実行する

```python
@when('status コマンドを "--filter implemented" オプション付きで実行する')
def step_impl_9(context):
    run_cli(context, ["status", "--repo-root", ".", "--filter", "implemented"])
```

#### Then 終了コード 0 が返ること

```python
@then('終了コード {code:d} が返ること')
def then_exit_code(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And REQ-001 が表示されること

```python
@then('REQ-001 が表示されること')
def step_impl_10(context):
    assert "REQ-001" in context.stdout
```

#### And REQ-002 は表示されないこと

```python
@then('REQ-002 は表示されないこと')
def step_impl_11(context):
    assert "REQ-002" not in context.stdout
```

</details>


---
## Scenario: --filter に一致するアイテムが存在しない場合に通知される

- **Given** すべてのアイテムの status が "draft" に設定されている
- **When** status コマンドを "--filter implemented" オプション付きで実行する
- **Then** 終了コード 0 が返ること
- **And** 一致するアイテムが見つからなかった旨が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given すべてのアイテムの status が "draft" に設定されている

```python
@given('すべてのアイテムの status が "draft" に設定されている')
def step_impl_12(context):
    setup_doorstop(context, prefixes=["SPEC"])
    add_item_manual(context, "SPEC", "SPEC-001", "draft")
```

#### When status コマンドを "--filter implemented" オプション付きで実行する

```python
@when('status コマンドを "--filter implemented" オプション付きで実行する')
def step_impl_9(context):
    run_cli(context, ["status", "--repo-root", ".", "--filter", "implemented"])
```

#### Then 終了コード 0 が返ること

```python
@then('終了コード {code:d} が返ること')
def then_exit_code(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"
```

#### And 一致するアイテムが見つからなかった旨が表示されること

```python
@then('一致するアイテムが見つからなかった旨が表示されること')
def step_impl_13(context):
    assert "見つかりませんでした" in context.stdout or "一致するアイテムが存在しません" in context.stdout
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
@SPEC-007
Feature: status コマンド
  REQ・SPECの実装ステータスをRichテーブル形式で一覧表示する。

  Scenario: 全アイテムのステータスを一覧表示する
    Given REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている
    When  status コマンドを実行する
    Then  終了コード 0 が返ること
    And   REQ-001 が "draft" バッジとともに表示されること
    And   SPEC-001 が "implemented" バッジとともに表示されること

  Scenario: status 未設定のアイテムは "-" と表示される
    Given SPEC-001 に status フィールドが設定されていない
    When  status コマンドを実行する
    Then  終了コード 0 が返ること
    And   SPEC-001 の実装状況が "-" と表示されること

  Scenario: --filter で特定ステータスに絞り込める
    Given REQ-001 が status: implemented、REQ-002 が status: draft に設定されている
    When  status コマンドを "--filter implemented" オプション付きで実行する
    Then  終了コード 0 が返ること
    And   REQ-001 が表示されること
    And   REQ-002 は表示されないこと

  Scenario: --filter に一致するアイテムが存在しない場合に通知される
    Given すべてのアイテムの status が "draft" に設定されている
    When  status コマンドを "--filter implemented" オプション付きで実行する
    Then  終了コード 0 が返ること
    And   一致するアイテムが見つからなかった旨が表示されること

```
</details>