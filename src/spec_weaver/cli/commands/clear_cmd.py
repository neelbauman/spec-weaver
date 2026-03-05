from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from spec_weaver.adapters.doorstop import get_item_map
from spec_weaver.services.clear_service import ClearService
from spec_weaver.services.status_service import StatusService

console = Console()


def _clear_cmd(
    item_id: Optional[str] = typer.Argument(None, help="gherkin_fingerprints を更新する Doorstop アイテム ID"),
    all_targets: bool = typer.Option(False, "--all", help="全アクティブ Doorstop アイテムを一括クリアする（エディタなし）"),
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True),
    no_edit: bool = typer.Option(False, "--no-edit", help="エディタを開かずにクリアする"),
) -> None:
    feature_dir = repo_root / ".specification" / "features"

    # 引数の相互排他チェック
    if all_targets and item_id:
        console.print("[bold red]❌ --all と対象IDは同時に指定できません。[/bold red]")
        raise typer.Exit(1)
    if not all_targets and not item_id:
        console.print("[bold red]❌ 対象IDを指定するか、--all を使用してください。[/bold red]")
        raise typer.Exit(1)

    try:
        if all_targets:
            _clear_all(feature_dir, repo_root)
        else:
            _clear_single(item_id, feature_dir, repo_root, no_edit)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ clear エラー: {e}[/bold red]")
        raise typer.Exit(1)


def _collect_related_files_for_clear(item_id: str, item, feature_dir: Path, repo_root: Path) -> list[Path]:
    """suspect 原因の Gherkin ファイルパスを収集する。"""
    from spec_weaver.adapters.doorstop import get_all_prefixes
    from spec_weaver.adapters.gherkin import get_spec_fingerprints

    try:
        all_prefixes = get_all_prefixes(repo_root)
        gherkin_fps = get_spec_fingerprints(feature_dir, repo_root, all_prefixes)
    except Exception:
        return []

    actual_fps = gherkin_fps.get(item_id, [])
    stored_fps = getattr(item, "gherkin_fingerprints", None) or []

    actual_dict: dict = {}
    for d in actual_fps:
        if d:
            k, v = list(d.items())[0]
            actual_dict[k] = v

    stored_dict: dict = {}
    for d in stored_fps:
        if d:
            k, v = list(d.items())[0]
            stored_dict[k] = v

    changed_files: set = set()
    for fpath, h in actual_dict.items():
        if stored_dict.get(fpath) != h:
            changed_files.add(fpath)
    for fpath in stored_dict:
        if fpath not in actual_dict:
            changed_files.add(fpath)

    if not changed_files:
        return []

    return [Path(fpath) for fpath in sorted(changed_files)]


def _resolve_repo_path(path: Path, repo_root: Path) -> Path:
    try:
        if path.is_absolute():
            return path
        return (repo_root / path).resolve()
    except Exception:
        return path


def _clear_single(item_id: str, feature_dir: Path, repo_root: Path, no_edit: bool) -> None:
    """単一アイテムの gherkin_fingerprints をエディタ確認後に更新する。"""
    from spec_weaver.utils.editor import EditorAbortedError, open_editor_with_files

    item_map = get_item_map(repo_root)
    if item_id not in item_map:
        console.print(f"[bold red]❌ アイテム {item_id} が見つかりません。[/bold red]")
        raise typer.Exit(1)

    report = StatusService().get_status_report(repo_root, feature_dir)
    status = report.review_state.get_status(item_id)
    if "suspect" not in status:
        console.print(f"[bold yellow]⚠️ {item_id} は suspect 状態ではないため、エディタを開かずに終了します。[/bold yellow]")
        raise typer.Exit(0)

    item = item_map[item_id]
    item_yaml_path = _resolve_repo_path(Path(item.path), repo_root)

    if not no_edit:
        related_paths = _collect_related_files_for_clear(item_id, item, feature_dir, repo_root)
        resolved_related = [_resolve_repo_path(p, repo_root) for p in related_paths]
        try:
            open_editor_with_files(item_yaml_path, resolved_related)
        except FileNotFoundError as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
            raise typer.Exit(1)
        except EditorAbortedError as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
            raise typer.Exit(1)

    result = ClearService().run_clear(item_id, feature_dir, repo_root)
    if not result.is_success:
        console.print(f"[bold red]❌ {result.error_message}[/bold red]")
        raise typer.Exit(1)

    for tag in result.skipped_unreviewed:
        console.print(f"⚠️ [bold yellow]{tag}[/bold yellow] は未レビューのためスキップしました。")
    for tag in result.skipped_suspect_unreviewed:
        console.print(f"⚠️ [bold yellow]{tag}[/bold yellow] は上位アイテムが未レビューのためスキップしました。")

    for tag in result.updated_items:
        console.print(f"✅ [bold]{tag}[/bold] の gherkin_fingerprints を更新しました。")


def _clear_all(feature_dir: Path, repo_root: Path) -> None:
    """全アクティブ Doorstop アイテムの gherkin_fingerprints を一括更新（エディタなし）。"""
    service = ClearService()
    with console.status("[bold cyan]全 Doorstop アイテムをクリア処理中...[/bold cyan]"):
        result = service.run_clear_all_items(feature_dir, repo_root)

    for tag in result.skipped_unreviewed:
        console.print(f"⚠️ [bold yellow]{tag}[/bold yellow] は未レビューのためスキップしました。")
    for tag in result.skipped_suspect_unreviewed:
        console.print(f"⚠️ [bold yellow]{tag}[/bold yellow] は上位アイテムが未レビューのためスキップしました。")

    for tag in result.updated_items:
        console.print(f"✅ [bold]{tag}[/bold] の gherkin_fingerprints を更新しました。")

    console.print(f"\n[bold green]✨ 合計 {len(result.updated_items)} 件更新しました。[/bold green]")
