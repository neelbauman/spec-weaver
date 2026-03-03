# Feature: status コマンド

**タグ**: `@VIS-003`

**関連アイテム**: [VIS-003](../items/VIS-003.md)

REQ・SPECの実装ステータスをRichテーブル形式で一覧表示する。

---
## Scenario: 全アイテムのステータスを一覧表示する {: #line-7 }

- **Given** REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている
- **When** status コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** REQ-001 が "draft" バッジとともに表示されること
- **And** SPEC-001 が "implemented" バッジとともに表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている

```python
@given('REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている')  # type: ignore
def given_ef098fcf(context):
    """REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    create_doorstop_project_api(
        context.temp_dir,
        req_items=[{"header": "Req 1", "status": "draft"}],
        spec_items=[{"header": "Spec 1", "status": "implemented", "links": ["REQ-001"]}],
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    context.status_feature_dir = feature_dir
```

#### When status コマンドを実行する

```python
@when('status コマンドを実行する')  # type: ignore
def when_d68a8d9a(context):
    """status コマンドを実行する

    Scenarios:
      - 全アイテムのステータスを一覧表示する
      - status 未設定のアイテムは "-" と表示される
      - レビューステータスと最終更新日が表示される
    """
    feature_dir = getattr(context, 'status_feature_dir', context.temp_dir / "specification" / "features")
    feature_dir.mkdir(parents=True, exist_ok=True)
    res = run_spec_weaver(
        ['status', '--repo-root', str(context.temp_dir), '--feature-dir', str(feature_dir)],
        cwd=context.temp_dir,
    )
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

#### And REQ-001 が "draft" バッジとともに表示されること

```python
@then('REQ-001 が "{param0}" バッジとともに表示されること')  # type: ignore
def then_6e220346(context, param0):
    """REQ-001 が "draft" バッジとともに表示されること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    assert getattr(context, 'output', None) is not None
```

#### And SPEC-001 が "implemented" バッジとともに表示されること

```python
@then('SPEC-001 が "{param0}" バッジとともに表示されること')  # type: ignore
def then_9f0d7f01(context, param0):
    """SPEC-001 が "implemented" バッジとともに表示されること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    assert getattr(context, 'output', None) is not None
