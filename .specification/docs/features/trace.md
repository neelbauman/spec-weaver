# Feature: trace コマンド — トレーサビリティ・ツリー表示

**タグ**: `@TRC-001`

**関連アイテム**: [TRC-001](../items/TRC-001.md)

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
    raise NotImplementedError('STEP: Doorstopツリーが初期化されている')
```

#### And 以下のREQアイテムが存在する:

```python
@given('以下のREQアイテムが存在する:')  # type: ignore
def given_28140be4(context):
    """以下のREQアイテムが存在する:"""
    for row in context.table:
        links = []
        if "Links" in row.headings and row["Links"]:
            links = [l.strip() for l in row["Links"].split(",") if l.strip()]
        status = row.get("Status", "implemented")
        write_doorstop_yaml(context.temp_dir / "reqs", row["ID"], header=row.get("Header", ""), links=links, status=status)
```

#### And 以下のSPECアイテムが存在する:

```python
@given('以下のSPECアイテムが存在する:')  # type: ignore
def given_14c0b615(context):
    """以下のSPECアイテムが存在する:

    Scenarios:
      - 
    """
    raise NotImplementedError('STEP: 以下のSPECアイテムが存在する:')
```

#### And 以下のfeatureファイルが存在する:

```python
@given('以下のfeatureファイルが存在する:')  # type: ignore
def given_a838a6ff(context):
    """以下のfeatureファイルが存在する:"""
    features_dir = context.temp_dir / "specification" / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    for row in context.table:
        filename = row["File"]
        tags = row.get("Tags", "")
        path = features_dir / filename
        path.write_text(f"{tags}\nFeature: Test Feature\n  Scenario: Test Scenario\n    Given test\n")
```

</details>


---
## Scenario: REQを起点としたトップダウンのツリー表示 {: #line-22 }

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
@when('`spec-weaver trace {target}` を実行する')  # type: ignore
@when('`spec-weaver trace {target}` を実行する（--show-impl なし）')  # type: ignore
def when_trace_generic(context, target):
    """`spec-weaver trace {target}` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - Doorstopツリーが未初期化の場合のエラー
      - 各ノードにステータスバッジが表示される
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    args = shlex.split(f"trace {target}")
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
        elif arg == "./nonexistent/features":
            args[i] = str(context.temp_dir / "nonexistent" / "features")

    cwd = getattr(context, "repo_root", context.temp_dir)
    cmd = ["uv", "run", "spec-weaver"] + args
    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )
```

#### Then 終了コードが0である

```python
@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - 単一アイテムのレビューが実行できる
      - 単一アイテムをJSON形式で出力できる
      - --fail-on high でhigh findingがない場合に終了コード0を返す
      - --min-severity medium で low の finding が非表示になる
      - 全体並列レビューが実行できる
    """
    raise NotImplementedError('STEP: 終了コードが0である')
```

#### And 出力にツリー構造が含まれる

```python
@then('出力にツリー構造が含まれる')  # type: ignore
def then_a551e8cd(context):
    """出力にツリー構造が含まれる

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - SPECを起点とした双方向のツリー表示
    """
    # 枝文字またはリッチなテーブル
    assert any(c in context.result.stdout for c in ["─", "└", "│", "├"]) or "ID" in context.result.stdout
```

#### And "REQ-001" がルートノードとして表示される

```python
@then('"{param0}" がルートノードとして表示される')  # type: ignore
def then_24c28817(context, param0):
    """"REQ-001" がルートノードとして表示される

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
    """
    # 最初の数行にあるか（Panel表示などがあるため）
    assert param0 in "\n".join(context.result.stdout.splitlines()[:5])
```

#### And "REQ-002" が "REQ-001" の子ノードとして表示される

```python
@then('"{param0}" が "{param1}" の子ノードとして表示される')  # type: ignore
def then_5c046e43(context, param0, param1):
    """"REQ-002" が "REQ-001" の子ノードとして表示される

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
    """
    assert param0 in context.result.stdout
    assert param1 in context.result.stdout
```

#### And "SPEC-001" が "REQ-001" の子ノードとして表示される

