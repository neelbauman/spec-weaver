from specification.features.steps._helpers import create_doorstop_project_api, write_feature_file, run_spec_weaver
"""behave steps for: semantic-review コマンド — セマンティックレビュー"""

from behave import given, when, then, step

# ======================================================================
# Steps
# ======================================================================

@given('claudeコマンドが利用可能である')  # type: ignore
def given_2b87969c(context):
    """claudeコマンドが利用可能である

    Scenarios:
      - 単一アイテムのレビューが実行できる
      - 単一アイテムをJSON形式で出力できる
      - --fail-on high でhigh findingがある場合に終了コード1を返す
      - --fail-on high でhigh findingがない場合に終了コード0を返す
      - --min-severity medium で low の finding が非表示になる
    """
    pass


@when('`spec-weaver semantic-review --item SPEC-003 --feature-dir ./specification/features` を実行する')  # type: ignore
def when_84125f26(context):
    """`spec-weaver semantic-review --item SPEC-003 --feature-dir ./specification/features` を実行する

    Scenarios:
      - 単一アイテムのレビューが実行できる
    """
    raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003 --feature-dir ./specification/features` を実行する')


@then('出力にレビュー結果が含まれる')  # type: ignore
def then_6d399f8f(context):
    """出力にレビュー結果が含まれる

    Scenarios:
      - 単一アイテムのレビューが実行できる
    """
    pass


@when('`spec-weaver semantic-review --item SPEC-003 --output json` を実行する')  # type: ignore
def when_48c7474c(context):
    """`spec-weaver semantic-review --item SPEC-003 --output json` を実行する

    Scenarios:
      - 単一アイテムをJSON形式で出力できる
    """
    raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003 --output json` を実行する')


@then('出力が有効なJSONである')  # type: ignore
def then_44c7668c(context):
    """出力が有効なJSONである

    Scenarios:
      - 単一アイテムをJSON形式で出力できる
    """
    pass


@then('JSONに "{param0}" フィールドが含まれる')  # type: ignore
def then_d68a96bd(context, param0):
    """JSONに "item_id" フィールドが含まれる

    Scenarios:
      - 単一アイテムをJSON形式で出力できる
    """
    pass


@when('`spec-weaver semantic-review --item NOTEXIST-999` を実行する')  # type: ignore
def when_d00f5929(context):
    """`spec-weaver semantic-review --item NOTEXIST-999` を実行する

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
    """
    raise NotImplementedError('STEP: `spec-weaver semantic-review --item NOTEXIST-999` を実行する')


@when('`spec-weaver semantic-review --item SPEC-003 --all` を実行する')  # type: ignore
def when_c4549933(context):
    """`spec-weaver semantic-review --item SPEC-003 --all` を実行する

    Scenarios:
      - --item と --all は同時に指定できない
    """
    raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003 --all` を実行する')


@then('終了コードが2である')  # type: ignore
def then_6ac18c13(context):
    """終了コードが2である

    Scenarios:
      - --item と --all は同時に指定できない
    """
    raise NotImplementedError('STEP: 終了コードが2である')


@given('レビュー結果に severity "{param0}" のfindingが含まれる')  # type: ignore
def given_7d56eddc(context, param0):
    """レビュー結果に severity "high" のfindingが含まれる

    Scenarios:
      - --fail-on high でhigh findingがある場合に終了コード1を返す
    """
    pass


@when('`spec-weaver semantic-review --item SPEC-003 --fail-on high` を実行する')  # type: ignore
def when_1d26b5da(context):
    """`spec-weaver semantic-review --item SPEC-003 --fail-on high` を実行する

    Scenarios:
      - --fail-on high でhigh findingがある場合に終了コード1を返す
      - --fail-on high でhigh findingがない場合に終了コード0を返す
    """
    raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003 --fail-on high` を実行する')


@given('レビュー結果に severity "{param0}" のfindingが含まれない')  # type: ignore
def given_1689dd54(context, param0):
    """レビュー結果に severity "high" のfindingが含まれない

    Scenarios:
      - --fail-on high でhigh findingがない場合に終了コード0を返す
    """
    pass


@when('`spec-weaver semantic-review --item SPEC-003 --min-severity medium` を実行する')  # type: ignore
def when_17c9fae3(context):
    """`spec-weaver semantic-review --item SPEC-003 --min-severity medium` を実行する

    Scenarios:
      - --min-severity medium で low の finding が非表示になる
    """
    raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003 --min-severity medium` を実行する')


@then('severity "{param0}" のfindingは出力に含まれない')  # type: ignore
def then_1da3fd36(context, param0):
    """severity "low" のfindingは出力に含まれない

    Scenarios:
      - --min-severity medium で low の finding が非表示になる
    """
    pass


@given('claudeコマンドが利用不可能である')  # type: ignore
def given_8b793538(context):
    """claudeコマンドが利用不可能である

    Scenarios:
      - claudeコマンドが見つからない場合にエラーになる
    """
    pass


@when('`spec-weaver semantic-review --item SPEC-003` を実行する')  # type: ignore
def when_6f8a42ad(context):
    """`spec-weaver semantic-review --item SPEC-003` を実行する

    Scenarios:
      - claudeコマンドが見つからない場合にエラーになる
    """
    raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003` を実行する')


@then('"{param0}" に関するエラーメッセージが表示される')  # type: ignore
def then_e0a5a7ab(context, param0):
    """"claude" に関するエラーメッセージが表示される

    Scenarios:
      - claudeコマンドが見つからない場合にエラーになる
    """
    pass
