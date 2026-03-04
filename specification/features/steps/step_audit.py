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


# --- QA-006: layer-aware audit ルール ---

@given('仕様 "{param0}" が "{param1}" かつ "{param2}" に設定されている')  # type: ignore
def given_d902e872(context, param0, param1, param2):
    # param1 = "layer: behavior", param2 = "testable: true"
    prefix = param0.split("-")[0]
    layer_val = param1.split(":")[1].strip() if ":" in param1 else param1
    testable_val = param2.split(":")[1].strip().lower() != "false" if ":" in param2 else True
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": testable_val, "extra": {"layer": layer_val}}]
            }
        ]
    )

@given('"{param0}" に対応するGherkinタグが存在しない')  # type: ignore
def given_b9e6bcbc(context, param0):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    # タグなしのfeatureファイルを作成（または何もしない）
    f = feature_dir / "test.feature"
    if not f.exists():
        write_feature_file(f, "Feature: Test\n  Scenario: S1\n    Given test\n")

@then('"{param0}" が behavior-without-gherkin として報告されること')  # type: ignore
def then_0a2ef35f(context, param0):
    assert param0 in context.output, f"Expected {param0} in output:\n{context.output}"
    assert "behavior-without-gherkin" in context.output.lower() or "Behavior Without Gherkin" in context.output, \
        f"Expected 'Behavior Without Gherkin' section in output:\n{context.output}"

@given('仕様 "{param0}" が "{param1}" に設定されている')  # type: ignore
def given_802bb420(context, param0, param1):
    # param1 = "layer: architecture"
    prefix = param0.split("-")[0]
    layer_val = param1.split(":")[1].strip() if ":" in param1 else param1
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": prefix,
                "items": [{"uid": param0, "testable": True, "extra": {"layer": layer_val}}]
            }
        ]
    )

@given('"{param0}" に対応するGherkinタグが存在する')  # type: ignore
def given_25d0a3d0(context, param0):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, f"@{param0}\nFeature: Test\n  Scenario: S1\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)

@then('"{param0}" が architecture-with-gherkin として警告表示されること')  # type: ignore
def then_c994e63b(context, param0):
    assert param0 in context.output, f"Expected {param0} in output:\n{context.output}"
    assert "architecture-with-gherkin" in context.output.lower() or "Architecture With Gherkin" in context.output, \
        f"Expected 'Architecture With Gherkin' section in output:\n{context.output}"

@then('architecture-with-gherkin は終了コードに影響しないこと')  # type: ignore
def then_9b9cd278(context):
    assert getattr(context, 'exit_code', 1) == 0, \
        f"Expected exit code 0 (architecture-with-gherkin is warning only), got {context.exit_code}. Output:\n{context.output}"

@given('アクティブかつ "{param0}" の仕様に "{param1}" 属性が設定されていない')  # type: ignore
def given_b00764d8(context, param0, param1):
    # param0 = "testable: true", param1 = "layer"
    # layer 属性なし・testable: true のアイテムを作成し、対応するGherkinタグも用意する（untested_specs を避けるため）
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [{"uid": "SPEC-001", "testable": True}]  # layer なし
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, "@SPEC-001\nFeature: Test\n  Scenario: S1\n    Given test\n")
    run_spec_weaver(["review", str(f), "-f", str(feature_dir)], cwd=context.temp_dir)

@then('当該仕様IDが layer-unset として情報表示されること')  # type: ignore
def then_7b421936(context):
    assert "SPEC-001" in context.output, f"Expected SPEC-001 in output:\n{context.output}"
    assert "layer-unset" in context.output.lower() or "Layer Unset" in context.output, \
        f"Expected 'Layer Unset' section in output:\n{context.output}"

@then('layer-unset は終了コードに影響しないこと')  # type: ignore
def then_8cfff823(context):
    assert getattr(context, 'exit_code', 1) == 0, \
        f"Expected exit code 0 (layer-unset is info only), got {context.exit_code}. Output:\n{context.output}"
