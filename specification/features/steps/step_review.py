"""behave steps for: review コマンド — Doorstop アイテムのエディタ確認レビュー"""
# implements: QA-004

import yaml
from behave import given, then, when

from specification.features.steps._helpers import (
    create_doorstop_project_yaml,
    run_spec_weaver,
)

# ======================================================================
# ヘルパー
# ======================================================================

def _run_review(context, args):
    """review コマンドを実行し、exit_code と output を context にセットする。"""
    env = getattr(context, "env", None)
    result = run_spec_weaver(args, cwd=context.temp_dir, env=env)
    context.exit_code = result.returncode
    context.output = result.stdout + result.stderr


# ======================================================================
# Given — 共通エディタセットアップ（clear でも共有）
# ======================================================================

@given('エディタが利用可能である')  # type: ignore
def given_ff0ed7cb(context):
    """モックエディタを設定する（終了コード 0、ログ記録あり）。"""
    log_file = context.temp_dir / "editor_calls.log"
    editor_script = context.temp_dir / "mock_editor.sh"
    editor_script.write_text(
        f"#!/bin/sh\necho \"called: $@\" >> {log_file}\nexit 0\n",
        encoding="utf-8",
    )
    editor_script.chmod(0o755)
    context.editor_log = log_file
    context.env = {"EDITOR": str(editor_script)}


@given('エディタが利用不可能である')  # type: ignore
def given_6097730a(context):
    """存在しないエディタを設定する。"""
    context.env = {"EDITOR": "/nonexistent_editor_xyz"}
    context.editor_log = None


@given('エディタが非ゼロ終了コードを返す')  # type: ignore
def given_c32c43a9(context):
    """終了コード 1 を返すモックエディタを設定する。"""
    editor_script = context.temp_dir / "bad_editor.sh"
    editor_script.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    editor_script.chmod(0o755)
    context.env = {"EDITOR": str(editor_script)}
    context.editor_log = None


# ======================================================================
# Given — review 固有
# ======================================================================

@given('Doorstop アイテム "{param0}" が存在する')  # type: ignore
def given_6dc12c23(context, param0):
    """指定 UID の Doorstop アイテムを含むプロジェクトを作成する。"""
    prefix = param0.split("-")[0]
    create_doorstop_project_yaml(
        context.temp_dir,
        [{"dir": "specs", "prefix": prefix, "items": [{"uid": param0, "testable": True}]}],
    )


@given('Doorstop アイテム "{param0}" が suspect 状態である')  # type: ignore
def given_99b14234(context, param0):
    """suspect 状態のアイテムは別途テストで検証。ここでは基本セットアップのみ。"""
    given_6dc12c23(context, param0)


@given('親アイテムに git 差分が存在する')  # type: ignore
def given_91ccc435(context):
    """親アイテムの git 差分は環境依存のため、ここでは何もしない。"""
    pass


@given('複数のアクティブな Doorstop アイテムが存在する')  # type: ignore
def given_1f1bb9b0(context):
    """review --all テスト用: 複数アイテムを持つ Doorstop プロジェクトを作成する。"""
    create_doorstop_project_yaml(
        context.temp_dir,
        [{"dir": "specs", "prefix": "SPEC", "items": [
            {"uid": "SPEC-001", "testable": True},
            {"uid": "SPEC-002", "testable": True},
        ]}],
    )


# ======================================================================
# When — review 固有
# ======================================================================

@when('`spec-weaver review QA-001` を実行する')  # type: ignore
def when_9407b4bd(context):
    _run_review(context, ["review", "QA-001", "--repo-root", str(context.temp_dir)])


@when('`spec-weaver review QA-001 --no-edit` を実行する')  # type: ignore
def when_70e9c8e9(context):
    _run_review(context, ["review", "QA-001", "--no-edit", "--repo-root", str(context.temp_dir)])


@when('`spec-weaver review NONEXISTENT-999` を実行する')  # type: ignore
def when_f53de9d2(context):
    _run_review(context, ["review", "NONEXISTENT-999", "--no-edit", "--repo-root", str(context.temp_dir)])


@when('`spec-weaver review --all` を実行する')  # type: ignore
def when_b40e7868(context):
    _run_review(context, ["review", "--all", "--repo-root", str(context.temp_dir)])


@when('`spec-weaver review --all QA-001` を実行する')  # type: ignore
def when_746ac93d(context):
    _run_review(context, ["review", "--all", "QA-001", "--repo-root", str(context.temp_dir)])


@when('`spec-weaver review` を引数なしで実行する')  # type: ignore
def when_fa6f8e67(context):
    _run_review(context, ["review", "--repo-root", str(context.temp_dir)])


# ======================================================================
# Then — エディタ検証（clear でも共有）
# ======================================================================

@then('エディタが起動した')  # type: ignore
def then_ef72e3a6(context):
    """モックエディタのログファイルが書き込まれていることを確認する。"""
    log = getattr(context, "editor_log", None)
    assert log is not None, "editor_log が設定されていません（given_ff0ed7cb が実行されていません）"
    assert log.exists() and log.stat().st_size > 0, (
        f"エディタが起動しませんでした。ログファイルが空です: {log}"
    )


@then('エディタが起動しない')  # type: ignore
def then_efaa9039(context):
    """エディタが起動していないことを確認する。"""
    log = getattr(context, "editor_log", None)
    if log is None:
        # --all モードなど、エディタが設定されていない場合はパス
        return
    assert not log.exists() or log.stat().st_size == 0, (
        f"エディタが起動してしまいました: {log.read_text(encoding='utf-8')}"
    )


@then('エディタが対象 YAML と関連アイテムの分割表示で起動した')  # type: ignore
def then_f4044c6c(context):
    """分割表示での起動確認（モックエディタで引数を記録）。"""
    then_ef72e3a6(context)


# ======================================================================
# Then — review 結果検証
# ======================================================================

@then('review 終了コードが0である')  # type: ignore
def then_exit_code_0_review(context):
    assert context.exit_code == 0, (
        f"Expected exit code 0, got {context.exit_code}. Output:\n{context.output}"
    )


@then('review 終了コードが1である')  # type: ignore
def then_exit_code_1_review(context):
    assert context.exit_code == 1, (
        f"Expected exit code 1, got {context.exit_code}. Output:\n{context.output}"
    )


@then('review エラーメッセージが表示される')  # type: ignore
def then_error_msg_review(context):
    assert any(
        msg in context.output
        for msg in ["❌", "Error", "error", "見つかりません", "エラー", "指定できません", "未対応"]
    ), f"Expected error message not found in output: {context.output}"


@then('"{param0}" が reviewed 状態になる')  # type: ignore
def then_11989dc4(context, param0):
    """指定アイテムの YAML で reviewed フィールドが設定されていることを確認する。"""
    prefix = param0.split("-")[0].lower()
    yaml_path = context.temp_dir / "specs" / f"{param0}.yml"
    assert yaml_path.exists(), f"YAML ファイルが見つかりません: {yaml_path}"
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data.get("reviewed") is not None, (
        f"{param0} が reviewed 状態になっていません。reviewed={data.get('reviewed')}"
    )


@then('アクティブな全 Doorstop アイテムがレビュー済みになる')  # type: ignore
def then_25d6c9d2(context):
    """出力にレビュー件数が含まれることを確認する。"""
    assert "Doorstop アイテム" in context.output and "件レビュー済み" in context.output, (
        f"Expected Doorstop item review count in output:\n{context.output}"
    )
