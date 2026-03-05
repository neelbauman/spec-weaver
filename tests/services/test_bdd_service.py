# tests/services/test_bdd_service.py
"""BDD サービスのユニットテスト。

parse / strip / extract 等のピュア関数のテストと、
Doorstop API をモックした import / create のテスト。
"""

from unittest.mock import MagicMock, patch

import pytest

from spec_weaver.services.bdd_service import (
    _build_feature_content,
    _check_slug_uniqueness,
    create_bdd_item,
    extract_feature_header,
    generate_feature_files,
    import_feature_file,
    parse_feature_tags,
    strip_feature_tags_and_comments,
)


# ---------------------------------------------------------------------------
# parse_feature_tags
# ---------------------------------------------------------------------------


class TestParseFeatureTags:
    def test_single_tag(self):
        text = "@QA-001\nFeature: テスト\n"
        assert parse_feature_tags(text) == ["QA-001"]

    def test_multiple_tags_single_line(self):
        text = "@TRC-002 @TRC-003 @QA-003\nFeature: トレース\n"
        assert parse_feature_tags(text) == ["TRC-002", "TRC-003", "QA-003"]

    def test_multiple_tag_lines(self):
        text = "@QA-001\n@VIS-002\nFeature: テスト\n"
        assert parse_feature_tags(text) == ["QA-001", "VIS-002"]

    def test_no_tags(self):
        text = "Feature: タグなし\n  Scenario: テスト\n"
        assert parse_feature_tags(text) == []

    def test_skips_comments(self):
        text = "# spec-weaver-fingerprint: abc\n@QA-001\nFeature: テスト\n"
        assert parse_feature_tags(text) == ["QA-001"]

    def test_skips_empty_lines(self):
        text = "\n\n@QA-001\n\nFeature: テスト\n"
        assert parse_feature_tags(text) == ["QA-001"]

    def test_stops_at_feature_line(self):
        """Feature 行以降のタグは抽出しない。"""
        text = "@QA-001\nFeature: テスト\n  @IGNORED-001\n"
        assert parse_feature_tags(text) == ["QA-001"]

    def test_with_fingerprint_comments(self):
        text = (
            "# spec-weaver-fingerprint: hash123\n"
            "# spec-weaver-fingerprint-QA-001: abc=\n"
            "@QA-001\n"
            "Feature: 監査\n"
        )
        assert parse_feature_tags(text) == ["QA-001"]


# ---------------------------------------------------------------------------
# strip_feature_tags_and_comments
# ---------------------------------------------------------------------------


class TestStripFeatureTagsAndComments:
    def test_strips_tags_and_fingerprints(self):
        text = (
            "# spec-weaver-fingerprint: hash123\n"
            "# spec-weaver-fingerprint-QA-001: abc=\n"
            "@QA-001 @QA-002\n"
            "Feature: 監査コマンド\n"
            "  Scenario: テスト\n"
        )
        result = strip_feature_tags_and_comments(text)
        assert "@QA-001" not in result
        assert "@QA-002" not in result
        assert "spec-weaver-fingerprint" not in result
        assert "Feature: 監査コマンド" in result
        assert "Scenario: テスト" in result

    def test_preserves_feature_content(self):
        text = (
            "@VIS-001\n"
            "Feature: build コマンド\n"
            "  説明文\n"
            "\n"
            "  Scenario: テスト\n"
            "    Given 前提条件\n"
        )
        result = strip_feature_tags_and_comments(text)
        assert result.startswith("Feature: build コマンド\n")
        assert "Scenario: テスト" in result
        assert "Given 前提条件" in result

    def test_no_tags(self):
        text = "Feature: シンプル\n  Scenario: テスト\n"
        result = strip_feature_tags_and_comments(text)
        assert "Feature: シンプル" in result

    def test_multiple_tag_lines(self):
        text = "@QA-001\n@VIS-002\nFeature: テスト\n"
        result = strip_feature_tags_and_comments(text)
        assert "@QA-001" not in result
        assert "@VIS-002" not in result
        assert "Feature: テスト" in result


