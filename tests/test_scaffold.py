"""scaffold / ci コマンド および codegen モジュールのテスト。"""

import hashlib
import re
import ast as python_ast
from pathlib import Path
from unittest.mock import patch, MagicMock

from typer.testing import CliRunner

from spec_weaver.cli import app
from spec_weaver.codegen import (
    _hash_name,
    _escape_string,
    _step_keyword_to_prefix,
    _resolve_step_prefixes,
    generate_test_file,
)

runner = CliRunner()

# ---------------------------------------------------------------------------
# サンプル .feature コンテンツ
# ---------------------------------------------------------------------------

SAMPLE_FEATURE_JA = """\
@SPEC-099
Feature: サンプル機能
  テスト用のサンプル Feature。

  Scenario: 完全一致時の監査成功
    Given すべてのtestable仕様に対応するGherkinテストが存在する
    When  audit コマンドを実行する
    Then  終了コード 0 が返ること

  Scenario: テスト漏れの検出
    Given testable な仕様に対応するGherkinテストが存在しない
    When  audit コマンドを実行する
    Then  終了コード 1 が返ること
"""

SAMPLE_FEATURE_QUOTES = """\
Feature: クオート含むステップ
  ダブルクオーテーションを含むステップのテスト。

  Scenario: 複合警告の表示
    Given アイテムに Suspect Link と Unreviewed Changes の両方がある
    When  build コマンドを実行する
    Then  一覧テーブルの状態列に "⚠️ Suspect" と "📋 Unreviewed" の両方が表示されること
"""

SAMPLE_FEATURE_SHARED_STEPS = """\
Feature: 共有ステップ
  同一ステップが複数シナリオで使用される。

  Scenario: シナリオA
    Given 共通の前提条件がある
    When  操作Aを実行する
    Then  結果Aが得られること

  Scenario: シナリオB
    Given 共通の前提条件がある
    When  操作Bを実行する
    Then  結果Bが得られること
"""


# ---------------------------------------------------------------------------
# codegen ユニットテスト
# ---------------------------------------------------------------------------


def test_hash_name_ascii_only():
    """ハッシュ名が ASCII 文字のみで構成されること。"""
    result = _hash_name("完全一致時の監査成功")
    assert result.isascii()
    assert len(result) == 8
    assert re.match(r"^[0-9a-f]{8}$", result)


def test_hash_name_deterministic():
    """同じ入力には同じハッシュが返ること。"""
    assert _hash_name("テスト") == _hash_name("テスト")


def test_hash_name_unique():
    """異なる入力には異なるハッシュが返ること。"""
    assert _hash_name("テストA") != _hash_name("テストB")


def test_step_keyword_to_prefix():
    """ステップキーワードが正しく変換されること。"""
    assert _step_keyword_to_prefix("Given") == "given"
    assert _step_keyword_to_prefix("When") == "when"
    assert _step_keyword_to_prefix("Then") == "then"
    assert _step_keyword_to_prefix("Given ") == "given"
    assert _step_keyword_to_prefix("And") == ""
    assert _step_keyword_to_prefix("But") == ""


def test_escape_string_double_quotes():
    """ダブルクオーテーションが <...> に変換されること。"""
    assert _escape_string('hello "world"') == 'hello <world>'
    assert _escape_string('no quotes') == 'no quotes'
    assert _escape_string('"⚠️ Suspect"') == '<⚠️ Suspect>'


def test_escape_string_backslash():
    """バックスラッシュが正しくエスケープされること。"""
    assert _escape_string('path\\to\\file') == 'path\\\\to\\\\file'


def test_generate_test_file_with_quotes(tmp_path):
    """ダブルクオーテーションを含むステップが正しく生成されること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "quotes.feature"
    feature_file.write_text(SAMPLE_FEATURE_QUOTES, encoding="utf-8")

    out_dir = tmp_path / "tests"
    result = generate_test_file(feature_file, out_dir, feature_dir)

    assert result is not None
    content = result.read_text(encoding="utf-8")

    # 構文的に正しい Python であること
    python_ast.parse(content)

    # <...> に変換された文字列が含まれること
    assert '<⚠️ Suspect>' in content
    assert '<📋 Unreviewed>' in content


def test_resolve_step_prefixes_and_but():
    """And/But は直前のキーワードを引き継ぐこと。"""
    steps = [
        {"keyword": "Given ", "text": "前提"},
        {"keyword": "And ", "text": "追加前提"},
        {"keyword": "When ", "text": "操作"},
        {"keyword": "Then ", "text": "結果"},
        {"keyword": "And ", "text": "追加結果"},
    ]
    resolved = _resolve_step_prefixes(steps)
    assert resolved == [
        ("given", "前提"),
        ("given", "追加前提"),
        ("when", "操作"),
        ("then", "結果"),
        ("then", "追加結果"),
    ]


def test_generate_test_file_basic(tmp_path):
    """基本的なテストファイル生成が動作すること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "sample.feature"
    feature_file.write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "tests"
    result = generate_test_file(feature_file, out_dir, feature_dir)

    assert result is not None
    assert result.name == "step_sample.py"
    assert result.exists()

    content = result.read_text(encoding="utf-8")

    # 構文的に正しい Python であること
    python_ast.parse(content)

    # behave のインポートが含まれること
    assert "from behave import" in content
    assert "@given" in content

    # 関数名に日本語が含まれないこと
    func_names = re.findall(r"def (\w+)\(", content)
    for name in func_names:
        assert name.isascii(), f"関数名に非 ASCII 文字: {name}"

    # ステップ文が含まれること
    assert "終了コード 0 が返ること" in content
    assert "終了コード 1 が返ること" in content


