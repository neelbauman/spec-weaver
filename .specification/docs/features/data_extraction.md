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
@given('Doorstopプロジェクトにアクティブな仕様アイテムが存在する')
def given_a04781e9(context):
    """Doorstopプロジェクトにアクティブな仕様アイテムが存在する"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
```

#### When 仕様ID集合を取得する

```python
@when('仕様ID集合を取得する')
def when_e56707cb(context):
    """仕様ID集合を取得する"""
    from spec_weaver.doorstop import get_specs
    from pathlib import Path
    context.spec_ids = get_specs(Path(context.temp_dir), prefix=None)
```

#### Then アクティブかつtestableな仕様IDのみが返されること

```python
@then('アクティブかつtestableな仕様IDのみが返されること')
def then_6823b180(context):
    """アクティブかつtestableな仕様IDのみが返されること"""
    assert 'SPEC-001' in context.spec_ids
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
@given('Doorstopプロジェクトに active: false のアイテムが存在する')
def given_dccca3dc(context):
    """Doorstopプロジェクトに active: false のアイテムが存在する"""
    import subprocess, os, re
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    path = os.path.join(context.temp_dir, 'specs', 'SPEC-001.yml')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Replace active: true or active: True with active: false
    content = re.sub(r'active:\s*(true|True)', 'active: false', content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
```

#### When 仕様ID集合を取得する

```python
@when('仕様ID集合を取得する')
def when_e56707cb(context):
    """仕様ID集合を取得する"""
    from spec_weaver.doorstop import get_specs
    from pathlib import Path
    context.spec_ids = get_specs(Path(context.temp_dir), prefix=None)
```

#### Then 非アクティブなアイテムは結果に含まれないこと

```python
@then('非アクティブなアイテムは結果に含まれないこと')
def then_99bfaa46(context):
    """非アクティブなアイテムは結果に含まれないこと"""
    assert 'SPEC-001' not in context.spec_ids
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
@given('Doorstopプロジェクトに testable: false のアイテムが存在する')
def given_d534a041(context):
    """Doorstopプロジェクトに testable: false のアイテムが存在する"""
    import subprocess, os
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
    path = os.path.join(context.temp_dir, 'specs', 'SPEC-001.yml')
    with open(path, 'a', encoding='utf-8') as f:
        f.write('testable: false\n')
```

#### When 仕様ID集合を取得する

```python
@when('仕様ID集合を取得する')
def when_e56707cb(context):
    """仕様ID集合を取得する"""
    from spec_weaver.doorstop import get_specs
    from pathlib import Path
    context.spec_ids = get_specs(Path(context.temp_dir), prefix=None)
```

#### Then testable: false のアイテムは結果に含まれないこと

```python
@then('testable: false のアイテムは結果に含まれないこと')
def then_f3fad2a6(context):
    """testable: false のアイテムは結果に含まれないこと"""
    assert 'SPEC-001' not in context.spec_ids
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
@given('DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する')
def given_7f8e9c65(context):
    """DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する"""
    import subprocess
    from helpers import setup_doorstop, create_feature_file, run_cli
    setup_doorstop(context, prefixes=['REQ', 'SPEC'])
    subprocess.run(['doorstop', 'add', 'REQ'], cwd=context.temp_dir, check=True)
    subprocess.run(['doorstop', 'add', 'SPEC'], cwd=context.temp_dir, check=True)
```

#### When プレフィックス "SPEC" で仕様ID集合を取得する

```python
@when('プレフィックス "{param0}" で仕様ID集合を取得する')
def when_1d11bcd6(context, param0):
    """プレフィックスで仕様ID集合を取得する"""
    from spec_weaver.doorstop import get_specs
    from pathlib import Path
    context.spec_ids = get_specs(Path(context.temp_dir), prefix=param0)
```

#### Then SPECプレフィックスのアイテムのみが返されること

```python
@then('SPECプレフィックスのアイテムのみが返されること')
def then_b5f39418(context):
    """SPECプレフィックスのアイテムのみが返されること"""
    assert 'SPEC-001' in context.spec_ids
    assert 'REQ-001' not in context.spec_ids
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
@given('Gherkin .feature ファイルに @SPEC-001 タグが付与されている')
def given_b830a393(context):
    """Gherkin .feature ファイルに @SPEC-001 タグが付与されている"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    create_feature_file(context, 'test.feature', '@SPEC-001\nFeature: Test\n  Scenario: Test\n    Given test')
