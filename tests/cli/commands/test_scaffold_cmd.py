"""scaffold / ci コマンド および codegen モジュールのテスト。"""

import hashlib
import re
import ast as python_ast
from pathlib import Path
from unittest.mock import patch, MagicMock

from typer.testing import CliRunner

from spec_weaver.cli.main import app
from spec_weaver.adapters.codegen import (
    _hash_name,
    _escape_string,
    _step_keyword_to_prefix,
    _resolve_step_prefixes,
    _collect_existing_steps,
    _parse_step_file,
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

SAMPLE_FEATURE_EXTENDED = """\
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

  Scenario: 新機能の検証
    Given 新しい前提条件がある
    When  新しい操作を実行する
    Then  新しい結果が得られること
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
    assert _escape_string('hello "world"') == "hello <world>"
    assert _escape_string("no quotes") == "no quotes"
    assert _escape_string('"⚠️ Suspect"') == "<⚠️ Suspect>"


def test_escape_string_backslash():
    """バックスラッシュが正しくエスケープされること。"""
    assert _escape_string("path\\to\\file") == "path\\\\to\\\\file"


def test_generate_test_file_with_quotes(tmp_path):
    """ダブルクオーテーションを含むステップが正しく生成されること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "quotes.feature"
    feature_file.write_text(SAMPLE_FEATURE_QUOTES, encoding="utf-8")

    out_dir = tmp_path / "tests"
    result = generate_test_file(feature_file, out_dir, feature_dir)

    assert result is not None
    out_file, status, diff_text = result
    assert status == "created"
    content = out_file.read_text(encoding="utf-8")

    # 構文的に正しい Python であること
    python_ast.parse(content)

    # ダブルクオーテーション内の文字列がパラメータ化されていること
    assert '"{param0}"' in content
    assert '"{param1}"' in content
    # オリジナルのステップ文が Docstring に保持されていること
    assert "⚠️ Suspect" in content
    assert "📋 Unreviewed" in content


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
    out_file, status, diff_text = result
    assert status == "created"
    assert diff_text == ""
    assert out_file.name == "step_sample.py"
    assert out_file.exists()

    content = out_file.read_text(encoding="utf-8")

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


def test_generate_test_file_docstring_scenarios(tmp_path):
    """各ステップ関数の Docstring に Scenarios セクションが含まれること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "sample.feature"
    feature_file.write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "tests"
    result = generate_test_file(feature_file, out_dir, feature_dir)

    assert result is not None
    out_file, _, _ = result
    content = out_file.read_text(encoding="utf-8")

    # Scenarios セクションが存在すること
    assert "Scenarios:" in content
    # 各シナリオ名が列挙されていること
    assert "- 完全一致時の監査成功" in content
    assert "- テスト漏れの検出" in content


def test_generate_test_file_step_dedup(tmp_path):
    """同一ステップが重複生成されないこと。共有ステップは両シナリオを Docstring に持つ。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "shared.feature"
    feature_file.write_text(SAMPLE_FEATURE_SHARED_STEPS, encoding="utf-8")

    out_dir = tmp_path / "tests"
    result = generate_test_file(feature_file, out_dir, feature_dir)

    assert result is not None
    out_file, _, _ = result
    content = out_file.read_text(encoding="utf-8")

    # 「共通の前提条件がある」ステップの関数は1回のみ
    step_hash = _hash_name("given:共通の前提条件がある")
    count = content.count(f"def given_{step_hash}")
    assert count == 1, f"重複ステップ関数: given_{step_hash} が {count} 回出現"

    # 共有ステップの Docstring に両シナリオが列挙されていること
    assert "- シナリオA" in content
    assert "- シナリオB" in content


def test_generate_test_file_no_change_returns_none(tmp_path):
    """同一 .feature で2度実行した場合、2回目は None（変更なし）を返すこと。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "sample.feature"
    feature_file.write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "tests"
    # 1回目: 生成
    first = generate_test_file(feature_file, out_dir, feature_dir)
    assert first is not None
    _, status, _ = first
    assert status == "created"

    # 2回目: 変更なし
    second = generate_test_file(feature_file, out_dir, feature_dir)
    assert second is None


def test_generate_test_file_merge_new_steps(tmp_path):
    """新規ステップが既存ファイルに差分マージされること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "sample.feature"

    out_dir = tmp_path / "tests"

    # 最初は元のフィーチャーで生成
    feature_file.write_text(SAMPLE_FEATURE_JA, encoding="utf-8")
    first = generate_test_file(feature_file, out_dir, feature_dir)
    assert first is not None

    # ステップを追加した拡張フィーチャーでマージ
    feature_file.write_text(SAMPLE_FEATURE_EXTENDED, encoding="utf-8")
    result = generate_test_file(feature_file, out_dir, feature_dir, overwrite=False)

    assert result is not None
    out_file, status, diff_text = result
    assert status == "updated"
    assert "--- a/" in diff_text
    assert "+++ b/" in diff_text

    merged = out_file.read_text(encoding="utf-8")

    # 元のステップが保持されていること
    assert "終了コード 0 が返ること" in merged
    assert "終了コード 1 が返ること" in merged

    # 新規ステップが追記されていること
    assert "新しい前提条件がある" in merged
    assert "新しい操作を実行する" in merged
    assert "新しい結果が得られること" in merged

    # 構文的に正しい Python であること
    python_ast.parse(merged)


def test_generate_test_file_merge_order(tmp_path):
    """新規ステップが .feature の出現順で挿入されること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "sample.feature"
    out_dir = tmp_path / "tests"

    # 1回目: 元のフィーチャーで生成
    feature_file.write_text(SAMPLE_FEATURE_JA, encoding="utf-8")
    generate_test_file(feature_file, out_dir, feature_dir)

    # 2回目: 新規ステップ追加でマージ
    feature_file.write_text(SAMPLE_FEATURE_EXTENDED, encoding="utf-8")
    result = generate_test_file(feature_file, out_dir, feature_dir)
    assert result is not None
    out_file, _, _ = result

    content = out_file.read_text(encoding="utf-8")

    # 新規ステップ（新しい前提条件がある）が、既存の最後のステップより後にあること
    pos_existing = content.rfind("終了コード 1 が返ること")
    pos_new = content.find("新しい前提条件がある")
    assert pos_existing < pos_new, "新規ステップが既存ステップより前に挿入されている"


def test_generate_test_file_merge_scenarios_update(tmp_path):
    """既存ステップの Docstring に新しいシナリオ名が追記されること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "shared.feature"
    out_dir = tmp_path / "tests"

    # 共有ステップを持つフィーチャー（シナリオA・Bで共有）
    feature_file.write_text(SAMPLE_FEATURE_SHARED_STEPS, encoding="utf-8")
    first = generate_test_file(feature_file, out_dir, feature_dir)
    assert first is not None

    # 新しいシナリオCを追加（共有ステップを再利用）
    extended = (
        SAMPLE_FEATURE_SHARED_STEPS
        + """\
  Scenario: シナリオC
    Given 共通の前提条件がある
    When  操作Cを実行する
    Then  結果Cが得られること
"""
    )
    feature_file.write_text(extended, encoding="utf-8")
    result = generate_test_file(feature_file, out_dir, feature_dir)

    assert result is not None
    out_file, status, _ = result
    assert status == "updated"

    content = out_file.read_text(encoding="utf-8")
    # 共有ステップの Docstring にシナリオCが追記されていること
    assert "- シナリオC" in content


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
    out_file, status, _ = result
    assert status == "created"
    assert "# existing" not in out_file.read_text()


# ---------------------------------------------------------------------------
# scaffold コマンド CLI テスト
# ---------------------------------------------------------------------------


def test_scaffold_cmd_generates_files(tmp_path):
    """scaffold コマンドでテストファイルが生成されること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    (feature_dir / "sample.feature").write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "tests"

    result = runner.invoke(
        app,
        [
            "scaffold",
            str(feature_dir),
            "--out-dir",
            str(out_dir),
        ],
    )

    assert result.exit_code == 0
    assert (out_dir / "step_sample.py").exists()
    assert "新規作成" in result.stdout


def test_scaffold_cmd_generates_environment_py(tmp_path):
    """scaffold コマンドで environment.py が生成されること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    (feature_dir / "sample.feature").write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "steps"

    result = runner.invoke(
        app,
        [
            "scaffold",
            str(feature_dir),
            "--out-dir",
            str(out_dir),
        ],
    )

    assert result.exit_code == 0
    assert (feature_dir / "environment.py").exists()
    assert "環境設定作成" in result.stdout
    assert "behave 環境設定" in (feature_dir / "environment.py").read_text()


def test_scaffold_cmd_skips_environment_py_if_exists(tmp_path):
    """environment.py が既に存在する場合、上書きせずにスキップすること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    (feature_dir / "sample.feature").write_text(SAMPLE_FEATURE_JA, encoding="utf-8")
    env_file = feature_dir / "environment.py"
    env_file.write_text("existing content", encoding="utf-8")

    out_dir = tmp_path / "steps"

    result = runner.invoke(
        app,
        [
            "scaffold",
            str(feature_dir),
            "--out-dir",
            str(out_dir),
        ],
    )

    assert result.exit_code == 0
    assert "スキップ" in result.stdout
    assert env_file.read_text() == "existing content"


def test_scaffold_cmd_skip_no_diff(tmp_path):
    """既存ファイルと差分がない場合はスキップされること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    (feature_dir / "sample.feature").write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "tests"

    # 1回目: 生成
    runner.invoke(app, ["scaffold", str(feature_dir), "--out-dir", str(out_dir)])
    original_content = (out_dir / "step_sample.py").read_text()

    # 2回目: 差分なし → スキップ
    result = runner.invoke(
        app, ["scaffold", str(feature_dir), "--out-dir", str(out_dir)]
    )

    assert result.exit_code == 0
    assert "スキップ" in result.stdout
    assert (out_dir / "step_sample.py").read_text() == original_content


def test_scaffold_cmd_merge_diff_display(tmp_path):
    """差分マージ時に diff が表示されること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "sample.feature"
    out_dir = tmp_path / "tests"

    # 1回目: 元の feature で生成
    feature_file.write_text(SAMPLE_FEATURE_JA, encoding="utf-8")
    runner.invoke(app, ["scaffold", str(feature_dir), "--out-dir", str(out_dir)])

    # 2回目: 新規ステップ追加でマージ
    feature_file.write_text(SAMPLE_FEATURE_EXTENDED, encoding="utf-8")
    result = runner.invoke(
        app, ["scaffold", str(feature_dir), "--out-dir", str(out_dir)]
    )

    assert result.exit_code == 0
    assert "差分更新" in result.stdout
    assert "生成/更新" in result.stdout


def test_scaffold_cmd_no_features(tmp_path):
    """feature ファイルがない場合の動作。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()

    result = runner.invoke(
        app,
        [
            "scaffold",
            str(feature_dir),
            "--out-dir",
            str(tmp_path / "tests"),
        ],
    )

    assert result.exit_code == 0
    assert "見つかりません" in result.stdout


@patch("spec_weaver.cli.commands.scaffold_cmd.is_file_dirty")
def test_scaffold_cmd_dirty_prompt_cancel(mock_dirty, tmp_path):
    """Git dirty ファイルの確認プロンプトでキャンセルするとスキップされること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "sample.feature"
    feature_file.write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "tests"
    out_dir.mkdir()
    out_file = out_dir / "step_sample.py"
    out_file.write_text("# existing", encoding="utf-8")

    mock_dirty.return_value = True

    # "n" を入力してキャンセル
    result = runner.invoke(
        app,
        [
            "scaffold",
            str(feature_dir),
            "--out-dir",
            str(out_dir),
        ],
        input="n\n",
    )

    assert result.exit_code == 0
    assert "スキップ" in result.stdout
    # ファイルは変更されていないこと
    assert out_file.read_text() == "# existing"


@patch("spec_weaver.cli.commands.scaffold_cmd.is_file_dirty")
def test_scaffold_cmd_force_skips_prompt(mock_dirty, tmp_path):
    """--force オプションで確認プロンプトなしにマージが実行されること。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    feature_file = feature_dir / "sample.feature"
    feature_file.write_text(SAMPLE_FEATURE_JA, encoding="utf-8")

    out_dir = tmp_path / "tests"

    # 1回目: 生成
    runner.invoke(app, ["scaffold", str(feature_dir), "--out-dir", str(out_dir)])

    # ファイルが dirty とみなされる状態で拡張 feature にマージ
    mock_dirty.return_value = True
    feature_file.write_text(SAMPLE_FEATURE_EXTENDED, encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "scaffold",
            str(feature_dir),
            "--out-dir",
            str(out_dir),
            "--force",
        ],
    )

    assert result.exit_code == 0
    # プロンプトなしでマージが実行されていること（差分更新 or 新規作成）
    assert "差分更新" in result.stdout or "新規作成" in result.stdout
    # 新規ステップが追記されていること
    assert "新しい前提条件がある" in (out_dir / "step_sample.py").read_text()


