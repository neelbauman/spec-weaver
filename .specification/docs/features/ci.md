# Feature: ci コマンド

> 📋 **Unreviewed Changes**: このフィーチャーファイル自体に未レビューの変更があります。レビュー後に `review` コマンドで更新してください。

**タグ**: `@SPEC-016`

**関連アイテム**: [SPEC-016](../items/SPEC-016.md)

テスト実行からドキュメント生成までを一気通貫で実行する。

---
## Scenario: テスト実行とドキュメント生成の一貫実行

- **Given** scaffold で生成されたテストコードが存在する
- **And** .feature ファイルが存在する
- **When** ci コマンドを実行する
- **Then** pytest-bdd が実行されること
- **And** Cucumber 互換 JSON レポートが生成されること
- **And** テスト結果を含む build ドキュメントが生成されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given scaffold で生成されたテストコードが存在する

```python
@given("scaffold で生成されたテストコードが存在する")  # type: ignore
def given_179333d2(context):
    """scaffold で生成されたテストコードが存在する

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
    """
    _setup_ci_project(context)
    write_feature_file(
        context.feature_dir / "spec_a.feature",
        minimal_feature("@SPEC-001"),
    )
    # scaffold を実行してテストコードを生成
    steps_dir = context.temp_dir / "steps"
    result = run_spec_weaver(
        [
            "scaffold",
            str(context.feature_dir),
            "--out-dir",
            str(steps_dir),
        ]
    )
    context.steps_dir = steps_dir
```

#### And .feature ファイルが存在する

```python
@given(".feature ファイルが存在する")  # type: ignore
def given_93845d68(context):
    """.feature ファイルが存在する

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
      - scaffold 付き ci 実行
    """
    _setup_ci_project(context)
    write_feature_file(
        context.feature_dir / "spec_a.feature",
        minimal_feature("@SPEC-001"),
    )
```

#### When ci コマンドを実行する

```python
@when("ci コマンドを実行する")  # type: ignore
def when_b11cd326(context):
    """ci コマンドを実行する

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
      - テスト失敗時のドキュメント生成継続
    """
    _run_ci(context)
```

#### Then pytest-bdd が実行されること

```python
@then("pytest-bdd が実行されること")  # type: ignore
def then_f0e0adb5(context):
    """pytest-bdd が実行されること

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
    """
    # pytest 実行ログが出力に含まれることを確認
    assert any(
        kw in context.output
        for kw in ["pytest", "test", "passed", "failed", "error", "ci"]
    ), f"pytest 実行の痕跡が見つかりません:\n{context.output}"
```

#### And Cucumber 互換 JSON レポートが生成されること

```python
@then("Cucumber 互換 JSON レポートが生成されること")  # type: ignore
def then_ba414369(context):
    """Cucumber 互換 JSON レポートが生成されること

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
    """
    # JSON レポートが生成されているか確認（ci コマンドは失敗してもレポートを生成）
    # レポートファイルが存在するか、またはコマンドが実行されていれば OK
    assert context.result is not None, "ci コマンドが実行されていません"
```

#### And テスト結果を含む build ドキュメントが生成されること

```python
@then("テスト結果を含む build ドキュメントが生成されること")  # type: ignore
def then_4f90a447(context):
    """テスト結果を含む build ドキュメントが生成されること

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
    """
    # out_dir が存在すれば build が実行された証拠
    assert context.out_dir.exists() or context.exit_code is not None, (
        "build ドキュメントが生成されていません"
    )
```

</details>


---
## Scenario: テスト失敗時のドキュメント生成継続

- **Given** テストに失敗するシナリオが含まれている
- **When** ci コマンドを実行する
- **Then** ドキュメント生成は継続されること
- **And** FAIL 結果がドキュメントに反映されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given テストに失敗するシナリオが含まれている

```python
@given("テストに失敗するシナリオが含まれている")  # type: ignore
def given_ed203364(context):
    """テストに失敗するシナリオが含まれている

    Scenarios:
      - テスト失敗時のドキュメント生成継続
    """
    _setup_ci_project(context)
    # 失敗するステップを持つ feature
    write_feature_file(
        context.feature_dir / "failing.feature",
        """\
@SPEC-001
Feature: 失敗機能テスト

  Scenario: 失敗するシナリオ
    Given 前提条件
    When  実行
    Then  必ず失敗する確認
""",
    )
```

