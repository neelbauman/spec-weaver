# Feature: データ抽出基盤

**タグ**: `@SPEC-002`

**関連アイテム**: [SPEC-002](../items/SPEC-002.md) / [SPEC-021](../items/SPEC-021.md)

Doorstop と Gherkin から仕様データとテストタグを正確に抽出する。

---
## Scenario: Doorstop APIによる仕様ID集合の取得

- **Given** Doorstopプロジェクトにアクティブな仕様アイテムが存在する
- **When** 仕様ID集合を取得する
- **Then** アクティブかつtestableな仕様IDのみが返されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopプロジェクトにアクティブな仕様アイテムが存在する

```python
@given('Doorstopプロジェクトにアクティブな仕様アイテムが存在する')  # type: ignore
def given_a04781e9(context):
    """Doorstopプロジェクトにアクティブな仕様アイテムが存在する

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(context.repo_root,
        req_items=[{"header":"要件A","testable":False}],
        spec_items=[{"header":"仕様A","testable":True}])
```

#### When 仕様ID集合を取得する

```python
@when('仕様ID集合を取得する')  # type: ignore
def when_e56707cb(context):
    """仕様ID集合を取得する

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
      - 非アクティブなアイテムの除外
      - テスト不可能な仕様の除外
    """
    from spec_weaver.doorstop import get_specs
    context.value = get_specs(repo_root=context.repo_root)
```

#### Then アクティブかつtestableな仕様IDのみが返されること

```python
@then('アクティブかつtestableな仕様IDのみが返されること')  # type: ignore
def then_6823b180(context):
    """アクティブかつtestableな仕様IDのみが返されること

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
    """
    specs = context.value
    assert len(specs) >= 1
    for uid in specs:
        assert not uid.startswith("REQ")
```

</details>


---
## Scenario: 非アクティブなアイテムの除外

- **Given** Doorstopプロジェクトに active: false のアイテムが存在する
- **When** 仕様ID集合を取得する
- **Then** 非アクティブなアイテムは結果に含まれないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopプロジェクトに active: false のアイテムが存在する

```python
@given('Doorstopプロジェクトに active: false のアイテムが存在する')  # type: ignore
def given_dccca3dc(context):
    """Doorstopプロジェクトに active: false のアイテムが存在する

    Scenarios:
      - 非アクティブなアイテムの除外
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(context.repo_root,
        spec_items=[
            {"header":"アクティブ","testable":True,"active":True},
            {"header":"非アクティブ","testable":True,"active":False}])
    context.inactive_uid = "SPEC-002"
```

#### When 仕様ID集合を取得する

```python
@when('仕様ID集合を取得する')  # type: ignore
def when_e56707cb(context):
    """仕様ID集合を取得する

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
      - 非アクティブなアイテムの除外
      - テスト不可能な仕様の除外
    """
    from spec_weaver.doorstop import get_specs
    context.value = get_specs(repo_root=context.repo_root)
```

#### Then 非アクティブなアイテムは結果に含まれないこと

```python
@then('非アクティブなアイテムは結果に含まれないこと')  # type: ignore
def then_99bfaa46(context):
    """非アクティブなアイテムは結果に含まれないこと

    Scenarios:
      - 非アクティブなアイテムの除外
    """
    assert context.inactive_uid not in context.value
```

</details>


---
## Scenario: テスト不可能な仕様の除外

- **Given** Doorstopプロジェクトに testable: false のアイテムが存在する
- **When** 仕様ID集合を取得する
- **Then** testable: false のアイテムは結果に含まれないこと

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopプロジェクトに testable: false のアイテムが存在する

```python
@given('Doorstopプロジェクトに testable: false のアイテムが存在する')  # type: ignore
def given_d534a041(context):
    """Doorstopプロジェクトに testable: false のアイテムが存在する

    Scenarios:
      - テスト不可能な仕様の除外
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(context.repo_root,
        spec_items=[
            {"header":"テスト可能","testable":True},
            {"header":"テスト不可","testable":False}])
    context.nontestable_uid = "SPEC-002"
```

#### When 仕様ID集合を取得する

