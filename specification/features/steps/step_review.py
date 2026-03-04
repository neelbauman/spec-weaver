"""behave steps for: review コマンド — .feature ファイルへのフィンガープリント書き込み"""
# implements: QA-004

import shutil
from pathlib import Path

from behave import given, then, when
from typer.testing import CliRunner

from spec_weaver.adapters.gherkin import read_stored_fingerprint
from spec_weaver.cli.main import app
from specification.features.steps._helpers import (
    create_doorstop_project_api,
    create_doorstop_project_yaml,
    run_spec_weaver,
    write_feature_file,
)

_runner = CliRunner()

# ======================================================================
# ヘルパー
# ======================================================================

_FEATURE_FIXTURE = Path("specification/features/audit.feature")
_OLD_FINGERPRINT = "0000000000000000000000000000000000000000000000000000000000000000"


def _invoke_review(context, args):
    result = _runner.invoke(app, args)
    context.exit_code = result.exit_code
    context.output = result.output


# ======================================================================
# Given — 前提条件
# ======================================================================

@given('"{param0}" ファイルが存在する')  # type: ignore
def given_1fcf216b(context, param0):
    """".feature" ファイルが存在する

    Scenarios:
      - .feature ファイルを指定してフィンガープリントが書き込まれる
      - 指定ファイルが .feature でない場合にエラーになる
    """
    create_doorstop_project_api(context.temp_dir)
    src = context.project_root / _FEATURE_FIXTURE
    dest = context.temp_dir / _FEATURE_FIXTURE.name
    shutil.copy(src, dest)
    context.review_target = dest


@given('"{param0}" ファイルの先頭に古いフィンガープリントコメントが存在する')  # type: ignore
def given_6d4c1005(context, param0):
    """".feature" ファイルの先頭に古いフィンガープリントコメントが存在する

    Scenarios:
      - 既存のフィンガープリントコメントが新しいハッシュで上書きされる
    """
    create_doorstop_project_api(context.temp_dir)
    src = context.project_root / _FEATURE_FIXTURE
    dest = context.temp_dir / _FEATURE_FIXTURE.name
    content = src.read_text(encoding="utf-8")
    dest.write_text(
        f"# spec-weaver-fingerprint: {_OLD_FINGERPRINT}\n{content}",
        encoding="utf-8",
    )
    context.review_target = dest


# ======================================================================
# When — 操作
# ======================================================================

@when('`spec-weaver review specification/features/audit.feature` を実行する')  # type: ignore
def when_9feea5cb(context):
    """`spec-weaver review specification/features/audit.feature` を実行する

    Scenarios:
      - .feature ファイルを指定してフィンガープリントが書き込まれる
      - 既存のフィンガープリントコメントが新しいハッシュで上書きされる
    """
    target = getattr(context, "review_target", context.project_root / _FEATURE_FIXTURE)
    _invoke_review(context, ["review", str(target), "-r", str(context.temp_dir), "-f", str(context.temp_dir)])


@then('review 終了コードが0である')  # type: ignore
def then_exit_code_0_review(context):
    assert context.exit_code == 0, f"Expected exit code 0, got {context.exit_code}. Output:\n{context.output}"


@when('`spec-weaver review nonexistent.feature` を実行する')  # type: ignore
def when_a5bfc0eb(context):
    """`spec-weaver review nonexistent.feature` を実行する

    Scenarios:
      - 存在しないファイルを指定するとエラーになる
    """
    _invoke_review(context, ["review", "nonexistent.feature", "-r", str(context.temp_dir), "-f", str(context.temp_dir)])


# ======================================================================
# Then — 検証
# ======================================================================

@then('review 終了コードが1である')  # type: ignore
def then_exit_code_1_review(context):
    assert context.exit_code == 1, f"Expected exit code 1, got {context.exit_code}. Output:\n{context.output}"


@then('review エラーメッセージが表示される')  # type: ignore
def then_error_msg_review(context):
    assert any(msg in context.output for msg in ["❌", "Error", "error", "見つかりません", "エラー", "指定できません", "未対応"]), f"Expected error message not found in output: {context.output}"


@when('`spec-weaver review not_feature.txt` を実行する')  # type: ignore
def when_da1afe24(context):
    """`spec-weaver review not_feature.txt` を実行する

    Scenarios:
      - 指定ファイルが .feature でない場合にエラーになる
    """
    target = context.temp_dir / "not_feature.txt"
    target.write_text("Hello", encoding="utf-8")
    _invoke_review(context, ["review", str(target), "-r", str(context.temp_dir), "-f", str(context.temp_dir)])


