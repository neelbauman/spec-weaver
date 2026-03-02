# Feature: ci コマンド

**タグ**: `@AUT-002`

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
@given(u'scaffold で生成されたテストコードが存在する')
def step_impl(context):
    pass
```

#### And .feature ファイルが存在する

```python
@given(u'.feature ファイルが存在する')
def step_impl(context):
    pass
```

#### When ci コマンドを実行する

```python
@when(u'ci コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['ci'], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then pytest-bdd が実行されること

```python
@then(u'pytest-bdd が実行されること')
def step_impl(context):
    pass
```

#### And Cucumber 互換 JSON レポートが生成されること

```python
@then(u'Cucumber 互換 JSON レポートが生成されること')
def step_impl(context):
    pass
```

#### And テスト結果を含む build ドキュメントが生成されること

```python
@then(u'テスト結果を含む build ドキュメントが生成されること')
def step_impl(context):
    pass
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
@given(u'テストに失敗するシナリオが含まれている')
def step_impl(context):
    pass
```

#### When ci コマンドを実行する

```python
@when(u'ci コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['ci'], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')
```

#### Then ドキュメント生成は継続されること

```python
@then(u'ドキュメント生成は継続されること')
def step_impl(context):
    pass
```

#### And FAIL 結果がドキュメントに反映されること

```python
@then(u'FAIL 結果がドキュメントに反映されること')
def step_impl(context):
    pass
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
@given(u'.feature ファイルが存在する')
def step_impl(context):
    pass
```

#### When ci コマンドを "--scaffold" オプション付きで実行する

```python
@when('ci コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_ec489531(context, param0):
    """ci コマンドを "--scaffold" オプション付きで実行する

    Scenarios:
      - scaffold 付き ci 実行
    """
    pass
```

#### Then テストコード生成が先に実行されること

```python
@then(u'テストコード生成が先に実行されること')
def step_impl(context):
    pass
```

#### And 続けてテスト実行とドキュメント生成が行われること

```python
@then(u'続けてテスト実行とドキュメント生成が行われること')
def step_impl(context):
    pass
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: 283aa0282d1c19b1bc130d2e18405561a84e83c1b6f10a4a382da9597b25529d
# spec-weaver-fingerprint-AUT-002: gASW5wMaDKZis4PQkfA4jgoesvwYa6hKWx21741Y9jg=
@AUT-002
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