# ---------------------------------------------------------------------------
# バグ修正テスト
# ---------------------------------------------------------------------------


def test_collect_existing_steps_ignores_commented_duplicates(tmp_path):
    """Duplicate コメントブロック内の @when 等はスキップされること（Bug 1 修正）。"""
    steps_dir = tmp_path / "steps"
    steps_dir.mkdir()

    # コメントのみで実装なしのファイル（Duplicate コメントブロック形式）
    commented_file = steps_dir / "step_other.py"
    commented_file.write_text(
        '"""behave steps for: other"""\n\n'
        "from behave import given, when, then, step\n\n"
        "# [Duplicate Skip] This step is already defined elsewhere\n"
        "# @when('コメントされたステップ')  # type: ignore\n"
        "# def when_abc12345(context):\n"
        "#     raise NotImplementedError('STEP: コメントされたステップ')\n",
        encoding="utf-8",
    )

    result = _collect_existing_steps(steps_dir)
    assert "コメントされたステップ" not in result


def test_merge_stub_replaced_with_duplicate_comment(tmp_path):
    """他ファイルで実装されたステップのスタブが Duplicate コメントに置き換わること（Bug 2 修正）。"""
    feature_dir = tmp_path / "features"
    feature_dir.mkdir()
    out_dir = tmp_path / "tests"
    out_dir.mkdir()

    foo_feature = feature_dir / "foo.feature"
    foo_feature.write_text(
        "Feature: foo機能\n"
        "  Scenario: シナリオ\n"
        "    Given 共有ステップがある\n"
        "    When  foo操作を実行する\n"
        "    Then  foo結果が得られること\n",
        encoding="utf-8",
    )

    # 1回目: step_foo.py のスタブを生成
    generate_test_file(foo_feature, out_dir, feature_dir)
    step_foo = out_dir / "step_foo.py"
    assert "@given('共有ステップがある')" in step_foo.read_text(encoding="utf-8")

    # step_bar.py に「共有ステップがある」の実装を追加
    step_bar = out_dir / "step_bar.py"
    step_bar.write_text(
        '"""behave steps for: bar機能"""\n\n'
        "from behave import given\n\n"
        "@given('共有ステップがある')  # type: ignore\n"
        "def given_shared(context):\n"
        '    """共有ステップがある"""\n'
        "    pass  # 実装済み\n",
        encoding="utf-8",
    )

    # 2回目: 差分マージ → スタブが Duplicate コメントに置き換わること
    result = generate_test_file(foo_feature, out_dir, feature_dir)

    assert result is not None
    _, status, _ = result
    assert status == "updated"

    content = step_foo.read_text(encoding="utf-8")

    # 「共有ステップがある」が Duplicate コメントに置き換わっていること
    assert "[Duplicate Skip]" in content
    # Active な @given('共有ステップがある') はないこと（コメント行以外には存在しない）
    active_given_lines = [
        line
        for line in content.splitlines()
        if "@given('共有ステップがある')" in line and not line.lstrip().startswith("#")
    ]
    assert not active_given_lines, f"Active @given が残っている: {active_given_lines}"

    # 他のスタブ（foo操作・foo結果）は残っていること
    assert "@when('foo操作を実行する')" in content
    assert "@then('foo結果が得られること')" in content


