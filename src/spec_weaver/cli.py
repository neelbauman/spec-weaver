# src/spec_weaver/cli.py

import typer
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

import re

from spec_weaver.doorstop import get_item_map, get_doorstop_tree, _get_custom_attribute, get_specs, is_suspect, get_all_prefixes
from spec_weaver.gherkin import get_tag_map, get_tags
from spec_weaver.test_results import (
    TestResultMap,
    format_status_badge,
    load_test_results,
    result_badge,
    spec_result_summary,
)

# ---------------------------------------------------------------------------
# 実装ステータス定義
# ---------------------------------------------------------------------------

IMPL_STATUS_BADGE: dict[str, str] = {
    "draft":       "📝 draft",
    "in-progress": "🚧 in-progress",
    "implemented": "✅ implemented",
    "deprecated":  "🗑️ deprecated",
}


def _impl_status_badge(item) -> str:
    """YAMLの status フィールドを絵文字バッジ文字列に変換する。未設定は '-'。"""
    status = _get_custom_attribute(item, "status", None)
    if not status:
        return "-"
    return IMPL_STATUS_BADGE.get(str(status), f"❓ {status}")


app = typer.Typer(
    help="Spec-Weaver: Doorstopの仕様とGherkinのテストをシームレスに統合・監査するツール",
    add_completion=False,
)
console = Console()


# ---------------------------------------------------------------------------
# audit コマンド
# ---------------------------------------------------------------------------

