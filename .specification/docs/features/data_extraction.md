# Feature: データ抽出基盤

**タグ**: `@CORE-001`

**関連アイテム**: [CORE-001](../items/CORE-001.md) / [CORE-002](../items/CORE-002.md)

Doorstop と Gherkin から仕様データとテストタグを正確に抽出する。

---
## Scenario: Doorstop APIによる仕様ID集合の取得 {: #line-10 }

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
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [
                    {"uid": "SPEC-001", "testable": True, "active": True},
                    {"uid": "SPEC-002", "testable": True, "active": True},
                ],
            }
        ],
    )
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
    context.spec_ids = get_specs(context.temp_dir, prefix=None)
```

#### Then アクティブかつtestableな仕様IDのみが返されること

```python
@then('アクティブかつtestableな仕様IDのみが返されること')  # type: ignore
def then_6823b180(context):
    """アクティブかつtestableな仕様IDのみが返されること

    Scenarios:
      - Doorstop APIによる仕様ID集合の取得
    """
    assert "SPEC-001" in context.spec_ids
    assert "SPEC-002" in context.spec_ids
```

</details>


---
## Scenario: 非アクティブなアイテムの除外 {: #line-15 }

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
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [
                    {"uid": "SPEC-001", "testable": True, "active": True},
                    {"uid": "SPEC-002", "testable": True, "active": False},
                ],
            }
        ],
    )
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
    context.spec_ids = get_specs(context.temp_dir, prefix=None)
```

#### Then 非アクティブなアイテムは結果に含まれないこと

```python
@then('非アクティブなアイテムは結果に含まれないこと')  # type: ignore
def then_99bfaa46(context):
    """非アクティブなアイテムは結果に含まれないこと

    Scenarios:
      - 非アクティブなアイテムの除外
    """
    assert "SPEC-001" in context.spec_ids
    assert "SPEC-002" not in context.spec_ids
```

</details>


---
## Scenario: テスト不可能な仕様の除外 {: #line-20 }

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
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [
                    {"uid": "SPEC-001", "testable": True, "active": True},
                    {"uid": "SPEC-002", "testable": False, "active": True},
                ],
            }
        ],
    )
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
    context.spec_ids = get_specs(context.temp_dir, prefix=None)
```

#### Then testable: false のアイテムは結果に含まれないこと

```python
@then('testable: false のアイテムは結果に含まれないこと')  # type: ignore
def then_f3fad2a6(context):
    """testable: false のアイテムは結果に含まれないこと

    Scenarios:
      - テスト不可能な仕様の除外
    """
    assert "SPEC-001" in context.spec_ids
    assert "SPEC-002" not in context.spec_ids
```

</details>


---
## Scenario: プレフィックスによるフィルタリング {: #line-25 }

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
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "reqs",
                "prefix": "REQ",
                "items": [{"uid": "REQ-001", "testable": False}],
            },
            {
                "dir": "specs",
                "prefix": "SPEC",
                "parent": "REQ",
                "items": [{"uid": "SPEC-001", "testable": True, "links": ["REQ-001"]}],
            },
        ],
    )
```

#### When プレフィックス "SPEC" で仕様ID集合を取得する

```python
@when('プレフィックス "{param0}" で仕様ID集合を取得する')  # type: ignore
def when_1d11bcd6(context, param0):
    """プレフィックス "SPEC" で仕様ID集合を取得する

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    from spec_weaver.doorstop import get_specs
    context.spec_ids = get_specs(context.temp_dir, prefix=param0)
```

#### Then SPECプレフィックスのアイテムのみが返されること

```python
@then('SPECプレフィックスのアイテムのみが返されること')  # type: ignore
def then_b5f39418(context):
    """SPECプレフィックスのアイテムのみが返されること

    Scenarios:
      - プレフィックスによるフィルタリング
    """
    assert all(uid.startswith("SPEC") for uid in context.spec_ids), (
        f"SPEC以外のIDが含まれています: {context.spec_ids}"
    )
    assert "SPEC-001" in context.spec_ids
```

</details>


---
## Scenario: Gherkin ASTからのタグ抽出 {: #line-32 }

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
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        feature_dir / "test.feature",
        "@SPEC-001\nFeature: Test\n  Scenario: S1\n    Given test\n",
    )
    context.feature_dir = feature_dir
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
    from spec_weaver.adapters.gherkin import get_tag_map
    try:
        tag_map = get_tag_map(context.feature_dir, context.temp_dir, {"SPEC", "REQ", "CORE"})
        context.tag_ids = set(tag_map.keys())
        context.tag_error = None
    except ValueError as e:
        context.tag_ids = set()
        context.tag_error = e
```

#### Then "SPEC-001" がタグ集合に含まれること

```python
@then('"{param0}" がタグ集合に含まれること')  # type: ignore
def then_e8d01468(context, param0):
    """"SPEC-001" がタグ集合に含まれること

    Scenarios:
      - Gherkin ASTからのタグ抽出
    """
    assert param0 in context.tag_ids, f"{param0} がタグ集合に含まれていません。タグ: {context.tag_ids}"
```

</details>


---
## Scenario: Feature・Scenario両レベルのタグ抽出 {: #line-37 }

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
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        feature_dir / "test.feature",
        "@SPEC-001\nFeature: Test\n\n  @SPEC-002\n  Scenario: S1\n    Given test\n",
    )
    context.feature_dir = feature_dir
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
    from spec_weaver.adapters.gherkin import get_tag_map
    try:
        tag_map = get_tag_map(context.feature_dir, context.temp_dir, {"SPEC", "REQ", "CORE"})
        context.tag_ids = set(tag_map.keys())
        context.tag_error = None
    except ValueError as e:
        context.tag_ids = set()
        context.tag_error = e
```

