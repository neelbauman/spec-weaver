import subprocess
from pathlib import Path


def is_file_dirty(file_path: Path, repo_root: Path) -> bool:
    """指定ファイルに未コミットの変更があるか Git ステータスで確認する。"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", str(file_path)],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        return bool(result.stdout.strip())
    except Exception:
        return False