```

#### When タグ集合を取得する

```python
@when('タグ集合を取得する')
def when_a12b8a55(context):
    """タグ集合を取得する"""
    from spec_weaver.gherkin import get_tags
    from pathlib import Path
    import os
    feature_dir = Path(context.temp_dir) / 'features'
    try:
        # get_tags returns a set of tag names (without @)
        context.tags = get_tags(feature_dir)
    except Exception as e:
        context.exc = e
```

#### Then "SPEC-001" がタグ集合に含まれること

```python
@then('"{param0}" がタグ集合に含まれること')
def then_e8d01468(context, param0):
    """タグ集合に含まれること"""
    assert param0 in context.tags
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
@given('Feature レベルと Scenario レベルに異なるSPECタグが付与されている')
def given_07def24f(context):
    """Feature レベルと Scenario レベルに異なるSPECタグが付与されている"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    create_feature_file(context, 'test.feature', '@SPEC-001\nFeature: Test\n  @SPEC-002\n  Scenario: Test\n    Given test')
```

#### When タグ集合を取得する

```python
@when('タグ集合を取得する')
def when_a12b8a55(context):
    """タグ集合を取得する"""
    from spec_weaver.gherkin import get_tags
    from pathlib import Path
    import os
    feature_dir = Path(context.temp_dir) / 'features'
    try:
        # get_tags returns a set of tag names (without @)
        context.tags = get_tags(feature_dir)
    except Exception as e:
        context.exc = e
```

#### Then 両方のレベルのタグがすべて抽出されること

```python
@then('両方のレベルのタグがすべて抽出されること')
def then_d712dc38(context):
    """両方のレベルのタグがすべて抽出されること"""
    assert 'SPEC-001' in context.tags
    assert 'SPEC-002' in context.tags
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
@given('サブディレクトリに .feature ファイルが存在する')
def given_1427ca58(context):
    """サブディレクトリに .feature ファイルが存在する"""
    import os
    os.makedirs(os.path.join(context.temp_dir, 'features', 'sub'), exist_ok=True)
    with open(os.path.join(context.temp_dir, 'features', 'sub', 'sub.feature'), 'w', encoding='utf-8') as f:
        f.write('@SPEC-003\nFeature: Sub\n  Scenario: Sub\n    Given sub')
```

#### When タグ集合を取得する

```python
@when('タグ集合を取得する')
def when_a12b8a55(context):
    """タグ集合を取得する"""
    from spec_weaver.gherkin import get_tags
    from pathlib import Path
    import os
    feature_dir = Path(context.temp_dir) / 'features'
    try:
        # get_tags returns a set of tag names (without @)
        context.tags = get_tags(feature_dir)
    except Exception as e:
        context.exc = e
```

#### Then サブディレクトリ内のタグも含めて抽出されること

```python
@then('サブディレクトリ内のタグも含めて抽出されること')
def then_1c0ec472(context):
    """サブディレクトリ内のタグも含めて抽出されること"""
    assert 'SPEC-003' in context.tags
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
@given('構文的に不正な .feature ファイルが存在する')
def given_540458bc(context):
    """構文的に不正な .feature ファイルが存在する"""
    from helpers import setup_doorstop, create_feature_file, run_cli
    create_feature_file(context, 'invalid.feature', 'Feature Test')
```

#### When タグ集合を取得する

```python
@when('タグ集合を取得する')
def when_a12b8a55(context):
    """タグ集合を取得する"""
    from spec_weaver.gherkin import get_tags
    from pathlib import Path
    import os
    feature_dir = Path(context.temp_dir) / 'features'
    try:
        # get_tags returns a set of tag names (without @)
        context.tags = get_tags(feature_dir)
    except Exception as e:
        context.exc = e
```

#### Then ValueError が発生しGherkin構文エラーが報告されること

```python
@then('ValueError が発生しGherkin構文エラーが報告されること')
def then_c5d0b4fe(context):
    """ValueError が発生しGherkin構文エラーが報告されること"""
    assert hasattr(context, 'exc')
    assert context.exc is not None
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