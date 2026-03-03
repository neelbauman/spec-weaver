import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from spec_weaver.services.audit_service import AuditService

console = Console()

def _audit_cmd(
    feature_dir: Path = typer.Argument(
        ..., help="Gherkinの .feature ファイルが格納されているディレクトリのパス",
        exists=True, file_okay=False, dir_okay=True, resolve_path=True,
    ),
    repo_root: Path = typer.Option(
        Path.cwd(), "--repo-root", "-r",
        help="Doorstopのプロジェクトルート（.doorstopディレクトリがある場所）",
        exists=True, file_okay=False, dir_okay=True, resolve_path=True,
    ),
    prefix: Optional[str] = typer.Option(
        None, "--prefix", "-p",
        help="監査対象とする仕様IDのプレフィックス",
    ),
    stale_days: int = typer.Option(
        90, "--stale-days",
        help="updated_at からの経過日数がこの値を超えたアイテムを stale として警告する。",
    ),
    check_impl: bool = typer.Option(
        False, "--check-impl",
        help="実装ファイルリンクの検証を有効化",
    ),
    extensions: Optional[str] = typer.Option(
        None, "--extensions",
        help="アノテーションスキャン対象の拡張子（カンマ区切り。例: py,ts）。",
    ),
) -> None:
    """
    Doorstopに登録された仕様と、Gherkinのフィーチャーファイル間のタグの乖離を監査します。
    """
    prefix_display = f"@{prefix}" if prefix else "All testable items"
    console.print(
        Panel.fit(
            f"Doorstop Root: [bold green]{repo_root}[/bold green]\n"
            f"Gherkin Dir  : [bold green]{feature_dir}[/bold green]\n"
            f"Target       : [bold cyan]{prefix_display}[/bold cyan]",
            title="Spec-Weaver Audit", border_style="blue",
        )
    )

    # ロジックの実行（UIと分離）
    service = AuditService()
    try:
        with console.status("[bold cyan]監査データを解析中...[/bold cyan]"):
            report = service.run_audit(
                feature_dir, repo_root, prefix, stale_days, check_impl, extensions
            )
    except Exception as e:
        console.print(f"[bold red]❌ 監査処理中にエラーが発生しました:[/bold red] {e}")
        raise typer.Exit(code=1)

    # 以降、純粋な表示(UI)処理
    if report.inactive_testable:
        console.print("\n[dim]⛔ 非活性のためスキップした仕様 (Inactive Testable Specs):[/dim]")
        table = Table(show_header=True, header_style="dim")
        table.add_column("Spec ID", style="dim")
        table.add_column("理由", style="dim")
        for spec in sorted(report.inactive_testable):
            table.add_row(spec, "active: false")
        console.print(table)

    if report.untested_specs:
        console.print("\n[bold red]❌ テストが実装されていない仕様 (Untested Specs):[/bold red]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Missing Spec ID", style="dim")
        for spec in sorted(report.untested_specs):
            table.add_row(spec)
        console.print(table)

    if report.orphaned_tags:
        console.print("\n[bold yellow]⚠️ 仕様書に存在しない孤児タグ (Orphaned Tags):[/bold yellow]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Orphaned Tag", style="dim")
        for tag in sorted(report.orphaned_tags):
            table.add_row(f"@{tag}")
        console.print(table)

    if report.suspect_specs or report.suspect_features:
        console.print("\n[bold yellow]⚠️ Suspect — 関連アイテムが変更されています:[/bold yellow]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Spec ID", style="dim")
        table.add_column("原因アイテム", style="dim")
        table.add_column("アクション", style="dim")
        for spec in sorted(report.suspect_specs):
            causes_list = []
            for c in report.suspect_specs[spec]:
                if c == "Doorstop native suspect link":
                    causes_list.extend(sorted(list(report.review_state_parents.get(spec, set()))))
                else:
                    causes_list.append(c)
            causes = ", ".join(causes_list) or "不明"
            action = f"spec-weaver clear {spec}"
            table.add_row(spec, causes, action)
        for fpath in sorted(report.suspect_features):
            fname = Path(fpath).name
            causes = ", ".join(sorted(report.suspect_features[fpath])) or "不明"
            table.add_row(fname, causes, "feature ファイルを確認し、必要に応じてシナリオを更新")
        console.print(table)

    if report.unreviewed_specs or report.unreviewed_features:
        console.print("\n[bold yellow]📋 未レビューの変更 (Unreviewed Changes):[/bold yellow]")
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("UID / File", style="dim")
        table.add_column("Type")
        for spec in sorted(report.unreviewed_specs):
            table.add_row(spec, "Doorstop Item")
        for fpath in sorted(report.unreviewed_features):
            table.add_row(Path(fpath).name, "Feature File")
        console.print(table)

    if report.broken_refs:
        console.print("\n[bold red]❌ 実装ファイルリンク切れ (Broken Implementation Refs):[/bold red]")
        table = Table(show_header=True, header_style="bold red")
        table.add_column("Spec ID")
        table.add_column("Path (not found)")
        for uid, p in sorted(report.broken_refs):
            table.add_row(uid, p)
        console.print(table)

    if report.ref_only:
        console.print("\n[bold yellow]⚠️ impl_files のみ（アノテーションなし）(Ref Only):[/bold yellow]")
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("Spec ID")
        table.add_column("Path")
        for uid, p in sorted(report.ref_only):
            table.add_row(uid, f"{uid} → {p}")
        console.print(table)

    if report.annotation_only:
        console.print("\n[bold yellow]⚠️ アノテーションのみ（impl_files なし）(Annotation Only):[/bold yellow]")
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("Spec ID")
        table.add_column("Path")
        for uid, p in sorted(report.annotation_only):
            table.add_row(uid, f"{uid} ← {p}")
        console.print(table)

    if report.stale_items:
        console.print("\n[bold yellow]⏳ 最終更新から長期間経過しているアイテム (Stale Items):[/bold yellow]")
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("Spec ID")
        table.add_column("最終更新日")
        table.add_column("経過日数")
        for uid, updated_at, delta in sorted(report.stale_items):
            table.add_row(uid, updated_at, f"{delta} days")
        console.print(table)

    if report.undefined_steps:
        console.print("\n[bold red]❌ ステップ定義が見つからないシナリオ (Undefined Steps):[/bold red]")
        table = Table(show_header=True, header_style="bold red")
        table.add_column("Missing Step Text")
        for step in sorted(report.undefined_steps):
            table.add_row(step)
        console.print(table)

    if report.unused_step_defs:
        console.print("\n[dim]💡 未使用のステップ定義 (Unused Step Definitions):[/dim]")
        for step in sorted(report.unused_step_defs):
            console.print(f"  [dim]- {step}[/dim]")

    if report.is_success:
        console.print(f"\n[bold green]✅ 完璧です！ {report.specs_count} 件の仕様がすべてGherkinテストでカバーされています。[/bold green]")
        raise typer.Exit(code=0)
    else:
        console.print("\n[bold red]監査が失敗しました。仕様とテストの乖離を修正してください。[/bold red]")
        raise typer.Exit(code=1)
