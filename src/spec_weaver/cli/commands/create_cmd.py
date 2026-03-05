import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

console = Console()

def _create_cmd(
    prefix: str = typer.Argument(..., help="新しいドキュメントのプレフィックス (例: REQ, SPEC)"),
    path: Path = typer.Argument(..., help="ドキュメントを配置するディレクトリのパス"),
    parent: Optional[str] = typer.Option(
        None, "--parent", "-p", help="親ドキュメントのプレフィックス (例: REQ)"
    ),
    digits: int = typer.Option(3, "--digits", "-d", help="アイテムUIDの数字の桁数"),
    sep: str = typer.Option(
        "-", "--separator", "-s", help="プレフィックスと数字の間の区切り文字 (Spec-Weaverのデフォルトは '-')"
    ),
) -> None:
    """
    新しいDoorstopドキュメントツリーを作成します（doorstop create のラッパー）。
    """
    cmd = [
        "doorstop",
        "create",
        prefix,
        str(path),
        "--digits",
        str(digits),
        "--separator",
        sep,
    ]
    if parent:
        cmd.extend(["--parent", parent])
    
    result = subprocess.run(cmd)
    if result.returncode != 0:
        console.print("[bold red]❌ ドキュメントの作成に失敗しました。[/bold red]")
        raise typer.Exit(code=result.returncode)
    
    # stdout is printed by doorstop itself, so we just add a success check.
    # doorstop create doesn't print anything by default on success, so we add a nice message.
    console.print(f"[bold green]✅ ドキュメント {prefix} を {path} に作成しました。[/bold green]")