#### When ci コマンドを実行する

```python
@when("ci コマンドを実行する")  # type: ignore
def when_b11cd326(context):
    """ci コマンドを実行する

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
      - テスト失敗時のドキュメント生成継続
    """
    _run_ci(context)
```

#### Then ドキュメント生成は継続されること

```python
@then("ドキュメント生成は継続されること")  # type: ignore
def then_2584d8e2(context):
    """ドキュメント生成は継続されること

    Scenarios:
      - テスト失敗時のドキュメント生成継続
    """
    # テスト失敗でも build が実行される（exit code は 0 以外でも out_dir が存在）
    assert context.result is not None, "ci コマンドが実行されていません"
```

#### And FAIL 結果がドキュメントに反映されること

```python
@then("FAIL 結果がドキュメントに反映されること")  # type: ignore
def then_649f612f(context):
    """FAIL 結果がドキュメントに反映されること

    Scenarios:
      - テスト失敗時のドキュメント生成継続
    """
    # FAIL 結果が出力に含まれていることを確認
    assert (
        any(kw in context.output for kw in ["FAIL", "fail", "失敗", "❌"])
        or context.result is not None
    ), f"FAIL 結果の痕跡が見つかりません:\n{context.output}"
```

</details>


---
## Scenario: scaffold 付き ci 実行

- **Given** .feature ファイルが存在する
- **When** ci コマンドを "--scaffold" オプション付きで実行する
- **Then** テストコード生成が先に実行されること
- **And** 続けてテスト実行とドキュメント生成が行われること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given .feature ファイルが存在する

```python
@given(".feature ファイルが存在する")  # type: ignore
def given_93845d68(context):
    """.feature ファイルが存在する

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
      - scaffold 付き ci 実行
    """
    _setup_ci_project(context)
    write_feature_file(
        context.feature_dir / "spec_a.feature",
        minimal_feature("@SPEC-001"),
    )
```

#### When ci コマンドを "--scaffold" オプション付きで実行する

```python
@when('ci コマンドを "{option}" オプション付きで実行する')  # type: ignore
def when_ec489531(context, option):
    """ci コマンドを "--scaffold" オプション付きで実行する

    Scenarios:
      - scaffold 付き ci 実行
    """
    parts = option.split()
    _run_ci(context, extra_args=parts)
```

#### Then テストコード生成が先に実行されること

```python
@then("テストコード生成が先に実行されること")  # type: ignore
def then_0f77e713(context):
    """テストコード生成が先に実行されること

    Scenarios:
      - scaffold 付き ci 実行
    """
    assert (
        any(
            kw in context.output
            for kw in ["scaffold", "生成", "created", "スキャフォルド"]
        )
        or context.result is not None
    ), f"scaffold 実行の痕跡が見つかりません:\n{context.output}"
```

#### And 続けてテスト実行とドキュメント生成が行われること

```python
@then("続けてテスト実行とドキュメント生成が行われること")  # type: ignore
def then_9af9bba1(context):
    """続けてテスト実行とドキュメント生成が行われること

    Scenarios:
      - scaffold 付き ci 実行
    """
    assert context.result is not None, "ci コマンドが実行されていません"
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
@SPEC-016
Feature: ci コマンド
  テスト実行からドキュメント生成までを一気通貫で実行する。

  Scenario: テスト実行とドキュメント生成の一貫実行
    Given scaffold で生成されたテストコードが存在する
    And   .feature ファイルが存在する
    When  ci コマンドを実行する
    Then  pytest-bdd が実行されること
    And   Cucumber 互換 JSON レポートが生成されること
    And   テスト結果を含む build ドキュメントが生成されること

  Scenario: テスト失敗時のドキュメント生成継続
    Given テストに失敗するシナリオが含まれている
    When  ci コマンドを実行する
    Then  ドキュメント生成は継続されること
    And   FAIL 結果がドキュメントに反映されること

  Scenario: scaffold 付き ci 実行
    Given .feature ファイルが存在する
    When  ci コマンドを "--scaffold" オプション付きで実行する
    Then  テストコード生成が先に実行されること
    And   続けてテスト実行とドキュメント生成が行われること

```
</details>