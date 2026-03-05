from pathlib import Path

import typer
from rich.console import Console

from spec_weaver.services.build_service import BuildService

console = Console()

def _build_cmd(
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True),
    out_dir: Path = typer.Option(Path(".specification"), "--out-dir", "-o", resolve_path=True),
    prefix: str = typer.Option("SPEC", "--prefix", "-p", help="Gherkinタグとして主に扱うデフォルトプレフィックス"),
    test_results_file: Path = typer.Option(
        None, "--test-results", "-t",
        help="pytest-bdd 生成の Cucumber 互換 JSON レポートのパス",
        exists=False, file_okay=True, dir_okay=False, resolve_path=True,
    ),
) -> None:
    """
    Doorstopの全ドキュメントを解析し、相互リンク・カバレッジ・テスト結果を含むポータルサイトをビルドします。
    """
    feature_dir = repo_root / ".specification" / "features"
    if test_results_file and not test_results_file.exists():
        console.print(f"[bold red]❌ テスト結果ファイルが見つかりません: {test_results_file}[/bold red]")
        raise typer.Exit(1)

    try:
        with console.status("[bold cyan]データの分析とドキュメントの生成を開始...[/bold cyan]"):
            service = BuildService()
            report = service.run_build(
                feature_dir=feature_dir,
                repo_root=repo_root,
                out_dir=out_dir,
                test_results_file=test_results_file,
                prefix=prefix
            )

        if not report.is_success:
            console.print(f"[bold red]❌ ビルドエラー:[/bold red]\n{report.error_message}")
            raise typer.Exit(1)

        console.print(f"[bold green]✅ ビルド成功！ [white]{report.out_dir}[/white][/bold green]")
        if report.bdd_generated_count > 0:
            console.print(f"  - BDD → .feature 生成: {report.bdd_generated_count} 件")
        console.print(f"  - 生成された Feature ページ: {report.generated_features_count} 件")
        console.print(f"  - 生成された アイテム ページ: {report.generated_items_count} 件")
        
        try:
            display_path = report.out_dir.relative_to(Path.cwd())
        except ValueError:
            display_path = report.out_dir
            
        console.print(f"\n閲覧するには以下のコマンドを実行してください:\n[bold magenta]mkdocs serve -f {display_path}/mkdocs.yml[/bold magenta]")

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ 予期せぬエラー: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        raise typer.Exit(1)
