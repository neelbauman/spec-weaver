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
    raise NotImplementedError('STEP: claudeコマンドが利用可能である')


# [Duplicate Skip] step_clear.py の @given('仕様アイテム "{param0}" が存在する') で処理される


# [Duplicate Skip] This step is already defined elsewhere
# @when('`spec-weaver semantic-review --item SPEC-003 --feature-dir ./specification/features` を実行する')  # type: ignore
# def when_84125f26(context):
#     """`spec-weaver semantic-review --item SPEC-003 --feature-dir ./specification/features` を実行する
# 
#     Scenarios:
#       - 単一アイテムのレビューが実行できる
#     """
#     raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003 --feature-dir ./specification/features` を実行する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('終了コードが0である')  # type: ignore
# def then_0f800e56(context):
#     """終了コードが0である
# 
#     Scenarios:
#       - 単一アイテムのレビューが実行できる
#       - 単一アイテムをJSON形式で出力できる
#       - --fail-on high でhigh findingがない場合に終了コード0を返す
#       - --min-severity medium で low の finding が非表示になる
#     """
#     raise NotImplementedError('STEP: 終了コードが0である')


@then('出力にレビュー結果が含まれる')  # type: ignore
def then_6d399f8f(context):
    """出力にレビュー結果が含まれる

    Scenarios:
      - 単一アイテムのレビューが実行できる
    """
    raise NotImplementedError('STEP: 出力にレビュー結果が含まれる')


# [Duplicate Skip] This step is already defined elsewhere
# @when('`spec-weaver semantic-review --item SPEC-003 --output json` を実行する')  # type: ignore
# def when_48c7474c(context):
#     """`spec-weaver semantic-review --item SPEC-003 --output json` を実行する
# 
#     Scenarios:
#       - 単一アイテムをJSON形式で出力できる
#     """
#     raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003 --output json` を実行する')


@then('出力が有効なJSONである')  # type: ignore
def then_44c7668c(context):
    """出力が有効なJSONである

    Scenarios:
      - 単一アイテムをJSON形式で出力できる
    """
    raise NotImplementedError('STEP: 出力が有効なJSONである')


@then('JSONに "{param0}" フィールドが含まれる')  # type: ignore
def then_d68a96bd(context, param0):
    """JSONに "item_id" フィールドが含まれる

    Scenarios:
      - 単一アイテムをJSON形式で出力できる
    """
    raise NotImplementedError('STEP: JSONに "{param0}" フィールドが含まれる')


# [Duplicate Skip] This step is already defined elsewhere
# @when('`spec-weaver semantic-review --item NOTEXIST-999` を実行する')  # type: ignore
# def when_d00f5929(context):
#     """`spec-weaver semantic-review --item NOTEXIST-999` を実行する
# 
#     Scenarios:
#       - 存在しないアイテムIDを指定するとエラーになる
#     """
#     raise NotImplementedError('STEP: `spec-weaver semantic-review --item NOTEXIST-999` を実行する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('終了コードが1である')  # type: ignore
# def then_9b731a71(context):
#     """終了コードが1である
# 
#     Scenarios:
#       - 存在しないアイテムIDを指定するとエラーになる
#       - --fail-on high でhigh findingがある場合に終了コード1を返す
#       - claudeコマンドが見つからない場合にエラーになる
#     """
#     raise NotImplementedError('STEP: 終了コードが1である')


# [Duplicate Skip] common_steps.py の @then('エラーメッセージが表示される') で処理される


# [Duplicate Skip] This step is already defined elsewhere
# @when('`spec-weaver semantic-review --item SPEC-003 --all` を実行する')  # type: ignore
# def when_c4549933(context):
#     """`spec-weaver semantic-review --item SPEC-003 --all` を実行する
# 
#     Scenarios:
#       - --item と --all は同時に指定できない
#     """
#     raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003 --all` を実行する')


# [Duplicate Skip] common_steps.py の @then('終了コードが{code:d}である') で処理される
# @then('終了コードが2である')


@given('レビュー結果に severity "{param0}" のfindingが含まれる')  # type: ignore
def given_7d56eddc(context, param0):
    """レビュー結果に severity "high" のfindingが含まれる

    Scenarios:
      - --fail-on high でhigh findingがある場合に終了コード1を返す
    """
    raise NotImplementedError('STEP: レビュー結果に severity "{param0}" のfindingが含まれる')


# [Duplicate Skip] This step is already defined elsewhere
# @when('`spec-weaver semantic-review --item SPEC-003 --fail-on high` を実行する')  # type: ignore
# def when_1d26b5da(context):
#     """`spec-weaver semantic-review --item SPEC-003 --fail-on high` を実行する
# 
#     Scenarios:
#       - --fail-on high でhigh findingがある場合に終了コード1を返す
#       - --fail-on high でhigh findingがない場合に終了コード0を返す
#     """
#     raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003 --fail-on high` を実行する')


@given('レビュー結果に severity "{param0}" のfindingが含まれない')  # type: ignore
def given_1689dd54(context, param0):
    """レビュー結果に severity "high" のfindingが含まれない

    Scenarios:
      - --fail-on high でhigh findingがない場合に終了コード0を返す
    """
    raise NotImplementedError('STEP: レビュー結果に severity "{param0}" のfindingが含まれない')


# [Duplicate Skip] This step is already defined elsewhere
# @when('`spec-weaver semantic-review --item SPEC-003 --min-severity medium` を実行する')  # type: ignore
# def when_17c9fae3(context):
#     """`spec-weaver semantic-review --item SPEC-003 --min-severity medium` を実行する
# 
#     Scenarios:
#       - --min-severity medium で low の finding が非表示になる
#     """
#     raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003 --min-severity medium` を実行する')


@then('severity "{param0}" のfindingは出力に含まれない')  # type: ignore
def then_1da3fd36(context, param0):
    """severity "low" のfindingは出力に含まれない

    Scenarios:
      - --min-severity medium で low の finding が非表示になる
    """
    raise NotImplementedError('STEP: severity "{param0}" のfindingは出力に含まれない')


@given('claudeコマンドが利用不可能である')  # type: ignore
def given_8b793538(context):
    """claudeコマンドが利用不可能である

    Scenarios:
      - claudeコマンドが見つからない場合にエラーになる
    """
    raise NotImplementedError('STEP: claudeコマンドが利用不可能である')


# [Duplicate Skip] This step is already defined elsewhere
# @when('`spec-weaver semantic-review --item SPEC-003` を実行する')  # type: ignore
# def when_6f8a42ad(context):
#     """`spec-weaver semantic-review --item SPEC-003` を実行する
# 
#     Scenarios:
#       - claudeコマンドが見つからない場合にエラーになる
#     """
#     raise NotImplementedError('STEP: `spec-weaver semantic-review --item SPEC-003` を実行する')


@then('"{param0}" に関するエラーメッセージが表示される')  # type: ignore
def then_e0a5a7ab(context, param0):
    """"claude" に関するエラーメッセージが表示される

    Scenarios:
      - claudeコマンドが見つからない場合にエラーになる
    """
    raise NotImplementedError('STEP: "{param0}" に関するエラーメッセージが表示される')
