# implements: QA-004, QA-005
"""エディタ起動ユーティリティ。

- open_editor_with_diff: 差分 + 対象ファイルを表示
- open_editor_with_files: 対象ファイル + 関連ファイルを表示

vim/nvim/vi/view/gvim は -O で縦分割表示する。
それ以外のエディタは複数ファイルをまとめて開く。
"""

import os
import shlex
import subprocess
import tempfile
from pathlib import Path

_SPLIT_CAPABLE = frozenset({"vim", "vi", "nvim", "view", "gvim"})


class EditorAbortedError(Exception):
    """エディタが非ゼロ終了コードで終了した。"""


def get_editor() -> str:
    """環境変数 $VISUAL → $EDITOR → vi の順でエディタを返す。"""
    return os.environ.get("VISUAL") or os.environ.get("EDITOR") or "vi"


def get_file_diff(file_path: Path, repo_root: Path) -> str:
    """ファイルの git diff を取得する。

    git diff HEAD で差分を取得し、なければ git log -p -1 で最終コミットの内容を返す。
    いずれも空の場合は空文字列を返す。
    """
    result = subprocess.run(
        ["git", "diff", "HEAD", "--", str(file_path)],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        return result.stdout

    result = subprocess.run(
        ["git", "log", "-p", "-1", "--", str(file_path)],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    return result.stdout


def open_editor_with_diff(target_path: Path, diff_content: str) -> None:
    """差分を左ペインに表示してエディタを開く。

    vim/nvim/vi/view/gvim の場合: -O2 で2画面分割し、左を差分(読み取り専用)、右を対象ファイルに設定する。
    その他のエディタ: 差分をstdoutに表示してから対象ファイルのみを開く。

    Args:
        target_path: エディタで開く対象ファイル（Doorstop YAML など）。
        diff_content: 左ペインに表示する差分テキスト。空の場合は "(差分なし)" を表示する。

    Raises:
        FileNotFoundError: エディタが見つからない場合。
        EditorAbortedError: エディタが非ゼロ終了コードで終了した場合。
    """
    editor_cmd = get_editor()
    editor_parts = shlex.split(editor_cmd)
    editor_base = os.path.basename(editor_parts[0])

    body = diff_content.strip() if diff_content and diff_content.strip() else "(差分なし / No diff available)"

    with tempfile.NamedTemporaryFile(
        suffix=".diff",
        prefix="spec-weaver-diff-",
        mode="w",
        encoding="utf-8",
        delete=False,
    ) as tmp:
        tmp.write(body + "\n")
        tmp_path = tmp.name

    try:
        if editor_base in _SPLIT_CAPABLE:
            cmd = editor_parts + [
                "-O2",
                tmp_path,
                str(target_path),
                "-c",
                "wincmd h | setlocal readonly nomodifiable | wincmd l",
            ]
        else:
            print(body)
            cmd = editor_parts + [str(target_path)]

        try:
            result = subprocess.run(cmd)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"エディタ '{editor_cmd}' が見つかりません。"
                "$EDITOR 環境変数を設定してください。"
            )

        if result.returncode != 0:
            raise EditorAbortedError(
                f"エディタが終了コード {result.returncode} で終了しました。"
                "レビューを中断します。"
            )
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def open_editor_with_files(target_path: Path, related_paths: list[Path]) -> None:
    """対象ファイルと関連ファイルをまとめて開く。

    vim/nvim/vi/view/gvim の場合: -O で縦分割し、対象+関連ファイルを並べて開く。
    それ以外のエディタ: 複数ファイルをまとめて開く。

    Args:
        target_path: エディタで開く対象ファイル。
        related_paths: 一緒に開く関連ファイルのリスト。

    Raises:
        FileNotFoundError: エディタが見つからない場合。
        EditorAbortedError: エディタが非ゼロ終了コードで終了した場合。
    """
    editor_cmd = get_editor()
    editor_parts = shlex.split(editor_cmd)
    editor_base = os.path.basename(editor_parts[0])

    ordered_paths: list[Path] = []
    seen: set[str] = set()

    def _add_path(p: Path) -> None:
        key = str(p)
        if key in seen:
            return
        seen.add(key)
        ordered_paths.append(p)

    _add_path(target_path)
    for p in related_paths:
        _add_path(p)

    if editor_base in _SPLIT_CAPABLE:
        cmd = editor_parts + ["-O"] + [str(p) for p in ordered_paths]
    else:
        cmd = editor_parts + [str(p) for p in ordered_paths]

    try:
        result = subprocess.run(cmd)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"エディタ '{editor_cmd}' が見つかりません。"
            "$EDITOR 環境変数を設定してください。"
        )

    if result.returncode != 0:
        raise EditorAbortedError(
            f"エディタが終了コード {result.returncode} で終了しました。"
            "レビューを中断します。"
        )