```python
@when('仕様ID集合を取得する')  # type: ignore
def when_e56707cb(context):
    """仕様ID集合を取得する

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
      - 非アクティブなアイテムの除外
      - テスト不可能な仕様の除外
    """
    from spec_weaver.doorstop import get_specs
    context.value = get_specs(repo_root=context.repo_root)
```

#### Then testable: false のアイテムは結果に含まれないこと

```python
@then('testable: false のアイテムは結果に含まれないこと')  # type: ignore
def then_f3fad2a6(context):
    """testable: false のアイテムは結果に含まれないこと

    Scenarios:
      - テスト不可能な仕様の除外
    """
    assert context.nontestable_uid not in context.value
```

</details>


---
## Scenario: プレフィックスによるフィルタリング

- **Given** DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する
- **When** プレフィックス "SPEC" で仕様ID集合を取得する
- **Then** SPECプレフィックスのアイテムのみが返されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する

```python
@given('DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する')  # type: ignore
def given_7f8e9c65(context):
    """DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    context.repo_root = context.temp_dir / "repo"
    create_doorstop_project_api(context.repo_root,
        req_items=[{"header":"要件","testable":True}],
        spec_items=[{"header":"仕様","testable":True}])
```

#### When プレフィックス "SPEC" で仕様ID集合を取得する

```python
@when('プレフィックス "{prefix}" で仕様ID集合を取得する')  # type: ignore
def when_1d11bcd6(context, prefix):
    """プレフィックス "SPEC" で仕様ID集合を取得する

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    from spec_weaver.doorstop import get_specs
    context.value = get_specs(repo_root=context.repo_root, prefix=prefix)
```

#### Then SPECプレフィックスのアイテムのみが返されること

```python
@then('SPECプレフィックスのアイテムのみが返されること')  # type: ignore
def then_b5f39418(context):
    """SPECプレフィックスのアイテムのみが返されること

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    for uid in context.value:
        assert uid.startswith("SPEC")
    assert any(uid.startswith("SPEC") for uid in context.value)
```

</details>


---
## Scenario: Gherkin ASTからのタグ抽出

- **Given** Gherkin .feature ファイルに @SPEC-001 タグが付与されている
- **When** タグ集合を取得する
- **Then** "SPEC-001" がタグ集合に含まれること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Gherkin .feature ファイルに @SPEC-001 タグが付与されている

```python
@given('Gherkin .feature ファイルに @SPEC-001 タグが付与されている')  # type: ignore
def given_b830a393(context):
    """Gherkin .feature ファイルに @SPEC-001 タグが付与されている

    Scenarios:
      - Gherkin ASTからのタグ抽出
    """
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(context.feature_dir / "test.feature", minimal_feature("@SPEC-001"))
```

#### When タグ集合を取得する

```python
@when('タグ集合を取得する')  # type: ignore
def when_a12b8a55(context):
    """タグ集合を取得する

    Scenarios:
      - Gherkin ASTからのタグ抽出
      - Feature・Scenario両レベルのタグ抽出
      - サブディレクトリ内のfeatureファイルの再帰探索
      - Gherkin構文エラーの検出
    """
    from spec_weaver.gherkin import get_tags
    try:
        context.value = get_tags(features_dir=context.feature_dir)
        context.error = None
    except ValueError as e:
        context.error = e
        context.value = set()
```

#### Then "SPEC-001" がタグ集合に含まれること

```python
@then('"{spec_id}" がタグ集合に含まれること')  # type: ignore
def then_e8d01468(context, spec_id):
    """"SPEC-001" がタグ集合に含まれること

    Scenarios:
      - Gherkin ASTからのタグ抽出
    """
    assert spec_id in context.value
```

</details>


---
## Scenario: Feature・Scenario両レベルのタグ抽出

- **Given** Feature レベルと Scenario レベルに異なるSPECタグが付与されている
- **When** タグ集合を取得する
- **Then** 両方のレベルのタグがすべて抽出されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Feature レベルと Scenario レベルに異なるSPECタグが付与されている