#### Then 両方のレベルのタグがすべて抽出されること

```python
@then('両方のレベルのタグがすべて抽出されること')  # type: ignore
def then_d712dc38(context):
    """両方のレベルのタグがすべて抽出されること

    Scenarios:
      - Feature・Scenario両レベルのタグ抽出
    """
    assert "SPEC-001" in context.tag_ids, f"SPEC-001 がタグ集合に含まれていません: {context.tag_ids}"
    assert "SPEC-002" in context.tag_ids, f"SPEC-002 がタグ集合に含まれていません: {context.tag_ids}"
```

</details>


---
## Scenario: サブディレクトリ内のfeatureファイルの再帰探索 {: #line-42 }

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
    feature_dir = context.temp_dir / "features"
    subdir = feature_dir / "sub"
    subdir.mkdir(parents=True, exist_ok=True)
    write_feature_file(
        subdir / "sub.feature",
        "@SPEC-010\nFeature: SubTest\n  Scenario: S1\n    Given test\n",
    )
    context.feature_dir = feature_dir
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
    from spec_weaver.adapters.gherkin import get_tag_map
    try:
        tag_map = get_tag_map(context.feature_dir, context.temp_dir, {"SPEC", "REQ", "CORE"})
        context.tag_ids = set(tag_map.keys())
        context.tag_error = None
    except ValueError as e:
        context.tag_ids = set()
        context.tag_error = e
```

#### Then サブディレクトリ内のタグも含めて抽出されること

```python
@then('サブディレクトリ内のタグも含めて抽出されること')  # type: ignore
def then_1c0ec472(context):
    """サブディレクトリ内のタグも含めて抽出されること

    Scenarios:
      - サブディレクトリ内のfeatureファイルの再帰探索
    """
    assert "SPEC-010" in context.tag_ids, f"SPEC-010 がタグ集合に含まれていません: {context.tag_ids}"
```

</details>


---
## Scenario: Gherkin構文エラーの検出 {: #line-47 }

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
    feature_dir = context.temp_dir / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    # 不正なGherkin構文（Feature キーワードなし、インデント誤り等）
    (feature_dir / "broken.feature").write_text(
        "This is not valid gherkin\n  And there is no feature keyword\n    Invalid stuff\n",
        encoding="utf-8",
    )
    context.feature_dir = feature_dir
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
    from spec_weaver.adapters.gherkin import get_tag_map
    try:
        tag_map = get_tag_map(context.feature_dir, context.temp_dir, {"SPEC", "REQ", "CORE"})
        context.tag_ids = set(tag_map.keys())
        context.tag_error = None
    except ValueError as e:
        context.tag_ids = set()
        context.tag_error = e
```

#### Then ValueError が発生しGherkin構文エラーが報告されること

```python
@then('ValueError が発生しGherkin構文エラーが報告されること')  # type: ignore
def then_c5d0b4fe(context):
    """ValueError が発生しGherkin構文エラーが報告されること

    Scenarios:
      - Gherkin構文エラーの検出
    """
    assert context.tag_error is not None, "ValueError が発生しませんでした"
    assert isinstance(context.tag_error, ValueError), f"ValueError ではなく {type(context.tag_error)} が発生しました"
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: 15d5fb6f482561665a6a41ec38e7d3dff795a95d4f7ab3c2a60a10a322b36fcb
# spec-weaver-fingerprint-CORE-001: HJLpd5cD5tt456G9mN57y5Z4dhnDtpUhGVBTdx00XRk=
# spec-weaver-fingerprint-CORE-002: eTEKht1I_h9S6wF4F2pVW4dUOyI2ti7EwNBY1aAZIPQ=
@CORE-001
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

    @CORE-002
    Scenario: Featureタグのみが付与されたfeatureファイルでScenarioがタグマップに登録される
      Given Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない
      When  タグマップを取得する
      Then  その仕様タグのエントリにシナリオの情報が紐付けられること

    @CORE-002
    Scenario: Featureタグを継承したエントリのkeywordはScenarioになる
      Given Feature レベルにのみ仕様タグが付与されている
      When  タグマップを取得する
      Then  tag_map エントリの keyword が "Scenario" または "Scenario Outline" であること

    @CORE-002
    Scenario: Feature→Rule→Scenarioの多段継承でEffective Tagsが正しく算出される
      Given Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている
      And   Rule 配下のシナリオにはタグが付いていない
      When  タグマップを取得する
      Then  そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること

    @CORE-002
    Scenario: シナリオ自身のタグと継承タグが共存してEffective Tagsを形成する
      Given Feature レベルに仕様タグ A が付与されている
      And   配下のシナリオに直接 仕様タグ B が付与されている
      When  タグマップを取得する
      Then  そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること

    @CORE-002
    Scenario: Scenario Outlineの全ExamplesタグがEffective Tagsに集約される
      Given Scenario Outline に仕様タグ A が付与されている
      And   いずれかの Examples テーブルに仕様タグ B が付与されている
      When  タグマップを取得する
      Then  仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること

    @CORE-002
    Scenario: プレフィックスフィルタはEffective Tags算出後に適用される
      Given Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている
      When  プレフィックス "SPEC" でタグマップを取得する
      Then  "SPEC-001" のみがタグマップに含まれ "REQ-001" は含まれないこと

```
</details>