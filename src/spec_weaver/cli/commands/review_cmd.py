from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from spec_weaver.adapters.doorstop import get_item_map
from spec_weaver.cli.commands.audit_cmd import _audit_cmd
from spec_weaver.services.review_service import ReviewService
from spec_weaver.services.status_service import StatusService

console = Console()


def _review_cmd(
    target_path: Optional[str] = typer.Argument(None, help="レビューする Doorstop アイテム ID"),
    all_targets: bool = typer.Option(False, "--all", help="全アクティブ Doorstop アイテムを一括レビューする（エディタなし）"),
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True),
    no_edit: bool = typer.Option(False, "--no-edit", help="エディタを開かずにレビューする"),
) -> None:
    # 引数の相互排他チェック
    if all_targets and target_path:
        console.print("[bold red]❌ --all と対象IDは同時に指定できません。[/bold red]")
        raise typer.Exit(1)
    if not all_targets and not target_path:
        console.print("[bold red]❌ 対象IDを指定するか、--all を使用してください。[/bold red]")
        raise typer.Exit(1)

    try:
        if all_targets:
            _review_all(repo_root)
        else:
            _review_single(target_path, repo_root, no_edit)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ review エラー: {e}[/bold red]")
        raise typer.Exit(1)


def _collect_related_files_for_review(item_id: str, item_map: dict, repo_root: Path) -> list[Path]:
    """suspect 原因アイテムの YAML パスを収集する。"""
    from spec_weaver.adapters.doorstop import check_suspect_cross_root, get_doorstop_tree

    try:
        item = item_map.get(item_id)
        if item is None:
            return []
        multi_tree = get_doorstop_tree(repo_root)
        suspect_parents, _ = check_suspect_cross_root(multi_tree, item)
    except Exception:
        return []

    related_paths: list[Path] = []
    for parent_id in sorted(str(p) for p in suspect_parents):
        parent = item_map.get(parent_id)
        if parent and hasattr(parent, "path") and parent.path:
            related_paths.append(Path(parent.path))

    return related_paths


def _resolve_repo_path(path: Path, repo_root: Path) -> Path:
    try:
        if path.is_absolute():
            return path
        return (repo_root / path).resolve()
    except Exception:
        return path


def _review_single(item_id: str, repo_root: Path, no_edit: bool) -> None:
    """単一 Doorstop アイテムをエディタ確認後にレビューする。"""
    from spec_weaver.utils.editor import EditorAbortedError, open_editor_with_files

    item_map = get_item_map(repo_root)
    if item_id not in item_map:
        console.print(f"[bold red]❌ アイテムが見つかりません: {item_id}[/bold red]")
        raise typer.Exit(1)

    feature_dir = repo_root / ".specification" / "features"
    report = StatusService().get_status_report(repo_root, feature_dir)
    status = report.review_state.get_status(item_id)
    if "unreviewed" not in status:
        console.print(f"[bold yellow]⚠️ {item_id} は unreviewed 状態ではないため、エディタを開かずに終了します。[/bold yellow]")
        raise typer.Exit(0)

    item = item_map[item_id]
    item_yaml_path = _resolve_repo_path(Path(item.path), repo_root)

    if not no_edit:
        related_paths = _collect_related_files_for_review(item_id, item_map, repo_root)
        resolved_related = [_resolve_repo_path(p, repo_root) for p in related_paths]
        try:
            open_editor_with_files(item_yaml_path, resolved_related)
        except FileNotFoundError as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
            raise typer.Exit(1)
        except EditorAbortedError as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
            raise typer.Exit(1)

    result = ReviewService().run_review(item_id, repo_root)
    if not result.is_success:
        console.print(f"[bold red]❌ {result.error_message}[/bold red]")
        raise typer.Exit(1)

    console.print(f"[bold green]✅ アイテム {item_id} をレビューしました[/bold green]")
    console.print()
    _audit_cmd(repo_root=repo_root, prefix=None, stale_days=90, check_impl=False, extensions=None)


def _review_all(repo_root: Path) -> None:
    """全アクティブ Doorstop アイテムを一括レビュー（エディタなし）。"""
    service = ReviewService()
    with console.status("[bold cyan]全 Doorstop アイテムをレビュー中...[/bold cyan]"):
        reviewed_items, failed = service.run_review_all_items(repo_root)

    console.print(f"[bold green]✅ Doorstop アイテム {len(reviewed_items)} 件レビュー済み[/bold green]")

    for uid, msg in failed:
        console.print(f"[bold yellow]⚠️ スキップ: {uid}: {msg}[/bold yellow]")

    console.print()
    _audit_cmd(repo_root=repo_root, prefix=None, stale_days=90, check_impl=False, extensions=None)

    if failed:
        raise typer.Exit(1)
