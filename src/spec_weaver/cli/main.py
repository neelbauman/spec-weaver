# src/spec_weaver/cli.py
from pathlib import Path
from typing import Optional

import typer
from rich import box
from rich.console import Console
from rich.table import Table

from spec_weaver.cli.commands.add_cmd import _add_cmd

# 各コマンドモジュールからのインポート
from spec_weaver.cli.commands.audit_cmd import _audit_cmd
from spec_weaver.cli.commands.build_cmd import _build_cmd
from spec_weaver.cli.commands.clear_cmd import _clear_cmd
from spec_weaver.cli.commands.create_cmd import _create_cmd
from spec_weaver.cli.commands.review_cmd import _review_cmd
from spec_weaver.cli.commands.scaffold_cmd import _scaffold_cmd
from spec_weaver.cli.commands.semantic_review_cmd import _semantic_review_cmd
from spec_weaver.cli.commands.status_cmd import _status_cmd
from spec_weaver.cli.commands.sync_cmd import _sync_cmd
from spec_weaver.cli.commands.trace_cmd import _trace_cmd

# Typerアプリケーションの初期化
app = typer.Typer(
    help="Spec-Weaver: Doorstopの仕様とGherkinのテストをシームレスに統合・監査するツール",
    add_completion=False,
    invoke_without_command=True,
)
console = Console()


@app.callback()
def callback(
    ctx: typer.Context,
    repo_root: Optional[Path] = typer.Option(
        None, "--repo-root", "-r", help="リポジトリのルートパス（デフォルト: カレントディレクトリ）"
    ),
) -> None:
    """サブコマンドが指定されない場合にドキュメントルートの一覧を表示する。"""
    if ctx.invoked_subcommand is not None:
        return

    root = repo_root or Path.cwd()
    _show_roots(root)


def _show_roots(repo_root: Path) -> None:
    """Doorstop のドキュメントルート一覧を Rich テーブルで表示する。"""
    from spec_weaver.adapters.doorstop import get_doorstop_tree

    try:
        multi_tree = get_doorstop_tree(repo_root)
    except Exception as e:
        console.print(f"[red]ドキュメントツリーの読み込みに失敗しました: {e}[/red]")
        raise typer.Exit(1)

    trees = multi_tree.trees
    console.print()
    console.print(
        f"[bold]ドキュメントルート[/bold] [dim]({len(trees)} 件)[/dim]"
    )
    console.rule()

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    table.add_column("ルート", style="bold cyan", no_wrap=True)
    table.add_column("パス", style="dim")
    table.add_column("ドキュメント数", justify="right")
    table.add_column("子ドキュメント")

    for tree in trees:
        root_doc = tree.document
        if root_doc is None:
            table.add_row("-", str(repo_root), "0", "（ドキュメントなし）")
            continue

        all_docs = list(tree)
        doc_count = len(all_docs)

        try:
            rel_path = Path(root_doc.path).relative_to(repo_root)
        except ValueError:
            rel_path = Path(root_doc.path)

        children = [
            str(doc.prefix)
            for doc in all_docs
            if str(doc.prefix) != str(root_doc.prefix)
        ]
        children_str = ", ".join(children) if children else "—"

        table.add_row(
            str(root_doc.prefix),
            str(rel_path),
            str(doc_count),
            children_str,
        )

    console.print(table)
    console.print(
        "[dim]詳細なコマンド一覧は [bold]spec-weaver --help[/bold] を参照してください。[/dim]"
    )


# コマンドの登録
app.command("audit")(_audit_cmd)
app.command("scaffold")(_scaffold_cmd)
app.command("review")(_review_cmd)
app.command("clear")(_clear_cmd)
app.command("status")(_status_cmd)
app.command("build")(_build_cmd)
app.command("trace")(_trace_cmd)
app.command("semantic-review")(_semantic_review_cmd)
app.command("create")(_create_cmd)
app.command("add")(_add_cmd)
app.command("sync")(_sync_cmd)

if __name__ == "__main__":
    app()