```python
@given('Feature レベルと Scenario レベルに異なるSPECタグが付与されている')  # type: ignore
def given_07def24f(context):
    """Feature レベルと Scenario レベルに異なるSPECタグが付与されている

    Scenarios:
      - Feature・Scenario両レベルのタグ抽出
    """
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(context.feature_dir / "dual.feature", """\
@SPEC-010
Feature: デュアルタグテスト

  @SPEC-011
  Scenario: シナリオレベルのタグ
    Given テスト
    When  実行
    Then  確認
""")
```

#### When タグ集合を取得する

```python
@when('タグ集合を取得する')  # type: ignore
def when_a12b8a55(context):
    """タグ集合を取得する

    Scenarios:
      - Gherkin ASTからのタグ抽出
      - Feature・Scenario両レベルのタグ抽出
      - サブディレクトリ内のfeatureファイルの再帰探索
      - Gherkin構文エラーの検出
    """
    from spec_weaver.gherkin import get_tags
    try:
        context.value = get_tags(features_dir=context.feature_dir)
        context.error = None
    except ValueError as e:
        context.error = e
        context.value = set()
```

#### Then 両方のレベルのタグがすべて抽出されること

```python
@then('両方のレベルのタグがすべて抽出されること')  # type: ignore
def then_d712dc38(context):
    """両方のレベルのタグがすべて抽出されること

    Scenarios:
      - Feature・Scenario両レベルのタグ抽出
    """
    assert "SPEC-010" in context.value
    assert "SPEC-011" in context.value
```

</details>


---
## Scenario: サブディレクトリ内のfeatureファイルの再帰探索

- **Given** サブディレクトリに .feature ファイルが存在する
- **When** タグ集合を取得する
- **Then** サブディレクトリ内のタグも含めて抽出されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given サブディレクトリに .feature ファイルが存在する

```python
@given('サブディレクトリに .feature ファイルが存在する')  # type: ignore
def given_1427ca58(context):
    """サブディレクトリに .feature ファイルが存在する

    Scenarios:
      - サブディレクトリ内のfeatureファイルの再帰探索
    """
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(context.feature_dir / "subdir" / "nested.feature", minimal_feature("@SPEC-099"))
```

#### When タグ集合を取得する

```python
@when('タグ集合を取得する')  # type: ignore
def when_a12b8a55(context):
    """タグ集合を取得する

    Scenarios:
      - Gherkin ASTからのタグ抽出
      - Feature・Scenario両レベルのタグ抽出
      - サブディレクトリ内のfeatureファイルの再帰探索
      - Gherkin構文エラーの検出
    """
    from spec_weaver.gherkin import get_tags
    try:
        context.value = get_tags(features_dir=context.feature_dir)
        context.error = None
    except ValueError as e:
        context.error = e
        context.value = set()
```

#### Then サブディレクトリ内のタグも含めて抽出されること

```python
@then('サブディレクトリ内のタグも含めて抽出されること')  # type: ignore
def then_1c0ec472(context):
    """サブディレクトリ内のタグも含めて抽出されること

    Scenarios:
      - サブディレクトリ内のfeatureファイルの再帰探索
    """
    assert "SPEC-099" in context.value
```

</details>


---
## Scenario: Gherkin構文エラーの検出

- **Given** 構文的に不正な .feature ファイルが存在する
- **When** タグ集合を取得する
- **Then** ValueError が発生しGherkin構文エラーが報告されること

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given 構文的に不正な .feature ファイルが存在する

```python
@given('構文的に不正な .feature ファイルが存在する')  # type: ignore
def given_540458bc(context):
    """構文的に不正な .feature ファイルが存在する

    Scenarios:
      - Gherkin構文エラーの検出
    """
    context.feature_dir = context.temp_dir / "features"
    write_feature_file(context.feature_dir / "bad.feature", "この行は Gherkin ではない\n  壊れた構文\n")
```

#### When タグ集合を取得する

```python
@when('タグ集合を取得する')  # type: ignore
def when_a12b8a55(context):
    """タグ集合を取得する

    Scenarios:
      - Gherkin ASTからのタグ抽出
      - Feature・Scenario両レベルのタグ抽出
      - サブディレクトリ内のfeatureファイルの再帰探索
      - Gherkin構文エラーの検出
    """
    from spec_weaver.gherkin import get_tags
    try:
        context.value = get_tags(features_dir=context.feature_dir)
        context.error = None
    except ValueError as e:
        context.error = e
        context.value = set()
```

