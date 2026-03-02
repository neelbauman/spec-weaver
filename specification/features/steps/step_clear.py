from specification.features.steps._helpers import create_doorstop_project_api, write_feature_file, run_spec_weaver
"""behave steps for: clear コマンド — Doorstop test_fingerprint 更新"""
# implements: QA-005

from unittest.mock import patch, MagicMock
from typer.testing import CliRunner

from behave import given, when, then, step

from spec_weaver.cli import app

_runner = CliRunner()


def _invoke_clear(context, args):
    with patch("spec_weaver.cli.update_item_attribute") as mock_update:
        result = _runner.invoke(app, args)
    context.exit_code = result.exit_code
    context.output = result.output
    context.mock_update = mock_update


# ======================================================================
# Given — 前提条件
# ======================================================================

@given('仕様アイテム "{param0}" が存在する')  # type: ignore
def given_ddd4e2bc(context, param0):
    """仕様アイテム "SPEC-003" が存在する（プロジェクト内に実在するため noop）

    Scenarios:
      - アイテムIDを指定して test_fingerprint を更新できる
      - アイテムIDを指定して gherkin_fingerprints を更新できる
    """
    context.target_item_id = param0


@given('"{param0}" に紐づく Gherkin シナリオが存在する')  # type: ignore
def given_efa9578a(context, param0):
    """"SPEC-003" に紐づく Gherkin シナリオが存在する（audit.feature に実在するため noop）

    Scenarios:
      - アイテムIDを指定して test_fingerprint を更新できる
      - アイテムIDを指定して gherkin_fingerprints を更新できる
    """
    pass


@given('"{param0}" ファイルに複数の仕様IDタグが含まれる')  # type: ignore
def given_dfa4c4a3(context, param0):
    """".feature" ファイルに複数の仕様IDタグが含まれる（audit.feature は SPEC-003/QA-001 を含むため noop）

    Scenarios:
      - .feature ファイルを指定して複数アイテムの test_fingerprint を一括更新できる
      - .feature ファイルを指定して複数アイテムの gherkin_fingerprints を一括更新できる
    """
    pass


# ======================================================================
# When — 操作
# ======================================================================

@when('`spec-weaver clear SPEC-003 --feature-dir ./specification/features` を実行する')  # type: ignore
def when_81d90ca5(context):
    """`spec-weaver clear SPEC-003 --feature-dir ./specification/features` を実行する

    Scenarios:
      - アイテムIDを指定して test_fingerprint を更新できる
      - アイテムIDを指定して gherkin_fingerprints を更新できる
    """
    _invoke_clear(context, [
        "clear", "SPEC-003",
        "--feature-dir", "./specification/features",
    ])


@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - アイテムIDを指定して test_fingerprint を更新できる
      - .feature ファイルを指定して複数アイテムの test_fingerprint を一括更新できる
      - アイテムIDを指定して gherkin_fingerprints を更新できる
      - .feature ファイルを指定して複数アイテムの gherkin_fingerprints を一括更新できる
    """
    raise NotImplementedError('STEP: 終了コードが0である')


@then('"{param0}" の YAML に gherkin_fingerprints が書き込まれる')  # type: ignore
def then_4a7cffb4(context, param0):
    """"SPEC-003" の YAML に gherkin_fingerprints が書き込まれる

    Scenarios:
      - アイテムIDを指定して gherkin_fingerprints を更新できる
    """
    raise NotImplementedError('STEP: "{param0}" の YAML に gherkin_fingerprints が書き込まれる')


@when('`spec-weaver clear specification/features/audit.feature --feature-dir ./specification/features` を実行する')  # type: ignore
def when_f5108e70(context):
    """`spec-weaver clear specification/features/audit.feature --feature-dir ./specification/features` を実行する

    Scenarios:
      - .feature ファイルを指定して複数アイテムの test_fingerprint を一括更新できる
      - .feature ファイルを指定して複数アイテムの gherkin_fingerprints を一括更新できる
    """
    _invoke_clear(context, [
        "clear", "specification/features/audit.feature",
        "--feature-dir", "./specification/features",
    ])


@then('ファイル内の各アイテムの gherkin_fingerprints が更新される')  # type: ignore
def then_c4c4abcc(context):
    """ファイル内の各アイテムの gherkin_fingerprints が更新される

    Scenarios:
      - .feature ファイルを指定して複数アイテムの gherkin_fingerprints を一括更新できる
    """
    raise NotImplementedError('STEP: ファイル内の各アイテムの gherkin_fingerprints が更新される')


@when('`spec-weaver clear SPEC-999 --feature-dir ./specification/features` を実行する')  # type: ignore
def when_9a4cc39b(context):
    """`spec-weaver clear SPEC-999 --feature-dir ./specification/features` を実行する

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
    """
    _invoke_clear(context, [
        "clear", "SPEC-999",
        "--feature-dir", "./specification/features",
    ])


# ======================================================================
# Then — 検証
# ======================================================================

@then('終了コードが1である')  # type: ignore
def then_9b731a71(context):
    """終了コードが1である

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
    """
    raise NotImplementedError('STEP: 終了コードが1である')


@then('エラーメッセージが表示される')  # type: ignore
def then_d53287cf(context):
    """エラーメッセージが表示される

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
    """
    raise NotImplementedError('STEP: エラーメッセージが表示される')
@then('"{param0}" の YAML に test_fingerprint が書き込まれる')  # type: ignore
def then_7cec042b(context, param0):
    """"SPEC-003" の YAML に test_fingerprint が書き込まれる

    Scenarios:
      - アイテムIDを指定して test_fingerprint を更新できる
    """
    assert "test_fingerprint を更新しました" in context.output, (
        f"test_fingerprint 更新メッセージが出力にありません。output:\n{context.output}"
    )


@then('ファイル内の各アイテムの test_fingerprint が更新される')  # type: ignore
def then_f939cd9e(context):
    """ファイル内の各アイテムの test_fingerprint が更新される

    Scenarios:
      - .feature ファイルを指定して複数アイテムの test_fingerprint を一括更新できる
    """
    assert "test_fingerprint を更新しました" in context.output, (
        f"test_fingerprint 更新メッセージが出力にありません。output:\n{context.output}"
    )


@then('更新件数が表示される')  # type: ignore
def then_b31aa65d(context):
    """更新件数が表示される

    Scenarios:
      - .feature ファイルを指定して複数アイテムの test_fingerprint を一括更新できる
      - .feature ファイルを指定して複数アイテムの gherkin_fingerprints を一括更新できる
    """
    assert "合計" in context.output and "個のアイテムの test_fingerprint を更新しました" in context.output, (
        f"更新件数メッセージが出力にありません。output:\n{context.output}"
    )
