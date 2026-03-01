"""behave steps for: ci コマンド"""

from behave import given, when, then, step

# ======================================================================
# Steps
# ======================================================================

@given('scaffold で生成されたテストコードが存在する')  # type: ignore
def given_179333d2(context):
    """scaffold で生成されたテストコードが存在する

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
    """
    raise NotImplementedError('STEP: scaffold で生成されたテストコードが存在する')


@given('.feature ファイルが存在する')  # type: ignore
def given_93845d68(context):
    """.feature ファイルが存在する

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
      - scaffold 付き ci 実行
    """
    raise NotImplementedError('STEP: .feature ファイルが存在する')


@when('ci コマンドを実行する')  # type: ignore
def when_b11cd326(context):
    """ci コマンドを実行する

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
      - テスト失敗時のドキュメント生成継続
    """
    raise NotImplementedError('STEP: ci コマンドを実行する')


@then('pytest-bdd が実行されること')  # type: ignore
def then_f0e0adb5(context):
    """pytest-bdd が実行されること

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
    """
    raise NotImplementedError('STEP: pytest-bdd が実行されること')


@then('Cucumber 互換 JSON レポートが生成されること')  # type: ignore
def then_ba414369(context):
    """Cucumber 互換 JSON レポートが生成されること

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
    """
    raise NotImplementedError('STEP: Cucumber 互換 JSON レポートが生成されること')


@then('テスト結果を含む build ドキュメントが生成されること')  # type: ignore
def then_4f90a447(context):
    """テスト結果を含む build ドキュメントが生成されること

    Scenarios:
      - テスト実行とドキュメント生成の一貫実行
    """
    raise NotImplementedError('STEP: テスト結果を含む build ドキュメントが生成されること')


@given('テストに失敗するシナリオが含まれている')  # type: ignore
def given_ed203364(context):
    """テストに失敗するシナリオが含まれている

    Scenarios:
      - テスト失敗時のドキュメント生成継続
    """
    raise NotImplementedError('STEP: テストに失敗するシナリオが含まれている')


@then('ドキュメント生成は継続されること')  # type: ignore
def then_2584d8e2(context):
    """ドキュメント生成は継続されること

    Scenarios:
      - テスト失敗時のドキュメント生成継続
    """
    raise NotImplementedError('STEP: ドキュメント生成は継続されること')


@then('FAIL 結果がドキュメントに反映されること')  # type: ignore
def then_649f612f(context):
    """FAIL 結果がドキュメントに反映されること

    Scenarios:
      - テスト失敗時のドキュメント生成継続
    """
    raise NotImplementedError('STEP: FAIL 結果がドキュメントに反映されること')


@when('ci コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_ec489531(context, param0):
    """ci コマンドを "--scaffold" オプション付きで実行する

    Scenarios:
      - scaffold 付き ci 実行
    """
    raise NotImplementedError('STEP: ci コマンドを "{param0}" オプション付きで実行する')


@then('テストコード生成が先に実行されること')  # type: ignore
def then_0f77e713(context):
    """テストコード生成が先に実行されること

    Scenarios:
      - scaffold 付き ci 実行
    """
    raise NotImplementedError('STEP: テストコード生成が先に実行されること')


@then('続けてテスト実行とドキュメント生成が行われること')  # type: ignore
def then_9af9bba1(context):
    """続けてテスト実行とドキュメント生成が行われること

    Scenarios:
      - scaffold 付き ci 実行
    """
    raise NotImplementedError('STEP: 続けてテスト実行とドキュメント生成が行われること')
