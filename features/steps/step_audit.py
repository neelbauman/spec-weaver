"""behave steps for: audit コマンド"""

from behave import given, when, then, step

# ======================================================================
# Steps
# ======================================================================

@given('すべてのtestable仕様に対応するGherkinテストが存在する')  # type: ignore
def given_a7b8516a(context):
    """すべてのtestable仕様に対応するGherkinテストが存在する

    Scenarios:
      - 完全一致時の監査成功
    """
    raise NotImplementedError('STEP: すべてのtestable仕様に対応するGherkinテストが存在する')


@when('audit コマンドを実行する')  # type: ignore
def when_20ad7547(context):
    """audit コマンドを実行する

    Scenarios:
      - 完全一致時の監査成功
      - テスト漏れの検出
      - 孤児タグの検出
      - テスト漏れと孤児タグの同時検出
      - testable: false の仕様はスキップされる
      - Suspect Link の検出
      - Unreviewed Changes の検出
    """
    raise NotImplementedError('STEP: audit コマンドを実行する')


@then('終了コード 0 が返ること')  # type: ignore
def then_4f25c571(context):
    """終了コード 0 が返ること

    Scenarios:
      - 完全一致時の監査成功
    """
    raise NotImplementedError('STEP: 終了コード 0 が返ること')


@then('成功メッセージが表示されること')  # type: ignore
def then_f7642361(context):
    """成功メッセージが表示されること

    Scenarios:
      - 完全一致時の監査成功
    """
    raise NotImplementedError('STEP: 成功メッセージが表示されること')


@given('testable な仕様 "{param0}" に対応するGherkinテストが存在しない')  # type: ignore
def given_03339ad7(context, param0):
    """testable な仕様 "SPEC-002" に対応するGherkinテストが存在しない

    Scenarios:
      - テスト漏れの検出
    """
    raise NotImplementedError('STEP: testable な仕様 "{param0}" に対応するGherkinテストが存在しない')


@then('終了コード 1 が返ること')  # type: ignore
def then_4dccc2fd(context):
    """終了コード 1 が返ること

    Scenarios:
      - テスト漏れの検出
      - 孤児タグの検出
      - テスト漏れと孤児タグの同時検出
      - Suspect Link の検出
      - Unreviewed Changes の検出
    """
    raise NotImplementedError('STEP: 終了コード 1 が返ること')


@then('テストが実装されていない仕様として "{param0}" が報告されること')  # type: ignore
def then_6664aa42(context, param0):
    """テストが実装されていない仕様として "SPEC-002" が報告されること

    Scenarios:
      - テスト漏れの検出
    """
    raise NotImplementedError('STEP: テストが実装されていない仕様として "{param0}" が報告されること')


@given('Gherkinに仕様書に存在しない "{param0}" タグが含まれている')  # type: ignore
def given_3aa00113(context, param0):
    """Gherkinに仕様書に存在しない "@SPEC-999" タグが含まれている

    Scenarios:
      - 孤児タグの検出
    """
    raise NotImplementedError('STEP: Gherkinに仕様書に存在しない "{param0}" タグが含まれている')


@then('孤児タグとして "{param0}" が報告されること')  # type: ignore
def then_33c30716(context, param0):
    """孤児タグとして "@SPEC-999" が報告されること

    Scenarios:
      - 孤児タグの検出
    """
    raise NotImplementedError('STEP: 孤児タグとして "{param0}" が報告されること')


@given('仕様 "{param0}" のテストが未実装で "{param1}" が孤児タグである')  # type: ignore
def given_ffdcf7f2(context, param0, param1):
    """仕様 "SPEC-002" のテストが未実装で "@SPEC-999" が孤児タグである

    Scenarios:
      - テスト漏れと孤児タグの同時検出
    """
    raise NotImplementedError('STEP: 仕様 "{param0}" のテストが未実装で "{param1}" が孤児タグである')


@then('テスト漏れと孤児タグの両方が報告されること')  # type: ignore
def then_4928ac49(context):
    """テスト漏れと孤児タグの両方が報告されること

    Scenarios:
      - テスト漏れと孤児タグの同時検出
    """
    raise NotImplementedError('STEP: テスト漏れと孤児タグの両方が報告されること')


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
    """仕様 "SPEC-009" の上位アイテムが変更されている（cleared=false）

    Scenarios:
      - Suspect Link の検出
    """
    raise NotImplementedError('STEP: 仕様 "{param0}" の上位アイテムが変更されている（cleared=false）')


@then('Suspect Link テーブルに "{param0}" が報告されること')  # type: ignore
def then_0149339a(context, param0):
    """Suspect Link テーブルに "SPEC-009" が報告されること

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
    """仕様 "SPEC-009" 自体に未レビューの変更がある（reviewed=false）

    Scenarios:
      - Unreviewed Changes の検出
    """
    raise NotImplementedError('STEP: 仕様 "{param0}" 自体に未レビューの変更がある（reviewed=false）')


@then('Unreviewed Changes テーブルに "{param0}" が報告されること')  # type: ignore
def then_56101a52(context, param0):
    """Unreviewed Changes テーブルに "SPEC-009" が報告されること

    Scenarios:
      - Unreviewed Changes の検出
    """
    raise NotImplementedError('STEP: Unreviewed Changes テーブルに "{param0}" が報告されること')
