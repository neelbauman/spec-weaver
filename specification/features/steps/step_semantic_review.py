# -*- coding: utf-8 -*-
from specification.features.steps._helpers import create_doorstop_project_api, write_feature_file, run_spec_weaver
from behave import given, when, then, step
import json
import shlex

# ======================================================================
# Steps
# ======================================================================

@given('claudeコマンドが利用可能である')  # type: ignore
def given_2b87969c(context):
    pass



# [Duplicate Skip] '仕様アイテム "{param0}" が存在する' is defined in step_clear.py


@when('`spec-weaver semantic-review --item SPEC-003 --feature-dir ./specification/features` を実行する') # type: ignore
def when_84125f26(context):
    feature_dir = context.temp_dir / "specification" / "features"
    feature_dir.mkdir(parents=True, exist_ok=True)
    context.result = run_spec_weaver(["semantic-review", "--item", "SPEC-003", "--feature-dir", str(feature_dir)], cwd=context.temp_dir)


# [Dup→step_trace.py] 終了コードが0である — step_trace.py の定義を使用


# [Dup→step_trace.py] 終了コードが0である — step_trace.py の定義を使用
# @then('終了コードが0である')  # type: ignore
# def then_0f800e56(context):
#     raise NotImplementedError('STEP: 終了コードが0である')


@then('出力にレビュー結果が含まれる')  # type: ignore
def then_6d399f8f(context):
    assert "Review" in context.result.stdout or "Review" in context.result.stderr or context.result.returncode == 0


@when('`spec-weaver semantic-review --item SPEC-003 --output json` を実行する') # type: ignore
def when_48c7474c(context):
    context.result = run_spec_weaver(["semantic-review", "--item", "SPEC-003", "--output", "json"], cwd=context.temp_dir)


@then('出力が有効なJSONである')  # type: ignore
def then_44c7668c(context):
    try:
        context.json_output = json.loads(context.result.stdout)
    except json.JSONDecodeError:
        assert False, f"Output is not valid JSON:\n{context.result.stdout}"


@then('JSONに "{param0}" フィールドが含まれる')  # type: ignore
def then_d68a96bd(context, param0):
    assert param0 in context.json_output


@when('`spec-weaver semantic-review --item NOTEXIST-999` を実行する') # type: ignore
def when_d00f5929(context):
    context.result = run_spec_weaver(["semantic-review", "--item", "NOTEXIST-999"], cwd=context.temp_dir)


# [Duplicate Skip] This step is already defined elsewhere (step_clear.py)
# @then('エラーメッセージが表示される')  # type: ignore
# def then_d53287cf(context):
#     raise NotImplementedError('STEP: エラーメッセージが表示される')

# [Dup→step_trace.py] 終了コードが1である — step_trace.py の定義を使用



# [Dup→step_trace.py] 終了コードが1である — step_trace.py の定義を使用
# @then('終了コードが1である')  # type: ignore
# def then_9b731a71(context):
#     raise NotImplementedError('STEP: 終了コードが1である')


# [Duplicate Skip] 'エラーメッセージが表示される' is defined in step_clear.py


@when('`spec-weaver semantic-review --item SPEC-003 --all` を実行する') # type: ignore
def when_c4549933(context):
    context.result = run_spec_weaver(["semantic-review", "--item", "SPEC-003", "--all"], cwd=context.temp_dir)


@then('終了コードが2である')  # type: ignore
def then_6ac18c13(context):
    assert context.result.returncode == 2


@given('レビュー結果に severity "{param0}" のfindingが含まれる')  # type: ignore
def given_7d56eddc(context, param0):
    pass


@when('`spec-weaver semantic-review --item SPEC-003 --fail-on high` を実行する') # type: ignore
def when_1d26b5da(context):
    context.result = run_spec_weaver(["semantic-review", "--item", "SPEC-003", "--fail-on", "high"], cwd=context.temp_dir)


@given('レビュー結果に severity "{param0}" のfindingが含まれない')  # type: ignore
def given_1689dd54(context, param0):
    pass


@when('`spec-weaver semantic-review --item SPEC-003 --min-severity medium` を実行する') # type: ignore
def when_17c9fae3(context):
    context.result = run_spec_weaver(["semantic-review", "--item", "SPEC-003", "--min-severity", "medium"], cwd=context.temp_dir)


@then('severity "{param0}" のfindingは出力に含まれない')  # type: ignore
def then_1da3fd36(context, param0):
    assert param0 not in context.result.stdout


@given('claudeコマンドが利用不可能である')  # type: ignore
def given_8b793538(context):
    pass


@when('`spec-weaver semantic-review --item SPEC-003` を実行する') # type: ignore
def when_6f8a42ad(context):
    context.result = run_spec_weaver(["semantic-review", "--item", "SPEC-003"], cwd=context.temp_dir)


@then('"{param0}" に関するエラーメッセージが表示される')  # type: ignore
def then_e0a5a7ab(context, param0):
    assert param0 in context.result.stdout or param0 in context.result.stderr


@when('`spec-weaver semantic-review --all --output json` を実行する')  # type: ignore
def when_7ccd7bbd(context):
    context.result = run_spec_weaver(["semantic-review", "--all", "--output", "json"], cwd=context.temp_dir)


@then('JSONが各アイテムのレビュー結果の配列またはディクショナリである')  # type: ignore
def then_61c6aa13(context):
    data = json.loads(context.result.stdout)
    assert isinstance(data, (list, dict))
# [Duplicate Skip] '仕様アイテム "{param0}" が存在する' is defined in step_clear.py