# ---------------------------------------------------------------------------
# AST 解析テスト
# ---------------------------------------------------------------------------


def test_collect_existing_steps_multiline_decorator(tmp_path):
    """複数行にまたがるデコレータからもステップ文を抽出できること。"""
    steps_dir = tmp_path / "steps"
    steps_dir.mkdir()

    py_file = steps_dir / "step_multi.py"
    py_file.write_text(
        "from behave import given\n\n"
        "@given(\n"
        "    '複数行のステップ'\n"
        ")\n"
        "def given_multi(context):\n"
        "    pass\n",
        encoding="utf-8",
    )

    result = _collect_existing_steps(steps_dir)
    assert "複数行のステップ" in result


def test_collect_existing_steps_non_step_decorator(tmp_path):
    """@property 等の非ステップデコレータは無視されること。"""
    steps_dir = tmp_path / "steps"
    steps_dir.mkdir()

    py_file = steps_dir / "step_helper.py"
    py_file.write_text(
        "from behave import given\n\n"
        "class Helper:\n"
        "    @property\n"
        "    def name(self):\n"
        "        return 'test'\n\n"
        "@given('正しいステップ')\n"
        "def given_correct(context):\n"
        "    pass\n",
        encoding="utf-8",
    )

    result = _collect_existing_steps(steps_dir)
    assert "正しいステップ" in result
    assert len(result) == 1


