# src/spec_weaver/cli/commands/add_cmd.py
"""BDD アイテム追加コマンド。

.feature ファイルの取り込み、または新規 BDD アイテムの作成を行う。
"""

from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console

console = Console()


def _add_cmd(
    source: Optional[Path] = typer.Argument(
        None, help=".feature ファイルのパス（省略時は --slug で新規作成）"
    ),
    slug: Optional[str] = typer.Option(
        None, "--slug", "-s", help=".feature ファイル名（拡張子なし）"
    ),
    link: Optional[List[str]] = typer.Option(
        None, "--link", "-l", help="リンク先の仕様 UID（複数指定可）"
    ),
    prefix: str = typer.Option(
        "BDD", "--prefix", "-p", help="BDD ドキュメントのプレフィックス"
    ),
    header: Optional[str] = typer.Option(
        None, "--header", "-H", help="Feature のタイトル（新規作成時）"
    ),
    repo_root: Optional[Path] = typer.Option(
        None, "--repo-root", "-r", help="リポジトリルートパス"
    ),
) -> None:
    """BDD アイテムを追加します。

    .feature ファイルを指定すると取り込みモード（タグ→リンク自動変換）。
    --slug のみ指定すると新規作成モード（テンプレート生成）。
    """
    from spec_weaver.services.bdd_service import (
        create_bdd_item,
        import_feature_file,
    )

    root = repo_root or Path.cwd()

    if source is not None:
        # --- 取り込みモード ---
        result = import_feature_file(
            feature_path=source,
            repo_root=root,
            prefix=prefix,
            slug=slug,
            extra_links=link,
        )
    elif slug is not None:
        # --- 新規作成モード ---
        result = create_bdd_item(
            repo_root=root,
            slug=slug,
            links=link,
            prefix=prefix,
            header=header or "",
        )
    else:
        console.print(
            "[red].feature ファイルパスまたは --slug を指定してください。[/red]"
        )
        raise typer.Exit(code=1)

    if not result.is_success:
        console.print(f"[bold red]{result.error}[/bold red]")
        raise typer.Exit(code=1)

    console.print(f"[bold green]{result.item_uid}[/bold green] を作成しました。")
    console.print(f"  slug: {result.slug}")
    if result.extracted_links:
        console.print(f"  links: {', '.join(result.extracted_links)}")
    if result.header:
        console.print(f"  header: {result.header}")
