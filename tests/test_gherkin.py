import pytest
from spec_weaver.gherkin import get_tags


def test_get_tags_success(tmp_path):
    # 正常なGherkinファイルを作成
    feature_file = tmp_path / "valid.feature"
    feature_file.write_text("""
@SPEC-001
Feature: User Login
  @SPEC-002
  Scenario: Successful login
    Given a user
    When they login
    Then it works
    """, encoding="utf-8")

    # サブディレクトリにもファイルを作成（再帰探索のテスト）
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    sub_feature = sub_dir / "sub.feature"
    sub_feature.write_text("""
Feature: Sub feature
  @SPEC-003 @other-tag
  Scenario: Sub scenario
    Given something
    """, encoding="utf-8")

    # 実行と検証
    tags = get_tags(tmp_path, prefix="SPEC")
    
    # SPEC-001 (Feature), SPEC-002 (Scenario), SPEC-003 (Sub-dir) が抽出されるべき
    assert tags == {"SPEC-001", "SPEC-002", "SPEC-003"}
    # @other-tag はプレフィックスが違うため無視されるべき

def test_get_tags_syntax_error(tmp_path):
    # 文法エラーのある（Feature宣言すらない）真に無効なGherkinファイルを作成
    invalid_file = tmp_path / "invalid.feature"
    invalid_file.write_text("""
This is completely invalid Gherkin.
いきなりプレーンテキストを書くことは許されません。
    """, encoding="utf-8")

    # 構文エラー時に ValueError が送出されることを検証
    with pytest.raises(ValueError, match="Gherkin構文エラー"):
        get_tags(tmp_path, prefix="SPEC")
