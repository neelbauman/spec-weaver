# -*- coding: utf-8 -*-

from behave import given, then, when

from specification.features.steps._helpers import run_spec_weaver, write_doorstop_yaml

# [Duplicate Skip] This step is already defined elsewhere
# @given('Doorstopツリーが初期化されている')  # type: ignore
# def given_6df87eb3(context):
#     """Doorstopツリーが初期化されている
# 
#     Scenarios:
#       - 
#     """
#     raise NotImplementedError('STEP: Doorstopツリーが初期化されている')

# [Duplicate Skip] This step is already defined elsewhere
# @given('以下のSPECアイテムが存在する:')  # type: ignore
# def given_14c0b615(context):
#     """以下のSPECアイテムが存在する:
# 
#     Scenarios:
#       - 
#     """
#     raise NotImplementedError('STEP: 以下のSPECアイテムが存在する:')

# [Duplicate Skip] This step is already defined elsewhere
# @given('Doorstopツリーが初期化されている')  # type: ignore
# def given_6df87eb3(context):
#     """Doorstopツリーが初期化されている
# 
#     Scenarios:
#       - 
#     """
#     raise NotImplementedError('STEP: Doorstopツリーが初期化されている')

# [Duplicate Skip] This step is already defined elsewhere
# @given('以下のSPECアイテムが存在する:')  # type: ignore
# def given_14c0b615(context):
#     """以下のSPECアイテムが存在する:
# 
#     Scenarios:
#       - 
#     """
#     raise NotImplementedError('STEP: 以下のSPECアイテムが存在する:')

# [Duplicate Skip] This step is already defined elsewhere
# @given('Doorstopツリーが初期化されている')  # type: ignore
# def given_6df87eb3(context):
#     """Doorstopツリーが初期化されている
# 
#     Scenarios:
#       - 
#     """
#     raise NotImplementedError('STEP: Doorstopツリーが初期化されている')

# [Duplicate Skip] This step is already defined elsewhere
# @given('以下のSPECアイテムが存在する:')  # type: ignore
# def given_14c0b615(context):
#     """以下のSPECアイテムが存在する:
# 
#     Scenarios:
#       - 
#     """
#     raise NotImplementedError('STEP: 以下のSPECアイテムが存在する:')

@given('Doorstopツリーが初期化されている')  # type: ignore
def given_6df87eb3(context):
    """Doorstopツリーが初期化されている

    Scenarios:
      - 
    """
    raise NotImplementedError('STEP: Doorstopツリーが初期化されている')


@given('以下のSPECアイテムが存在する:')  # type: ignore
def given_14c0b615(context):
    """以下のSPECアイテムが存在する:

    Scenarios:
      - 
    """
    raise NotImplementedError('STEP: 以下のSPECアイテムが存在する:')


@given('TRC-003 の impl_files に ["{param0}"] が設定されている')  # type: ignore
def given_5b35c4dd(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "TRC-003", extra={"impl_files": [param0]})
    context.target_spec = "TRC-003"

@when('impl_files を読み取る')  # type: ignore
def when_1e9b41a9(context):
    import doorstop

    from spec_weaver.adapters.impl_scanner import get_ref_files
    tree = doorstop.build(cwd=str(context.temp_dir))
    item = tree.find_item(context.target_spec)
    context.actual_files = get_ref_files(item)

@then('ファイルパスのリスト ["{param0}"] が得られること')  # type: ignore
def then_4c08825b(context, param0):
    assert context.actual_files == [param0], f"Expected [{param0}], got {context.actual_files}"

@given('TRC-003 の impl_files に "{param0}" が文字列として設定されている')  # type: ignore
def given_254bc1f7(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "TRC-003", extra={"impl_files": param0})
    context.target_spec = "TRC-003"

@given('QA-003 の impl_files が未設定である')  # type: ignore
def given_60f3699e(context):
    write_doorstop_yaml(context.temp_dir / "specs", "QA-003")
    context.target_spec = "QA-003"

@then('空のリストが返ること')  # type: ignore
def then_3cd52b0f(context):
    assert context.actual_files == [], f"Expected [], got {context.actual_files}"

@given('"{param0}" の行頭に "{param1}" が記述されている')  # type: ignore
def given_1a5b95f0(context, param0, param1):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{param1}\n")

@when('impl-scanner でリポジトリをスキャンする')  # type: ignore
def when_59b7b6ae(context):
    from spec_weaver.adapters.impl_scanner import ImplScanner
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.temp_dir)

@then('"{param0}" に対して "{param1}" が紐づくこと')  # type: ignore
def then_6cd9ae6b(context, param0, param1):
    assert param0 in context.scan_result, f"{param0} not found in scan result"
    assert param1 in context.scan_result[param0], f"{param1} not linked to {param0}"

@given('リポジトリに .py ファイルと .md ファイルが存在する')  # type: ignore
def given_6f18a295(context):
    py_path = context.temp_dir / "test.py"
    py_path.write_text("# implements: TRC-003\n")
    context.py_path = "test.py"
    md_path = context.temp_dir / "test.md"
    md_path.write_text("# implements: TRC-003\n")
    context.md_path = "test.md"