# ---------------------------------------------------------------------------
# extract_feature_header
# ---------------------------------------------------------------------------


class TestExtractFeatureHeader:
    def test_basic(self):
        assert extract_feature_header("Feature: 監査コマンド\n") == "監査コマンド"

    def test_with_tags_before(self):
        text = "@QA-001\nFeature: audit コマンド\n  Scenario: ...\n"
        assert extract_feature_header(text) == "audit コマンド"

    def test_no_feature_line(self):
        assert extract_feature_header("Scenario: テスト\n") == ""

    def test_whitespace_handling(self):
        assert extract_feature_header("  Feature:   タイトル  \n") == "タイトル"


# ---------------------------------------------------------------------------
# _check_slug_uniqueness
# ---------------------------------------------------------------------------


class TestCheckSlugUniqueness:
    def test_unique_slug(self):
        item = MagicMock()
        item.active = True
        item.get.return_value = "other_slug"
        doc = MagicMock()
        doc.__iter__ = MagicMock(return_value=iter([item]))

        # 例外が発生しないこと
        _check_slug_uniqueness(doc, "new_slug")

    def test_duplicate_slug(self):
        item = MagicMock()
        item.active = True
        item.uid = "BDD-001"
        item.get.return_value = "audit"
        doc = MagicMock()
        doc.__iter__ = MagicMock(return_value=iter([item]))

        with pytest.raises(ValueError, match="audit"):
            _check_slug_uniqueness(doc, "audit")

    def test_inactive_item_ignored(self):
        item = MagicMock()
        item.active = False
        item.get.return_value = "audit"
        doc = MagicMock()
        doc.__iter__ = MagicMock(return_value=iter([item]))

        # inactive なアイテムの slug は無視される
        _check_slug_uniqueness(doc, "audit")


# ---------------------------------------------------------------------------
# import_feature_file (Doorstop モック)
# ---------------------------------------------------------------------------


class TestImportFeatureFile:
    def test_file_not_found(self, tmp_path):
        result = import_feature_file(
            tmp_path / "nonexistent.feature", repo_root=tmp_path
        )
        assert not result.is_success
        assert "見つかりません" in result.error

    @patch("spec_weaver.services.bdd_service._create_bdd_item")
    def test_import_success(self, mock_create, tmp_path):
        mock_create.return_value = "BDD-001"

        feature = tmp_path / "audit.feature"
        feature.write_text(
            "# spec-weaver-fingerprint: hash\n"
            "@QA-001 @QA-002\n"
            "Feature: 監査コマンド\n"
            "  Scenario: テスト\n"
            "    Given 前提条件\n",
            encoding="utf-8",
        )

        result = import_feature_file(feature, repo_root=tmp_path)

        assert result.is_success
        assert result.item_uid == "BDD-001"
        assert result.slug == "audit"
        assert result.extracted_links == ["QA-001", "QA-002"]
        assert result.header == "監査コマンド"

        # _create_bdd_item に渡された引数を検証
        call_kwargs = mock_create.call_args[1]
        assert call_kwargs["prefix"] == "BDD"
        assert call_kwargs["slug"] == "audit"
        assert call_kwargs["links"] == ["QA-001", "QA-002"]
        assert "@QA-001" not in call_kwargs["text"]
        assert "spec-weaver-fingerprint" not in call_kwargs["text"]
        assert "Feature: 監査コマンド" in call_kwargs["text"]

    @patch("spec_weaver.services.bdd_service._create_bdd_item")
    def test_import_with_extra_links(self, mock_create, tmp_path):
        mock_create.return_value = "BDD-002"

        feature = tmp_path / "build.feature"
        feature.write_text(
            "@VIS-001\nFeature: build\n  Scenario: テスト\n",
            encoding="utf-8",
        )

        result = import_feature_file(
            feature, repo_root=tmp_path, extra_links=["VIS-005"]
        )

        assert result.is_success
        assert result.extracted_links == ["VIS-001", "VIS-005"]

    @patch("spec_weaver.services.bdd_service._create_bdd_item")
    def test_import_with_custom_slug(self, mock_create, tmp_path):
        mock_create.return_value = "BDD-003"

        feature = tmp_path / "my_feature.feature"
        feature.write_text("Feature: テスト\n", encoding="utf-8")

        result = import_feature_file(
            feature, repo_root=tmp_path, slug="custom_name"
        )

        assert result.slug == "custom_name"
        call_kwargs = mock_create.call_args[1]
        assert call_kwargs["slug"] == "custom_name"

    @patch("spec_weaver.services.bdd_service._create_bdd_item")
    def test_import_doorstop_error(self, mock_create, tmp_path):
        mock_create.side_effect = ValueError("ドキュメントが見つかりません")

        feature = tmp_path / "test.feature"
        feature.write_text("Feature: テスト\n", encoding="utf-8")

        result = import_feature_file(feature, repo_root=tmp_path)

        assert not result.is_success
        assert "失敗" in result.error


