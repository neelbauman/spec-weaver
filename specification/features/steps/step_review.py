from specification.features.steps._helpers import create_doorstop_project_api, write_feature_file, run_spec_weaver
"""behave steps for: review コマンド — .feature ファイルへのフィンガープリント書き込み"""
# implements: QA-004

import shutil
from pathlib import Path
from typer.testing import CliRunner

from behave import given, when, then, step

from spec_weaver.cli import app
from spec_weaver.gherkin import read_stored_fingerprint

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
    """
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
    _invoke_review(context, ["review", str(target)])


@when('`spec-weaver review nonexistent.feature` を実行する')  # type: ignore
def when_a5bfc0eb(context):
    """`spec-weaver review nonexistent.feature` を実行する

    Scenarios:
      - 存在しないファイルを指定するとエラーになる
    """
    _invoke_review(context, ["review", "nonexistent.feature"])


# ======================================================================
# Then — 検証
# ======================================================================

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
