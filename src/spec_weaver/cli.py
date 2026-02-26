# src/spec_weaver/cli.py

import typer
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from spec_weaver.doorstop import get_item_map, _get_custom_attribute, get_specs
from spec_weaver.gherkin import get_tag_map, get_tags

app = typer.Typer(
    help="Spec-Weaver: Doorstopの仕様とGherkinのテストをシームレスに統合・監査するツール",
    add_completion=False,
)
console = Console()

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
    prefix: str = typer.Option(
        "SPEC",
        "--prefix",
        "-p",
        help="Doorstopの仕様IDのプレフィックス（例: SPEC）",
    ),
) -> None:
    """
    Doorstopに登録された仕様と、Gherkinのフィーチャーファイル間のタグの乖離を監査します。
    """
    console.print(
        Panel.fit(
            f"Doorstop Root: [bold green]{repo_root}[/bold green]\n"
            f"Gherkin Dir  : [bold green]{feature_dir}[/bold green]\n"
            f"Prefix       : [bold cyan]@{prefix}[/bold cyan]",
            title="Spec-Weaver Audit",
            border_style="blue",
        )
    )

    try:
        # 1. Doorstopから「テストすべき仕様」の正本データを取得
        with console.status("[bold cyan]Doorstopの仕様データベースを構築中...[/bold cyan]"):
            try:
                specs_in_db = get_specs(repo_root=repo_root, prefix=prefix)
            except Exception as e:
                console.print(f"[bold red]❌ Doorstopデータの読み込みに失敗しました:[/bold red] {e}")
                raise typer.Exit(code=1)

        # 2. Gherkinファイルから「実装済みのテスト」のタグを取得
        with console.status("[bold cyan]Gherkinのフィーチャーファイルを解析中...[/bold cyan]"):
            try:
                tags_in_code = get_tags(features_dir=feature_dir, prefix=prefix)
            except ValueError as e:
                console.print(f"[bold red]❌ Gherkinファイルのパースに失敗しました:[/bold red] {e}")
                raise typer.Exit(code=1)

        # 3. 集合演算による乖離の検出
        untested_specs = specs_in_db - tags_in_code
        orphaned_tags = tags_in_code - specs_in_db

        has_error = False

        # 4. 結果の評価とUI描画
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

        # 5. 最終的な終了コードの決定
        if not has_error:
            console.print(f"\n[bold green]✅ 完璧です！ {len(specs_in_db)} 件の仕様がすべてGherkinテストでカバーされています。[/bold green]")
            raise typer.Exit(code=0)
        else:
            # CI/CDパイプラインを止めるために終了コード1を返す
            console.print("\n[bold red]監査が失敗しました。仕様とテストの乖離を修正してください。[/bold red]")
            raise typer.Exit(code=1)

    except typer.Exit:
        # Typerの正常な終了処理はそのまま流す
        raise
    except Exception as e:
        # 想定外のクラッシュに対する最終防衛線
        console.print(f"\n[bold white on red] 予期せぬ致命的なエラーが発生しました: {e} [/bold white on red]")
        raise typer.Exit(code=1)

@app.command("scaffold")
def scaffold_cmd() -> None:
    """
    (開発中) Gherkinに定義されていて、まだ実装されていないテストステップの雛形を生成します。
    """
    console.print("[yellow]🚧 scaffold コマンドは現在開発中です。[/yellow]")


@app.command()
def build(
    feature_dir: Path = typer.Argument(..., exists=True, resolve_path=True),
    repo_root: Path = typer.Option(Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True),
    out_dir: Path = typer.Option(Path(".specification"), "--out-dir", "-o", resolve_path=True),
    prefix: str = typer.Option("SPEC", "--prefix", "-p"),
):
    """REQとSPECを分離し、相互リンクを含むサイトをビルドします。"""
    try:
        with console.status("[bold cyan]データの分析と結合を開始...[/bold cyan]"):
            # 1. Doorstopから全アイテムを取得し、即座にstrキーの辞書に変換 (バグ回避)
            raw_items = get_item_map(repo_root)
            all_items_str = {str(uid): item for uid, item in raw_items.items()}
            
            # 2. Gherkinからタグマップを取得
            tag_map = get_tag_map(feature_dir, prefix)

            # 3. 相互リンク（子への逆引き）の計算
            child_map = {}
            for uid, item in all_items_str.items():
                for link in item.links:
                    parent_uid = str(link)
                    child_map.setdefault(parent_uid, []).append(uid)

        # 出力ディレクトリ準備
        docs_dir = out_dir / "docs"
        items_dir = docs_dir / "items"
        items_dir.mkdir(parents=True, exist_ok=True)

        # プレフィックスによるグループ分け
        req_items = {uid: item for uid, item in all_items_str.items() if uid.startswith("REQ")}
        spec_items = {uid: item for uid, item in all_items_str.items() if uid.startswith("SPEC")}

        # 1. 個別ページ (items/*.md)
        for uid, item in all_items_str.items():
            content = _generate_item_markdown(uid, item, all_items_str, child_map, tag_map)
            (items_dir / f"{uid}.md").write_text(content, encoding="utf-8")

        # 2. 要件一覧 (requirements.md) の生成
        req_table = _generate_index_table(
            "要件一覧 (REQ)", req_items, all_items_str, child_map, tag_map, "関連仕様 (SPEC)", is_parent_view=True
        )
        (docs_dir / "requirements.md").write_text(req_table, encoding="utf-8")

        # 3. 仕様一覧 (specifications.md) の生成
        spec_table = _generate_index_table(
            "仕様一覧 (SPEC)", spec_items, all_items_str, child_map, tag_map, "関連要件 (REQ)", is_parent_view=False
        )
        (docs_dir / "specifications.md").write_text(spec_table, encoding="utf-8")

        # 4. index.md と mkdocs.yml の生成
        _generate_basic_files(docs_dir, out_dir, repo_root.name)

        console.print(f"[bold green]✅ ビルド成功！ [white]{out_dir}[/white][/bold green]")
        console.print(f"閲覧: [bold magenta]mkdocs serve -f {out_dir.relative_to(Path.cwd())}/mkdocs.yml[/bold magenta]")

    except Exception as e:
        console.print(f"[bold red]❌ ビルドエラー: {e}[/bold red]")
        raise typer.Exit(1)