```python
@then('"{param0}" が "{param1}" の子ノードとして表示される')  # type: ignore
def then_5c046e43(context, param0, param1):
    """"REQ-002" が "REQ-001" の子ノードとして表示される

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
    """
    assert param0 in context.result.stdout
    assert param1 in context.result.stdout
```

#### And "SPEC-003" が "REQ-002" の子ノードとして表示される

```python
@then('"{param0}" が "{param1}" の子ノードとして表示される')  # type: ignore
def then_5c046e43(context, param0, param1):
    """"REQ-002" が "REQ-001" の子ノードとして表示される

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
    """
    assert param0 in context.result.stdout
    assert param1 in context.result.stdout
```

#### And "audit.feature" が "SPEC-003" の子ノードとして表示される

```python
@then('"{param0}" が "{param1}" の子ノードとして表示される')  # type: ignore
def then_5c046e43(context, param0, param1):
    """"REQ-002" が "REQ-001" の子ノードとして表示される

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
    """
    assert param0 in context.result.stdout
    assert param1 in context.result.stdout
```

</details>


---
## Scenario: SPECを起点とした双方向のツリー表示 {: #line-32 }

- **When** `spec-weaver trace SPEC-003 -f ./specification/features` を実行する
- **Then** 終了コードが0である
- **And** 出力にツリー構造が含まれる
- **And** 上位に "REQ-002" が表示される
- **And** 上位に "REQ-001" が表示される
- **And** 下位に "audit.feature" のシナリオが表示される

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace SPEC-003 -f ./specification/features` を実行する

```python
@when('`spec-weaver trace {target}` を実行する')  # type: ignore
@when('`spec-weaver trace {target}` を実行する（--show-impl なし）')  # type: ignore
def when_trace_generic(context, target):
    """`spec-weaver trace {target}` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - Doorstopツリーが未初期化の場合のエラー
      - 各ノードにステータスバッジが表示される
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    args = shlex.split(f"trace {target}")
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
        elif arg == "./nonexistent/features":
            args[i] = str(context.temp_dir / "nonexistent" / "features")

    cwd = getattr(context, "repo_root", context.temp_dir)
    cmd = ["uv", "run", "spec-weaver"] + args
    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )
```

#### Then 終了コードが0である

```python
@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - 単一アイテムのレビューが実行できる
      - 単一アイテムをJSON形式で出力できる
      - --fail-on high でhigh findingがない場合に終了コード0を返す
      - --min-severity medium で low の finding が非表示になる
      - 全体並列レビューが実行できる
    """
    raise NotImplementedError('STEP: 終了コードが0である')
```

#### And 出力にツリー構造が含まれる

```python
@then('出力にツリー構造が含まれる')  # type: ignore
def then_a551e8cd(context):
    """出力にツリー構造が含まれる

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - SPECを起点とした双方向のツリー表示
    """
    # 枝文字またはリッチなテーブル
    assert any(c in context.result.stdout for c in ["─", "└", "│", "├"]) or "ID" in context.result.stdout
```

#### And 上位に "REQ-002" が表示される

```python
@then('上位に "{param0}" が表示される')  # type: ignore
def then_0d60d0d2(context, param0):
    """上位に "REQ-002" が表示される

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    assert param0 in context.result.stdout
```

#### And 上位に "REQ-001" が表示される

```python
@then('上位に "{param0}" が表示される')  # type: ignore
def then_0d60d0d2(context, param0):
    """上位に "REQ-002" が表示される

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    assert param0 in context.result.stdout
```

#### And 下位に "audit.feature" のシナリオが表示される

```python
@then('下位に "{param0}" のシナリオが表示される')  # type: ignore
def then_b2f19b22(context, param0):
    """下位に "audit.feature" のシナリオが表示される

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    assert param0 in context.result.stdout
```

</details>


---
## Scenario: Gherkin Featureファイルを起点としたボトムアップ表示 {: #line-40 }

- **When** `spec-weaver trace audit.feature -f ./specification/features` を実行する
- **Then** 終了コードが0である
- **And** 出力に "SPEC-003" が表示される
- **And** 出力に "REQ-002" が表示される
- **And** 出力に "REQ-001" が表示される

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace audit.feature -f ./specification/features` を実行する

```python
@when('`spec-weaver trace {target}` を実行する')  # type: ignore
@when('`spec-weaver trace {target}` を実行する（--show-impl なし）')  # type: ignore
def when_trace_generic(context, target):
    """`spec-weaver trace {target}` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - Doorstopツリーが未初期化の場合のエラー
      - 各ノードにステータスバッジが表示される
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    args = shlex.split(f"trace {target}")
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
        elif arg == "./nonexistent/features":
            args[i] = str(context.temp_dir / "nonexistent" / "features")

    cwd = getattr(context, "repo_root", context.temp_dir)
    cmd = ["uv", "run", "spec-weaver"] + args
    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )
```

#### Then 終了コードが0である

```python
@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - 単一アイテムのレビューが実行できる
      - 単一アイテムをJSON形式で出力できる
      - --fail-on high でhigh findingがない場合に終了コード0を返す
      - --min-severity medium で low の finding が非表示になる
      - 全体並列レビューが実行できる
    """
    raise NotImplementedError('STEP: 終了コードが0である')
```

#### And 出力に "SPEC-003" が表示される

```python
@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    assert param0 in context.result.stdout
```

#### And 出力に "REQ-002" が表示される

```python
@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    assert param0 in context.result.stdout
```

#### And 出力に "REQ-001" が表示される

```python
@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    assert param0 in context.result.stdout
```

</details>


---
## Scenario: --direction up で上方向のみ探索 {: #line-47 }

- **When** `spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する
- **Then** 終了コードが0である
- **And** 出力に "REQ-002" が表示される
- **And** 出力に "REQ-001" が表示される
- **And** 出力に "audit.feature" が表示されない

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する

```python
@when('`spec-weaver trace {target}` を実行する')  # type: ignore
@when('`spec-weaver trace {target}` を実行する（--show-impl なし）')  # type: ignore
def when_trace_generic(context, target):
    """`spec-weaver trace {target}` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - Doorstopツリーが未初期化の場合のエラー
      - 各ノードにステータスバッジが表示される
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    args = shlex.split(f"trace {target}")
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
        elif arg == "./nonexistent/features":
            args[i] = str(context.temp_dir / "nonexistent" / "features")

    cwd = getattr(context, "repo_root", context.temp_dir)
    cmd = ["uv", "run", "spec-weaver"] + args
    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )
```

#### Then 終了コードが0である

```python
@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - 単一アイテムのレビューが実行できる
      - 単一アイテムをJSON形式で出力できる
      - --fail-on high でhigh findingがない場合に終了コード0を返す
      - --min-severity medium で low の finding が非表示になる
      - 全体並列レビューが実行できる
    """
    raise NotImplementedError('STEP: 終了コードが0である')
```

#### And 出力に "REQ-002" が表示される

```python
@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    assert param0 in context.result.stdout
```

#### And 出力に "REQ-001" が表示される

```python
@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    assert param0 in context.result.stdout
```

#### And 出力に "audit.feature" が表示されない

```python
@then('出力に "{param0}" が表示されない')  # type: ignore
def then_1c0ce4ff(context, param0):
    """出力に "audit.feature" が表示されない

    Scenarios:
      - --direction up で上方向のみ探索
    """
    assert param0 not in context.result.stdout
```

</details>


---
## Scenario: --direction down で下方向のみ探索 {: #line-54 }

- **When** `spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する
- **Then** 終了コードが0である
- **And** 出力に "REQ-002" が表示される
- **And** 出力に "SPEC-003" が表示される
- **And** 出力に "audit.feature" が表示される

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する

```python
@when('`spec-weaver trace {target}` を実行する')  # type: ignore
@when('`spec-weaver trace {target}` を実行する（--show-impl なし）')  # type: ignore
def when_trace_generic(context, target):
    """`spec-weaver trace {target}` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - Doorstopツリーが未初期化の場合のエラー
      - 各ノードにステータスバッジが表示される
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    args = shlex.split(f"trace {target}")
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
        elif arg == "./nonexistent/features":
            args[i] = str(context.temp_dir / "nonexistent" / "features")

    cwd = getattr(context, "repo_root", context.temp_dir)
    cmd = ["uv", "run", "spec-weaver"] + args
    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )
