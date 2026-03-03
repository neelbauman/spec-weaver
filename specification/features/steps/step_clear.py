# -*- coding: utf-8 -*-
from specification.features.steps._helpers import create_doorstop_project_api, write_feature_file, run_spec_weaver, create_doorstop_project_yaml, write_doorstop_yaml
from behave import given, when, then, step
from pathlib import Path
import yaml
import shlex

# ======================================================================
# Steps
# ======================================================================

@given('仕様アイテム "{param0}" が存在する')  # type: ignore
def given_ddd4e2bc(context, param0):
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
    context.target_item_id = param0


@given('"{param0}" に紐づく Gherkin シナリオが存在する')  # type: ignore
def given_efa9578a(context, param0):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "test.feature"
    write_feature_file(f, f"@{param0}\nFeature: Test\n  Scenario: Test\n    Given test\n")
    context.feature_dir = feature_dir


@when('`spec-weaver clear SPEC-003 --feature-dir ./specification/features` を実行する')  # type: ignore
def when_81d90ca5(context):
    """`spec-weaver clear SPEC-003 --feature-dir ./specification/features` を実行する

    Scenarios:
      - アイテムIDを指定して gherkin_fingerprints を更新できる
    """
    raise NotImplementedError('STEP: `spec-weaver clear SPEC-003 --feature-dir ./specification/features` を実行する')


@given('"{param0}" ファイルに複数の仕様IDタグが含まれる')  # type: ignore
def given_dfa4c4a3(context, param0):
    create_doorstop_project_yaml(
        context.temp_dir,
        [
            {
                "dir": "specs",
                "prefix": "SPEC",
                "items": [
                    {"uid": "SPEC-001", "testable": True},
                    {"uid": "SPEC-002", "testable": True}
                ]
            }
        ]
    )
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    f = feature_dir / "audit.feature"
    write_feature_file(f, "@SPEC-001 @SPEC-002\nFeature: Test\n  Scenario: Test\n    Given test\n")
    context.feature_dir = feature_dir


@when('`spec-weaver clear specification/features/audit.feature --feature-dir ./specification/features` を実行する')  # type: ignore
def when_f5108e70(context):
    """`spec-weaver clear specification/features/audit.feature --feature-dir ./specification/features` を実行する

    Scenarios:
      - .feature ファイルを指定して複数アイテムの gherkin_fingerprints を一括更新できる
      - .feature ファイルを指定してファイル自身の suspect 状態も解除できる
    """
    raise NotImplementedError('STEP: `spec-weaver clear specification/features/audit.feature --feature-dir ./specification/features` を実行する')


@when('`spec-weaver clear {target}` を実行する')  # type: ignore
def when_clear_generic(context, target):
    args = shlex.split(f"clear {target}")
    # Ensure feature dir exists
    features_dir = context.temp_dir / "specification" / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    
    # Map feature dir
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            args[i] = str(features_dir)
        elif arg == "specification/features/audit.feature":
            args[i] = str(features_dir / "audit.feature")

    context.result = run_spec_weaver(args, cwd=context.temp_dir)