@app.command("audit")
def audit_cmd(
    feature_dir: Path = typer.Argument(
        ...,
        help="Gherkinの .feature ファイルが格納されているディレクトリのパス",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    repo_root: Path = typer.Option(
        Path.cwd(),
        "--repo-root",
        "-r",
        help="Doorstopのプロジェクトルート（.doorstopディレクトリがある場所）",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    prefix: Optional[str] = typer.Option(
        None,
        "--prefix",
        "-p",
        help="監査対象とする仕様IDのプレフィックス（省略した場合は全ドキュメントの testable アイテムが対象）",
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
            title="Spec-Weaver Audit",
            border_style="blue",
        )
    )

    try:
        with console.status("[bold cyan]Doorstopの仕様データベースを構築中...[/bold cyan]"):
            try:
                specs_in_db = get_specs(repo_root=repo_root, prefix=prefix)
                all_prefixes = get_all_prefixes(repo_root=repo_root)
            except Exception as e:
                console.print(f"[bold red]❌ Doorstopデータの読み込みに失敗しました:[/bold red] {e}")
                raise typer.Exit(code=1)

        with console.status("[bold cyan]Gherkinのフィーチャーファイルを解析中...[/bold cyan]"):
            try:
                # 検索対象のプレフィックスを決定
                search_prefixes = {prefix} if prefix else all_prefixes
                tags_in_code = get_tags(features_dir=feature_dir, prefixes=search_prefixes)
            except ValueError as e:
                console.print(f"[bold red]❌ Gherkinファイルのパースに失敗しました:[/bold red] {e}")
                raise typer.Exit(code=1)

        with console.status("[bold cyan]Suspect状態の仕様を確認中...[/bold cyan]"):
            try:
                raw_items = get_item_map(repo_root=repo_root)
                suspect_specs = {
                    uid for uid, item in raw_items.items()
                    if (not prefix or uid.startswith(prefix)) and is_suspect(item)
                }
            except Exception as e:
                console.print(f"[bold red]❌ Suspect状態の確認に失敗しました:[/bold red] {e}")
                suspect_specs = set()

        untested_specs = specs_in_db - tags_in_code
        orphaned_tags = tags_in_code - specs_in_db
        has_error = False

        if untested_specs:
            has_error = True
            console.print("\n[bold red]❌ テストが実装されていない仕様 (Untested Specs):[/bold red]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Missing Spec ID", style="dim")
            for spec in sorted(untested_specs):
                table.add_row(spec)
            console.print(table)

        if orphaned_tags:
            has_error = True
            console.print("\n[bold yellow]⚠️ 仕様書に存在しない孤児タグ (Orphaned Tags):[/bold yellow]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Orphaned Tag", style="dim")
            for tag in sorted(orphaned_tags):
                table.add_row(f"@{tag}")
            console.print(table)

        if suspect_specs:
            has_error = True
            console.print("\n[bold yellow]⚠️ レビューが必要なSuspect仕様 (Suspect Specs):[/bold yellow]")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Suspect Spec ID", style="dim")
            table.add_column("理由", style="dim")
            for spec in sorted(suspect_specs):
                table.add_row(spec, "上位要件が変更されました。レビューが必要です。")
            console.print(table)

        if not has_error:
            console.print(
                f"\n[bold green]✅ 完璧です！ {len(specs_in_db)} 件の仕様がすべてGherkinテストでカバーされています。[/bold green]"
            )
            raise typer.Exit(code=0)
        else:
            console.print("\n[bold red]監査が失敗しました。仕様とテストの乖離を修正してください。[/bold red]")
            raise typer.Exit(code=1)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"\n[bold white on red] 予期せぬ致命的なエラーが発生しました: {e} [/bold white on red]")
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# scaffold コマンド
# ---------------------------------------------------------------------------

@app.command("scaffold")
def scaffold_cmd() -> None:
    """
    (開発中) Gherkinに定義されていて、まだ実装されていないテストステップの雛形を生成します。
    """
    console.print("[yellow]🚧 scaffold コマンドは現在開発中です。[/yellow]")


# ---------------------------------------------------------------------------
# status コマンド
# ---------------------------------------------------------------------------

@app.command("status")
def status_cmd(
    repo_root: Path = typer.Option(
        Path.cwd(),
        "--repo-root",
        "-r",
        help="Doorstopのプロジェクトルート",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    filter_status: Optional[str] = typer.Option(
        None,
        "--filter",
        "-f",
        help="表示するステータスで絞り込む（draft / in-progress / implemented / deprecated）",
    ),
) -> None:
    """
    REQ・SPECの実装ステータス（status フィールド）を一覧表示します。
    """
    try:
        with console.status("[bold cyan]Doorstopデータを読み込み中...[/bold cyan]"):
            raw_items = get_item_map(repo_root=repo_root)
            all_items_str = {str(uid): item for uid, item in raw_items.items()}

        req_items = {uid: item for uid, item in all_items_str.items() if uid.startswith("REQ")}
        spec_items = {uid: item for uid, item in all_items_str.items() if uid.startswith("SPEC")}

        def _print_status_table(title: str, items: dict) -> int:
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("ID", style="bold cyan", no_wrap=True)
            table.add_column("タイトル")
            table.add_column("実装ステータス")
            shown = 0
            for uid in sorted(items.keys()):
                item = items[uid]
                raw_status = _get_custom_attribute(item, "status", None)
                if filter_status and str(raw_status or "") != filter_status:
                    continue
                badge = _impl_status_badge(item)
                title_text = (item.header or "").strip()
                table.add_row(uid, title_text, badge)
                shown += 1
            if shown > 0:
                console.print(table)
            return shown

        req_shown = _print_status_table("要件 (REQ)", req_items)
        spec_shown = _print_status_table("仕様 (SPEC)", spec_items)

        total = req_shown + spec_shown
        if total == 0:
            if filter_status:
                console.print(f"[yellow]ステータス '{filter_status}' に一致するアイテムが見つかりませんでした。[/yellow]")
            else:
                console.print("[yellow]アイテムが見つかりませんでした。[/yellow]")
        else:
            console.print(f"\n[bold green]合計 {total} 件を表示しました。[/bold green]")
            console.print(
                "[dim]ステータスを更新するには、対象の YAML ファイルに [bold]status: in-progress[/bold] などを追記してください。[/dim]"
            )

    except Exception as e:
        console.print(f"[bold red]❌ エラー: {e}[/bold red]")
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# build コマンド
# ---------------------------------------------------------------------------

@app.command()
def build(
    feature_dir: Path = typer.Argument(..., exists=True, resolve_path=True),
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True),
    out_dir: Path = typer.Option(Path(".specification"), "--out-dir", "-o", resolve_path=True),
    prefix: str = typer.Option("SPEC", "--prefix", "-p", help="Gherkinタグとして主に扱うデフォルトプレフィックス"),
    test_results_file: Path = typer.Option(
        None,
        "--test-results",
        "-t",
        help="pytest-bdd 生成の Cucumber 互換 JSON レポートのパス（省略可）",
        exists=False,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
):
    """Doorstopの全ドキュメントを解析し、相互リンク・カバレッジ・テスト結果を含むポータルサイトをビルドします。"""
    try:
        with console.status("[bold cyan]データの分析と結合を開始...[/bold cyan]"):
            # 1. Doorstopから全アイテムと全プレフィックス取得
            raw_items = get_item_map(repo_root)
            all_items_str = {str(uid): item for uid, item in raw_items.items()}
            doorstop_tree = get_doorstop_tree(repo_root)
            all_prefixes = {str(doc.prefix) for doc in doorstop_tree}

            # 2. Gherkinタグマップ取得 (全プレフィックスを対象にする)
            tag_map = get_tag_map(feature_dir, all_prefixes)

            # 3. 子への逆引きマップ（parent_uid -> [child_uid, ...]）
            child_map: dict[str, list[str]] = {}
            for uid, item in all_items_str.items():
                for link in item.links:
                    parent_uid = str(link)
                    child_map.setdefault(parent_uid, []).append(uid)

            # 4. 兄弟マップ（同じ親を持つアイテム同士）
            sibling_map = _compute_sibling_map(all_items_str, child_map)

            # 5. テスト実行結果（省略可）
            test_result_map: TestResultMap | None = None
            if test_results_file is not None:
                if not test_results_file.exists():
                    console.print(
                        f"[bold red]❌ テスト結果ファイルが見つかりません: {test_results_file}[/bold red]"
                    )
                    raise typer.Exit(1)
                try:
                    test_result_map = load_test_results(test_results_file)
                    console.print(
                        f"[bold cyan]📊 テスト結果を読み込みました: {len(test_result_map)} シナリオ[/bold cyan]"
                    )
                except Exception as e:
                    console.print(f"[bold red]❌ テスト結果の読み込みに失敗しました: {e}[/bold red]")
                    raise typer.Exit(1)

        # 出力ディレクトリ準備
        docs_dir = out_dir / "docs"
        items_dir = docs_dir / "items"
        features_md_dir = docs_dir / "features"
        items_dir.mkdir(parents=True, exist_ok=True)
        features_md_dir.mkdir(parents=True, exist_ok=True)

        # 6. Gherkin .feature → Markdown 変換
        feature_md_map: dict[str, str] = {}
        for feature_file in feature_dir.rglob("*.feature"):
            try:
                rel = feature_file.relative_to(feature_dir)
                md_rel = rel.with_suffix(".md")
                out_path = features_md_dir / md_rel
                out_path.parent.mkdir(parents=True, exist_ok=True)
                md_content = _feature_to_markdown(feature_file)
                out_path.write_text(md_content, encoding="utf-8")
                try:
                    tag_rel = str(feature_file.relative_to(feature_dir.parent))
                except ValueError:
                    tag_rel = str(feature_file)
                feature_md_map[tag_rel] = f"../features/{md_rel.as_posix()}"
            except Exception as e:
                console.print(f"[yellow]⚠️ feature変換スキップ: {feature_file}: {e}[/yellow]")

        # 7. 個別アイテムページ (items/*.md)
        for uid, item in all_items_str.items():
            content = _generate_item_markdown(
                uid, item, all_items_str, child_map, sibling_map, tag_map, feature_md_map,
                test_result_map=test_result_map,
            )
            (items_dir / f"{uid}.md").write_text(content, encoding="utf-8")

        # 8. 各ドキュメントの一覧ページ生成
        prefix_to_file = {}
        for doc in doorstop_tree:
            p = str(doc.prefix)
            doc_items = {uid: item for uid, item in all_items_str.items() if uid.startswith(p + "-")}
            # プレフィックスが完全に一致する場合（ハイフンなし）も考慮が必要な場合があるが、Doorstopの標準はハイフン区切り
            if not doc_items:
                doc_items = {uid: item for uid, item in all_items_str.items() if uid.startswith(p)}
            
            filename = f"{p.lower()}.md"
            table = _generate_index_table(
                f"ドキュメント: {p}", doc_items, all_items_str, child_map, sibling_map, tag_map,
                test_result_map=test_result_map,
            )
            (docs_dir / filename).write_text(table, encoding="utf-8")
            prefix_to_file[p] = filename

        # 9. index.md と mkdocs.yml
        _generate_basic_files(
            docs_dir, out_dir, repo_root.name, feature_md_map,
            all_items_str, child_map, tag_map, doorstop_tree, prefix_to_file
        )

        console.print(f"[bold green]✅ ビルド成功！ [white]{out_dir}[/white][/bold green]")
        console.print(
            f"閲覧: [bold magenta]mkdocs serve -f {out_dir.relative_to(Path.cwd())}/mkdocs.yml[/bold magenta]"
        )

        console.print(f"[bold green]✅ ビルド成功！ [white]{out_dir}[/white][/bold green]")
        console.print(
            f"閲覧: [bold magenta]mkdocs serve -f {out_dir.relative_to(Path.cwd())}/mkdocs.yml[/bold magenta]"
        )

    except Exception as e:
        console.print(f"[bold red]❌ ビルドエラー: {e}[/bold red]")
        import traceback
        traceback.print_exc()
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# ヘルパー: 兄弟マップ計算
# ---------------------------------------------------------------------------

def _compute_sibling_map(all_items_str: dict, child_map: dict) -> dict[str, list[str]]:
    """同じ親（リンク先）を持ち、かつ同じプレフィックスを持つアイテムを兄弟として計算する。"""
    sibling_map: dict[str, list[str]] = {}
    for uid, item in all_items_str.items():
        my_prefix = _get_uid_prefix(uid)
        siblings: set[str] = set()
        for link in item.links:
            parent_uid = str(link)
            for sibling_uid in child_map.get(parent_uid, []):
                if sibling_uid != uid:
                    # 同じプレフィックス（ドキュメントタイプ）の場合のみ兄弟とする
                    if _get_uid_prefix(sibling_uid) == my_prefix:
                        siblings.add(sibling_uid)
        if siblings:
            sibling_map[uid] = sorted(siblings)
    return sibling_map


# ---------------------------------------------------------------------------
# ヘルパー: カバレッジ計算
# ---------------------------------------------------------------------------

def _spec_coverage(uid: str, tag_map: dict, item, all_items_str: dict) -> tuple[int, int]:
    """
    SPEC単体のカバレッジを返す。
    Returns: (covered_scenario_count, 1) ただしnot testableなら(0, 0)
    """
    testable = _get_custom_attribute(item, "testable", True)
    if not testable:
        return (0, 0)
    scenarios = tag_map.get(uid, [])
    return (1 if scenarios else 0, 1)


def _req_coverage(req_uid: str, child_map: dict, all_items_str: dict, tag_map: dict) -> tuple[int, int]:
    """
    REQの集約カバレッジ: 関連するテスト対象SPECのうち、シナリオが存在するものの割合。
    Returns: (covered, total)
    """
    children = child_map.get(req_uid, [])
    covered = 0
    total = 0
    for child_uid in children:
        child_item = all_items_str.get(child_uid)
        if child_item is None:
            continue
        c, t = _spec_coverage(child_uid, tag_map, child_item, all_items_str)
        covered += c
        total += t
    return (covered, total)


def _coverage_badge(covered: int, total: int) -> str:
    """カバレッジを絵文字付きの割合文字列で返す。"""
    if total == 0:
        return "⚪️ -"
    pct = int(covered / total * 100)
    icon = "🟢" if pct == 100 else ("🟡" if pct >= 50 else "🔴")
    return f"{icon} {covered}/{total} ({pct}%)"


# ---------------------------------------------------------------------------
# ヘルパー: Gherkin → Markdown 変換
# ---------------------------------------------------------------------------

def _feature_to_markdown(feature_file: Path) -> str:
    """
    .featureファイルをGherkinパーサーで解析し、ブラウザで読みやすいMarkdownに変換する。
    """
    from gherkin.parser import Parser
    from gherkin.token_scanner import TokenScanner

    with open(feature_file, "r", encoding="utf-8") as f:
        raw = f.read()

    parser = Parser()
    ast = parser.parse(TokenScanner(raw))
    feature_node = ast.get("feature", {})

    feature_name = feature_node.get("name", feature_file.stem)
    feature_desc = (feature_node.get("description") or "").strip()
    feature_tags = [t["name"] for t in feature_node.get("tags", [])]

    lines: list[str] = [f"# Feature: {feature_name}\n"]

    if feature_tags:
        lines.append("**タグ**: " + " ".join(f"`{t}`" for t in feature_tags) + "\n")

    if feature_desc:
        lines.append(f"{feature_desc}\n")

    for child in feature_node.get("children", []):
        # Background
        if "background" in child:
            bg = child["background"]
            lines.append("---\n## Background\n")
            for step in bg.get("steps", []):
                kw = step["keyword"].strip()
                lines.append(f"- **{kw}** {step['text']}")
            lines.append("")

        # Scenario / Scenario Outline
        if "scenario" in child:
            sc = child["scenario"]
            sc_name = sc.get("name", "")
            sc_keyword = (sc.get("keyword") or "Scenario").strip()
            sc_tags = [t["name"] for t in sc.get("tags", [])]
            sc_desc = (sc.get("description") or "").strip()

            tag_str = " ".join(f"`{t}`" for t in sc_tags) if sc_tags else ""
            lines.append(f"---\n## {sc_keyword}: {sc_name}\n")
            if tag_str:
                lines.append(f"**タグ**: {tag_str}\n")
            if sc_desc:
                lines.append(f"{sc_desc}\n")

            for step in sc.get("steps", []):
                kw = step["keyword"].strip()
                lines.append(f"- **{kw}** {step['text']}")

            # Examples (Scenario Outline)
            for example in sc.get("examples", []):
                ex_name = example.get("name", "")
                lines.append(f"\n### Examples{': ' + ex_name if ex_name else ''}\n")
                header = example.get("tableHeader", {})
                rows = example.get("tableBody", [])
                if header:
                    cells = [c["value"] for c in header.get("cells", [])]
                    lines.append("| " + " | ".join(cells) + " |")
                    lines.append("| " + " | ".join(["---"] * len(cells)) + " |")
                    for row in rows:
                        row_cells = [c["value"] for c in row.get("cells", [])]
                        lines.append("| " + " | ".join(row_cells) + " |")

            lines.append("")

    # フッターにrawソースも折り畳みで表示
    lines.append("\n---\n<details><summary>Raw .feature source</summary>\n")
    lines.append(f"```gherkin\n{raw}\n```\n</details>")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# ヘルパー: 一覧ページ生成
# ---------------------------------------------------------------------------

def _generate_index_table(
    title, target_items, all_items_str, child_map, sibling_map, tag_map,
    test_result_map: "TestResultMap | None" = None,
):
    """一覧ページのテーブルMarkdownを生成。"""
    has_results = test_result_map is not None
    result_col_header = " | テスト結果" if has_results else ""
    result_col_sep = " | :--- " if has_results else ""

    # ID | タイトル | 親 | 子 | 兄弟 | カバレッジ | 実装状況 | 状態
    header = f"| ID | タイトル | 親 | 子 | 兄弟 | カバレッジ | 実装状況 | 状態{result_col_header} |"
    sep = f"| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---{result_col_sep}|"

    lines = [f"# {title}\n", header, sep]

    for uid in sorted(target_items.keys()):
        item = target_items[uid]
        testable = _get_custom_attribute(item, "testable", True)
        scenarios = tag_map.get(uid, [])

        # リンクの抽出
        parents = [str(l) for l in item.links if str(l) in all_items_str]
        children = child_map.get(uid, [])
        siblings = sibling_map.get(uid, [])

        parents_col = "<br>".join(f"[{p}](items/{p}.md)" for p in parents) or "-"
        children_col = "<br>".join(f"[{c}](items/{c}.md)" for c in children) or "-"
        siblings_col = "<br>".join(f"[{s}](items/{s}.md)" for s in siblings) or "-"

        # カバレッジ計算
        # 子がいる場合は集約カバレッジ、いない場合は自身のカバレッジを表示
        if children:
            covered, total = _req_coverage(uid, child_map, all_items_str, tag_map)
            coverage_col = _coverage_badge(covered, total) + " [agg]"
        else:
            covered, total = _spec_coverage(uid, tag_map, item, all_items_str)
            coverage_col = _coverage_badge(covered, total)

        impl_col = _impl_status_badge(item)

        # 状態アイコン
        if is_suspect(item): gherkin_status = "⚠️ Suspect"
        elif not testable: gherkin_status = "⚪️"
        elif scenarios: gherkin_status = "🟢"
        else: gherkin_status = "🔴"

        # 行の組み立て
        row = f"| [{uid}](items/{uid}.md) | {item.header} | {parents_col} | {children_col} | {siblings_col} | {coverage_col} | {impl_col} | {gherkin_status} |"

        if has_results:
            from .test_results import spec_result_summary, result_badge
            if children:
                cp = cf = ct = 0
                for child_uid in children:
                    # 子がSPEC相当（テストを持つ可能性があるもの）であれば集計
                    p, f, t = spec_result_summary(child_uid, tag_map, test_result_map)
                    cp += p; cf += f; ct += t
                res_badge = result_badge(cp, cf, ct)
            else:
                p, f, t = spec_result_summary(uid, tag_map, test_result_map)
                res_badge = result_badge(p, f, t)
            row += f" {res_badge} |"

        lines.append(row)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# ヘルパー: 個別詳細ページ生成
# ---------------------------------------------------------------------------

def _generate_item_markdown(
    uid, item, all_items_str, child_map, sibling_map, tag_map, feature_md_map,
    test_result_map: "TestResultMap | None" = None,
):
    """個別詳細Markdownを生成（兄弟リンク・カバレッジ割合・featureリンク付き）。"""
    testable = _get_custom_attribute(item, "testable", True)
    scenarios = tag_map.get(uid, [])
    children = child_map.get(uid, [])

    content: list[str] = [f"# [{uid}] {item.header}\n"]

    # ---- Suspect警告バナー ----
    if is_suspect(item):
        content.append(
            "> ⚠️ **Suspect**: 上位要件が変更されました。このアイテムのレビューが必要です。\n"
        )

    # ---- 実装ステータス ----
    impl_badge = _impl_status_badge(item)
    content.append(f"**実装状況**: {impl_badge}\n")

    # ---- リンクセクション（親・子・兄弟）----
    link_parts: list[str] = []

    # 親関係
    if item.links:
        parents = [str(l) for l in item.links if str(l) in all_items_str]
        if parents:
            link_parts.append(f"**上位アイテム**: {', '.join(f'[{p}]({p}.md)' for p in parents)}")

    # 子関係
    if children:
        valid_children = [c for c in children if c in all_items_str]
        if valid_children:
            link_parts.append(f"**下位アイテム**: {', '.join(f'[{c}]({c}.md)' for c in valid_children)}")

    # 兄弟関係
    siblings = sibling_map.get(uid, [])
    if siblings:
        sibling_links = ", ".join(f"[{s}]({s}.md)" for s in siblings if s in all_items_str)
        if sibling_links:
            link_parts.append(f"**兄弟アイテム**: {sibling_links}")

    if link_parts:
        content.append(" / ".join(link_parts) + "\n")

    # ---- カバレッジバッジ ----
    if children:
        covered, total = _req_coverage(uid, child_map, all_items_str, tag_map)
        coverage_str = _coverage_badge(covered, total)
        content.append(f"**テストカバレッジ**: {coverage_str} （下位アイテムの集計）\n")
    
    # 自身がテスト対象、またはシナリオがある場合
    if testable or scenarios:
        covered, total = _spec_coverage(uid, tag_map, item, all_items_str)
        coverage_str = _coverage_badge(covered, total)
        content.append(f"**テスト対象**: {'Yes' if testable else 'No'}　**個別カバレッジ**: {coverage_str}\n")

    # ---- 本文 ----
    content.append(f"\n### 内容\n\n{item.text}\n")

    # ---- テスト実行結果サマリー ----
    if test_result_map is not None:
        if children:
            cp = cf = ct = 0
            for child_uid in children:
                p, f, t = spec_result_summary(child_uid, tag_map, test_result_map)
                cp += p; cf += f; ct += t
            summary = result_badge(cp, cf, ct)
            content.append(f"**テスト実行結果 (集計)**: {summary}\n")
        
        if testable or scenarios:
            p, f, t = spec_result_summary(uid, tag_map, test_result_map)
            summary = result_badge(p, f, t)
            content.append(f"**テスト実行結果 (個別)**: {summary}\n")

    # ---- 検証シナリオ ----
    if scenarios:
        content.append("### 🧪 検証シナリオ\n")
        for s in scenarios:
            file_path = s["file"]
            md_link = feature_md_map.get(file_path)
            if md_link:
                loc = f"[{file_path}:{s['line']}]({md_link})"
            else:
                loc = f"`{file_path}:{s['line']}`"
            # テスト結果がある場合はバッジを先頭に付与
            if test_result_map is not None:
                key = (Path(file_path).stem, s["name"])
                status = test_result_map.get(key)
                badge = format_status_badge(status) if status is not None else "❓ -"
                content.append(f"- {badge} **{s['name']}** — {s['keyword']} （{loc}）")
            else:
                content.append(f"- **{s['name']}** — {s['keyword']} （{loc}）")
    elif testable:
        content.append("### 🧪 検証シナリオ\n\n❌ まだ Gherkin シナリオが登録されていません。")

    return "\n".join(content)


# ---------------------------------------------------------------------------
# ヘルパー: UID → ドキュメントプレフィックス変換
# ---------------------------------------------------------------------------

def _get_uid_prefix(uid: str) -> str:
    """'REQ-001' → 'REQ'、'AUTH-REQ-001' → 'AUTH-REQ'"""
    m = re.match(r'^(.*)-\d+$', uid)
    return m.group(1) if m else uid


# ---------------------------------------------------------------------------
# ヘルパー: 階層ツリー生成
# ---------------------------------------------------------------------------

def _build_hierarchy_tree(doorstop_tree, prefix_to_file: dict) -> str:
    """
    Doorstopのドキュメント階層をMarkdownのネストリストで返す。
    ドキュメントノードを **PREFIX** として見出し行にし、
    それぞれの一覧ページへリンクする。
    """
    lines: list[str] = []

    def render_tree_node(tree_node, depth: int) -> None:
        if tree_node.document is None:
            return
        prefix = str(tree_node.document.prefix)
        indent = "    " * depth

        link = prefix_to_file.get(prefix)
        if link:
            lines.append(f"{indent}- [**{prefix}**]({link})")
        else:
            lines.append(f"{indent}- **{prefix}**")

        # 子ドキュメントを再帰的に描画
        for child_tree in sorted(tree_node.children, key=lambda t: str(t.document.prefix)):
            render_tree_node(child_tree, depth + 1)

    render_tree_node(doorstop_tree, 0)
    return "\n".join(lines) if lines else "_（ドキュメント階層が見つかりません）_"


# ---------------------------------------------------------------------------
# ヘルパー: index.md と mkdocs.yml 生成
# ---------------------------------------------------------------------------

def _generate_basic_files(
    docs_dir: Path,
    out_dir: Path,
    project_name: str,
    feature_md_map: dict,
    all_items_str: dict,
    child_map: dict,
    tag_map: dict,
    doorstop_tree,
    prefix_to_file: dict,
) -> None:
    """index.md と mkdocs.yml を生成。"""
    # index.md
    index_path = docs_dir / "index.md"
    tree_md = _build_hierarchy_tree(doorstop_tree, prefix_to_file)
    
    doc_links = "\n".join(f"- [{p}]({f})" for p, f in sorted(prefix_to_file.items()))

    index_content = (
        f"# {project_name} Specification Site\n\n"
        "Spec-Weaverによって自動生成されたドキュメントポータルです。\n\n"
        "### ドキュメント一覧\n"
        f"{doc_links}\n"
        "- [振る舞い仕様 (Gherkin Features)](features/)\n\n"
        "---\n\n"
        "## 仕様階層ツリー\n\n"
        f"{tree_md}\n"
    )
    index_path.write_text(index_content, encoding="utf-8")

    # features/ に index.md がなければ生成
    features_index = docs_dir / "features" / "index.md"
    if not features_index.exists():
        feature_links = "\n".join(
            f"- [{Path(tag_rel).name}]({Path(md_url).name})"
            for tag_rel, md_url in sorted(feature_md_map.items())
        )
        features_index.write_text(
            f"# 振る舞い仕様一覧 (Gherkin Features)\n\n{feature_links or '（まだフィーチャーファイルがありません）'}\n",
            encoding="utf-8",
        )

    # mkdocs.yml
    # 各ドキュメントをナビに追加
    docs_nav_entries = ""
    for p, f in sorted(prefix_to_file.items()):
        docs_nav_entries += f"  - {p}:\n"
        docs_nav_entries += f"      - {p}一覧: {f}\n"
        p_items = [uid for uid in all_items_str if uid.startswith(f"{p}-")]
        if not p_items:
            p_items = [uid for uid in all_items_str if uid.startswith(p)]
        for uid in sorted(p_items):
            docs_nav_entries += f"      - {uid}: items/{uid}.md\n"

    # features/ 以下の .md を動的にナビに追加
    features_nav_entries = "".join(
        f"      - {Path(md_url).name}: features/{Path(md_url).name}\n"
        for md_url in sorted(set(feature_md_map.values()))
    )

    mkdocs_config = f"""site_name: "{project_name} Spec"
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.top
    - navigation.footer
    - search.suggest
    - search.highlight
nav:
  - Home: index.md
{docs_nav_entries}
  - 振る舞い仕様 (Features):
      - features/index.md
{features_nav_entries}
markdown_extensions:
  - tables
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
"""
    (out_dir / "mkdocs.yml").write_text(mkdocs_config, encoding="utf-8")


if __name__ == "__main__":
    app()
