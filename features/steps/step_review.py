"""behave steps for: review コマンド — セマンティックレビュー"""

import json
from unittest.mock import MagicMock, patch

from behave import given, when, then, step
from typer.testing import CliRunner

from spec_weaver.cli import app
from spec_weaver.review import (
    ReviewFinding,
    ReviewResult,
    SCHEMA_VERSION,
)

runner = CliRunner(mix_stderr=False)

# ======================================================================
# ヘルパー
# ======================================================================

def _make_result(item_id="SPEC-003", findings=None):
    """テスト用の ReviewResult を生成する。"""
    return ReviewResult(
        schema_version=SCHEMA_VERSION,
        item_id=item_id,
        item_title="テスト仕様",
        reviewed_files=["specification/specs/SPEC-003.yml"],
        findings=findings or [],
        summary="問題なし",
    )


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
    context.claude_available = True
    if not hasattr(context, "mock_findings"):
        context.mock_findings = []


@given('仕様アイテム "{param0}" が存在する')  # type: ignore
def given_ddd4e2bc(context, param0):
    """仕様アイテム "SPEC-003" が存在する

    Scenarios:
      - 単一アイテムのレビューが実行できる
      - 単一アイテムをJSON形式で出力できる
    """
    context.target_item_id = param0


@when('`spec-weaver review --item SPEC-003 --feature-dir ./specification/features` を実行する')  # type: ignore
def when_2635ff54(context):
    """`spec-weaver review --item SPEC-003 --feature-dir ./specification/features` を実行する

    Scenarios:
      - 単一アイテムのレビューが実行できる
    """
    mock_result = _make_result(findings=getattr(context, "mock_findings", []))
    with patch("spec_weaver.review.run_claude_review", return_value=mock_result):
        context.result = runner.invoke(
            app,
            ["review", "--item", "SPEC-003", "--feature-dir", "./specification/features"],
        )


@then('終了コードが0である')  # type: ignore
def then_0f800e56(context):
    """終了コードが0である

    Scenarios:
      - 単一アイテムのレビューが実行できる
      - 単一アイテムをJSON形式で出力できる
      - --fail-on high でhigh findingがない場合に終了コード0を返す
      - --min-severity medium で low の finding が非表示になる
    """
    assert context.result.exit_code == 0, (
        f"Expected exit code 0, got {context.result.exit_code}.\n"
        f"Output: {context.result.output}"
    )


@then('出力にレビュー結果が含まれる')  # type: ignore
def then_6d399f8f(context):
    """出力にレビュー結果が含まれる

    Scenarios:
      - 単一アイテムのレビューが実行できる
    """
    assert "SPEC-003" in context.result.output, (
        f"Expected 'SPEC-003' in output. Output: {context.result.output}"
    )


@when('`spec-weaver review --item SPEC-003 --output json` を実行する')  # type: ignore
def when_074bba10(context):
    """`spec-weaver review --item SPEC-003 --output json` を実行する

    Scenarios:
      - 単一アイテムをJSON形式で出力できる
    """
    mock_result = _make_result(findings=getattr(context, "mock_findings", []))
    with patch("spec_weaver.review.run_claude_review", return_value=mock_result):
        context.result = runner.invoke(
            app,
            ["review", "--item", "SPEC-003", "--output", "json"],
        )
    try:
        context.json_output = json.loads(context.result.output)
    except json.JSONDecodeError:
        context.json_output = None


@then('出力が有効なJSONである')  # type: ignore
def then_44c7668c(context):
    """出力が有効なJSONである

    Scenarios:
      - 単一アイテムをJSON形式で出力できる
    """
    assert context.json_output is not None, (
        f"Expected valid JSON output. Output: {context.result.output}"
    )


@then('JSONに "{param0}" フィールドが含まれる')  # type: ignore
def then_d68a96bd(context, param0):
    """JSONに "item_id" フィールドが含まれる

    Scenarios:
      - 単一アイテムをJSON形式で出力できる
    """
    assert param0 in context.json_output, (
        f"Expected field '{param0}' in JSON. Got: {list(context.json_output.keys())}"
    )


@when('`spec-weaver review --item NOTEXIST-999` を実行する')  # type: ignore
def when_0c73b4bf(context):
    """`spec-weaver review --item NOTEXIST-999` を実行する

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
    """
    context.result = runner.invoke(
        app,
        ["review", "--item", "NOTEXIST-999"],
    )


@then('終了コードが1である')  # type: ignore
def then_9b731a71(context):
    """終了コードが1である

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
      - --fail-on high でhigh findingがある場合に終了コード1を返す
      - claudeコマンドが見つからない場合にエラーになる
    """
    assert context.result.exit_code == 1, (
        f"Expected exit code 1, got {context.result.exit_code}.\n"
        f"Output: {context.result.output}"
    )