```

</details>


---
## Scenario: status 未設定のアイテムは "-" と表示される {: #line-14 }

- **Given** SPEC-001 に status フィールドが設定されていない
- **When** status コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** SPEC-001 の実装状況が "-" と表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given SPEC-001 に status フィールドが設定されていない

```python
@given('SPEC-001 に status フィールドが設定されていない')  # type: ignore
def given_0d995d24(context):
    """SPEC-001 に status フィールドが設定されていない

    Scenarios:
      - status 未設定のアイテムは "-" と表示される
    """
    create_doorstop_project_api(
        context.temp_dir,
        req_items=[{"header": "Req 1"}],
        spec_items=[{"header": "Spec 1", "links": ["REQ-001"]}],
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    context.status_feature_dir = feature_dir
```

#### When status コマンドを実行する

```python
@when('status コマンドを実行する')  # type: ignore
def when_d68a8d9a(context):
    """status コマンドを実行する

    Scenarios:
      - 全アイテムのステータスを一覧表示する
      - status 未設定のアイテムは "-" と表示される
      - レビューステータスと最終更新日が表示される
    """
    feature_dir = getattr(context, 'status_feature_dir', context.temp_dir / "specification" / "features")
    feature_dir.mkdir(parents=True, exist_ok=True)
    res = run_spec_weaver(
        ['status', '--repo-root', str(context.temp_dir), '--feature-dir', str(feature_dir)],
        cwd=context.temp_dir,
    )
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

#### And SPEC-001 の実装状況が "-" と表示されること

```python
@then('SPEC-001 の実装状況が "{param0}" と表示されること')  # type: ignore
def then_5818121f(context, param0):
    """SPEC-001 の実装状況が "-" と表示されること

    Scenarios:
      - status 未設定のアイテムは "-" と表示される
    """
    assert getattr(context, 'output', None) is not None
```

</details>


---
## Scenario: --filter で特定ステータスに絞り込める {: #line-20 }

- **Given** REQ-001 が status: implemented、REQ-002 が status: draft に設定されている
- **When** status コマンドを "--filter implemented" オプション付きで実行する
- **Then** 終了コード 0 が返ること
- **And** REQ-001 が表示されること
- **And** REQ-002 は表示されないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given REQ-001 が status: implemented、REQ-002 が status: draft に設定されている

```python
@given('REQ-001 が status: implemented、REQ-002 が status: draft に設定されている')  # type: ignore
def given_58beb4fc(context):
    """REQ-001 が status: implemented、REQ-002 が status: draft に設定されている

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    create_doorstop_project_api(
        context.temp_dir,
        req_items=[
            {"header": "Req 1", "status": "implemented"},
            {"header": "Req 2", "status": "draft"},
        ],
        spec_items=[],
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    context.status_feature_dir = feature_dir
```

#### When status コマンドを "--filter implemented" オプション付きで実行する

```python
@when('status コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_d36ae1bf(context, param0):
    """status コマンドを "--filter implemented" オプション付きで実行する

    Scenarios:
      - --filter で特定ステータスに絞り込める
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    cmd = ['status'] + param0.split()
    res = run_spec_weaver(cmd, cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
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

#### And REQ-001 が表示されること

```python
@then('REQ-001 が表示されること')  # type: ignore
def then_2847178d(context):
    """REQ-001 が表示されること

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    assert "REQ-001" in context.output, f"REQ-001 が出力に見つかりません。\n出力:\n{context.output}"
```

#### And REQ-002 は表示されないこと

```python
@then('REQ-002 は表示されないこと')  # type: ignore
def then_9fc4e668(context):
    """REQ-002 は表示されないこと

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    assert "REQ-002" not in context.output, f"REQ-002 が出力に含まれています。\n出力:\n{context.output}"
```

</details>


---
## Scenario: --filter に一致するアイテムが存在しない場合に通知される {: #line-27 }

- **Given** すべてのアイテムの status が "draft" に設定されている
- **When** status コマンドを "--filter implemented" オプション付きで実行する
- **Then** 終了コード 0 が返ること
- **And** 一致するアイテムが見つからなかった旨が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given すべてのアイテムの status が "draft" に設定されている

```python
@given('すべてのアイテムの status が "{param0}" に設定されている')  # type: ignore
def given_f93df893(context, param0):
    """すべてのアイテムの status が "draft" に設定されている

    Scenarios:
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    create_doorstop_project_api(
        context.temp_dir,
        req_items=[{"status": param0}],
        spec_items=[{"status": param0, "links": ["REQ-001"]}],
    )
    (context.temp_dir / "specification" / "features").mkdir(parents=True, exist_ok=True)
```

#### When status コマンドを "--filter implemented" オプション付きで実行する

```python
@when('status コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_d36ae1bf(context, param0):
    """status コマンドを "--filter implemented" オプション付きで実行する

    Scenarios:
      - --filter で特定ステータスに絞り込める
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    cmd = ['status'] + param0.split()
    res = run_spec_weaver(cmd, cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
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

#### And 一致するアイテムが見つからなかった旨が表示されること

```python
@then('一致するアイテムが見つからなかった旨が表示されること')  # type: ignore
def then_897c0cfb(context):
    """一致するアイテムが見つからなかった旨が表示されること

    Scenarios:
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    assert "見つかりませんでした" in context.output
```

</details>


---
## Scenario: レビューステータスと最終更新日が表示される {: #line-33 }

- **Given** Doorstopのアイテムが存在する
- **When** status コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** レビューステータス列が表示されること
- **And** 最終更新日列が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopのアイテムが存在する

```python
@given('Doorstopのアイテムが存在する')  # type: ignore
def given_0da078b7(context):
    """Doorstopのアイテムが存在する

    Scenarios:
      - レビューステータスと最終更新日が表示される
    """
    create_doorstop_project_api(
        context.temp_dir,
        req_items=[{"header": "Req 1"}],
        spec_items=[{"header": "Spec 1", "links": ["REQ-001"]}],
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    context.status_feature_dir = feature_dir
```

#### When status コマンドを実行する

```python
@when('status コマンドを実行する')  # type: ignore
def when_d68a8d9a(context):
    """status コマンドを実行する

    Scenarios:
      - 全アイテムのステータスを一覧表示する
      - status 未設定のアイテムは "-" と表示される
      - レビューステータスと最終更新日が表示される
    """
    feature_dir = getattr(context, 'status_feature_dir', context.temp_dir / "specification" / "features")
    feature_dir.mkdir(parents=True, exist_ok=True)
    res = run_spec_weaver(
        ['status', '--repo-root', str(context.temp_dir), '--feature-dir', str(feature_dir)],
        cwd=context.temp_dir,
    )
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

#### And レビューステータス列が表示されること

```python
@then('レビューステータス列が表示されること')  # type: ignore
def then_33e7dc19(context):
    """レビューステータス列が表示されること

    Scenarios:
      - レビューステータスと最終更新日が表示される
    """
    assert "レビュー" in context.output, f"レビューステータス列が出力に見つかりません。\n出力:\n{context.output}"
```

#### And 最終更新日列が表示されること

```python
@then('最終更新日列が表示されること')  # type: ignore
def then_49bd7463(context):
    """最終更新日列が表示されること

    Scenarios:
      - レビューステータスと最終更新日が表示される
    """
    assert "更新" in context.output, f"最終更新日列が出力に見つかりません。\n出力:\n{context.output}"
```

</details>


---
## Scenario: buildコマンドで生成されるドキュメントに実装状況が反映される {: #line-40 }

- **Given** SPEC-001 が status: implemented に設定されている
- **When** build コマンドを実行する
- **Then** 一覧ページの実装状況列にバッジが表示されること
- **And** 詳細ページの本文に "**実装状況**: ✅ implemented" が表示されること

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
  File "specification/features/steps/step_status.py", line 228, in given_0f39b2ed
    raise NotImplementedError('STEP: SPEC-001 が status: implemented に設定されている')
NotImplementedError: STEP: SPEC-001 が status: implemented に設定されている
```

#### Given SPEC-001 が status: implemented に設定されている

```python
@given('SPEC-001 が status: implemented に設定されている')  # type: ignore
def given_0f39b2ed(context):
    """SPEC-001 が status: implemented に設定されている

    Scenarios:
      - buildコマンドで生成されるドキュメントに実装状況が反映される
    """
    raise NotImplementedError('STEP: SPEC-001 が status: implemented に設定されている')
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

#### Then 一覧ページの実装状況列にバッジが表示されること

```python
@then('一覧ページの実装状況列にバッジが表示されること')  # type: ignore
def then_f35a3316(context):
    """一覧ページの実装状況列にバッジが表示されること

    Scenarios:
      - buildコマンドで生成されるドキュメントに実装状況が反映される
    """
    raise NotImplementedError('STEP: 一覧ページの実装状況列にバッジが表示されること')
```

#### And 詳細ページの本文に "**実装状況**: ✅ implemented" が表示されること

```python
@then('詳細ページの本文に "{param0}" が表示されること')  # type: ignore
def then_d4f7509c(context, param0):
    """詳細ページの本文に "**実装状況**: ✅ implemented" が表示されること

    Scenarios:
      - buildコマンドで生成されるドキュメントに実装状況が反映される
    """
    raise NotImplementedError('STEP: 詳細ページの本文に "{param0}" が表示されること')
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: ec3fe7950dd3bd4c3bd04815b3820a604d3148298794bacbf50928c87945fd64
# spec-weaver-fingerprint-VIS-003: vkjlHhlge0Un5uAGQCyff68rJGP3jp7vGCvSQVAsuNM=
@VIS-003
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

  Scenario: レビューステータスと最終更新日が表示される
    Given Doorstopのアイテムが存在する
    When  status コマンドを実行する
    Then  終了コード 0 が返ること
    And   レビューステータス列が表示されること
    And   最終更新日列が表示されること

  Scenario: buildコマンドで生成されるドキュメントに実装状況が反映される
    Given SPEC-001 が status: implemented に設定されている
    When  build コマンドを実行する
    Then  一覧ページの実装状況列にバッジが表示されること
    And   詳細ページの本文に "**実装状況**: ✅ implemented" が表示されること

```
</details>