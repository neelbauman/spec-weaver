import typer
from pathlib import Path
from rich.console import Console

from spec_weaver.services.review_service import ReviewService
from spec_weaver.commands.audit_cmd import _audit_cmd # 完了後に呼び出すため

console = Console()

def _review_cmd(
    target_path: str = typer.Argument(..., help="レビュー対象 ( .feature ファイルのパス, Doorstop アイテム ID, または .yml ファイルのパス )"),
    feature_dir: Path = typer.Option(Path("specification/features"), "--feature-dir", "-f", exists=True, resolve_path=True),
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True),
) -> None:
    try:
        with console.status(f"[bold cyan]{target_path} をレビュー中...[/bold cyan]"):
            result = ReviewService().run_review(target_path, feature_dir, repo_root)

        if not result.is_success:
            console.print(f"[bold red]❌ {result.error_message}[/bold red]")
            raise typer.Exit(1)

        if result.target_type == "feature":
            console.print(f"[bold green]✅ フィンガープリントを書き込みました: {target_path}[/bold green]")
            console.print(f"[dim]ハッシュ: {result.fingerprint}[/dim]")
            if result.linked_items:
                console.print(f"[dim]関連アイテム: {', '.join(result.linked_items.keys())}[/dim]")
        
        elif result.target_type == "doorstop":
            console.print(f"[bold green]✅ アイテム {result.item_id} をレビューしました[/bold green]")

        console.print()
        
        # レビュー後に監査を実行 (引数はデフォルト値で実行)
        # ※AuditServiceに分離したおかげで、本来はAuditService().run_audit()を直接呼んで
        #   表示を制御することも可能ですが、既存の挙動を保つためにコマンドを呼び出します。
        _audit_cmd(feature_dir=feature_dir, repo_root=repo_root, prefix=None, stale_days=90, check_impl=False, extensions=None)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ review エラー: {e}[/bold red]")
        raise typer.Exit(1)