# ---------------------------------------------------------------------------
# create_bdd_item (Doorstop モック)
# ---------------------------------------------------------------------------


class TestCreateBddItem:
    @patch("spec_weaver.services.bdd_service._create_bdd_item")
    def test_create_success(self, mock_create, tmp_path):
        mock_create.return_value = "BDD-001"

        result = create_bdd_item(
            repo_root=tmp_path,
            slug="monitoring",
            links=["QA-003"],
            header="監視機能",
        )

        assert result.is_success
        assert result.item_uid == "BDD-001"
        assert result.slug == "monitoring"
        assert result.header == "監視機能"

        call_kwargs = mock_create.call_args[1]
        assert call_kwargs["slug"] == "monitoring"
        assert call_kwargs["links"] == ["QA-003"]
        assert "Feature: 監視機能" in call_kwargs["text"]

    @patch("spec_weaver.services.bdd_service._create_bdd_item")
    def test_create_uses_slug_as_header_fallback(self, mock_create, tmp_path):
        mock_create.return_value = "BDD-002"

        result = create_bdd_item(
            repo_root=tmp_path,
            slug="monitoring",
        )

        assert result.header == "monitoring"
        call_kwargs = mock_create.call_args[1]
        assert "Feature: monitoring" in call_kwargs["text"]

    @patch("spec_weaver.services.bdd_service._create_bdd_item")
    def test_create_error(self, mock_create, tmp_path):
        mock_create.side_effect = ValueError("ドキュメントが見つかりません")

        result = create_bdd_item(repo_root=tmp_path, slug="test")

        assert not result.is_success
        assert "失敗" in result.error


# ---------------------------------------------------------------------------
# _build_feature_content テスト
# ---------------------------------------------------------------------------


class TestBuildFeatureContent:
    def test_inserts_tag_before_feature(self):
        text = "Feature: 監査コマンド\n  Scenario: テスト\n"
        result = _build_feature_content("BDD-001", text)
        lines = result.splitlines()
        assert lines[0] == "@BDD-001"
        assert lines[1] == "Feature: 監査コマンド"

    def test_no_feature_line(self):
        text = "Scenario: テスト\n"
        result = _build_feature_content("BDD-001", text)
        assert result.startswith("@BDD-001")

    def test_preserves_content_after_feature(self):
        text = "Feature: テスト\n  Scenario: A\n    Given 前提\n"
        result = _build_feature_content("BDD-002", text)
        assert "Scenario: A" in result
        assert "Given 前提" in result


# ---------------------------------------------------------------------------
# generate_feature_files テスト (Doorstop モック)
# ---------------------------------------------------------------------------


class MockBddItem:
    """generate_feature_files テスト用の BDD アイテムモック。"""

    def __init__(self, uid, slug=None, text="", active=True):
        self.uid = uid
        self._slug = slug
        self.text = text
        self.active = active

    def get(self, key, default=None):
        if key == "slug":
            return self._slug
        return default


class MockBddDocument:
    """BDD ドキュメントモック。"""

    def __init__(self, items, prefix="BDD"):
        self.items = items
        self.prefix = prefix

    def __iter__(self):
        return iter(self.items)


