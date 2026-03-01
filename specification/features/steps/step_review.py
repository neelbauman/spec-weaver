"""behave steps for: review コマンド — セマンティックレビュー"""

import json
from unittest.mock import patch

from behave import given, when, then, step
from typer.testing import CliRunner

from spec_weaver.cli import app
from spec_weaver.review import (
    ReviewFinding,
    ReviewResult,
    SCHEMA_VERSION,
)

_runner = CliRunner()

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


def _invoke(context, args, *, mock_result=None, claude_not_found=False):
    """CliRunner でコマンドを実行し、context に結果を格納する。"""
    if claude_not_found:
        with patch("shutil.which", return_value=None):
            result = _runner.invoke(app, args)
    elif mock_result is not None:
        with patch("spec_weaver.review.run_claude_review", return_value=mock_result):
            result = _runner.invoke(app, args)
    else:
        result = _runner.invoke(app, args)

    context.exit_code = result.exit_code
    context.stdout = result.output
    context.stderr = ""
    context.result = result


# ======================================================================
# Given — 前提条件
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


@given('claudeコマンドが利用不可能である')  # type: ignore
def given_8b793538(context):
    """claudeコマンドが利用不可能である

    Scenarios:
      - claudeコマンドが見つからない場合にエラーになる
    """
    context.claude_available = False


# ======================================================================
# When — 操作
# ======================================================================

@when('`spec-weaver review --item SPEC-003 --feature-dir ./specification/features` を実行する')  # type: ignore
def when_2635ff54(context):
    """`spec-weaver review --item SPEC-003 --feature-dir ./specification/features` を実行する

    Scenarios:
      - 単一アイテムのレビューが実行できる
    """
    mock_result = _make_result(findings=getattr(context, "mock_findings", []))
    _invoke(context, ["review", "--item", "SPEC-003",
                      "--feature-dir", "./specification/features"],
            mock_result=mock_result)


@when('`spec-weaver review --item SPEC-003 --output json` を実行する')  # type: ignore
def when_074bba10(context):
    """`spec-weaver review --item SPEC-003 --output json` を実行する

    Scenarios:
      - 単一アイテムをJSON形式で出力できる
    """
    mock_result = _make_result(findings=getattr(context, "mock_findings", []))
    _invoke(context, ["review", "--item", "SPEC-003", "--output", "json"],
            mock_result=mock_result)
    try:
        context.json_output = json.loads(context.stdout)
    except json.JSONDecodeError:
        context.json_output = None


@when('`spec-weaver review --item NOTEXIST-999` を実行する')  # type: ignore
def when_0c73b4bf(context):
    """`spec-weaver review --item NOTEXIST-999` を実行する

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
    """
    _invoke(context, ["review", "--item", "NOTEXIST-999"])


@when('`spec-weaver review --item SPEC-003 --all` を実行する')  # type: ignore
def when_d3ec47d8(context):
    """`spec-weaver review --item SPEC-003 --all` を実行する

    Scenarios:
      - --item と --all は同時に指定できない
    """
    _invoke(context, ["review", "--item", "SPEC-003", "--all"])


@when('`spec-weaver review --item SPEC-003 --fail-on high` を実行する')  # type: ignore
def when_ab60e989(context):
    """`spec-weaver review --item SPEC-003 --fail-on high` を実行する

    Scenarios:
      - --fail-on high でhigh findingがある場合に終了コード1を返す
      - --fail-on high でhigh findingがない場合に終了コード0を返す
    """
    mock_result = _make_result(findings=getattr(context, "mock_findings", []))
    _invoke(context, ["review", "--item", "SPEC-003", "--fail-on", "high"],
            mock_result=mock_result)


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
    _invoke(context, ["review", "--item", "SPEC-003", "--min-severity", "medium"],
            mock_result=mock_result)


@when('`spec-weaver review --item SPEC-003` を実行する')  # type: ignore
def when_b44e1049(context):
    """`spec-weaver review --item SPEC-003` を実行する

    Scenarios:
      - claudeコマンドが見つからない場合にエラーになる
    """
    if getattr(context, "claude_available", True) is False:
        _invoke(context, ["review", "--item", "SPEC-003"], claude_not_found=True)
    else:
        mock_result = _make_result()
        _invoke(context, ["review", "--item", "SPEC-003"], mock_result=mock_result)


# ======================================================================
# Then — 検証
# ======================================================================

@then('出力にレビュー結果が含まれる')  # type: ignore
def then_6d399f8f(context):
    """出力にレビュー結果が含まれる

    Scenarios:
      - 単一アイテムのレビューが実行できる
    """
    assert "SPEC-003" in context.stdout, (
        f"Expected 'SPEC-003' in output. Output: {context.stdout}"
    )


@then('出力が有効なJSONである')  # type: ignore
def then_44c7668c(context):
    """出力が有効なJSONである

    Scenarios:
      - 単一アイテムをJSON形式で出力できる
    """
    assert context.json_output is not None, (
        f"Expected valid JSON output. Output: {context.stdout}"
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


@then('エラーメッセージが表示される')  # type: ignore
def then_d53287cf(context):
    """エラーメッセージが表示される

    Scenarios:
      - 存在しないアイテムIDを指定するとエラーになる
    """
    assert len(context.stdout.strip()) > 0, (
        f"Expected error message in output. Output: {context.stdout}"
    )


@then('severity "{param0}" のfindingは出力に含まれない')  # type: ignore
def then_1da3fd36(context, param0):
    """severity "low" のfindingは出力に含まれない

    Scenarios:
      - --min-severity medium で low の finding が非表示になる
    """
    assert "low finding" not in context.stdout, (
        f"Expected 'low finding' to be filtered from output. Output: {context.stdout}"
    )


@then('"{param0}" に関するエラーメッセージが表示される')  # type: ignore
def then_e0a5a7ab(context, param0):
    """"claude" に関するエラーメッセージが表示される

    Scenarios:
      - claudeコマンドが見つからない場合にエラーになる
    """
    assert param0 in context.stdout, (
        f"Expected '{param0}' in output. Output: {context.stdout}"
    )