#### Then ValueError が発生しGherkin構文エラーが報告されること

```python
@then('ValueError が発生しGherkin構文エラーが報告されること')  # type: ignore
def then_c5d0b4fe(context):
    """ValueError が発生しGherkin構文エラーが報告されること

    Scenarios:
      - Gherkin構文エラーの検出
    """
    assert context.error is not None
    assert isinstance(context.error, ValueError)
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
@SPEC-002
Feature: データ抽出基盤
  Doorstop と Gherkin から仕様データとテストタグを正確に抽出する。

  # --- Doorstop解析 ---

  Scenario: Doorstop APIによる仕様ID集合の取得
    Given Doorstopプロジェクトにアクティブな仕様アイテムが存在する
    When  仕様ID集合を取得する
    Then  アクティブかつtestableな仕様IDのみが返されること

  Scenario: 非アクティブなアイテムの除外
    Given Doorstopプロジェクトに active: false のアイテムが存在する
    When  仕様ID集合を取得する
    Then  非アクティブなアイテムは結果に含まれないこと

  Scenario: テスト不可能な仕様の除外
    Given Doorstopプロジェクトに testable: false のアイテムが存在する
    When  仕様ID集合を取得する
    Then  testable: false のアイテムは結果に含まれないこと

  Scenario: プレフィックスによるフィルタリング
    Given DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する
    When  プレフィックス "SPEC" で仕様ID集合を取得する
    Then  SPECプレフィックスのアイテムのみが返されること

  # --- Gherkin解析 ---

  Scenario: Gherkin ASTからのタグ抽出
    Given Gherkin .feature ファイルに @SPEC-001 タグが付与されている
    When  タグ集合を取得する
    Then  "SPEC-001" がタグ集合に含まれること

  Scenario: Feature・Scenario両レベルのタグ抽出
    Given Feature レベルと Scenario レベルに異なるSPECタグが付与されている
    When  タグ集合を取得する
    Then  両方のレベルのタグがすべて抽出されること

  Scenario: サブディレクトリ内のfeatureファイルの再帰探索
    Given サブディレクトリに .feature ファイルが存在する
    When  タグ集合を取得する
    Then  サブディレクトリ内のタグも含めて抽出されること

  Scenario: Gherkin構文エラーの検出
    Given 構文的に不正な .feature ファイルが存在する
    When  タグ集合を取得する
    Then  ValueError が発生しGherkin構文エラーが報告されること

  # --- Gherkinタグ継承（Effective Tags）---

  Rule: Featureレベルのタグは配下のすべてのScenarioに継承される

    @SPEC-021
    Scenario: Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
      Given Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない
      When  タグマップを取得する
      Then  その仕様タグのエントリにシナリオの情報が紐付けられること

    @SPEC-021
    Scenario: Featureタグを継承したエントリのkeywordはScenarioになる
      Given Feature レベルにのみ仕様タグが付与されている
      When  タグマップを取得する
      Then  tag_map エントリの keyword が "Scenario" または "Scenario Outline" であること

    @SPEC-021
    Scenario: Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
      Given Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている
      And   Rule 配下のシナリオにはタグが付いていない
      When  タグマップを取得する
      Then  そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること

    @SPEC-021
    Scenario: シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
      Given Feature レベルに仕様タグ A が付与されている
      And   配下のシナリオに直接 仕様タグ B が付与されている
      When  タグマップを取得する
      Then  そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること

    @SPEC-021
    Scenario: Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
      Given Scenario Outline に仕様タグ A が付与されている
      And   いずれかの Examples テーブルに仕様タグ B が付与されている
      When  タグマップを取得する
      Then  仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること

    @SPEC-021
    Scenario: プレフィックスフィルタはEffective Tags算出後に適用される
      Given Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている
      When  プレフィックス "SPEC" でタグマップを取得する
      Then  "SPEC-001" のみがタグマップに含まれ "REQ-001" は含まれないこと

```
</details>