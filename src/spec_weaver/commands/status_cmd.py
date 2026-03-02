import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table

from spec_weaver.services.status_service import StatusService
from spec_weaver.utils.formatters import get_impl_status_badge, get_review_status_badge, get_timestamp

console = Console()

def _status_cmd(
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True),
    feature_dir: Path = typer.Option(Path("specification/features"), "--feature-dir", "-f", exists=True, resolve_path=True),
    filter_status: Optional[str] = typer.Option(None, "--filter", "-F", help="表示するステータスで絞り込む"),
) -> None:
    """
    REQ・SPECの実装ステータス（status フィールド）を一覧表示します。
    """
    try:
        with console.status("[bold cyan]ステータスを集計中...[/bold cyan]"):
            report = StatusService().get_status_report(repo_root, feature_dir, filter_status)

        def _print_status_table(title: str, items: list) -> None:
            if not items:
                return
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("ID", style="bold cyan", no_wrap=True)
            table.add_column("タイトル")
            table.add_column("活性", no_wrap=True)
            table.add_column("実装ステータス")
            table.add_column("レビューステータス")
            table.add_column("最終更新日", no_wrap=True)
            
            for dto in sorted(items, key=lambda x: x.uid):
                active_badge = "✅" if dto.active else "[dim]⛔ 非活性[/dim]"
                impl_badge = get_impl_status_badge(dto.item_obj)
                review_badge = get_review_status_badge(dto.uid, review_state=report.review_state)
                updated = get_timestamp(dto.item_obj, "updated_at")
                
                if not dto.active:
                    table.add_row(f"[dim]{dto.uid}[/dim]", f"[dim]{dto.title}[/dim]", active_badge, f"[dim]{impl_badge}[/dim]", f"[dim]{review_badge}[/dim]", f"[dim]{updated}[/dim]")
                else:
                    table.add_row(dto.uid, dto.title, active_badge, impl_badge, review_badge, updated)
            console.print(table)

        # 優先順位付けして表示
        priority_prefixes = ["REQ", "SPEC", "CORE", "QA", "VIS", "TRC", "AUT", "DESIGN", "PLAN", "ADR", "RESEARCH"]
        for prefix in priority_prefixes:
            if prefix in report.grouped_items and report.grouped_items[prefix]:
                _print_status_table(f"ドキュメント: {prefix}", report.grouped_items.pop(prefix))

        # 残りのプレフィックスを表示
        for prefix, items in sorted(report.grouped_items.items()):
            _print_status_table(f"ドキュメント: {prefix}", items)

        # Featureファイルのステータス表示
        if report.feature_files:
            table = Table(title="振る舞い仕様 (Gherkin Features)", show_header=True, header_style="bold green")
            table.add_column("ファイルパス", style="bold cyan")
            table.add_column("シナリオ数", justify="right")
            table.add_column("レビューステータス")
            table.add_column("関連仕様ID")
            for f in report.feature_files:
                table.add_row(f.file_path, str(f.scenario_count), f.status, ", ".join(f.related_specs))
            console.print(table)

        # Behaveステップ整合性のサマリー表示
        if report.unused_step_defs_count > 0 or report.undefined_steps_count > 0:
            console.print("\n[bold magenta]Step Definitions Info:[/bold magenta]")
            if report.unused_step_defs_count > 0:
                console.print(f"  [yellow]⚠️  未使用のステップ定義: {report.unused_step_defs_count} 件[/yellow]")
            if report.undefined_steps_count > 0:
                console.print(f"  [red]❌ 未定義のステップ: {report.undefined_steps_count} 件[/red]")

        if report.total_items_shown == 0:
            msg = f"[yellow]ステータス '{filter_status}' に一致するアイテムが見つかりませんでした。[/yellow]" if filter_status else "[yellow]アイテムが見つかりませんでした。[/yellow]"
            console.print(msg)
        else:
            console.print(f"\n[bold green]合計 {report.total_items_shown} 件を表示しました。[/bold green]")
            console.print("[dim]ステータスを更新するには、対象の YAML ファイルに [bold]status: in-progress[/bold] などを追記してください。[/dim]")

    except Exception as e:
        console.print(f"[bold red]❌ エラー: {e}[/bold red]")
        raise typer.Exit(code=1)
