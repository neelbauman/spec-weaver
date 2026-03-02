# Feature: status コマンド

> 📋 **Unreviewed Changes**: このフィーチャーファイル自体に未レビューの変更があります。レビュー後に `review` コマンドで更新してください。

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
@given("REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている")  # type: ignore
def given_ef098fcf(context):
    """REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        req_items=[{"header": "要件A", "testable": False, "status": "draft"}],
        spec_items=[{"header": "仕様A", "testable": True, "status": "implemented"}],
    )
```

#### When status コマンドを実行する

```python
@when("status コマンドを実行する")  # type: ignore
def when_d68a8d9a(context):
    """status コマンドを実行する

    Scenarios:
      - 全アイテムのステータスを一覧表示する
      - status 未設定のアイテムは "-" と表示される
      - レビューステータスと最終更新日が表示される
    """
    _run_status(context)
```

#### And REQ-001 が "draft" バッジとともに表示されること

```python
@then('REQ-001 が "{badge}" バッジとともに表示されること')  # type: ignore
def then_6e220346(context, badge):
    """REQ-001 が "draft" バッジとともに表示されること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    assert "REQ-001" in context.output, f"REQ-001 が出力にありません:\n{context.output}"
    assert badge in context.output, (
        f"バッジ {badge!r} が出力にありません:\n{context.output}"
    )
```

#### And SPEC-001 が "implemented" バッジとともに表示されること

```python
@then('SPEC-001 が "{badge}" バッジとともに表示されること')  # type: ignore
def then_9f0d7f01(context, badge):
    """SPEC-001 が "implemented" バッジとともに表示されること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    assert "SPEC-001" in context.output, (
        f"SPEC-001 が出力にありません:\n{context.output}"
    )
    assert badge in context.output, (
        f"バッジ {badge!r} が出力にありません:\n{context.output}"
    )
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
@given("SPEC-001 に status フィールドが設定されていない")  # type: ignore
def given_0d995d24(context):
    """SPEC-001 に status フィールドが設定されていない

    Scenarios:
      - status 未設定のアイテムは "-" と表示される
    """
    context.repo_root = context.temp_dir / "repo"
    # status なしで作成
    create_doorstop_project_api(
        context.repo_root,
        spec_items=[{"header": "仕様A", "testable": True}],
    )
```

#### When status コマンドを実行する

```python
@when("status コマンドを実行する")  # type: ignore
def when_d68a8d9a(context):
    """status コマンドを実行する

    Scenarios:
      - 全アイテムのステータスを一覧表示する
      - status 未設定のアイテムは "-" と表示される
      - レビューステータスと最終更新日が表示される
    """
    _run_status(context)
```

#### And SPEC-001 の実装状況が "-" と表示されること

```python
@then('SPEC-001 の実装状況が "{expected}" と表示されること')  # type: ignore
def then_5818121f(context, expected):
    """SPEC-001 の実装状況が "-" と表示されること

    Scenarios:
      - status 未設定のアイテムは "-" と表示される
    """
    assert expected in context.output, (
        f"{expected!r} が出力にありません:\n{context.output}"
    )
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
@given("REQ-001 が status: implemented、REQ-002 が status: draft に設定されている")  # type: ignore
def given_58beb4fc(context):
    """REQ-001 が status: implemented、REQ-002 が status: draft に設定されている

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(
        context.repo_root,
        req_items=[
            {"header": "実装済み要件", "testable": False, "status": "implemented"},
            {"header": "ドラフト要件", "testable": False, "status": "draft"},
        ],
    )
```

#### When status コマンドを "--filter implemented" オプション付きで実行する

```python
@when('status コマンドを "{option}" オプション付きで実行する')  # type: ignore
def when_d36ae1bf(context, option):
    """status コマンドを "--filter implemented" オプション付きで実行する

    Scenarios:
      - --filter で特定ステータスに絞り込める
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    # option例: "--filter implemented"
    parts = option.split()
    _run_status(context, extra_args=parts)
```

#### And REQ-001 が表示されること

```python
@then("REQ-001 が表示されること")  # type: ignore
def then_2847178d(context):
    """REQ-001 が表示されること

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    assert "REQ-001" in context.output, f"REQ-001 が出力にありません:\n{context.output}"
```

#### And REQ-002 は表示されないこと

```python
@then("REQ-002 は表示されないこと")  # type: ignore
def then_9fc4e668(context):
    """REQ-002 は表示されないこと

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    assert "REQ-002" not in context.output, (
        f"REQ-002 が出力に含まれています:\n{context.output}"
    )
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
@given('すべてのアイテムの status が "{status}" に設定されている')  # type: ignore
def given_f93df893(context, status):
    """すべてのアイテムの status が "draft" に設定されている

    Scenarios:
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    raise NotImplementedError('STEP: すべてのアイテムの status が "{param0}" に設定されている')
```

#### When status コマンドを "--filter implemented" オプション付きで実行する

```python
@when('status コマンドを "{option}" オプション付きで実行する')  # type: ignore
def when_d36ae1bf(context, option):
    """status コマンドを "--filter implemented" オプション付きで実行する

    Scenarios:
      - --filter で特定ステータスに絞り込める
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    # option例: "--filter implemented"
    parts = option.split()
    _run_status(context, extra_args=parts)
```

#### And 一致するアイテムが見つからなかった旨が表示されること

```python
@then('一致するアイテムが見つからなかった旨が表示されること')
def step_impl_13(context):
    assert "見つかりませんでした" in context.stdout or "一致するアイテムが存在しません" in context.stdout
```

</details>


---
## Scenario: レビューステータスと最終更新日が表示される

- **Given** Doorstopのアイテムが存在する
- **When** status コマンドを実行する
- **Then** 終了コード 0 が返ること
- **And** レビューステータス列が表示されること
- **And** 最終更新日列が表示されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When status コマンドを実行する

```python
@when("status コマンドを実行する")  # type: ignore
def when_d68a8d9a(context):
    """status コマンドを実行する

    Scenarios:
      - 全アイテムのステータスを一覧表示する
      - status 未設定のアイテムは "-" と表示される
      - レビューステータスと最終更新日が表示される
    """
    _run_status(context)
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

  Scenario: レビューステータスと最終更新日が表示される
    Given Doorstopのアイテムが存在する
    When  status コマンドを実行する
    Then  終了コード 0 が返ること
    And   レビューステータス列が表示されること
    And   最終更新日列が表示されること

```
</details>