import typer
import json
from pathlib import Path
from typing import Optional
from rich.console import Console

from spec_weaver.core.review import (
    ReviewResult, filter_findings, run_all_reviews, run_claude_review, severity_gte
)

console = Console()

def _semantic_review_cmd(
    item: Optional[str] = typer.Option(None, "--item", "-i", help="レビュー対象の仕様アイテムID。--all と排他。"),
    all_items: bool = typer.Option(False, "--all", help="全仕様アイテムを並列レビューする。--item と排他。"),
    feature_dir: Path = typer.Option(Path("specification/features"), "--feature-dir", "-f", resolve_path=True),
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", resolve_path=True),
    output: str = typer.Option("text", "--output", "-o", help="出力形式: text（Markdown） / json"),
    min_severity: str = typer.Option("low", "--min-severity", help="表示する finding の最低重大度"),
    fail_on: Optional[str] = typer.Option(None, "--fail-on", help="指定重大度以上の finding があれば終了コード 1 を返す"),
    max_workers: int = typer.Option(3, "--max-workers", help="--all 時の並列プロセス数"),
    timeout: int = typer.Option(300, "--timeout", help="最大待機秒数"),
) -> None:
    """仕様・Gherkin・実装コードの意味的整合性を Claude でレビューします。"""
    if bool(item) == bool(all_items):
        console.print("[bold red]❌ --item または --all のどちらか一方を指定してください。[/bold red]")
        raise typer.Exit(code=2)

    if not feature_dir.exists() and (repo_root / feature_dir).exists():
        feature_dir = repo_root / feature_dir

    if item:
        try:
            if output != "json":
                with console.status(f"[bold cyan]🔍 {item} をレビュー中...[/bold cyan]"):
                    result = run_claude_review(item, feature_dir, repo_root, timeout=timeout)
            else:
                result = run_claude_review(item, feature_dir, repo_root, timeout=timeout)
        except Exception as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
            raise typer.Exit(code=1)

        result.findings = filter_findings(result.findings, min_severity)

        if output == "json":
            print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        else:
            _print_review_result(console, result)

        if fail_on and any(severity_gte(f.severity, fail_on) for f in result.findings):
            raise typer.Exit(code=1)
        raise typer.Exit(code=0)

    # --all の場合
    try:
        if output != "json":
            from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, MofNCompleteColumn, TimeElapsedColumn
            from spec_weaver.adopters.doorstop import get_item_map
            
            total = len(get_item_map(repo_root))
            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), MofNCompleteColumn(), TimeElapsedColumn(), console=console) as progress:
                task_id = progress.add_task("[cyan]セマンティックレビュー実行中...[/cyan]", total=total)
                def _on_complete(iid: str, _result: ReviewResult) -> None:
                    progress.advance(task_id)
                    progress.update(task_id, description=f"[cyan]完了: {iid}[/cyan]")
                report = run_all_reviews(feature_dir, repo_root, max_workers=max_workers, on_complete=_on_complete, timeout=timeout)
        else:
            report = run_all_reviews(feature_dir, repo_root, max_workers=max_workers, timeout=timeout)
    except Exception as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(code=1)

    for r in report.items:
        r.findings = filter_findings(r.findings, min_severity)

    if output == "json":
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        for r in report.items:
            _print_review_result(console, r)

    if fail_on and any(any(severity_gte(f.severity, fail_on) for f in r.findings) for r in report.items):
        raise typer.Exit(code=1)
    raise typer.Exit(code=0)

def _print_review_result(console: Console, result: ReviewResult) -> None:
    from rich.markdown import Markdown
    console.print(Markdown(f"## {result.item_id} — {result.item_title}"))
    if not result.findings:
        console.print("[green]✅ finding なし[/green]")
    else:
        for f in result.findings:
            sev_color = {"high": "red", "medium": "yellow", "low": "cyan"}.get(f.severity, "white")
            console.print(f"  [{sev_color}][{f.severity.upper()}][/{sev_color}] [bold]{f.title}[/bold] ({f.kind})")
            if f.detail: console.print(f"    {f.detail}")
            if f.location: console.print(f"    → {f.location}")
    if result.summary:
        console.print(f"\n[dim]{result.summary}[/dim]\n")