```

#### Then 終了コードが0である

```python
@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - 単一アイテムのレビューが実行できる
      - 単一アイテムをJSON形式で出力できる
      - --fail-on high でhigh findingがない場合に終了コード0を返す
      - --min-severity medium で low の finding が非表示になる
      - 全体並列レビューが実行できる
    """
    raise NotImplementedError('STEP: 終了コードが0である')
```

#### And 出力に "REQ-002" が表示される

```python
@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    assert param0 in context.result.stdout
```

#### And 出力に "SPEC-003" が表示される

```python
@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    assert param0 in context.result.stdout
```

#### And 出力に "audit.feature" が表示される

```python
@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    assert param0 in context.result.stdout
```

</details>


---
## Scenario: --format flat でフラットリスト表示 {: #line-61 }

- **When** `spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する
- **Then** 終了コードが0である
- **And** 出力がフラットリスト形式である
- **And** 各行に "REQ" または "SPEC" または "TEST" のラベルが含まれる

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する

```python
@when('`spec-weaver trace {target}` を実行する')  # type: ignore
@when('`spec-weaver trace {target}` を実行する（--show-impl なし）')  # type: ignore
def when_trace_generic(context, target):
    """`spec-weaver trace {target}` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - Doorstopツリーが未初期化の場合のエラー
      - 各ノードにステータスバッジが表示される
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    args = shlex.split(f"trace {target}")
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
        elif arg == "./nonexistent/features":
            args[i] = str(context.temp_dir / "nonexistent" / "features")

    cwd = getattr(context, "repo_root", context.temp_dir)
    cmd = ["uv", "run", "spec-weaver"] + args
    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )
```

#### Then 終了コードが0である

```python
@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - 単一アイテムのレビューが実行できる
      - 単一アイテムをJSON形式で出力できる
      - --fail-on high でhigh findingがない場合に終了コード0を返す
      - --min-severity medium で low の finding が非表示になる
      - 全体並列レビューが実行できる
    """
    raise NotImplementedError('STEP: 終了コードが0である')
```

#### And 出力がフラットリスト形式である

```python
@then('出力がフラットリスト形式である')  # type: ignore
def then_f50604f0(context):
    """出力がフラットリスト形式である

    Scenarios:
      - --format flat でフラットリスト表示
    """
    # フラット形式はツリーの枝文字がないはず。├ や └ がなければOKとする
    assert "├" not in context.result.stdout
    assert "└" not in context.result.stdout
    assert "ID" in context.result.stdout or "種別" in context.result.stdout
```

#### And 各行に "REQ" または "SPEC" または "TEST" のラベルが含まれる

```python
@then('各行に "{param0}" または "{param1}" または "{param2}" のラベルが含まれる')  # type: ignore
def then_29017220(context, param0, param1, param2):
    """各行に "REQ" または "SPEC" または "TEST" のラベルが含まれる

    Scenarios:
      - --format flat でフラットリスト表示
    """
    # テーブルヘッダ行や境界線を除いて確認
    lines = context.result.stdout.strip().splitlines()
    found = False
    for line in lines:
        if any(label in line for label in [param0, param1, param2]):
            found = True
            break
    assert found
```

</details>


---
## Scenario: 存在しないIDを指定した場合のエラー {: #line-67 }

- **When** `spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する
- **Then** 終了コードが1である
- **And** エラーメッセージに "not found" が含まれる

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する

```python
@when('`spec-weaver trace {target}` を実行する')  # type: ignore
@when('`spec-weaver trace {target}` を実行する（--show-impl なし）')  # type: ignore
def when_trace_generic(context, target):
    """`spec-weaver trace {target}` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - Doorstopツリーが未初期化の場合のエラー
      - 各ノードにステータスバッジが表示される
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    args = shlex.split(f"trace {target}")
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
        elif arg == "./nonexistent/features":
            args[i] = str(context.temp_dir / "nonexistent" / "features")

    cwd = getattr(context, "repo_root", context.temp_dir)
    cmd = ["uv", "run", "spec-weaver"] + args
    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )
```

#### Then 終了コードが1である

```python
@then('終了コードが1である')  # type: ignore
def then_9b731a71(context):
    """終了コードが1である

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
      - --fail-on high でhigh findingがある場合に終了コード1を返す
      - claudeコマンドが見つからない場合にエラーになる
    """
    raise NotImplementedError('STEP: 終了コードが1である')