@then('エラーメッセージが表示される')  # type: ignore
def then_d53287cf(context):
    """エラーメッセージが表示される

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
    """
    assert len(context.result.output.strip()) > 0, (
        f"Expected error message in output. Output: {context.result.output}"
    )


@when('`spec-weaver review --item SPEC-003 --all` を実行する')  # type: ignore
def when_d3ec47d8(context):
    """`spec-weaver review --item SPEC-003 --all` を実行する

    Scenarios:
      - --item と --all は同時に指定できない
    """
    context.result = runner.invoke(
        app,
        ["review", "--item", "SPEC-003", "--all"],
    )


@then('終了コードが2である')  # type: ignore
def then_6ac18c13(context):
    """終了コードが2である

    Scenarios:
      - --item と --all は同時に指定できない
    """
    assert context.result.exit_code == 2, (
        f"Expected exit code 2, got {context.result.exit_code}.\n"
        f"Output: {context.result.output}"
    )


@given('レビュー結果に severity "{param0}" のfindingが含まれる')  # type: ignore
def given_7d56eddc(context, param0):
    """レビュー結果に severity "high" のfindingが含まれる

    Scenarios:
      - --fail-on high でhigh findingがある場合に終了コード1を返す
    """
    context.mock_findings = [
        ReviewFinding(
            kind="missing_implementation",
            severity=param0,
            title=f"{param0} severity finding",
            detail="テスト用finding",
        )
    ]


@when('`spec-weaver review --item SPEC-003 --fail-on high` を実行する')  # type: ignore
def when_ab60e989(context):
    """`spec-weaver review --item SPEC-003 --fail-on high` を実行する

    Scenarios:
      - --fail-on high でhigh findingがある場合に終了コード1を返す
      - --fail-on high でhigh findingがない場合に終了コード0を返す
    """
    mock_result = _make_result(findings=getattr(context, "mock_findings", []))
    with patch("spec_weaver.review.run_claude_review", return_value=mock_result):
        context.result = runner.invoke(
            app,
            ["review", "--item", "SPEC-003", "--fail-on", "high"],
        )


@given('レビュー結果に severity "{param0}" のfindingが含まれない')  # type: ignore
def given_1689dd54(context, param0):
    """レビュー結果に severity "high" のfindingが含まれない

    Scenarios:
      - --fail-on high でhigh findingがない場合に終了コード0を返す
    """
    context.mock_findings = [
        ReviewFinding(
            kind="missing_implementation",
            severity="low",
            title="low severity finding",
            detail="テスト用finding",
        )
    ]


@when('`spec-weaver review --item SPEC-003 --min-severity medium` を実行する')  # type: ignore
def when_72d3dd9b(context):
    """`spec-weaver review --item SPEC-003 --min-severity medium` を実行する

    Scenarios:
      - --min-severity medium で low の finding が非表示になる
    """
    mock_result = _make_result(findings=[
        ReviewFinding(
            kind="missing_implementation",
            severity="low",
            title="low finding",
            detail="低重大度",
        ),
        ReviewFinding(
            kind="missing_implementation",
            severity="medium",
            title="medium finding",
            detail="中重大度",
        ),
    ])
    with patch("spec_weaver.review.run_claude_review", return_value=mock_result):
        context.result = runner.invoke(
            app,
            ["review", "--item", "SPEC-003", "--min-severity", "medium"],
        )


@then('severity "{param0}" のfindingは出力に含まれない')  # type: ignore
def then_1da3fd36(context, param0):
    """severity "low" のfindingは出力に含まれない

    Scenarios:
      - --min-severity medium で low の finding が非表示になる
    """
    assert "low finding" not in context.result.output, (
        f"Expected 'low finding' to be filtered from output. Output: {context.result.output}"
    )


@given('claudeコマンドが利用不可能である')  # type: ignore
def given_8b793538(context):
    """claudeコマンドが利用不可能である

    Scenarios:
      - claudeコマンドが見つからない場合にエラーになる
    """
    context.claude_available = False


@when('`spec-weaver review --item SPEC-003` を実行する')  # type: ignore
def when_b44e1049(context):
    """`spec-weaver review --item SPEC-003` を実行する

    Scenarios:
      - claudeコマンドが見つからない場合にエラーになる
    """
    if getattr(context, "claude_available", True) is False:
        with patch("shutil.which", return_value=None):
            context.result = runner.invoke(
                app,
                ["review", "--item", "SPEC-003"],
            )
    else:
        mock_result = _make_result()
        with patch("spec_weaver.review.run_claude_review", return_value=mock_result):
            context.result = runner.invoke(
                app,
                ["review", "--item", "SPEC-003"],
            )


@then('"{param0}" に関するエラーメッセージが表示される')  # type: ignore
def then_e0a5a7ab(context, param0):
    """"claude" に関するエラーメッセージが表示される

    Scenarios:
      - claudeコマンドが見つからない場合にエラーになる
    """
    assert param0 in context.result.output, (
        f"Expected '{param0}' in output. Output: {context.result.output}"
    )
