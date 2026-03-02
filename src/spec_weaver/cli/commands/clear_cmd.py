import typer
from pathlib import Path
from rich.console import Console
from spec_weaver.services.clear_service import ClearService

console = Console()

def _clear_cmd(
    item_id: str = typer.Argument(..., help="test_fingerprint を更新するアイテムID、または .feature ファイルパス"),
    feature_dir: Path = typer.Option(Path("specification/features"), "--feature-dir", "-f", exists=True, resolve_path=True),
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True),
) -> None:
    try:
        with console.status(f"[bold cyan]{item_id} をクリア処理中...[/bold cyan]"):
            result = ClearService().run_clear(item_id, feature_dir, repo_root)

        if not result.is_success:
            console.print(f"[bold red]❌ {result.error_message}[/bold red]")
            raise typer.Exit(1)

        for tag in result.skipped_unreviewed:
            console.print(f"⚠️ [bold yellow]{tag}[/bold yellow] は未レビューのためスキップしました。")
        for tag in result.skipped_suspect_unreviewed:
            console.print(f"⚠️ [bold yellow]{tag}[/bold yellow] は上位アイテムが未レビューのためスキップしました。")

        for tag in result.updated_items:
            console.print(f"✅ [bold]{tag}[/bold] の gherkin_fingerprints (またはsuspect) を更新/解除しました。")

        if Path(item_id).suffix == ".feature" and result.updated_items:
            console.print(f"\n[bold green]✨ 合計 {len(result.updated_items)} 個のアイテムを更新しました。[/bold green]")

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ clear エラー: {e}[/bold red]")
        raise typer.Exit(1)
