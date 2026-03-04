from specification.features.steps._helpers import create_doorstop_project_api, write_feature_file, run_spec_weaver, create_doorstop_project_yaml
"""behave steps for: audit コマンド"""

from behave import given, when, then, step

@given('すべてのtestable仕様に対応するGherkinテストが存在する')  # type: ignore
def given_a7b8516a(context):
    create_doorstop_project_api(
        context.temp_dir,
        req_items=[{"status": "implemented"}],
        spec_items=[{"status": "implemented", "links": ["REQ-001"]}],
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, "@SPEC-001\nFeature: Test\n  Scenario: Test\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)

@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    feature_dir = context.temp_dir / "specification" / "features"
    cmd = ['audit', str(feature_dir)]
    res = run_spec_weaver(cmd, cwd=context.temp_dir)
    context.exit_code = res.returncode
    context.output = res.stdout + '\n' + res.stderr


@then('終了コード 0 が返ること')  # type: ignore
def then_4f25c571(context):
    """終了コード 0 が返ること

    Scenarios:
      - 完全一致で、監査が成功する
    """
    raise NotImplementedError('STEP: 終了コード 0 が返ること')


@then('成功メッセージが表示されること')  # type: ignore
def then_f7642361(context):
    assert "完璧です" in context.output or "Success" in context.output

@given('testable な仕様 "{param0}" に対応するGherkinテストが存在しない')  # type: ignore
def given_03339ad7(context, param0):
    prefix = param0.split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": True}]
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)

@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    assert getattr(context, 'exit_code', 0) == 1, f"Expected exit code 1, but got {context.exit_code}. Output:\n{context.output}"

@then('テストが実装されていない仕様として "{param0}" が報告されること')  # type: ignore
def then_6664aa42(context, param0):
    assert param0 in context.output

@given('Gherkinに仕様書に存在しない "{param0}" タグが含まれている')  # type: ignore
def given_3aa00113(context, param0):
    orphan_prefix = param0.lstrip('@').split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [{"uid": "SPEC-001", "testable": True}]
            },
            {
                "dir": "orphans",
                "prefix": orphan_prefix,
                "parent": "SPEC",
                "items": []
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, f"{param0}\n@SPEC-001\nFeature: Test\n  Scenario: Test\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)

@then('orphanタグとして "{param0}" が報告されること')  # type: ignore
def then_33c30716(context, param0):
    assert param0 in context.output

@given('仕様 "{param0}" のテストが未実装で "{param1}" がorphanタグである')  # type: ignore
def given_ffdcf7f2(context, param0, param1):
    prefix = param0.split("-")[0]
    orphan_prefix = param1.lstrip('@').split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": True}]
            },
            {
                "dir": "orphans",
                "prefix": orphan_prefix,
                "parent": prefix,
                "items": []
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, f"{param1}\nFeature: Test\n  Scenario: Test\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)

@then('テスト漏れとorphanタグの両方が報告されること')  # type: ignore
def then_755ec6da(context):
    assert "Untested Specs" in context.output or "テストが実装されていません" in context.output or "テスト漏れ" in context.output or "Missing" in context.output
    assert "Orphaned Tags" in context.output or "orphan" in context.output.lower() or "存在しない仕様" in context.output

@given('仕様 "{param0}" が testable: false に設定されている')  # type: ignore
def given_624f5f06(context, param0):
    prefix = param0.split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": False}]
            }
        ]
    )

@given('"{param0}" に対応するGherkinテストが存在しない')  # type: ignore
def given_ea690d53(context, param0):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)

@then('"{param0}" はテスト漏れとして報告されないこと')  # type: ignore
def then_55c71a2c(context, param0):
    assert param0 not in context.output

