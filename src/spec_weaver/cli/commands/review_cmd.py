from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from spec_weaver.cli.commands.audit_cmd import _audit_cmd
from spec_weaver.services.review_service import ReviewService

console = Console()

def _review_cmd(
    target_path: Optional[str] = typer.Argument(None, help="レビュー対象 ( .feature ファイルのパス, Doorstop アイテム ID, または .yml ファイルのパス )"),
    all_targets: bool = typer.Option(False, "--all", help="feature_dir 内の全 .feature ファイルと全アクティブ Doorstop アイテムを一括レビューする"),
    feature_dir: Path = typer.Option(Path("specification/features"), "--feature-dir", "-f", exists=True, resolve_path=True),
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True),
) -> None:
    # 引数の相互排他チェック
    if all_targets and target_path:
        console.print("[bold red]❌ --all と対象パス/IDは同時に指定できません。[/bold red]")
        raise typer.Exit(1)
    if not all_targets and not target_path:
        console.print("[bold red]❌ 対象パス/IDを指定するか、--all を使用してください。[/bold red]")
        raise typer.Exit(1)

    try:
        if all_targets:
            _review_all(feature_dir, repo_root)
        else:
            _review_single(target_path, feature_dir, repo_root)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ review エラー: {e}[/bold red]")
        raise typer.Exit(1)


def _review_single(target_path: str, feature_dir: Path, repo_root: Path) -> None:
    """単一ターゲットのレビュー（既存動作）。"""
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
    _audit_cmd(feature_dir=feature_dir, repo_root=repo_root, prefix=None, stale_days=90, check_impl=False, extensions=None)


def _review_all(feature_dir: Path, repo_root: Path) -> None:
    """全 .feature ファイルと全アクティブ Doorstop アイテムを一括レビュー。"""
    feature_files = sorted(feature_dir.glob("*.feature"))
    if not feature_files:
        console.print(f"[bold yellow]⚠️ {feature_dir} に .feature ファイルが見つかりません。[/bold yellow]")
        raise typer.Exit(1)

    service = ReviewService()
    failed: list[tuple[str, str]] = []

    # 1. 全 .feature ファイルのレビュー
    with console.status("[bold cyan]全 .feature ファイルをレビュー中...[/bold cyan]"):
        for f in feature_files:
            result = service.run_review(str(f), feature_dir, repo_root)
            if not result.is_success:
                failed.append((str(f), result.error_message or "不明なエラー"))

    reviewed_feature_count = len(feature_files) - len(failed)
    console.print(f"[bold green]✅ .feature {reviewed_feature_count} 件レビュー済み[/bold green]")

    # 2. 全アクティブ Doorstop アイテムのレビュー
    with console.status("[bold cyan]全 Doorstop アイテムをレビュー中...[/bold cyan]"):
        reviewed_items, item_failed = service.run_review_all_items(repo_root)

    failed.extend(item_failed)
    console.print(f"[bold green]✅ Doorstop アイテム {len(reviewed_items)} 件レビュー済み[/bold green]")

    # 失敗報告
    for target, msg in failed:
        console.print(f"[bold yellow]⚠️ スキップ: {target}: {msg}[/bold yellow]")

    console.print()
    _audit_cmd(feature_dir=feature_dir, repo_root=repo_root, prefix=None, stale_days=90, check_impl=False, extensions=None)

    if failed:
        raise typer.Exit(1)
