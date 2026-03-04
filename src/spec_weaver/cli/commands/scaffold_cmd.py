import typer
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm
from rich.syntax import Syntax

from spec_weaver.adapters.codegen import (
    generate_test_file,
    generate_environment_file,
    prepare_test_file_content,
    collect_all_feature_steps,
    _load_existing_resolver,
)
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

        # 全 .feature から使用中ステップを収集
        all_used_steps = collect_all_feature_steps(feature_files)

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

                # 1. 差分チェックを先に行う
                prep_result = prepare_test_file_content(fpath, out_dir, feature_dir, overwrite=overwrite)
                if prep_result is None:
                    console.print(f"  [dim]⏭️ スキップ[/dim]: {_display_path(out_file)} (差分なし)")
                    skipped += 1
                    continue

                status, new_content, diff_text = prep_result

                diff_shown = False
                # 2. 差分がある場合に Git チェックと確認
                if out_file.exists() and not force and not overwrite:
                    if is_file_dirty(out_file, repo_root):
                        console.print(f"\n[bold yellow]⚠️  {_display_path(out_file)} に未コミットの変更があります。[/bold yellow]")
                        if status == "updated" and diff_text:
                            console.print(f"  [dim]マージ予定の差分:[/dim]")
                            console.print(Syntax(diff_text, "diff", theme="monokai", padding=(0, 2)))
                            diff_shown = True
                        
                        if not Confirm.ask("差分マージを続行しますか？"):
                            console.print(f"  [dim]⏭️ スキップ[/dim]: {_display_path(out_file)} (キャンセル)")
                            skipped += 1
                            continue

                # 3. ファイル書き出し
                out_dir.mkdir(parents=True, exist_ok=True)
                out_file.write_text(new_content, encoding="utf-8")

                # 4. 表示
                if status == "created":
                    console.print(f"  [green]✅ 新規作成[/green]: {_display_path(out_file)}")
                else:
                    console.print(f"\n  [blue]🔄 差分更新[/blue]: {_display_path(out_file)}")
                    if not diff_shown and diff_text:
                        console.print(Syntax(diff_text, "diff", theme="monokai", padding=(0, 2)))
                        console.print()
                
                generated += 1

            except Exception as e:
                console.print(f"  [red]❌ エラー[/red]: {fpath.name}: {e}")
                errors += 1

        # 未使用ステップ定義の警告
        try:
            resolver = _load_existing_resolver(out_dir)
            unused_count = 0
            for step_def in resolver.steps:
                if step_def.is_stub:
                    continue
                
                is_used = False
                for prefix, raw_text in all_used_steps:
                    if step_def.matches(prefix, raw_text):
                        is_used = True
                        break
                
                if not is_used:
                    rel_file = _display_path(Path(step_def.file))
                    console.print(f"  [yellow]⚠️  未使用のステップ定義: {step_def.pattern} ({rel_file}:{step_def.line})[/yellow]")
                    unused_count += 1
            
            if unused_count > 0:
                console.print(f"\n[yellow]合計 {unused_count} 件の未使用ステップ定義が見つかりました。[/yellow]")
        except Exception as e:
             console.print(f"  [dim]⏭️ 未使用チェックをスキップ (エラー: {e})[/dim]")

        console.print(f"\n[bold green]生成/更新: {generated}[/bold green]  [dim]スキップ: {skipped}[/dim]  " + (f"[bold red]エラー: {errors}[/bold red]" if errors else ""))
        if errors:
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ scaffold エラー: {e}[/bold red]")
        raise typer.Exit(1)
