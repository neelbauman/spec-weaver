"""review コマンドと clear コマンドのユニットテスト。"""

import shutil
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from spec_weaver.cli import app
from spec_weaver.gherkin import read_stored_fingerprint, _FINGERPRINT_PREFIX

runner = CliRunner()


# ---------------------------------------------------------------------------
# review コマンド
# ---------------------------------------------------------------------------

def test_review_writes_fingerprint_to_feature_file(tmp_path):
    """review コマンドが .feature ファイル先頭にフィンガープリントコメントを書き込む。"""
    feature_file = tmp_path / "test.feature"
    feature_file.write_text(
        "@SPEC-003\nFeature: test\n  Scenario: s1\n    Given something\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["review", str(feature_file)])

    assert result.exit_code == 0, f"exit_code={result.exit_code}\n{result.output}"
    stored = read_stored_fingerprint(feature_file)
    assert stored is not None, "先頭コメントが書き込まれていません"
    assert len(stored) == 64, f"SHA-256 ハッシュ長が不正: {stored}"


def test_review_overwrites_existing_fingerprint(tmp_path):
    """review コマンドが既存のフィンガープリントコメントを上書きする。"""
    feature_file = tmp_path / "test.feature"
    old_fp = "0" * 64
    feature_file.write_text(
        f"{_FINGERPRINT_PREFIX}{old_fp}\n@SPEC-003\nFeature: test\n",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["review", str(feature_file)])

    assert result.exit_code == 0, f"exit_code={result.exit_code}\n{result.output}"
    stored = read_stored_fingerprint(feature_file)
    assert stored != old_fp, "古いフィンガープリントが上書きされていません"


def test_review_nonexistent_file_returns_exit_1():
    """.feature ファイルが存在しない場合は終了コード 1 を返す。"""
    result = runner.invoke(app, ["review", "nonexistent.feature"])
    assert result.exit_code == 1


def test_review_non_feature_file_returns_exit_1(tmp_path):
    """.feature 以外のファイルを指定した場合は終了コード 1 を返す。"""
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("hello")
    result = runner.invoke(app, ["review", str(txt_file)])
    assert result.exit_code == 1


# ---------------------------------------------------------------------------
# clear コマンド
# ---------------------------------------------------------------------------

@patch("spec_weaver.cli.get_all_prefixes")
@patch("spec_weaver.cli.get_tags")
@patch("spec_weaver.cli.get_spec_fingerprints")
@patch("spec_weaver.cli.update_item_attribute")
def test_clear_feature_file_updates_yaml(
    mock_update, mock_get_fp, mock_get_tags, mock_get_prefixes, tmp_path
):
    """.feature ファイルを指定した場合、ファイル内の全タグの test_fingerprint を更新する。"""
    feature_file = tmp_path / "test.feature"
    feature_file.write_text("@SPEC-001\n@SPEC-002\nFeature: test\n")

    mock_get_prefixes.return_value = {"SPEC"}
    mock_get_tags.return_value = {"SPEC-001", "SPEC-002"}
    mock_get_fp.return_value = {
        "SPEC-001": "hash1",
        "SPEC-002": "hash2",
    }

    result = runner.invoke(app, ["clear", str(feature_file), "--repo-root", str(tmp_path)])

    assert result.exit_code == 0, f"exit_code={result.exit_code}\n{result.output}"
    assert mock_update.call_count == 2
    mock_update.assert_any_call(tmp_path, "SPEC-001", "test_fingerprint", "hash1")
    mock_update.assert_any_call(tmp_path, "SPEC-002", "test_fingerprint", "hash2")


@patch("spec_weaver.cli.get_all_prefixes")
@patch("spec_weaver.cli.get_spec_fingerprints")
@patch("spec_weaver.cli.update_item_attribute")
def test_clear_single_item_updates_yaml(
    mock_update, mock_get_fp, mock_get_prefixes, tmp_path
):
    """アイテムIDを指定した場合、そのアイテムの test_fingerprint を更新する。"""
    mock_get_prefixes.return_value = {"SPEC"}
    mock_get_fp.return_value = {"SPEC-001": "hash1"}

    result = runner.invoke(app, [
        "clear", "SPEC-001",
        "--repo-root", str(tmp_path),
        "--feature-dir", "specification/features",
    ])

    assert result.exit_code == 0, f"exit_code={result.exit_code}\n{result.output}"
    mock_update.assert_called_once_with(tmp_path, "SPEC-001", "test_fingerprint", "hash1")


@patch("spec_weaver.cli.get_all_prefixes")
@patch("spec_weaver.cli.get_spec_fingerprints")
def test_clear_nonexistent_item_returns_exit_1(
    mock_get_fp, mock_get_prefixes, tmp_path
):
    """存在しないアイテム ID を指定した場合は終了コード 1 を返す。"""
    mock_get_prefixes.return_value = {"SPEC"}
    mock_get_fp.return_value = {}

    result = runner.invoke(app, [
        "clear", "SPEC-999",
        "--repo-root", str(tmp_path),
        "--feature-dir", "specification/features",
    ])

    assert result.exit_code == 1
