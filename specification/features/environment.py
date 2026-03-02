"""behave 環境設定: シナリオごとの共通 setup / teardown。"""

import os
import shutil
import tempfile
from pathlib import Path

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