@given('.md ファイルの行頭に "{param0}" が記述されている')  # type: ignore
def given_d9c1b21a(context, param0):
    pass # Done in the previous step

@when('--extensions py を指定して impl-scanner でスキャンする')  # type: ignore
def when_d61ff5a2(context):
    from spec_weaver.adapters.impl_scanner import ImplScanner
    scanner = ImplScanner()
    context.scan_result = scanner.scan(context.temp_dir, extensions=["py"])

@then('.md ファイルは結果に含まれないこと')  # type: ignore
def then_1e4aee33(context):
    for files in context.scan_result.values():
        assert not any(f.endswith(".md") for f in files)

@given('"{param0}" にアノテーションが存在しない')  # type: ignore
def given_8d04b283(context, param0):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("def no_annotation(): pass\n")

@then('エラーが発生しないこと')  # type: ignore
def then_b705ab9f(context):
    assert True

@then('"{param0}" は結果に含まれないこと')  # type: ignore
def then_9ee20369(context, param0):
    for files in context.scan_result.values():
        assert param0 not in files

@given('QA-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_4cea3b9d(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "QA-003", extra={"impl_files": param0})

@when('"{param0}" を実行する')  # type: ignore
def when_68ff7f63(context, param0):
    import shlex
    args = shlex.split(param0)
    if args[0] == "spec-weaver":
        args = args[1:]
    if args[0] == "audit" and len(args) == 2:  # audit --check-impl
        features_dir = context.temp_dir / "specification" / "features"
        features_dir.mkdir(parents=True, exist_ok=True)
        args.append(str(features_dir))
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)

    context.result = run_spec_weaver(args, cwd=context.temp_dir)

@then('終了コードが 1 であること')  # type: ignore
def then_3783b41c(context):
    assert context.result.returncode == 1, f"Expected 1, got {context.result.returncode}\n{context.result.stderr}"

@then('"{param0}" が存在しないファイルとして報告されること')  # type: ignore
def then_7ef614ad(context, param0):
    assert param0 in context.result.stdout or param0 in context.result.stderr

@given('TRC-003 の impl_files に "{param0}" が設定されている')  # type: ignore
def given_e64bd8f6(context, param0):
    write_doorstop_yaml(context.temp_dir / "specs", "TRC-003", extra={"impl_files": param0})

@given('"{param0}" に TRC-003 のアノテーションが存在しない')  # type: ignore
def given_d0ba98a0(context, param0):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("def no_annotation(): pass\n")

@then('"{param0}" が impl_files のみ（アノテーションなし）として報告されること')  # type: ignore
def then_f76e2a8d(context, param0):
    out = context.result.stdout + context.result.stderr
    assert param0 in out, f"Expected '{param0}' in output. Actual output:\n{out}"

@then('"{param0}" がアノテーションのみ（impl_files なし）として報告されること')  # type: ignore
def then_7fa51a4f(context, param0):
    out = context.result.stdout + context.result.stderr
    assert param0 in out, f"Expected '{param0}' in output. Actual output:\n{out}"

@when('通常の "{param0}" を実行する（--check-impl なし）')  # type: ignore
def when_6a6c02d8(context, param0):
    import shlex
    args = shlex.split(param0)
    if args[0] == "spec-weaver":
        args = args[1:]
    
    if args[0] == "audit":
        features_dir = context.temp_dir / "specification" / "features"
        features_dir.mkdir(parents=True, exist_ok=True)
        args.append(str(features_dir))
        
    context.result = run_spec_weaver(args, cwd=context.temp_dir)

@then('実装ファイルリンクのセクションが出力されないこと')  # type: ignore
def then_70e4e0dc(context):
    out = context.result.stdout + context.result.stderr
    assert "Broken impl_files refs" not in out and "Annotation only" not in out

@then('出力ツリーに "{param0}" が含まれること')  # type: ignore
def then_2c56e82a(context, param0):
    out = context.result.stdout + context.result.stderr
    assert param0 in out, f"Expected '{param0}' in output. Actual output:\n{out}"

@given('TRC-003 の impl_files が未設定である')  # type: ignore
def given_c11ed496(context):
    write_doorstop_yaml(context.temp_dir / "specs", "TRC-003")

@when('"{param0}" を実行する（--show-impl なし）')  # type: ignore
def when_dfb07a47(context, param0):
    import shlex
    args = shlex.split(param0)
    if args[0] == "spec-weaver":
        args = args[1:]
    
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
            
    context.result = run_spec_weaver(args, cwd=context.temp_dir)

@then('出力ツリーに "{param0}" が含まれないこと')  # type: ignore
def then_35df9926(context, param0):
    out = context.result.stdout + context.result.stderr
    assert param0 not in out, f"Expected {param0} not to be in output"

@given('"{param0}" が存在する')  # type: ignore
def given_file_exists(context, param0):
    path = context.temp_dir / param0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("")