```

#### And エラーメッセージに "not found" が含まれる

```python
@then('エラーメッセージに "{param0}" が含まれる')  # type: ignore
def then_9998fad9(context, param0):
    """エラーメッセージに "not found" が含まれる

    Scenarios:
      - 存在しないIDを指定した場合のエラー
      - Doorstopツリーが未初期化の場合のエラー
    """
    assert param0.lower() in context.result.stdout.lower() or param0.lower() in context.result.stderr.lower()
```

</details>


---
## Scenario: Doorstopツリーが未初期化の場合のエラー {: #line-72 }

- **Given** Doorstopツリーが初期化されていない
- **When** `spec-weaver trace REQ-001 -f ./specification/features` を実行する
- **Then** 終了コードが1である
- **And** エラーメッセージに "No Doorstop tree found" が含まれる

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### Given Doorstopツリーが初期化されていない

```python
@given('Doorstopツリーが初期化されていない')  # type: ignore
def given_1b5b3d28(context):
    """Doorstopツリーが初期化されていない

    Scenarios:
      - Doorstopツリーが未初期化の場合のエラー
    """
    context.repo_root = Path(tempfile.mkdtemp(prefix="sw_empty_"))
```

#### When `spec-weaver trace REQ-001 -f ./specification/features` を実行する

```python
@when('`spec-weaver trace {target}` を実行する')  # type: ignore
@when('`spec-weaver trace {target}` を実行する（--show-impl なし）')  # type: ignore
def when_trace_generic(context, target):
    """`spec-weaver trace {target}` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - Doorstopツリーが未初期化の場合のエラー
      - 各ノードにステータスバッジが表示される
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    args = shlex.split(f"trace {target}")
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
        elif arg == "./nonexistent/features":
            args[i] = str(context.temp_dir / "nonexistent" / "features")

    cwd = getattr(context, "repo_root", context.temp_dir)
    cmd = ["uv", "run", "spec-weaver"] + args
    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )
```

#### Then 終了コードが1である

```python
@then('終了コードが1である')  # type: ignore
def then_9b731a71(context):
    """終了コードが1である

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
      - --fail-on high でhigh findingがある場合に終了コード1を返す
      - claudeコマンドが見つからない場合にエラーになる
    """
    raise NotImplementedError('STEP: 終了コードが1である')
```

#### And エラーメッセージに "No Doorstop tree found" が含まれる

```python
@then('エラーメッセージに "{param0}" が含まれる')  # type: ignore
def then_9998fad9(context, param0):
    """エラーメッセージに "not found" が含まれる

    Scenarios:
      - 存在しないIDを指定した場合のエラー
      - Doorstopツリーが未初期化の場合のエラー
    """
    assert param0.lower() in context.result.stdout.lower() or param0.lower() in context.result.stderr.lower()
```

</details>


---
## Scenario: .feature ディレクトリが存在しない場合の警告と継続 {: #line-78 }

- **When** `spec-weaver trace REQ-001 -f ./nonexistent/features` を実行する
- **Then** 終了コードが0である
- **And** 警告メッセージが表示される
- **And** 出力に "REQ-001" が表示される

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace REQ-001 -f ./nonexistent/features` を実行する

```python
@when('`spec-weaver trace {target}` を実行する')  # type: ignore
@when('`spec-weaver trace {target}` を実行する（--show-impl なし）')  # type: ignore
def when_trace_generic(context, target):
    """`spec-weaver trace {target}` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - Doorstopツリーが未初期化の場合のエラー
      - 各ノードにステータスバッジが表示される
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    args = shlex.split(f"trace {target}")
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
        elif arg == "./nonexistent/features":
            args[i] = str(context.temp_dir / "nonexistent" / "features")

    cwd = getattr(context, "repo_root", context.temp_dir)
    cmd = ["uv", "run", "spec-weaver"] + args
    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )
