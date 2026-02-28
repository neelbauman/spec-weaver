"""behave steps for: status コマンド"""

from behave import given, when, then, step

# ======================================================================
# Steps
# ======================================================================

@given('REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている')  # type: ignore
def given_ef098fcf(context):
    """REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    raise NotImplementedError('STEP: REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている')


@when('status コマンドを実行する')  # type: ignore
def when_d68a8d9a(context):
    """status コマンドを実行する

    Scenarios:
      - 全アイテムのステータスを一覧表示する
      - status 未設定のアイテムは "-" と表示される
    """
    raise NotImplementedError('STEP: status コマンドを実行する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('終了コード 0 が返ること')  # type: ignore
# def then_4f25c571(context):
#     """終了コード 0 が返ること
# 
#     Scenarios:
#       - 全アイテムのステータスを一覧表示する
#       - status 未設定のアイテムは "-" と表示される
#       - --filter で特定ステータスに絞り込める
#       - --filter に一致するアイテムが存在しない場合に通知される
#     """
#     raise NotImplementedError('STEP: 終了コード 0 が返ること')


@then('REQ-001 が "{param0}" バッジとともに表示されること')  # type: ignore
def then_6e220346(context, param0):
    """REQ-001 が "draft" バッジとともに表示されること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    raise NotImplementedError('STEP: REQ-001 が "{param0}" バッジとともに表示されること')


@then('SPEC-001 が "{param0}" バッジとともに表示されること')  # type: ignore
def then_9f0d7f01(context, param0):
    """SPEC-001 が "implemented" バッジとともに表示されること

    Scenarios:
      - 全アイテムのステータスを一覧表示する
    """
    raise NotImplementedError('STEP: SPEC-001 が "{param0}" バッジとともに表示されること')


@given('SPEC-001 に status フィールドが設定されていない')  # type: ignore
def given_0d995d24(context):
    """SPEC-001 に status フィールドが設定されていない

    Scenarios:
      - status 未設定のアイテムは "-" と表示される
    """
    raise NotImplementedError('STEP: SPEC-001 に status フィールドが設定されていない')


@then('SPEC-001 の実装状況が "{param0}" と表示されること')  # type: ignore
def then_5818121f(context, param0):
    """SPEC-001 の実装状況が "-" と表示されること

    Scenarios:
      - status 未設定のアイテムは "-" と表示される
    """
    raise NotImplementedError('STEP: SPEC-001 の実装状況が "{param0}" と表示されること')


@given('REQ-001 が status: implemented、REQ-002 が status: draft に設定されている')  # type: ignore
def given_58beb4fc(context):
    """REQ-001 が status: implemented、REQ-002 が status: draft に設定されている

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    raise NotImplementedError('STEP: REQ-001 が status: implemented、REQ-002 が status: draft に設定されている')


@when('status コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_d36ae1bf(context, param0):
    """status コマンドを "--filter implemented" オプション付きで実行する

    Scenarios:
      - --filter で特定ステータスに絞り込める
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    raise NotImplementedError('STEP: status コマンドを "{param0}" オプション付きで実行する')


@then('REQ-001 が表示されること')  # type: ignore
def then_2847178d(context):
    """REQ-001 が表示されること

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    raise NotImplementedError('STEP: REQ-001 が表示されること')


@then('REQ-002 は表示されないこと')  # type: ignore
def then_9fc4e668(context):
    """REQ-002 は表示されないこと

    Scenarios:
      - --filter で特定ステータスに絞り込める
    """
    raise NotImplementedError('STEP: REQ-002 は表示されないこと')


@given('すべてのアイテムの status が "{param0}" に設定されている')  # type: ignore
def given_f93df893(context, param0):
    """すべてのアイテムの status が "draft" に設定されている

    Scenarios:
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    raise NotImplementedError('STEP: すべてのアイテムの status が "{param0}" に設定されている')


@then('一致するアイテムが見つからなかった旨が表示されること')  # type: ignore
def then_897c0cfb(context):
    """一致するアイテムが見つからなかった旨が表示されること

    Scenarios:
      - --filter に一致するアイテムが存在しない場合に通知される
    """
    raise NotImplementedError('STEP: 一致するアイテムが見つからなかった旨が表示されること')
