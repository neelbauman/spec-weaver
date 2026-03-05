from pathlib import Path
from typing import Optional, Set

import typer
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from spec_weaver.services.trace_service import TraceService
from spec_weaver.utils.formatters import (
    get_impl_status_badge,
    get_review_status_badge,
    get_uid_prefix,
)

console = Console()

# ---------------------------------------------------------------------------
# UI描画用 ヘルパー関数群
# ---------------------------------------------------------------------------

def _collect_all_ancestors(uid: str, all_items: dict, visited: Optional[Set] = None) -> Set[str]:
    """指定UIDの全祖先UIDの集合を返す（uid自身は含まない）。循環参照を visited で防止。"""
    if visited is None:
        visited = set()
    item = all_items.get(uid)
    if item is None:
        return visited
    for link in item.links:
        parent_uid = str(link)
        if parent_uid not in visited and parent_uid in all_items:
            visited.add(parent_uid)
            _collect_all_ancestors(parent_uid, all_items, visited)
    return visited

def _format_trace_node(uid: str, item, is_origin: bool = False, review_state=None) -> str:
    """Rich マークアップ付きのノードラベル文字列を返す。"""
    header = (item.header or "").strip() if item else ""
    impl_badge = get_impl_status_badge(item) if item else "-"
    review_badge = get_review_status_badge(item or uid, review_state)
    badge = f"{impl_badge} / {review_badge}"
    if is_origin:
        return f"[bold yellow]★[/bold yellow] [bold]{uid}[/bold] {header} {badge}"
    return f"[bold cyan]{uid}[/bold cyan] {header} {badge}"

def _add_impl_files_to_node(node, uid: str, impl_map: dict, repo_root: Path) -> None:
    """実装ファイルノードを Rich Tree ノードに追加する（TRC-004）。"""
    impl_list = impl_map.get(uid)
    if not impl_list:
        return
    for item in impl_list:
        path_str = item["path"]
        source = item["source"]
        exists = item["exists"]
        
        icon = "📁"
        if source == "annotation":
            icon = "📝"
            
        if not exists:
            node.add(f"❌ {path_str} [red](not found)[/red]")
        else:
            node.add(f"{icon} {path_str}")

def _add_descendants_to_rich_node(
    node, uid: str, all_items: dict, child_map: dict, tag_map: dict,
    visited: set, impl_map: Optional[dict] = None, repo_root: Optional[Path] = None,
    review_state=None
) -> None:
    """子アイテム・Gherkinシナリオを再帰的にRich Treeノードへ追加する。"""
    scenarios = tag_map.get(uid, [])
    if scenarios:
        file_scenarios: dict = {}
        for sc in scenarios:
            fname = Path(sc["file"]).name
            file_scenarios.setdefault(fname, []).append(sc)
        for fname, scs in sorted(file_scenarios.items()):
            rel_path = scs[0]["file"]
            review_badge = get_review_status_badge(rel_path, review_state)
            feature_node = node.add(f"🥒 {fname} {review_badge}")
            for sc in scs:
                feature_node.add(f"Scenario: {sc['name']}")

    if impl_map is not None and repo_root is not None:
        _add_impl_files_to_node(node, uid, impl_map, repo_root)

    for child_uid in sorted(child_map.get(uid, [])):
        if child_uid in visited:
            continue
        child_item = all_items.get(child_uid)
        label = _format_trace_node(child_uid, child_item, review_state=review_state)
        child_node = node.add(label)
        new_visited = set(visited)
        new_visited.add(child_uid)
        _add_descendants_to_rich_node(
            child_node, child_uid, all_items, child_map, tag_map, new_visited,
            impl_map=impl_map, repo_root=repo_root, review_state=review_state
        )

def _add_focused_path(
    node, current_uid: str, origin_uid: str, on_path: set, all_items: dict,
    child_map: dict, tag_map: dict, visited: set, expand_at_origin: bool = True,
    impl_map: Optional[dict] = None, repo_root: Optional[Path] = None, review_state=None
) -> None:
    """祖先からoriginまでのパスを辿り、originで全子孫を展開する。"""
    if current_uid == origin_uid:
        if expand_at_origin:
            _add_descendants_to_rich_node(
                node, current_uid, all_items, child_map, tag_map, set(visited),
                impl_map=impl_map, repo_root=repo_root, review_state=review_state
            )
        return

    for child_uid in sorted(child_map.get(current_uid, [])):
        if child_uid not in on_path or child_uid in visited:
            continue
        child_item = all_items.get(child_uid)
        is_origin = child_uid == origin_uid
        label = _format_trace_node(child_uid, child_item, is_origin=is_origin, review_state=review_state)
        child_node = node.add(label)
        new_visited = set(visited)
        new_visited.add(child_uid)
        _add_focused_path(
            child_node, child_uid, origin_uid, on_path, all_items, child_map,
            tag_map, new_visited, expand_at_origin, impl_map=impl_map,
            repo_root=repo_root, review_state=review_state
        )

