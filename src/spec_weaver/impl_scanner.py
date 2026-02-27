# src/spec_weaver/impl_scanner.py
# implements: SPEC-017, SPEC-018

"""
実装ファイルと仕様アイテムのリンク管理。

- get_ref_files(item): Doorstopアイテムの impl_files カスタム属性をリストとして返す
- ImplScanner: ソースファイル中の implements アノテーションをスキャンする
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

# アノテーション行にマッチする正規表現
# 対応形式（コメント記号 + "implements:" + ID）:
#   (hash) implements: SPEC-001
#   (slash) implements: SPEC-001, SPEC-002
#   (dash) implements: SPEC-001
_ANNOTATION_RE = re.compile(
    r'^\s*(?:#|//|--)\s*implements:\s*(.+)',
    re.IGNORECASE,
)

# 有効な Doorstop ID 形式: 大文字アルファベット + ハイフン + 数字（例: SPEC-001, REQ-012）
_VALID_ID_RE = re.compile(r'^[A-Z][A-Z0-9_-]*-\d+$')

# スキャン除外ディレクトリ
_EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".mypy_cache", ".ruff_cache"}


def get_ref_files(item: Any) -> list[str]:
    """Doorstopアイテムのカスタム属性 `impl_files` をファイルパスのリストとして返す。

    Doorstop の組み込み `ref` フィールドは文字列専用のため、
    複数ファイルパスの管理には `impl_files` カスタム属性を使用する（SPEC-017）。

    - リスト形式 → そのまま返す
    - 文字列形式 → 単一要素リストとして返す
    - 空 / None → 空リストを返す
    """
    try:
        value = item.get("impl_files")
    except AttributeError:
        value = getattr(item, "impl_files", None)

    if not value:
        return []
    if isinstance(value, list):
        return [str(p) for p in value if str(p).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


class ImplScanner:
    """ソースファイルのアノテーションをスキャンして仕様IDとのマッピングを構築するクラス。"""

    def scan(
        self,
        repo_root: Path,
        extensions: list[str] | None = None,
    ) -> dict[str, set[str]]:
        """リポジトリ内のファイルをスキャンし、仕様ID → ファイルパス集合のマッピングを返す。

        Args:
            repo_root: リポジトリルートのパス（相対パスの基準）
            extensions: スキャン対象の拡張子リスト（例: ["py", "ts"]）。
                        None または空の場合は全テキストファイルを対象とする。

        Returns:
            {spec_id: {relative_file_path, ...}} の辞書
        """
        result: dict[str, set[str]] = {}
        ext_set = {e.lstrip(".").lower() for e in extensions} if extensions else None

        for file_path in self._iter_files(repo_root, ext_set):
            rel_path = str(file_path.relative_to(repo_root))
            for spec_id in self._extract_annotations(file_path):
                result.setdefault(spec_id, set()).add(rel_path)

        return result

    def _iter_files(self, root: Path, ext_set: set[str] | None):
        """除外ディレクトリをスキップしながらファイルを列挙する。"""
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            # 除外ディレクトリのチェック
            if any(part in _EXCLUDE_DIRS for part in path.parts):
                continue
            # 拡張子フィルタ
            if ext_set is not None:
                if path.suffix.lstrip(".").lower() not in ext_set:
                    continue
            yield path

    def _extract_annotations(self, file_path: Path) -> list[str]:
        """ファイルからアノテーションを抽出し、仕様IDのリストを返す。

        有効な Doorstop ID 形式（例: SPEC-001, REQ-012）に一致するものだけを返す。
        文字列リテラル等に埋め込まれた不完全なパターンは除外される。
        """
        ids: list[str] = []
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except (OSError, PermissionError):
            return ids

        for line in text.splitlines():
            m = _ANNOTATION_RE.search(line)
            if m:
                raw = m.group(1)
                for part in raw.split(","):
                    spec_id = part.strip()
                    if spec_id and _VALID_ID_RE.match(spec_id):
                        ids.append(spec_id)
        return ids