def test_parse_step_file_multiple_decorators():
    """1関数に複数のステップデコレータがある場合、すべて param_texts に含まれること。"""
    content = (
        '"""steps"""\n'
        "from behave import given\n\n"
        "@given('ステップA')\n"
        "@given('ステップB')\n"
        "def given_multi(context):\n"
        "    pass\n"
    )
    header, infos = _parse_step_file(content)
    assert len(infos) == 1
    assert infos[0].name == "given_multi"
    assert "ステップA" in infos[0].param_texts
    assert "ステップB" in infos[0].param_texts


def test_parse_step_file_helper_functions():
    """ステップデコレータのないヘルパー関数は source_text に含まれ、独立ブロックにならないこと。"""
    content = (
        '"""steps"""\n'
        "from behave import given, when\n\n"
        "@given('最初のステップ')\n"
        "def given_first(context):\n"
        "    pass\n\n"
        "def helper_func():\n"
        "    return 42\n\n"
        "@when('次のステップ')\n"
        "def when_next(context):\n"
        "    pass\n"
    )
    header, infos = _parse_step_file(content)
    assert len(infos) == 2
    assert infos[0].name == "given_first"
    assert infos[1].name == "when_next"
    # ヘルパー関数は最初のステップ関数の source_text に含まれる
    assert "helper_func" in infos[0].source_text


def test_parse_step_file_syntax_error():
    """構文エラーのあるファイルでは (content, []) を返すこと。"""
    content = "def broken(\n"
    header, infos = _parse_step_file(content)
    assert header == content
    assert infos == []
