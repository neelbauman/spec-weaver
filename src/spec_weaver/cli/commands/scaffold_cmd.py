import typer
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm
from rich.syntax import Syntax

from spec_weaver.adapters.codegen import generate_test_file, generate_environment_file
from spec_weaver.utils.git_utils import is_file_dirty

console = Console()

def _scaffold_cmd(
    feature_dir: Path = typer.Argument(..., exists=True, resolve_path=True, help=".feature ファイルが格納されたディレクトリ"),
    out_dir: Path = typer.Option(Path("specification/features/steps"), "--out-dir", "-o", resolve_path=True, help="テストコード出力先ディレクトリ"),
    overwrite: bool = typer.Option(False, "--overwrite", help="既存ファイルを全上書きする"),
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", resolve_path=True, help="Git dirty チェック用リポジトリルート"),
    force: bool = typer.Option(False, "--force", help="Git 未コミット変更の確認プロンプトをスキップして強制マージする"),
) -> None:
    """Gherkin .feature ファイルから behave テストコードの雛形を生成・差分マージします。"""
    try:
        feature_files = sorted(feature_dir.rglob("*.feature"))
        if not feature_files:
            console.print("[yellow]⚠️ .feature ファイルが見つかりませんでした。[/yellow]")
            raise typer.Exit(0)

        generated, skipped, errors = 0, 0, 0

        def _display_path(p: Path) -> str:
            try: return str(p.relative_to(Path.cwd()))
            except ValueError: return str(p)

        # environment.py の生成
        try:
            res = generate_environment_file(feature_dir, overwrite=overwrite)
            if res:
                out_path, _, _ = res
                console.print(f"  [green]✅ 環境設定作成[/green]: {_display_path(out_path)}")
                generated += 1
            elif (feature_dir / "environment.py").exists():
                console.print(f"  [dim]⏭️ スキップ[/dim]: {_display_path(feature_dir / 'environment.py')} (存在済み)")
                skipped += 1
        except Exception as e:
            console.print(f"  [red]❌ 環境設定エラー[/red]: environment.py: {e}")
            errors += 1

        for fpath in feature_files:
            try:
                out_file = out_dir / f"step_{fpath.stem}.py"

                if out_file.exists() and not force and not overwrite:
                    if is_file_dirty(out_file, repo_root):
                        console.print(f"\n[bold yellow]⚠️  {_display_path(out_file)} に未コミットの変更があります。[/bold yellow]")
                        if not Confirm.ask("差分マージを続行しますか？"):
                            console.print(f"  [dim]⏭️ スキップ[/dim]: {_display_path(out_file)} (キャンセル)")
                            skipped += 1
                            continue

                result = generate_test_file(fpath, out_dir, feature_dir, overwrite=overwrite)

                if result is None:
                    console.print(f"  [dim]⏭️ スキップ[/dim]: {_display_path(out_file)} (差分なし)")
                    skipped += 1
                else:
                    out_path, status, diff_text = result
                    if status == "created":
                        console.print(f"  [green]✅ 新規作成[/green]: {_display_path(out_path)}")
                    else:
                        console.print(f"\n  [blue]🔄 差分更新[/blue]: {_display_path(out_path)}")
                        console.print(Syntax(diff_text, "diff", theme="monokai", padding=(0, 2)))
                        console.print()
                    
                    generated += 1

            except Exception as e:
                console.print(f"  [red]❌ エラー[/red]: {fpath.name}: {e}")
                errors += 1

        console.print(f"\n[bold green]生成/更新: {generated}[/bold green]  [dim]スキップ: {skipped}[/dim]  " + (f"[bold red]エラー: {errors}[/bold red]" if errors else ""))
        if errors:
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ scaffold エラー: {e}[/bold red]")
        raise typer.Exit(1)