@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - アイテムIDを指定して gherkin_fingerprints を更新できる
      - .feature ファイルを指定して複数アイテムの gherkin_fingerprints を一括更新できる
      - .feature ファイルを指定してファイル自身の suspect 状態も解除できる
    """
    exit_code = getattr(context, "exit_code", None)
    if exit_code is None and hasattr(context, "result") and context.result is not None:
        exit_code = context.result.returncode
    
    output = getattr(context, "output", "")
    if not output and hasattr(context, "result") and context.result is not None:
        output = context.result.stdout + context.result.stderr

    assert exit_code == 0, f"Expected exit code 0, got {exit_code}. Output:\n{output}"


@then('終了コードが1である')  # type: ignore
def then_9b731a71(context):
    """終了コードが1である

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
      - 紐づくGherkinシナリオが存在しないアイテムを指定するとエラーになる
    """
    exit_code = getattr(context, "exit_code", None)
    if exit_code is None and hasattr(context, "result") and context.result is not None:
        exit_code = context.result.returncode
    
    output = getattr(context, "output", "")
    if not output and hasattr(context, "result") and context.result is not None:
        output = context.result.stdout + context.result.stderr

    assert exit_code == 1, f"Expected exit code 1, got {exit_code}. Output:\n{output}"


@then('"{param0}" の YAML に gherkin_fingerprints が書き込まれる')  # type: ignore
def then_4a7cffb4(context, param0):
    # Find YAML file
    yaml_path = context.temp_dir / "specs" / f"{param0}.yml"
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)
    assert "gherkin_fingerprints" in data, f"gherkin_fingerprints missing in {yaml_path}"


@then('ファイル内の各アイテムの gherkin_fingerprints が更新される')  # type: ignore
def then_c4c4abcc(context):
    for uid in ["SPEC-001", "SPEC-002"]:
        yaml_path = context.temp_dir / "specs" / f"{uid}.yml"
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
        assert "gherkin_fingerprints" in data


@then('更新件数が表示される')  # type: ignore
def then_b31aa65d(context):
    assert "更新しました" in context.result.stdout or "updated" in context.result.stdout


@given('"{param0}" ファイルが "{param1}" 状態である')  # type: ignore
def given_d4ac810a(context, param0, param1):
    # SPEC-001 created
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
    f = feature_dir / "audit.feature"
    # Write feature with old stamp for SPEC-001
    # We use a dummy stamp to simulate suspect
    write_feature_file(f, "# spec-weaver-fingerprint: dummy-hash\n# spec-weaver-fingerprint-SPEC-001: OLD_STAMP\n@SPEC-001\nFeature: Test\n  Scenario: Test\n    Given test\n")
    context.feature_dir = feature_dir


@then('"{param0}" の内部フィンガープリントが最新の Doorstop スタンプで更新される')  # type: ignore
def then_d6213e80(context, param0):
    feature_path = context.temp_dir / param0
    content = feature_path.read_text()
    assert "# spec-weaver-fingerprint-SPEC-001:" in content
    assert "OLD_STAMP" not in content


@then('`spec-weaver status` で当該ファイルが "{param0}" となる')  # type: ignore
def then_6caa1cf0(context, param0):
    result = run_spec_weaver(["status"], cwd=context.temp_dir)
    assert param0 in result.stdout


@when('`spec-weaver clear SPEC-999 --feature-dir ./specification/features` を実行する')  # type: ignore
def when_9a4cc39b(context):
    """`spec-weaver clear SPEC-999 --feature-dir ./specification/features` を実行する

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
    """
    raise NotImplementedError('STEP: `spec-weaver clear SPEC-999 --feature-dir ./specification/features` を実行する')


@then('エラーメッセージが表示される')  # type: ignore
def then_d53287cf(context):
    output = getattr(context, "output", "")
    if not output and hasattr(context, "result") and context.result is not None:
        output = context.result.stdout + context.result.stderr
    assert any(msg in output for msg in ["Error", "error", "見つかりません", "not found", "エラー", "❌", "未対応"]), f"Expected error message not found in output: {output}"


@given('"{param0}" に紐づく Gherkin シナリオが存在しない')  # type: ignore
def given_b669b903(context, param0):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    context.feature_dir = feature_dir


@when('`spec-weaver clear SPEC-004 --feature-dir ./specification/features` を実行する')  # type: ignore
def when_254d955f(context):
    """`spec-weaver clear SPEC-004 --feature-dir ./specification/features` を実行する

    Scenarios:
      - 紐づくGherkinシナリオが存在しないアイテムを指定するとエラーになる
    """
    raise NotImplementedError('STEP: `spec-weaver clear SPEC-004 --feature-dir ./specification/features` を実行する')


@then('警告メッセージが表示される')  # type: ignore
def then_a11d14f9(context):
    assert "Warning" in context.result.stdout or "warning" in context.result.stdout or "警告" in context.result.stdout