@given('複数のアクティブな Doorstop アイテムが存在する')  # type: ignore
def given_1f1bb9b0(context):
    """複数のアクティブな Doorstop アイテムが存在する

    Scenarios:
      - --all で全 .feature ファイルと全 Doorstop アイテムを一括レビューできる
    """
    pass  # given_2e849535 でセットアップ済み


@when('`spec-weaver review --all --feature-dir ./specification/features` を実行する')  # type: ignore
def when_0656954c(context):
    """`spec-weaver review --all --feature-dir ./specification/features` を実行する

    Scenarios:
      - --all で全 .feature ファイルと全 Doorstop アイテムを一括レビューできる
    """
    feature_dir = getattr(context, "feature_dir",
                          context.project_root / "specification" / "features")
    result = run_spec_weaver(
        ["review", "--all", "--feature-dir", str(feature_dir)],
        cwd=context.temp_dir,
    )
    context.exit_code = result.returncode
    context.output = result.stdout + result.stderr


@then('全 "{param0}" ファイルにフィンガープリントが書き込まれる')  # type: ignore
def then_225cbe73(context, param0):
    """全 ".feature" ファイルにフィンガープリントが書き込まれる

    Scenarios:
      - --all で全 .feature ファイルと全 Doorstop アイテムを一括レビューできる
    """
    assert "件レビュー済み" in context.output, (
        f"Expected '件レビュー済み' in output:\n{context.output}"
    )
    feature_dir = getattr(context, "feature_dir",
                          context.project_root / "specification" / "features")
    for f in feature_dir.glob("*.feature"):
        stored = read_stored_fingerprint(f)
        assert stored is not None, f"{f.name} にフィンガープリントが書き込まれていません"


@then('アクティブな全 Doorstop アイテムがレビュー済みになる')  # type: ignore
def then_25d6c9d2(context):
    """アクティブな全 Doorstop アイテムがレビュー済みになる

    Scenarios:
      - --all で全 .feature ファイルと全 Doorstop アイテムを一括レビューできる
    """
    assert "Doorstop アイテム" in context.output and "件レビュー済み" in context.output, (
        f"Expected Doorstop item review count in output:\n{context.output}"
    )


@when('`spec-weaver review --all specification/features/audit.feature` を実行する')  # type: ignore
def when_b791afe5(context):
    """`spec-weaver review --all specification/features/audit.feature` を実行する

    Scenarios:
      - --all と対象パスを同時に指定するとエラーになる
    """
    _invoke_review(context, ["review", "--all", "specification/features/audit.feature"])


@when('`spec-weaver review` を引数なしで実行する')  # type: ignore
def when_fa6f8e67(context):
    """`spec-weaver review` を引数なしで実行する

    Scenarios:
      - 引数も --all も指定しないとエラーになる
    """
    _invoke_review(context, ["review"])
@then('ファイル先頭に "{param0}" コメントが追加される')  # type: ignore
def then_22d76672(context, param0):
    """ファイル先頭に "# spec-weaver-fingerprint:" コメントが追加される

    Scenarios:
      - .feature ファイルを指定してフィンガープリントが書き込まれる
    """
    target = context.review_target
    stored = read_stored_fingerprint(target)
    assert stored is not None, (
        f"先頭コメントが書き込まれていません。ファイル先頭:\n{target.read_text()[:200]}"
    )
    assert stored != _OLD_FINGERPRINT or param0 not in "# spec-weaver-fingerprint:", (
        f"期待するコメントが存在しません。stored={stored}"
    )


@then('ファイル先頭のコメントが新しいハッシュ値で上書きされる')  # type: ignore
def then_aa6656f4(context):
    """ファイル先頭のコメントが新しいハッシュ値で上書きされる

    Scenarios:
      - 既存のフィンガープリントコメントが新しいハッシュで上書きされる
    """
    target = context.review_target
    stored = read_stored_fingerprint(target)
    assert stored is not None, "フィンガープリントコメントが存在しません"
    assert stored != _OLD_FINGERPRINT, (
        f"古いフィンガープリント '{_OLD_FINGERPRINT}' が上書きされていません。stored={stored}"
    )