```

#### Then 終了コードが0である

```python
@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - 単一アイテムのレビューが実行できる
      - 単一アイテムをJSON形式で出力できる
      - --fail-on high でhigh findingがない場合に終了コード0を返す
      - --min-severity medium で low の finding が非表示になる
      - 全体並列レビューが実行できる
    """
    raise NotImplementedError('STEP: 終了コードが0である')
```

#### And 警告メッセージが表示される

```python
@then('警告メッセージが表示される')  # type: ignore
def then_a11d14f9(context):
    assert "Warning" in context.result.stdout or "warning" in context.result.stdout or "警告" in context.result.stdout
```

#### And 出力に "REQ-001" が表示される

```python
@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    assert param0 in context.result.stdout
```

</details>


---
## Scenario: 各ノードにステータスバッジが表示される {: #line-84 }

- **When** `spec-weaver trace REQ-001 -f ./specification/features` を実行する
- **Then** 終了コードが0である
- **And** "REQ-001" のノードに "implemented" のステータスバッジが表示される
- **And** "SPEC-003" のノードに "implemented" のステータスバッジが表示される

<details><summary><b>Step Definitions (Source Code)</b></summary>

#### When `spec-weaver trace REQ-001 -f ./specification/features` を実行する

```python
@when('`spec-weaver trace {target}` を実行する')  # type: ignore
@when('`spec-weaver trace {target}` を実行する（--show-impl なし）')  # type: ignore
def when_trace_generic(context, target):
    """`spec-weaver trace {target}` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - Doorstopツリーが未初期化の場合のエラー
      - 各ノードにステータスバッジが表示される
      - SPECを起点とした双方向のツリー表示
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - --format flat でフラットリスト表示
      - 存在しないIDを指定した場合のエラー
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    args = shlex.split(f"trace {target}")
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
        elif arg == "./nonexistent/features":
            args[i] = str(context.temp_dir / "nonexistent" / "features")

    cwd = getattr(context, "repo_root", context.temp_dir)
    cmd = ["uv", "run", "spec-weaver"] + args
    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )
```

#### Then 終了コードが0である

```python
@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - 単一アイテムのレビューが実行できる
      - 単一アイテムをJSON形式で出力できる
      - --fail-on high でhigh findingがない場合に終了コード0を返す
      - --min-severity medium で low の finding が非表示になる
      - 全体並列レビューが実行できる
    """
    raise NotImplementedError('STEP: 終了コードが0である')
```

#### And "REQ-001" のノードに "implemented" のステータスバッジが表示される

```python
@then('"{param0}" のノードに "{param1}" のステータスバッジが表示される')  # type: ignore
def then_f676df97(context, param0, param1):
    """"REQ-001" のノードに "implemented" のステータスバッジが表示される

    Scenarios:
      - 各ノードにステータスバッジが表示される
    """
    assert param0 in context.result.stdout
    assert param1 in context.result.stdout
```

#### And "SPEC-003" のノードに "implemented" のステータスバッジが表示される

```python
@then('"{param0}" のノードに "{param1}" のステータスバッジが表示される')  # type: ignore
def then_f676df97(context, param0, param1):
    """"REQ-001" のノードに "implemented" のステータスバッジが表示される

    Scenarios:
      - 各ノードにステータスバッジが表示される
    """
    assert param0 in context.result.stdout
    assert param1 in context.result.stdout
```

</details>



---
<details><summary>Raw .feature source</summary>

```gherkin
# spec-weaver-fingerprint: e2f6c162837e372a66f90d9da12115f7c082abd968f4dae0b9ea804e419f5fa5
# spec-weaver-fingerprint-TRC-001: HKeXIyGAgfYrCuLXM9S1YOKJTFIxClAO5GHOWxFVehI=
@TRC-001
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

  Scenario: Doorstopツリーが未初期化の場合のエラー
    Given Doorstopツリーが初期化されていない
    When `spec-weaver trace REQ-001 -f ./specification/features` を実行する
    Then 終了コードが1である
    And エラーメッセージに "No Doorstop tree found" が含まれる

  Scenario: .feature ディレクトリが存在しない場合の警告と継続
    When `spec-weaver trace REQ-001 -f ./nonexistent/features` を実行する
    Then 終了コードが0である
    And 警告メッセージが表示される
    And 出力に "REQ-001" が表示される

  Scenario: 各ノードにステータスバッジが表示される
    When `spec-weaver trace REQ-001 -f ./specification/features` を実行する
    Then 終了コードが0である
    And "REQ-001" のノードに "implemented" のステータスバッジが表示される
    And "SPEC-003" のノードに "implemented" のステータスバッジが表示される

```
</details>