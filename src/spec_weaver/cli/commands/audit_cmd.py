# implements: QA-006
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from spec_weaver.services.audit_service import AuditService

console = Console()

def _audit_cmd(
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
    feature_dir = repo_root / ".specification" / "features"
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
    # テスト環境などでの表示崩れ（自動折り返しによるアサーション失敗）を防ぐため、
    # 幅を十分広く設定した一時的なコンソールで出力する
    from rich.console import Console as RichConsole
    wide_console = RichConsole(width=200)

    try:
        with wide_console.status("[bold cyan]監査データを解析中...[/bold cyan]"):
            report = service.run_audit(
                feature_dir, repo_root, prefix, stale_days, check_impl, extensions
            )
    except Exception as e:
        wide_console.print(f"[bold red]❌ 監査処理中にエラーが発生しました:[/bold red] {e}")
        raise typer.Exit(code=1)

    # 以降、純粋な表示(UI)処理
    
    # 1. サマリー計算
    error_count = (
        len(report.untested_specs) + len(report.orphaned_tags) + 
        len(report.broken_refs) + len(report.behavior_without_gherkin) + 
        len(report.undefined_steps) + len(report.suspect_specs) + 
        len(report.suspect_features) + len(report.unreviewed_specs) + 
        len(report.unreviewed_features)
    )
    warning_count = (
        len(report.ref_only) + len(report.annotation_only) + 
        len(report.architecture_with_gherkin) + len(report.stale_items)
    )
    info_count = len(report.layer_unset) + len(report.unused_step_defs)

    summary_text = (
        f"[bold red]❌ Errors   (Action Required) :[/bold red] {error_count}\n"
        f"[bold yellow]⚠️ Warnings (Needs Review)    :[/bold yellow] {warning_count}\n"
        f"[bold blue]ℹ️ Infos    (Good to know)   :[/bold blue] {info_count}"
    )
    wide_console.print(Panel(summary_text, title="Audit Summary", border_style="cyan"))

    # 2. 詳細表示 (Errors - 要対応)
    if error_count > 0:
        wide_console.print("\n[bold red]=== 🔴 ERRORS (Action Required) ===[/bold red]")
        
        if report.untested_specs:
            wide_console.print("\n[bold red]❌ テストが実装されていない仕様 (Untested Specs):[/bold red]")
            wide_console.print(f"  [red]{', '.join(sorted(report.untested_specs))}[/red]")
            
        if report.orphaned_tags:
            wide_console.print("\n[bold red]❌ 仕様書に存在しない孤児タグ (Orphaned Tags):[/bold red]")
            tags = [f"@{t}" for t in sorted(report.orphaned_tags)]
            wide_console.print(f"  [red]{', '.join(tags)}[/red]")

        if report.suspect_specs or report.suspect_features:
            wide_console.print("\n[bold red]❌ Suspect — 関連アイテムが変更されています:[/bold red]")
            table = Table(show_header=True, header_style="bold red", box=None)
            table.add_column("ID / File", style="bold")
            table.add_column("原因", style="dim")
            table.add_column("アクション", style="dim")
            for spec in sorted(report.suspect_specs):
                causes = ", ".join(report.suspect_specs[spec]) or "不明"
                action = f"必要に応じて編集し、spec-weaver review {spec} 後、 spec-weaver clear {spec}"
                table.add_row(spec, causes, action)
            for fpath in sorted(report.suspect_features):
                causes = ", ".join(sorted(report.suspect_features[fpath])) or "不明"
                table.add_row(Path(fpath).name, causes, "feature ファイルを確認し必要に応じて更新")
            wide_console.print(table)

        if report.unreviewed_specs or report.unreviewed_features:
            wide_console.print("\n[bold red]📋 未レビューの変更 (Unreviewed Changes):[/bold red]")
            items = sorted(report.unreviewed_specs) + [Path(p).name for p in sorted(report.unreviewed_features)]
            wide_console.print(f"  [red]{', '.join(items)}[/red]")

        if report.broken_refs:
            wide_console.print("\n[bold red]❌ 実装ファイルリンク切れ (Broken Implementation Refs):[/bold red]")
            for uid, p in sorted(report.broken_refs):
                wide_console.print(f"  - [bold]{uid}[/bold]: {p}")

        if report.behavior_without_gherkin:
            wide_console.print("\n[bold red]❌ layer: behavior なのにGherkinテストがない (Behavior Without Gherkin):[/bold red]")
            for spec in sorted(report.behavior_without_gherkin):
                wide_console.print(f"  - [bold]{spec}[/bold]: .feature ファイルに @{spec} タグを追加してください")

        if report.undefined_steps:
            wide_console.print("\n[bold red]❌ ステップ定義が見つからないシナリオ (Undefined Steps):[/bold red]")
            for step in sorted(report.undefined_steps):
                wide_console.print(f"  - [red]{step}[/red]")

    # 3. 詳細表示 (Warnings)
    if warning_count > 0:
        wide_console.print("\n[bold yellow]=== 🟡 WARNINGS (Needs Review) ===[/bold yellow]")

        if report.ref_only:
            wide_console.print("\n[bold yellow]⚠️ impl_files のみ（アノテーションなし）(Ref Only):[/bold yellow]")
            for uid, p in sorted(report.ref_only):
                wide_console.print(f"  - [bold]{uid}[/bold] → {p}")

        if report.annotation_only:
            wide_console.print("\n[bold yellow]⚠️ アノテーションのみ（impl_files なし）(Annotation Only):[/bold yellow]")
            for uid, p in sorted(report.annotation_only):
                wide_console.print(f"  - [bold]{uid}[/bold] ← {p}")

        if report.architecture_with_gherkin:
            wide_console.print("\n[bold yellow]⚠️ layer: architecture なのにGherkinタグが存在する (Architecture With Gherkin):[/bold yellow]")
            for spec in sorted(report.architecture_with_gherkin):
                wide_console.print(f"  - [bold]{spec}[/bold]: Gherkin テストを単体テスト（pytest）へ移行を検討してください")

        if report.stale_items:
            wide_console.print("\n[bold yellow]⏳ 最終更新から長期間経過しているアイテム (Stale Items):[/bold yellow]")
            for uid, updated_at, delta in sorted(report.stale_items):
                wide_console.print(f"  - [bold]{uid}[/bold]: {updated_at} ({delta} days ago)")

    # 4. 詳細表示 (Infos)
    if info_count > 0:
        wide_console.print("\n[bold blue]=== 🔵 INFOS ===[/bold blue]")
        
        if report.layer_unset:
            wide_console.print("\n[bold blue]ℹ️ layer 属性が未設定のアイテム (Layer Unset):[/bold blue]")
            wide_console.print(f"  [blue]{', '.join(sorted(report.layer_unset))}[/blue]")

        if report.unused_step_defs:
            wide_console.print("\n[dim]💡 未使用のステップ定義 (Unused Step Definitions):[/dim]")
            for step in sorted(report.unused_step_defs):
                wide_console.print(f"  [dim]- {step}[/dim]")

    if report.is_success:
        wide_console.print(f"\n[bold green]✅ 完璧です！ {report.specs_count} 件の仕様がすべてGherkinテストでカバーされています。[/bold green]")
        raise typer.Exit(code=0)
    else:
        wide_console.print("\n[bold red]監査が失敗しました。仕様とテストの乖離を修正してください。[/bold red]")
        raise typer.Exit(code=1)
