from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from spec_weaver.services.sync_service import SyncService

console = Console()

def _sync_cmd(
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True, help="リポジトリルート"),
    feature_dir: Optional[Path] = typer.Option(None, "--feature-dir", "-f", help="Gherkin .feature ファイルのディレクトリ（省略時は .specification/features）"),
    extensions: Optional[str] = typer.Option(None, "--extensions", help="アノテーションスキャン対象の拡張子（カンマ区切り）"),
    sync_children: bool = typer.Option(False, "--sync-children", help="親子ハッシュ (child_stamps) の同期も実行する"),
) -> None:
    """
    AST解析結果やアノテーションをスキャンし、Doorstop YAMLに feature_files や scanned_impl_files として同期します。
    """
    actual_feature_dir = feature_dir or (repo_root / ".specification" / "features")
    if not actual_feature_dir.exists():
        console.print(f"[yellow]⚠️  Warning: Feature directory '{actual_feature_dir}' does not exist. Skipping Gherkin AST analysis.[/yellow]")
        actual_feature_dir = None

    try:
        with console.status("[bold cyan]紐づけ情報を同期中...[/bold cyan]"):
            ext_list = [e.strip() for e in extensions.split(",")] if extensions else None
            
            service = SyncService()
            updated_count, error_count = service.sync_all(
                repo_root=repo_root,
                feature_dir=actual_feature_dir,
                extensions=ext_list,
                sync_children=sync_children,
            )

        if error_count > 0:
            console.print(f"[bold yellow]⚠️ 同期完了: {updated_count}件更新されましたが、{error_count}件のエラーが発生しました。[/bold yellow]")
        else:
            console.print(f"[bold green]✅ 同期完了: {updated_count}件のアイテムを更新しました。[/bold green]")
            
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ エラー: {e}[/bold red]")
        raise typer.Exit(1)
