from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from spec_weaver.services.clear_service import ClearService

console = Console()

def _clear_cmd(
    item_id: Optional[str] = typer.Argument(None, help="test_fingerprint を更新するアイテムID、または .feature ファイルパス"),
    all_targets: bool = typer.Option(False, "--all", help="feature_dir 内の全 .feature ファイルを一括クリアする"),
    feature_dir: Path = typer.Option(Path("specification/features"), "--feature-dir", "-f", exists=True, resolve_path=True),
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True),
) -> None:
    # 引数の相互排他チェック
    if all_targets and item_id:
        console.print("[bold red]❌ --all と対象パス/IDは同時に指定できません。[/bold red]")
        raise typer.Exit(1)
    if not all_targets and not item_id:
        console.print("[bold red]❌ 対象パス/IDを指定するか、--all を使用してください。[/bold red]")
        raise typer.Exit(1)

    try:
        if all_targets:
            _clear_all(feature_dir, repo_root)
        else:
            _clear_single(item_id, feature_dir, repo_root)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ clear エラー: {e}[/bold red]")
        raise typer.Exit(1)


def _clear_single(item_id: str, feature_dir: Path, repo_root: Path) -> None:
    """単一ターゲットのクリア（既存動作）。"""
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


def _clear_all(feature_dir: Path, repo_root: Path) -> None:
    """全 .feature ファイルの全アイテムを一括クリア。"""
    feature_files = sorted(feature_dir.glob("*.feature"))
    if not feature_files:
        console.print(f"[bold yellow]⚠️ {feature_dir} に .feature ファイルが見つかりません。[/bold yellow]")
        raise typer.Exit(1)

    service = ClearService()
    total_updated: list[str] = []
    total_skipped_unreviewed: list[str] = []
    total_skipped_suspect_unreviewed: list[str] = []

    with console.status("[bold cyan]全 .feature ファイルをクリア処理中...[/bold cyan]"):
        for f in feature_files:
            result = service.run_clear(str(f), feature_dir, repo_root)
            # --all モードでは is_success=False（"更新なし" 相当）はエラーとして扱わない
            total_updated.extend(result.updated_items)
            total_skipped_unreviewed.extend(result.skipped_unreviewed)
            total_skipped_suspect_unreviewed.extend(result.skipped_suspect_unreviewed)

    # 重複排除（複数ファイルから同一タグが参照される場合）
    total_updated = list(dict.fromkeys(total_updated))
    total_skipped_unreviewed = list(dict.fromkeys(total_skipped_unreviewed))
    total_skipped_suspect_unreviewed = list(dict.fromkeys(total_skipped_suspect_unreviewed))

    for tag in total_skipped_unreviewed:
        console.print(f"⚠️ [bold yellow]{tag}[/bold yellow] は未レビューのためスキップしました。")
    for tag in total_skipped_suspect_unreviewed:
        console.print(f"⚠️ [bold yellow]{tag}[/bold yellow] は上位アイテムが未レビューのためスキップしました。")

    for tag in total_updated:
        console.print(f"✅ [bold]{tag}[/bold] の gherkin_fingerprints (またはsuspect) を更新/解除しました。")

    console.print(f"\n[bold green]✨ 合計 {len(total_updated)} 件更新しました。[/bold green]")
