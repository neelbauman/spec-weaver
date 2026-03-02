"""behave 環境設定: シナリオごとの共通 setup / teardown。"""

import os
import shutil
import tempfile
import traceback
from pathlib import Path
from behave.model_core import Status

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def before_scenario(context, scenario):
    """各シナリオ開始前にテスト用一時ディレクトリを用意する。"""
    context.project_root = PROJECT_ROOT
    context.temp_dir = Path(tempfile.mkdtemp(prefix="sw_test_"))
    context.repo_root = None  # ステップで設定
    context.feature_dir = None  # ステップで設定
    context.out_dir = None  # ステップで設定
    context.result = None  # subprocess.CompletedProcess
    context.exit_code = None
    context.output = ""
    # 単体テスト用
    context.item = None
    context.value = None
    context.error = None
    context.items_dir = None


def after_scenario(context, scenario):
    """各シナリオ終了後に一時ファイルを削除し、作業ディレクトリを戻す。"""
    os.chdir(PROJECT_ROOT)
    if hasattr(context, "temp_dir") and context.temp_dir and context.temp_dir.exists():
        shutil.rmtree(context.temp_dir, ignore_errors=True)


def after_step(context, step):
    """ステップ実行後の処理。エラー時に詳細な実行ログを記録する（REQ-005 拡張）。"""
    if step.status == Status.error:
        # トレースバックをキャプチャして step.error_message に格納
        if hasattr(step, "exception") and step.exception:
            if hasattr(step, "exc_traceback") and step.exc_traceback:
                # exc_traceback がある場合は完全なトレースバックを取得
                tb = "".join(
                    traceback.format_exception(
                        type(step.exception), step.exception, step.exc_traceback
                    )
                )
                step.error_message = tb
            else:
                # 例外のみの場合
                step.error_message = (
                    f"{type(step.exception).__name__}: {str(step.exception)}"
                )

        # JSON フォーマッタに error_message フィールドを出力させるため、
        # error ステータスを failed に強制する（behave の JSON フォーマッタの制約への対策）
        step.status = Status.failed