def _build_trace_rich_tree(
    origin_uid: str, all_items: dict, child_map: dict, tag_map: dict, direction: str,
    impl_map: Optional[dict] = None, repo_root: Optional[Path] = None, review_state=None
):
    """トレースツリーを構築して返す。複数ルート祖先がある場合はリストで返す。"""
    origin_item = all_items.get(origin_uid)

    if direction == "down":
        label = _format_trace_node(origin_uid, origin_item, is_origin=True, review_state=review_state)
        tree = Tree(label)
        _add_descendants_to_rich_node(
            tree, origin_uid, all_items, child_map, tag_map, {origin_uid},
            impl_map=impl_map, repo_root=repo_root, review_state=review_state
        )
        return tree

    ancestors = _collect_all_ancestors(origin_uid, all_items)
    if not ancestors:
        label = _format_trace_node(origin_uid, origin_item, is_origin=True, review_state=review_state)
        tree = Tree(label)
        if direction == "both":
            _add_descendants_to_rich_node(
                tree, origin_uid, all_items, child_map, tag_map, {origin_uid},
                impl_map=impl_map, repo_root=repo_root, review_state=review_state
            )
        return tree

    on_path = ancestors | {origin_uid}
    expand_at_origin = direction == "both"

    root_ancestors: Set[str] = set()
    for anc_uid in ancestors:
        anc_item = all_items.get(anc_uid)
        if anc_item is None:
            root_ancestors.add(anc_uid)
            continue
        parents_in_ancestors = [str(link) for link in anc_item.links if str(link) in ancestors]
        if not parents_in_ancestors:
            root_ancestors.add(anc_uid)

    trees = []
    for root_uid in sorted(root_ancestors):
        root_item = all_items.get(root_uid)
        label = _format_trace_node(root_uid, root_item, review_state=review_state)
        tree = Tree(label)
        _add_focused_path(
            tree, root_uid, origin_uid, on_path, all_items, child_map, tag_map,
            {root_uid}, expand_at_origin, impl_map=impl_map, repo_root=repo_root, review_state=review_state
        )
        trees.append(tree)

    return trees if len(trees) > 1 else trees[0]

def _trace_flat_output(
    origin_uid: str, all_items_str: dict, child_map: dict, direction: str, review_state=None
) -> None:
    """flat形式でトレース結果をテーブル表示する。"""
    all_relevant: Set[str] = set()
    if direction in ("up", "both"):
        all_relevant.update(_collect_all_ancestors(origin_uid, all_items_str))
    all_relevant.add(origin_uid)
    if direction in ("down", "both"):
        def _collect_descendants(uid: str, collected: set) -> None:
            for child_uid in child_map.get(uid, []):
                if child_uid not in collected:
                    collected.add(child_uid)
                    _collect_descendants(child_uid, collected)
        _collect_descendants(origin_uid, all_relevant)

    table = Table(show_header=True, header_style="bold magenta", box=None)
    table.add_column("種別", style="bold")
    table.add_column("ID", style="bold cyan")
    table.add_column("タイトル")
    table.add_column("実装ステータス")
    table.add_column("レビューステータス")
    for uid in sorted(all_relevant):
        item = all_items_str.get(uid)
        prefix = get_uid_prefix(uid)
        header = (item.header or "").strip() if item else ""
        impl_badge = get_impl_status_badge(item) if item else "-"
        review_badge = get_review_status_badge(item or uid, review_state)
        table.add_row(prefix, uid, header, impl_badge, review_badge)
    console.print(table)


# ---------------------------------------------------------------------------
# エントリポイント
# ---------------------------------------------------------------------------

def _trace_cmd(
    item_id: str = typer.Argument(..., help="探索起点ID (例: REQ-001, SPEC-003, audit.feature)"),
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", help="リポジトリルート"),
    direction: str = typer.Option("both", "--direction", "-d", help="探索方向: up / down / both (デフォルト: both)"),
    output_format: str = typer.Option("tree", "--format", help="出力形式: tree (デフォルト) / flat"),
    show_impl: bool = typer.Option(False, "--show-impl", help="実装ファイルをツリーに表示する"),
    extensions: Optional[str] = typer.Option(None, "--extensions", help="アノテーションスキャン対象の拡張子（カンマ区切り）"),
) -> None:
    """指定したアイテムを起点として、上位・下位のトレーサビリティツリーを表示します。"""
    try:
        actual_feature_dir = repo_root / ".specification" / "features"
        if not actual_feature_dir.exists():
            console.print(f"[yellow]⚠️  Warning: Feature directory '{actual_feature_dir}' does not exist. Skipping Gherkin trace.[/yellow]")
            actual_feature_dir = None

        with console.status("[bold cyan]データを読み込み中...[/bold cyan]"):
            ext_list = [e.strip() for e in extensions.split(",")] if extensions else None
            data = TraceService().prepare_trace_data(repo_root, actual_feature_dir, show_impl, ext_list)

        # 起点アイテムの解決
        origin_uid: str
        if item_id.endswith(".feature"):
            if actual_feature_dir is None:
                console.print("[bold red]❌ .featureファイルを起点にするには --feature-dir を指定してください。[/bold red]")
                raise typer.Exit(1)
            found_uid = None
            for spec_uid, scenarios in data.tag_map.items():
                for sc in scenarios:
                    if Path(sc["file"]).name == item_id:
                        found_uid = spec_uid
                        break
                if found_uid:
                    break
            if found_uid is None:
                console.print(f"[bold red]❌ Error: Item '{item_id}' not found[/bold red]")
                raise typer.Exit(1)
            origin_uid = found_uid
        else:
            if item_id not in data.all_items_str:
                console.print(f"[bold red]❌ Error: Item '{item_id}' not found[/bold red]")
                raise typer.Exit(1)
            origin_uid = item_id

        # 出力
        if output_format == "flat":
            _trace_flat_output(origin_uid, data.all_items_str, data.child_map, direction, data.review_state)
        else:
            result = _build_trace_rich_tree(
                origin_uid, data.all_items_str, data.child_map, data.tag_map, direction,
                impl_map=data.impl_map, repo_root=repo_root if show_impl else None, review_state=data.review_state
            )
            if isinstance(result, list):
                for tree in result:
                    console.print(tree)
            else:
                console.print(result)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ エラー: {e}[/bold red]")
        raise typer.Exit(1)
