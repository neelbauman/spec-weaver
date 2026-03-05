# src/spec_weaver/services/bdd_service.py
"""BDD アイテムの追加・管理サービス。

.feature ファイルの取り込み（タグ→リンク変換）および
BDD アイテムの新規作成を担当する。
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional

from spec_weaver.adapters.doorstop import get_doorstop_tree

# spec タグのパターン: @PREFIX-NNN（大文字英字 + ハイフン + 数字）
_TAG_PATTERN = re.compile(r"@([A-Z]+-\d+)")
# fingerprint コメント行
_FINGERPRINT_COMMENT = re.compile(r"^#\s*spec-weaver-fingerprint.*$", re.MULTILINE)


@dataclass
class ImportResult:
    """BDD アイテム取り込み結果。"""

    item_uid: str
    slug: str
    extracted_links: List[str] = field(default_factory=list)
    header: str = ""
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.error is None


def parse_feature_tags(text: str) -> list[str]:
    """Gherkin テキストの Feature 行より前にあるタグを抽出する。

    Returns:
        抽出された仕様タグの UID リスト（例: ["QA-001", "VIS-002"]）。
    """
    tags: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        # 空行・コメント行はスキップ
        if not stripped or stripped.startswith("#"):
            continue
        # Feature: 行に達したら終了
        if stripped.startswith("Feature:"):
            break
        # タグ行: @XXX-NNN を抽出
        found = _TAG_PATTERN.findall(stripped)
        tags.extend(found)
    return tags


def strip_feature_tags_and_comments(text: str) -> str:
    """Gherkin テキストから仕様タグ行と fingerprint コメントを除去する。

    Feature 行より前のタグ行（@PREFIX-NNN を含む行）を除去し、
    spec-weaver-fingerprint コメント行も除去する。
    Feature 行以降はそのまま保持する。
    """
    # fingerprint コメント除去
    text = _FINGERPRINT_COMMENT.sub("", text)

    lines = text.splitlines()
    result_lines: list[str] = []
    reached_feature = False

    for line in lines:
        if not reached_feature:
            stripped = line.strip()
            # 空行はスキップ（Feature 行前の空行を除去）
            if not stripped:
                continue
            # タグ行をスキップ
            if _TAG_PATTERN.search(stripped) and not stripped.startswith("Feature:"):
                continue
            # Feature: 行に達した
            if stripped.startswith("Feature:"):
                reached_feature = True
                result_lines.append(line)
                continue
            # その他の行（コメントなど）は保持
            result_lines.append(line)
        else:
            result_lines.append(line)

    return "\n".join(result_lines) + "\n" if result_lines else ""


def extract_feature_header(text: str) -> str:
    """Gherkin テキストから Feature タイトルを抽出する。"""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("Feature:"):
            return stripped[len("Feature:") :].strip()
    return ""


def import_feature_file(
    feature_path: Path,
    repo_root: Path,
    prefix: str = "BDD",
    slug: Optional[str] = None,
    extra_links: Optional[List[str]] = None,
) -> ImportResult:
    """既存の .feature ファイルを BDD アイテムとして取り込む。

    1. .feature ファイルを読み込む
    2. タグを抽出してリンクに変換
    3. タグ・fingerprint コメントを除去
    4. BDD アイテムを作成（text, links, slug, header 設定）

    Args:
        feature_path: 取り込む .feature ファイルのパス。
        repo_root: Doorstop リポジトリルート。
        prefix: BDD ドキュメントのプレフィックス。
        slug: .feature ファイル名（省略時はファイル名のステムを使用）。
        extra_links: 追加リンク先 UID リスト。

    Returns:
        ImportResult。
    """
    if not feature_path.exists():
        return ImportResult(
            item_uid="", slug="", error=f"ファイルが見つかりません: {feature_path}"
        )

    raw_text = feature_path.read_text(encoding="utf-8")

    # タグ抽出
    extracted_tags = parse_feature_tags(raw_text)

    # テキストからタグ・コメント除去
    clean_text = strip_feature_tags_and_comments(raw_text)

    # ヘッダー抽出
    header = extract_feature_header(raw_text)

    # slug 決定
    if slug is None:
        slug = feature_path.stem

    # 全リンク（タグから抽出 + 追加指定）
    all_links = list(extracted_tags)
    if extra_links:
        for link in extra_links:
            if link not in all_links:
                all_links.append(link)

    # Doorstop でアイテム作成
    try:
        item_uid = _create_bdd_item(
            repo_root=repo_root,
            prefix=prefix,
            text=clean_text,
            header=header,
            slug=slug,
            links=all_links,
        )
    except Exception as e:
        return ImportResult(
            item_uid="", slug=slug, error=f"アイテム作成に失敗: {e}"
        )

    return ImportResult(
        item_uid=item_uid,
        slug=slug,
        extracted_links=all_links,
        header=header,
    )


def create_bdd_item(
    repo_root: Path,
    slug: str,
    links: Optional[List[str]] = None,
    prefix: str = "BDD",
    header: str = "",
) -> ImportResult:
    """新規 BDD アイテムをテンプレートから作成する。

    Args:
        repo_root: Doorstop リポジトリルート。
        slug: .feature ファイル名（拡張子なし）。
        links: リンク先 UID リスト。
        prefix: BDD ドキュメントのプレフィックス。
        header: Feature のタイトル。

    Returns:
        ImportResult。
    """
    if not header:
        header = slug

    template_text = f"Feature: {header}\n"

    try:
        item_uid = _create_bdd_item(
            repo_root=repo_root,
            prefix=prefix,
            text=template_text,
            header=header,
            slug=slug,
            links=links or [],
        )
    except Exception as e:
        return ImportResult(
            item_uid="", slug=slug, error=f"アイテム作成に失敗: {e}"
        )

    return ImportResult(
        item_uid=item_uid,
        slug=slug,
        extracted_links=links or [],
        header=header,
    )


# ---------------------------------------------------------------------------
# .feature ファイル生成
# ---------------------------------------------------------------------------


@dataclass
class GenerateResult:
    """BDD → .feature 生成結果。"""

    generated_count: int = 0
    skipped_count: int = 0
    generated_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def is_success(self) -> bool:
        return len(self.errors) == 0


def generate_feature_files(
    repo_root: Path,
    out_dir: Path,
    prefix: str = "BDD",
) -> GenerateResult:
    """BDD アイテムから .feature ファイルを生成する。

    各 BDD アイテムの text フィールドから Gherkin を取り出し、
    @BDD-XXX タグを先頭に付与して out_dir に書き出す。

    Args:
        repo_root: Doorstop リポジトリルート。
        out_dir: .feature ファイルの出力先ディレクトリ。
        prefix: BDD ドキュメントのプレフィックス。

    Returns:
        GenerateResult。
    """
    multi_tree = get_doorstop_tree(repo_root)
    doc = _find_document(multi_tree, prefix)

    result = GenerateResult()

    if doc is None:
        # BDD ドキュメントが存在しない場合はスキップ（エラーではない）
        return result

    out_dir.mkdir(parents=True, exist_ok=True)

    # slug の重複チェック用
    seen_slugs: dict[str, str] = {}

    for item in doc:
        if not item.active:
            result.skipped_count += 1
            continue

        uid = str(item.uid)
        slug = None
        try:
            slug = item.get("slug")
        except (AttributeError, KeyError):
            pass

        if not slug:
            result.errors.append(f"{uid}: slug が設定されていません")
            continue

        # slug 重複チェック
        if slug in seen_slugs:
            result.errors.append(
                f"{uid}: slug '{slug}' が {seen_slugs[slug]} と重複しています"
            )
            continue
        seen_slugs[slug] = uid

        text = item.text or ""
        if not text.strip():
            result.errors.append(f"{uid}: text が空です")
            continue

        # @BDD-XXX タグを付与して .feature を生成
        feature_content = _build_feature_content(uid, text)
        feature_path = out_dir / f"{slug}.feature"
        feature_path.write_text(feature_content, encoding="utf-8")

        result.generated_count += 1
        result.generated_files.append(str(feature_path))

    return result


def _build_feature_content(uid: str, text: str) -> str:
    """BDD アイテムの text に @BDD-XXX タグを付与した .feature 内容を生成する。"""
    lines = text.splitlines()
    result_lines: list[str] = []
    tag_inserted = False

    for line in lines:
        stripped = line.strip()
        if not tag_inserted and stripped.startswith("Feature:"):
            # Feature 行の直前に @BDD-XXX タグを挿入
            result_lines.append(f"@{uid}")
            tag_inserted = True
        result_lines.append(line)

    if not tag_inserted:
        # Feature 行がない場合は先頭にタグを追加
        result_lines.insert(0, f"@{uid}")

    return "\n".join(result_lines)
    # 末尾改行は text に含まれている前提


def _create_bdd_item(
    repo_root: Path,
    prefix: str,
    text: str,
    header: str,
    slug: str,
    links: List[str],
) -> str:
    """Doorstop API を使って BDD アイテムを作成する。

    Returns:
        作成されたアイテムの UID 文字列。
    """
    multi_tree = get_doorstop_tree(repo_root)

    # BDD ドキュメントを検索
    doc = _find_document(multi_tree, prefix)
    if doc is None:
        raise ValueError(
            f"ドキュメント '{prefix}' が見つかりません。"
            f"先に 'spec-weaver create {prefix} <path>' で作成してください。"
        )

    # slug の一意性チェック
    _check_slug_uniqueness(doc, slug)

    # アイテム追加
    item = doc.add_item()
    item.text = text
    item.header = header
    item.set("slug", slug)

    # リンク設定
    for link_uid in links:
        item.link(link_uid)

    item.save()
    return str(item.uid)


def _find_document(multi_tree: Any, prefix: str) -> Any:
    """MultiTree からプレフィックスでドキュメントを検索する。"""
    for doc in multi_tree:
        if str(doc.prefix) == prefix:
            return doc
    return None


def _check_slug_uniqueness(doc: Any, slug: str) -> None:
    """ドキュメント内で slug が一意であることを確認する。"""
    for item in doc:
        if not item.active:
            continue
        existing_slug = None
        try:
            existing_slug = item.get("slug")
        except (AttributeError, KeyError):
            pass
        if existing_slug == slug:
            raise ValueError(
                f"slug '{slug}' は既に {item.uid} で使用されています。"
                f"別の slug を指定してください。"
            )
