# Feature: trace コマンド — トレーサビリティ・ツリー表示

**タグ**: `@SPEC-010`

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
@given('Doorstopツリーが初期化されている')  # type: ignore
def given_6df87eb3(context):
    """Doorstopツリーが初期化されている

    Scenarios:
      - 
    """
    pass
```

#### And 以下のREQアイテムが存在する:

```python
@given(u'以下のREQアイテムが存在する:')
def step_impl(context):
    pass
```

#### And 以下のSPECアイテムが存在する:

```python
@given('以下のSPECアイテムが存在する:')  # type: ignore
def given_14c0b615(context):
    """以下のSPECアイテムが存在する:

    Scenarios:
      - 
    """
    pass
```

#### And 以下のfeatureファイルが存在する:

```python
@given(u'以下のfeatureファイルが存在する:')
def step_impl(context):
    pass
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
@when(u'`spec-weaver trace REQ-001 -f ./specification/features` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace REQ-001 -f ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コードが0である

```python
@then("終了コードが{code:d}である")  # type: ignore
def then_exit_code(context, code):
    """終了コードが0である / 終了コードが1である

    Scenarios:
      - trace, review, semantic_review 各コマンドの共通ステップ
    """
    assert context.exit_code == code, (
        f"終了コード {code} を期待しましたが {context.exit_code} でした。\n出力:\n{context.output}"
    )
```

#### And 出力にツリー構造が含まれる

```python
@then("出力にツリー構造が含まれる")  # type: ignore
def then_output_has_tree(context):
    """出力にツリー構造が含まれる

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - SPECを起点とした双方向のツリー表示
    """
    assert any(
        kw in context.output
        for kw in ["REQ-", "SPEC-", "├", "└", "│", "─"]
    ), f"ツリー構造が出力にありません:\n{context.output}"
```

#### And "REQ-001" がルートノードとして表示される

```python
@then(u'"REQ-001" がルートノードとして表示される')
def step_impl(context):
    pass
```

#### And "REQ-002" が "REQ-001" の子ノードとして表示される

```python
@then(u'"REQ-002" が "REQ-001" の子ノードとして表示される')
def step_impl(context):
    pass
```

#### And "SPEC-001" が "REQ-001" の子ノードとして表示される

```python
@then(u'"SPEC-001" が "REQ-001" の子ノードとして表示される')
def step_impl(context):
    pass
```

#### And "SPEC-003" が "REQ-002" の子ノードとして表示される

```python
@then(u'"SPEC-003" が "REQ-002" の子ノードとして表示される')
def step_impl(context):
    pass
```

#### And "audit.feature" が "SPEC-003" の子ノードとして表示される

```python
@then(u'"audit.feature" が "SPEC-003" の子ノードとして表示される')
def step_impl(context):
    pass
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
@when(u'`spec-weaver trace SPEC-003 -f ./specification/features` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace SPEC-003 -f ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コードが0である

```python
@then("終了コードが{code:d}である")  # type: ignore
def then_exit_code(context, code):
    """終了コードが0である / 終了コードが1である

    Scenarios:
      - trace, review, semantic_review 各コマンドの共通ステップ
    """
    assert context.exit_code == code, (
        f"終了コード {code} を期待しましたが {context.exit_code} でした。\n出力:\n{context.output}"
    )
```

#### And 出力にツリー構造が含まれる

```python
@then("出力にツリー構造が含まれる")  # type: ignore
def then_output_has_tree(context):
    """出力にツリー構造が含まれる

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - SPECを起点とした双方向のツリー表示
    """
    assert any(
        kw in context.output
        for kw in ["REQ-", "SPEC-", "├", "└", "│", "─"]
    ), f"ツリー構造が出力にありません:\n{context.output}"
```

#### And 上位に "REQ-002" が表示される

```python
@then(u'上位に "REQ-002" が表示される')
def step_impl(context):
    pass
```

#### And 上位に "REQ-001" が表示される

```python
@then(u'上位に "REQ-001" が表示される')
def step_impl(context):
    pass
```

#### And 下位に "audit.feature" のシナリオが表示される

```python
@then(u'下位に "audit.feature" のシナリオが表示される')
def step_impl(context):
    pass
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
@when(u'`spec-weaver trace audit.feature -f ./specification/features` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace audit.feature -f ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コードが0である

```python
@then("終了コードが{code:d}である")  # type: ignore
def then_exit_code(context, code):
    """終了コードが0である / 終了コードが1である

    Scenarios:
      - trace, review, semantic_review 各コマンドの共通ステップ
    """
    assert context.exit_code == code, (
        f"終了コード {code} を期待しましたが {context.exit_code} でした。\n出力:\n{context.output}"
    )
```

#### And 出力に "SPEC-003" が表示される

```python
@then(u'出力に "SPEC-003" が表示される')
def step_impl(context):
    pass
```

#### And 出力に "REQ-002" が表示される

```python
@then(u'出力に "REQ-002" が表示される')
def step_impl(context):
    pass
```

#### And 出力に "REQ-001" が表示される

```python
@then(u'出力に "REQ-001" が表示される')
def step_impl(context):
    pass
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
@when('`spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する')  # type: ignore
def when_770f884f(context):
    """`spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する

    Scenarios:
      - --direction up で上方向のみ探索
    """
    pass
```

#### Then 終了コードが0である

```python
@then("終了コードが{code:d}である")  # type: ignore
def then_exit_code(context, code):
    """終了コードが0である / 終了コードが1である

    Scenarios:
      - trace, review, semantic_review 各コマンドの共通ステップ
    """
    assert context.exit_code == code, (
        f"終了コード {code} を期待しましたが {context.exit_code} でした。\n出力:\n{context.output}"
    )
```

#### And 出力に "REQ-002" が表示される

```python
@then(u'出力に "REQ-002" が表示される')
def step_impl(context):
    pass
```

#### And 出力に "REQ-001" が表示される

```python
@then(u'出力に "REQ-001" が表示される')
def step_impl(context):
    pass
```

#### And 出力に "audit.feature" が表示されない

```python
@then(u'出力に "audit.feature" が表示されない')
def step_impl(context):
    pass
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
@when('`spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する')  # type: ignore
def when_24d70f7f(context):
    """`spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する

    Scenarios:
      - --direction down で下方向のみ探索
    """
    pass
```

#### Then 終了コードが0である

```python
@then("終了コードが{code:d}である")  # type: ignore
def then_exit_code(context, code):
    """終了コードが0である / 終了コードが1である

    Scenarios:
      - trace, review, semantic_review 各コマンドの共通ステップ
    """
    assert context.exit_code == code, (
        f"終了コード {code} を期待しましたが {context.exit_code} でした。\n出力:\n{context.output}"
    )
```

#### And 出力に "REQ-002" が表示される

```python
@then(u'出力に "REQ-002" が表示される')
def step_impl(context):
    pass
```

#### And 出力に "SPEC-003" が表示される

```python
@then(u'出力に "SPEC-003" が表示される')
def step_impl(context):
    pass
```

#### And 出力に "audit.feature" が表示される

```python
@then(u'出力に "audit.feature" が表示される')
def step_impl(context):
    pass
```

</details>


---
## Scenario: --format flat でフラットリスト表示

- **When** `spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する
- **Then** 終了コードが0である
- **And** 出力がフラットリスト形式である
- **And** 各行に "REQ" または "SPEC" または "TEST" のラベルが含まれる

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する

```python
@when('`spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する')  # type: ignore
def when_816b7b2c(context):
    """`spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する

    Scenarios:
      - --format flat でフラットリスト表示
    """
    pass
```

#### Then 終了コードが0である

```python
@then("終了コードが{code:d}である")  # type: ignore
def then_exit_code(context, code):
    """終了コードが0である / 終了コードが1である

    Scenarios:
      - trace, review, semantic_review 各コマンドの共通ステップ
    """
    assert context.exit_code == code, (
        f"終了コード {code} を期待しましたが {context.exit_code} でした。\n出力:\n{context.output}"
    )
```

#### And 出力がフラットリスト形式である

```python
@then(u'出力がフラットリスト形式である')
def step_impl(context):
    pass
```

#### And 各行に "REQ" または "SPEC" または "TEST" のラベルが含まれる

```python
@then(u'各行に "REQ" または "SPEC" または "TEST" のラベルが含まれる')
def step_impl(context):
    pass
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
@when(u'`spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace NONEXIST-999 -f ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コードが1である

```python
@then("終了コードが{code:d}である")  # type: ignore
def then_exit_code(context, code):
    """終了コードが0である / 終了コードが1である

    Scenarios:
      - trace, review, semantic_review 各コマンドの共通ステップ
    """
    assert context.exit_code == code, (
        f"終了コード {code} を期待しましたが {context.exit_code} でした。\n出力:\n{context.output}"
    )
```

#### And エラーメッセージに "not found" が含まれる

```python
@then(u'エラーメッセージに "not found" が含まれる')
def step_impl(context):
    pass
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
@when(u'`spec-weaver trace REQ-001 -f ./specification/features` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace REQ-001 -f ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then 終了コードが0である

```python
@then("終了コードが{code:d}である")  # type: ignore
def then_exit_code(context, code):
    """終了コードが0である / 終了コードが1である

    Scenarios:
      - trace, review, semantic_review 各コマンドの共通ステップ
    """
    assert context.exit_code == code, (
        f"終了コード {code} を期待しましたが {context.exit_code} でした。\n出力:\n{context.output}"
    )
```

#### And "REQ-001" のノードに "implemented" のステータスバッジが表示される

```python
@then(u'"REQ-001" のノードに "implemented" のステータスバッジが表示される')
def step_impl(context):
    pass
```

#### And "SPEC-003" のノードに "implemented" のステータスバッジが表示される

```python
@then(u'"SPEC-003" のノードに "implemented" のステータスバッジが表示される')
def step_impl(context):
    pass
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: 800e543e22e3ca019b5ccbd6efea879aa5ea3dbb2a3afafc7f4e63db24015318
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
    And 各行に "REQ" または "SPEC" または "TEST" のラベルが含まれる

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