class TestGenerateFeatureFiles:
    def _make_mock_tree(self, items):
        """MockBddDocument を含む MultiTree 相当のモックを作成。"""
        doc = MockBddDocument(items)
        # _find_document が prefix で検索するため、__iter__ で doc を返す
        mock_tree = MagicMock()
        mock_tree.__iter__ = MagicMock(return_value=iter([doc]))
        return mock_tree

    @patch("spec_weaver.services.bdd_service.get_doorstop_tree")
    def test_generate_basic(self, mock_get_tree, tmp_path):
        items = [
            MockBddItem(
                "BDD-001",
                slug="audit",
                text="Feature: 監査コマンド\n  Scenario: テスト\n",
            ),
            MockBddItem(
                "BDD-002",
                slug="build",
                text="Feature: ビルド\n  Scenario: ビルドテスト\n",
            ),
        ]
        mock_get_tree.return_value = self._make_mock_tree(items)

        out_dir = tmp_path / "features"
        result = generate_feature_files(tmp_path, out_dir)

        assert result.is_success
        assert result.generated_count == 2
        assert (out_dir / "audit.feature").exists()
        assert (out_dir / "build.feature").exists()

        audit_content = (out_dir / "audit.feature").read_text(encoding="utf-8")
        assert "@BDD-001" in audit_content
        assert "Feature: 監査コマンド" in audit_content

    @patch("spec_weaver.services.bdd_service.get_doorstop_tree")
    def test_generate_skips_inactive(self, mock_get_tree, tmp_path):
        items = [
            MockBddItem("BDD-001", slug="audit", text="Feature: A\n", active=True),
            MockBddItem("BDD-002", slug="old", text="Feature: B\n", active=False),
        ]
        mock_get_tree.return_value = self._make_mock_tree(items)

        out_dir = tmp_path / "features"
        result = generate_feature_files(tmp_path, out_dir)

        assert result.generated_count == 1
        assert result.skipped_count == 1
        assert (out_dir / "audit.feature").exists()
        assert not (out_dir / "old.feature").exists()

    @patch("spec_weaver.services.bdd_service.get_doorstop_tree")
    def test_generate_error_no_slug(self, mock_get_tree, tmp_path):
        items = [MockBddItem("BDD-001", slug=None, text="Feature: テスト\n")]
        mock_get_tree.return_value = self._make_mock_tree(items)

        result = generate_feature_files(tmp_path, tmp_path / "features")

        assert not result.is_success
        assert any("slug" in e for e in result.errors)

    @patch("spec_weaver.services.bdd_service.get_doorstop_tree")
    def test_generate_error_duplicate_slug(self, mock_get_tree, tmp_path):
        items = [
            MockBddItem("BDD-001", slug="audit", text="Feature: A\n"),
            MockBddItem("BDD-002", slug="audit", text="Feature: B\n"),
        ]
        mock_get_tree.return_value = self._make_mock_tree(items)

        result = generate_feature_files(tmp_path, tmp_path / "features")

        assert result.generated_count == 1
        assert any("重複" in e for e in result.errors)

    @patch("spec_weaver.services.bdd_service.get_doorstop_tree")
    def test_generate_error_empty_text(self, mock_get_tree, tmp_path):
        items = [MockBddItem("BDD-001", slug="empty", text="")]
        mock_get_tree.return_value = self._make_mock_tree(items)

        result = generate_feature_files(tmp_path, tmp_path / "features")

        assert not result.is_success
        assert any("空" in e for e in result.errors)

    @patch("spec_weaver.services.bdd_service.get_doorstop_tree")
    def test_generate_no_bdd_document(self, mock_get_tree, tmp_path):
        """BDD ドキュメントが存在しない場合は空の結果を返す。"""
        mock_tree = MagicMock()
        mock_tree.__iter__ = MagicMock(return_value=iter([]))
        mock_get_tree.return_value = mock_tree

        result = generate_feature_files(tmp_path, tmp_path / "features")

        assert result.is_success
        assert result.generated_count == 0