@given('仕様 "{param0}" の上位アイテムが変更されている（cleared=false）')  # type: ignore
def given_db49ffab(context, param0):
    prefix = param0.split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "reqs",
                "prefix": "REQ",
                "items": [{"uid": "REQ-001", "testable": False, "text": "Old text"}]
            },
            {
                "dir": "specs",
                "prefix": prefix,
                "parent": "REQ",
                "items": [{"uid": param0, "testable": True, "links": ["REQ-001"]}]
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, f"@{param0}\nFeature: Test\n  Scenario: Test\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)
    
    req_file = context.temp_dir / "reqs" / "REQ-001.yml"
    with open(req_file, "r") as f_yml:
        content = f_yml.read()
    with open(req_file, "w") as f_yml:
        f_yml.write(content.replace("Old text", "New text"))

@then('Suspect Link テーブルに "{param0}" が報告されること')  # type: ignore
def then_0149339a(context, param0):
    assert param0 in context.output
    assert "Suspect" in context.output or "suspect" in context.output.lower()

@then('変更された上位アイテムのIDが表示されること')  # type: ignore
def then_407500a2(context):
    assert "REQ-001" in context.output

@given('仕様 "{param0}" 自体に未レビューの変更がある（reviewed=false）')  # type: ignore
def given_8ceeca7b(context, param0):
    prefix = param0.split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": True, "text": "Old spec text"}]
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, f"@{param0}\nFeature: Test\n  Scenario: Test\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)
    
    spec_file = context.temp_dir / "specs" / f"{param0}.yml"
    with open(spec_file, "r") as f_yml:
        content = f_yml.read()
    with open(spec_file, "w") as f_yml:
        f_yml.write(content.replace("Old spec text", "New spec text"))

@then('Unreviewed Changes テーブルに "{param0}" が報告されること')  # type: ignore
def then_56101a52(context, param0):
    assert param0 in context.output
    assert "Unreviewed" in context.output or "unreviewed" in context.output.lower()

@given('"{param0}" ファイルのフィンガープリントコメントが現在の内容と一致しない')  # type: ignore
def given_f066bd3a(context, param0):
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [{"uid": "SPEC-001", "testable": True}]
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, "@SPEC-001\nFeature: Test\n  Scenario: Old\n    Given old\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)
    
    with open(f, "r") as f_feat:
        content = f_feat.read()
    with open(f, "w") as f_feat:
        f_feat.write(content.replace("Old", "New").replace("old", "new"))

@then('Unreviewed テーブルに対応する feature ファイル名が表示されること')  # type: ignore
def then_c1e4063b(context):
    assert "test.feature" in context.output
@given('すべてのtestable仕様に対応するGherkinテストが存在する')  # type: ignore
def given_a7b8516a(context):
    """すべてのtestable仕様に対応するGherkinテストが存在する

    Scenarios:
      - 完全一致で、監査が成功する
    """
    raise NotImplementedError('STEP: すべてのtestable仕様に対応するGherkinテストが存在する')


@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する

    Scenarios:
      - 完全一致で、監査が成功する
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - testable: false の仕様はスキップされる
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: audit コマンドを実行する')


@then('終了コード 0 が返ること')  # type: ignore
def then_4f25c571(context):
    """終了コード 0 が返ること

    Scenarios:
      - 完全一致で、監査が成功する
    """
    raise NotImplementedError('STEP: 終了コード 0 が返ること')


@then('成功メッセージが表示されること')  # type: ignore
def then_f7642361(context):
    """成功メッセージが表示されること

    Scenarios:
      - 完全一致で、監査が成功する
    """
    raise NotImplementedError('STEP: 成功メッセージが表示されること')


@given('testable な仕様 "{param0}" に対応するGherkinテストが存在しない')  # type: ignore
def given_03339ad7(context, param0):
    """testable な仕様 "CORE-001" に対応するGherkinテストが存在しない

    Scenarios:
      - テスト漏れの検出
    """
    raise NotImplementedError('STEP: testable な仕様 "{param0}" に対応するGherkinテストが存在しない')


@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    """終了コード 1 が返ること

    Scenarios:
      - テスト漏れの検出
      - orphanタグの検出
      - テスト漏れとorphanタグの同時検出
      - Suspect Link の検出
      - Unreviewed Changes の検出
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: 終了コード 1 が返ること')


@then('テストが実装されていない仕様として "{param0}" が報告されること')  # type: ignore
def then_6664aa42(context, param0):
    """テストが実装されていない仕様として "CORE-001" が報告されること

    Scenarios:
      - テスト漏れの検出
    """
    raise NotImplementedError('STEP: テストが実装されていない仕様として "{param0}" が報告されること')


@given('Gherkinに仕様書に存在しない "{param0}" タグが含まれている')  # type: ignore
def given_3aa00113(context, param0):
    """Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている

    Scenarios:
      - orphanタグの検出
    """
    raise NotImplementedError('STEP: Gherkinに仕様書に存在しない "{param0}" タグが含まれている')


@then('orphanタグとして "{param0}" が報告されること')  # type: ignore
def then_7be6aa31(context, param0):
    """orphanタグとして "@SPEC-999" が報告されること

    Scenarios:
      - orphanタグの検出
    """
    raise NotImplementedError('STEP: orphanタグとして "{param0}" が報告されること')


@given('仕様 "{param0}" のテストが未実装で "{param1}" がorphanタグである')  # type: ignore
def given_f74eb6d0(context, param0, param1):
    """仕様 "CORE-001" のテストが未実装で "@SPEC-999" がorphanタグである

    Scenarios:
      - テスト漏れとorphanタグの同時検出
    """
    raise NotImplementedError('STEP: 仕様 "{param0}" のテストが未実装で "{param1}" がorphanタグである')


@then('テスト漏れとorphanタグの両方が報告されること')  # type: ignore
def then_755ec6da(context):
    """テスト漏れとorphanタグの両方が報告されること

    Scenarios:
      - テスト漏れとorphanタグの同時検出
    """
    raise NotImplementedError('STEP: テスト漏れとorphanタグの両方が報告されること')


@given('仕様 "{param0}" が testable: false に設定されている')  # type: ignore
def given_624f5f06(context, param0):
    """仕様 "SPEC-001" が testable: false に設定されている

    Scenarios:
      - testable: false の仕様はスキップされる
    """
    raise NotImplementedError('STEP: 仕様 "{param0}" が testable: false に設定されている')


@given('"{param0}" に対応するGherkinテストが存在しない')  # type: ignore
def given_ea690d53(context, param0):
    """"SPEC-001" に対応するGherkinテストが存在しない

    Scenarios:
      - testable: false の仕様はスキップされる
    """
    raise NotImplementedError('STEP: "{param0}" に対応するGherkinテストが存在しない')


@then('"{param0}" はテスト漏れとして報告されないこと')  # type: ignore
def then_55c71a2c(context, param0):
    """"SPEC-001" はテスト漏れとして報告されないこと

    Scenarios:
      - testable: false の仕様はスキップされる
    """
    raise NotImplementedError('STEP: "{param0}" はテスト漏れとして報告されないこと')


@given('仕様 "{param0}" の上位アイテムが変更されている（cleared=false）')  # type: ignore
def given_db49ffab(context, param0):
    """仕様 "VIS-005" の上位アイテムが変更されている（cleared=false）

    Scenarios:
      - Suspect Link の検出
    """
    raise NotImplementedError('STEP: 仕様 "{param0}" の上位アイテムが変更されている（cleared=false）')


@then('Suspect Link テーブルに "{param0}" が報告されること')  # type: ignore
def then_0149339a(context, param0):
    """Suspect Link テーブルに "VIS-005" が報告されること

    Scenarios:
      - Suspect Link の検出
    """
    raise NotImplementedError('STEP: Suspect Link テーブルに "{param0}" が報告されること')


@then('変更された上位アイテムのIDが表示されること')  # type: ignore
def then_407500a2(context):
    """変更された上位アイテムのIDが表示されること

    Scenarios:
      - Suspect Link の検出
    """
    raise NotImplementedError('STEP: 変更された上位アイテムのIDが表示されること')


@given('仕様 "{param0}" 自体に未レビューの変更がある（reviewed=false）')  # type: ignore
def given_8ceeca7b(context, param0):
    """仕様 "VIS-005" 自体に未レビューの変更がある（reviewed=false）

    Scenarios:
      - Unreviewed Changes の検出
    """
    raise NotImplementedError('STEP: 仕様 "{param0}" 自体に未レビューの変更がある（reviewed=false）')


@then('Unreviewed Changes テーブルに "{param0}" が報告されること')  # type: ignore
def then_56101a52(context, param0):
    """Unreviewed Changes テーブルに "VIS-005" が報告されること

    Scenarios:
      - Unreviewed Changes の検出
    """
    raise NotImplementedError('STEP: Unreviewed Changes テーブルに "{param0}" が報告されること')


@given('"{param0}" ファイルのフィンガープリントコメントが現在の内容と一致しない')  # type: ignore
def given_f066bd3a(context, param0):
    """".feature" ファイルのフィンガープリントコメントが現在の内容と一致しない

    Scenarios:
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: "{param0}" ファイルのフィンガープリントコメントが現在の内容と一致しない')


@then('Unreviewed テーブルに対応する feature ファイル名が表示されること')  # type: ignore
def then_c1e4063b(context):
    """Unreviewed テーブルに対応する feature ファイル名が表示されること

    Scenarios:
      - feature ファイルが Unreviewed として検出される
    """
    raise NotImplementedError('STEP: Unreviewed テーブルに対応する feature ファイル名が表示されること')