def _generate_index_table(title, target_items, all_items_str, child_map, tag_map, link_col_name, is_parent_view):
    """一覧ページのテーブルMarkdownを生成。"""
    lines = [
        f"# {title}\n", 
        f"| ID | タイトル | {link_col_name} | テスト状況 | 状態 |", 
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for uid in sorted(target_items.keys()):
        item = target_items[uid]
        testable = _get_custom_attribute(item, "testable", True)
        scenarios = tag_map.get(uid, [])
        status = "🟢" if scenarios else ("🔴" if testable else "⚪️")
        
        # 相互リンクのカラム作成
        if is_parent_view:
            related_uids = child_map.get(uid, [])
        else:
            related_uids = [str(l) for l in item.links]
        
        # item_str辞書に存在するIDのみリンク化
        links = [f"[{ruid}](items/{ruid}.md)" for ruid in related_uids if ruid in all_items_str]
        related_links = "<br>".join(links) or "-"
        
        test_info = "<br>".join([f"{s['file']}:{s['line']}" for s in scenarios]) or ("-" if not testable else "未実装")
        lines.append(f"| [{uid}](items/{uid}.md) | {item.header} | {related_links} | {test_info} | {status} |")
    
    return "\n".join(lines)

def _generate_item_markdown(uid, item, all_items_str, child_map, tag_map):
    """個別詳細Markdownを生成。"""
    testable = _get_custom_attribute(item, "testable", True)
    scenarios = tag_map.get(uid, [])
    content = [f"# [{uid}] {item.header}\n"]
    
    # 上位・下位リンクの構築
    links = []
    if item.links:
        parents = ", ".join([f"[{str(l)}]({str(l)}.md)" for l in item.links if str(l) in all_items_str])
        if parents: links.append(f"**関連要件**: {parents}")
    if uid in child_map:
        children = ", ".join([f"[{c}]({c}.md)" for c in child_map[uid]])
        if children: links.append(f"**関連仕様**: {children}")
    
    if links:
        content.append(" / ".join(links) + "\n")
    
    content.append(f"**テスト対象**: {'Yes' if testable else 'No'}\n\n### 内容\n\n{item.text}\n")
    
    if scenarios:
        content.append("### 🧪 検証シナリオ")
        for s in scenarios:
            content.append(f"- **{s['name']}** (`{s['file']}:{s['line']}`)")
    
    return "\n".join(content)

def _generate_basic_files(docs_dir, out_dir, project_name):
    """index.mdとmkdocs.ymlを生成。"""
    # index.md
    if not (docs_dir / "index.md").exists():
        index_content = (
            f"# {project_name} Specification Site\n\n"
            "Spec-Weaverによって自動生成されたドキュメントポータルです。\n\n"
            "- [要件一覧 (REQ)](requirements.md)\n"
            "- [仕様一覧 (SPEC)](specifications.md)"
        )
        (docs_dir / "index.md").write_text(index_content, encoding="utf-8")

    # mkdocs.yml
    mkdocs_config = f"""site_name: "{project_name} Spec"
theme:
  name: material
  features:
    - navigation.tabs
    - navigation.top
    - search.suggest
    - search.highlight
nav:
  - Home: index.md
  - 要件一覧 (REQ): requirements.md
  - 仕様一覧 (SPEC): specifications.md

markdown_extensions:
  - tables
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
"""
    (out_dir / "mkdocs.yml").write_text(mkdocs_config, encoding="utf-8")


if __name__ == "__main__":
    app()