def test_generate_test_file_step_dedup(tmp_path):
    """同一ステップが重複生成されないこと。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "shared.feature"
    feature_file.write_text(SAMPLE_FEATURE_SHARED_STEPS, encoding="utf-8")

    out_dir = tmp_path / "tests"
    result = generate_test_file(feature_file, out_dir, feature_dir)

    assert result is not None
    content = result.read_text(encoding="utf-8")

    # 「共通の前提条件がある」ステップの関数は1回のみ
    step_hash = _hash_name("given:共通の前提条件がある")
    count = content.count(f"def given_{step_hash}")
    assert count == 1, f"重複ステップ関数: given_{step_hash} が {count} 回出現"


def test_generate_test_file_skip_existing(tmp_path):
    """既存ファイルがある場合スキップすること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "sample.feature"
    feature_file.write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "tests"
    out_dir.mkdir()
    existing = out_dir / "step_sample.py"
    existing.write_text("# existing", encoding="utf-8")

    result = generate_test_file(feature_file, out_dir, feature_dir, overwrite=False)
    assert result is None
    assert existing.read_text() == "# existing"


def test_generate_test_file_overwrite(tmp_path):
    """--overwrite で既存ファイルが上書きされること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "sample.feature"
    feature_file.write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "tests"
    out_dir.mkdir()
    existing = out_dir / "step_sample.py"
    existing.write_text("# existing", encoding="utf-8")

    result = generate_test_file(feature_file, out_dir, feature_dir, overwrite=True)
    assert result is not None
    assert "# existing" not in result.read_text()


# ---------------------------------------------------------------------------
# scaffold コマンド CLI テスト
# ---------------------------------------------------------------------------


def test_scaffold_cmd_generates_files(tmp_path):
    """scaffold コマンドでテストファイルが生成されること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    (feature_dir / "sample.feature").write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "tests"

    result = runner.invoke(app, [
        "scaffold", str(feature_dir),
        "--out-dir", str(out_dir),
    ])

    assert result.exit_code == 0
    assert (out_dir / "step_sample.py").exists()
    assert "生成" in result.stdout


def test_scaffold_cmd_skip_existing(tmp_path):
    """scaffold コマンドで既存ファイルがスキップされること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    (feature_dir / "sample.feature").write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "tests"
    out_dir.mkdir()
    (out_dir / "step_sample.py").write_text("# existing", encoding="utf-8")

    result = runner.invoke(app, [
        "scaffold", str(feature_dir),
        "--out-dir", str(out_dir),
    ])

    assert result.exit_code == 0
    assert "スキップ" in result.stdout
    assert (out_dir / "step_sample.py").read_text() == "# existing"


def test_scaffold_cmd_no_features(tmp_path):
    """feature ファイルがない場合の動作。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()

    result = runner.invoke(app, [
        "scaffold", str(feature_dir),
        "--out-dir", str(tmp_path / "tests"),
    ])

    assert result.exit_code == 0
    assert "見つかりません" in result.stdout


# ---------------------------------------------------------------------------
# ci コマンド CLI テスト
# ---------------------------------------------------------------------------


@patch("spec_weaver.cli.subprocess.run")
@patch("spec_weaver.cli._run_build")
def test_ci_cmd_full_flow(mock_build, mock_subprocess, tmp_path):
    """ci コマンドのフルフローが動作すること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    (feature_dir / "sample.feature").write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    (test_dir / "step_sample.py").write_text("# test", encoding="utf-8")

    report_path = tmp_path / "results.json"
    # pytest の実行をモック（成功）
    mock_subprocess.return_value = MagicMock(returncode=0, stdout="passed", stderr="")
    # report ファイルを作成してモック
    report_path.write_text("[]", encoding="utf-8")

    result = runner.invoke(app, [
        "ci", str(feature_dir),
        "--test-dir", str(test_dir),
        "--out-dir", str(tmp_path / "out"),
        "--report", str(report_path),
        "--repo-root", str(tmp_path),
    ])

    assert mock_subprocess.called
    assert mock_build.called
    # build に report パスが渡されること
    build_args = mock_build.call_args
    assert build_args[0][3] == report_path


@patch("spec_weaver.cli.subprocess.run")
@patch("spec_weaver.cli._run_build")
def test_ci_cmd_test_failure_continues_build(mock_build, mock_subprocess, tmp_path):
    """テスト失敗時もドキュメント生成が継続されること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()

    test_dir = tmp_path / "tests"
    test_dir.mkdir()

    report_path = tmp_path / "results.json"
    mock_subprocess.return_value = MagicMock(returncode=1, stdout="1 failed", stderr="")
    report_path.write_text("[]", encoding="utf-8")

    result = runner.invoke(app, [
        "ci", str(feature_dir),
        "--test-dir", str(test_dir),
        "--report", str(report_path),
        "--repo-root", str(tmp_path),
    ])

    # テスト失敗でも build は呼ばれる
    assert mock_build.called
    assert "テストに失敗があります" in result.stdout
    assert result.exit_code == 1


@patch("spec_weaver.cli.subprocess.run")
@patch("spec_weaver.cli._run_build")
def test_ci_cmd_with_scaffold(mock_build, mock_subprocess, tmp_path):
    """--scaffold オプション付き ci がテストコード生成を行うこと。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    (feature_dir / "sample.feature").write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    test_dir = tmp_path / "tests_out"

    report_path = tmp_path / "results.json"
    mock_subprocess.return_value = MagicMock(returncode=0, stdout="passed", stderr="")
    report_path.write_text("[]", encoding="utf-8")

    result = runner.invoke(app, [
        "ci", str(feature_dir),
        "--test-dir", str(test_dir),
        "--report", str(report_path),
        "--scaffold",
        "--repo-root", str(tmp_path),
    ])

    # scaffold で生成されたファイルが存在すること
    assert (test_dir / "step_sample.py").exists()
