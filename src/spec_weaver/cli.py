# src/spec_weaver/cli.py
# implements: QA-003, TRC-004, AUT-003, QA-004, QA-005

import typer
import shutil

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources  # type: ignore
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from spec_weaver.review import ReviewResult
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

import json
import re
import subprocess
import sys
from datetime import date as _date

from spec_weaver.doorstop import (
    get_item_map,
    get_doorstop_tree,
    _get_custom_attribute,
    _get_git_file_date,
    get_specs,
    is_suspect,
    get_all_prefixes,
    get_item_warnings,
    update_item_attribute,
    clear_doorstop_suspects,
)
from spec_weaver.review_state import compute_review_state, ReviewState
from spec_weaver.gherkin import (
    get_tag_map,
    get_tags,
    get_spec_fingerprints,
    compute_feature_file_hash,
    read_stored_fingerprint,
    write_feature_fingerprint,
    write_feature_fingerprints,
)
from spec_weaver.behave import check_behave_steps
from spec_weaver.test_results import (
    TestResultMap,
    format_status_badge,
    load_test_results,
    result_badge,
    spec_result_summary,
)
from spec_weaver.codegen import (
    generate_test_file,
    generate_environment_file,
    _step_keyword_to_prefix,
)
from spec_weaver.step_resolver import StepResolver
from spec_weaver.impl_scanner import get_ref_files, ImplScanner

# ---------------------------------------------------------------------------
# 実装ステータス定義
# ---------------------------------------------------------------------------

IMPL_STATUS_BADGE: dict[str, str] = {
    "draft": "📝 draft",
    "in-progress": "🚧 in-progress",
    "implemented": "✅ implemented",
    "deprecated": "🗑️ deprecated",
}


def _impl_status_badge(item) -> str:
    """YAMLの status フィールドを絵文字バッジ文字列に変換する。未設定は '-'。"""
    status = _get_custom_attribute(item, "status", None)
    if not status:
        return "-"
    return IMPL_STATUS_BADGE.get(str(status), f"{status}")


def _review_status_badge(item_or_id: str | Any, review_state: Optional[ReviewState] = None) -> str:
    """DoorstopのレビューステータスまたはGherkin Featureのステータスをバッジ文字列に変換する。"""
    if review_state:
        uid = str(getattr(item_or_id, "uid", item_or_id))
        return review_state.get_status(uid)
    return "✅ reviewed"


def _compute_feature_file_states(
    feature_dir: Path, repo_root: Path | None = None
) -> dict[str, dict]:
    """
    feature_dir 以下の全 .feature ファイルについて、先頭コメントのハッシュ群を読み取り、
    現在のコンテンツハッシュとともに {相対パス: {"stored": {dict}, "actual_file": hash}} を返す。
    相対パスは get_tag_map() と同じ基準（repo_root を起点、"./" プレフィックス付き）で生成する。
    """
    from spec_weaver.gherkin import read_stored_fingerprints

    if repo_root is None:
        repo_root = Path.cwd()

    states: dict[str, dict] = {}
    if not feature_dir.is_dir():
        return states
    for f in feature_dir.rglob("*.feature"):
        try:
            rel = "./" + str(f.relative_to(repo_root))
        except ValueError:
            rel = str(f)
        try:
            stored = read_stored_fingerprints(f)
            current = compute_feature_file_hash(f)
            states[rel] = {"stored": stored, "actual_file": current}
        except Exception:
            states[rel] = {"stored": {}, "actual_file": None}  # 読み取り失敗は未レビュー扱い
    return states


def _get_timestamp(item, key: str) -> str:
    """タイムスタンプを取得する。Git履歴 → YAML属性 → '-' の優先順位。"""
    # 1. Git から取得を試みる
    file_path = getattr(item, "path", None)
    if file_path:
        mode = "first" if key == "created_at" else "latest"
        git_date = _get_git_file_date(str(file_path), mode=mode)
        if git_date:
            return git_date
    # 2. YAML のカスタム属性にフォールバック
    val = _get_custom_attribute(item, key, None)
    return str(val) if val else "-"


app = typer.Typer(
    help="Spec-Weaver: Doorstopの仕様とGherkinのテストをシームレスに統合・監査するツール",
    add_completion=False,
)
console = Console()


def _is_file_dirty(file_path: Path, repo_root: Path) -> bool:
    """指定ファイルに未コミットの変更があるか Git ステータスで確認する。"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", str(file_path)],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        return bool(result.stdout.strip())
    except Exception:
        return False


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
    stale_days: int = typer.Option(
        90,
        "--stale-days",
        help="updated_at からの経過日数がこの値を超えたアイテムを stale（陳腐化の可能性）として警告する。0 で無効。",
    ),
    check_impl: bool = typer.Option(
        False,
        "--check-impl",
        help="実装ファイルリンクの検証を有効化（ref フィールドとコードアノテーションの乖離を検出）",
    ),
    extensions: Optional[str] = typer.Option(
        None,
        "--extensions",
        help="アノテーションスキャン対象の拡張子（カンマ区切り。例: py,ts）。未指定時は全テキストファイルを対象とする。",
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
        with console.status(
            "[bold cyan]Doorstopの仕様データベースを構築中...[/bold cyan]"
        ):
            try:
                specs_in_db = get_specs(repo_root=repo_root, prefix=prefix)
                all_prefixes = get_all_prefixes(repo_root=repo_root)
                # 非活性のテスト対象アイテムを別途収集（スキップ通知用）
                all_items_with_inactive = get_item_map(repo_root=repo_root, include_inactive=True)
                inactive_testable: set[str] = set()
                for uid, item in all_items_with_inactive.items():
                    if item.active:
                        continue
                    if prefix and not uid.startswith(prefix):
                        continue
                    is_testable = _get_custom_attribute(item, "testable", True)
                    if is_testable:
                        inactive_testable.add(uid)
            except Exception as e:
                console.print(
                    f"[bold red]❌ Doorstopデータの読み込みに失敗しました:[/bold red] {e}"
                )
                raise typer.Exit(code=1)

        with console.status(
            "[bold cyan]Gherkinのフィーチャーファイルを解析中...[/bold cyan]"
        ):
            try:
                # 検索対象のプレフィックスを決定
                search_prefixes = {prefix} if prefix else all_prefixes
                tags_in_code = get_tags(
                    features_dir=feature_dir, repo_root=repo_root, prefixes=search_prefixes
                )
            except ValueError as e:
                console.print(
                    f"[bold red]❌ Gherkinファイルのパースに失敗しました:[/bold red] {e}"
                )
                raise typer.Exit(code=1)

        with console.status("[bold cyan]Suspect状態の仕様を確認中...[/bold cyan]"):
            try:
                raw_items = get_item_map(repo_root=repo_root)
                # Gherkin フィンガープリントを取得
                try:
                    search_prefixes = {prefix} if prefix else all_prefixes
                    gherkin_fingerprints = get_spec_fingerprints(
                        feature_dir, repo_root, search_prefixes
                    )
                except Exception:
                    gherkin_fingerprints = {}

                try:
                    tag_map = get_tag_map(feature_dir, repo_root, search_prefixes)
                except Exception:
                    tag_map = {}

                feature_file_states = _compute_feature_file_states(feature_dir, repo_root)
                review_state = compute_review_state(
                    raw_items, gherkin_fingerprints, tag_map, feature_file_states
                )

                suspect_specs: dict[str, set[str]] = {}
                unreviewed_specs: set[str] = set()

                for uid, item in raw_items.items():
                    if prefix and not uid.startswith(prefix):
                        continue

                    status = review_state.get_status(uid)
                    if uid in review_state.unreviewed_nodes:
                        unreviewed_specs.add(uid)
                    if "suspect" in status:
                        suspect_specs[uid] = review_state.suspect_causes.get(uid, set())

                # feature ファイルの suspect/unreviewed を収集
                feature_to_specs: dict[str, set[str]] = {}
                for tag, scenarios in tag_map.items():
                    if prefix and not str(tag).startswith(prefix):
                        continue
                    for s in scenarios:
                        fpath = s["file"]
                        feature_to_specs.setdefault(fpath, set()).add(str(tag))

                suspect_features: dict[str, set[str]] = {}
                unreviewed_features: set[str] = set()

                for fpath in feature_to_specs:
                    fstatus = review_state.get_status(fpath)
                    if fpath in review_state.unreviewed_nodes:
                        unreviewed_features.add(fpath)
                    if "suspect" in fstatus:
                        suspect_features[fpath] = review_state.suspect_causes.get(fpath, set())

            except Exception as e:
                console.print(
                    f"[bold red]❌ Suspect状態の確認に失敗しました:[/bold red] {e}"
                )
                suspect_specs = {}
                unreviewed_specs = set()
                feature_to_specs = {}
                suspect_features = {}
                unreviewed_features = set()

        untested_specs = specs_in_db - tags_in_code
        orphaned_tags = tags_in_code - specs_in_db
        has_error = False

        if inactive_testable:
            console.print(
                "\n[dim]⛔ 非活性のためスキップした仕様 (Inactive Testable Specs):[/dim]"
            )
            table = Table(show_header=True, header_style="dim")
            table.add_column("Spec ID", style="dim")
            table.add_column("理由", style="dim")
            for spec in sorted(inactive_testable):
                table.add_row(spec, "active: false")
            console.print(table)

        if untested_specs:
            has_error = True
            console.print(
                "\n[bold red]❌ テストが実装されていない仕様 (Untested Specs):[/bold red]"
            )
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Missing Spec ID", style="dim")
            for spec in sorted(untested_specs):
                table.add_row(spec)
            console.print(table)

        if orphaned_tags:
            has_error = True
            console.print(
                "\n[bold yellow]⚠️ 仕様書に存在しない孤児タグ (Orphaned Tags):[/bold yellow]"
            )
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Orphaned Tag", style="dim")
            for tag in sorted(orphaned_tags):
                table.add_row(f"@{tag}")
            console.print(table)

        if suspect_specs or suspect_features:
            has_error = True
            console.print(
                "\n[bold yellow]⚠️ Suspect — 関連アイテムが変更されています:[/bold yellow]"
            )
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Spec ID", style="dim")
            table.add_column("原因アイテム", style="dim")
            table.add_column("アクション", style="dim")
            for spec in sorted(suspect_specs):
                # 原因アイテム（原因となった ID やファイル名）を表示
                causes_list = []
                for c in suspect_specs[spec]:
                    if c == "Doorstop native suspect link":
                        # 親アイテムを特定
                        parents = review_state.parents.get(spec, set())
                        causes_list.extend(sorted(list(parents)))
                    else:
                        causes_list.append(c)
                causes = ", ".join(causes_list) or "不明"
                
                status = review_state.get_status(spec)
                if "suspect-with-unreviewed" in status:
                    action = "[bold red]要レビュー[/bold red] (doorstop review / spec-weaver review)"
                else:
                    # QA-001: Suspect の SPEC のアクションには spec-weaver clear <SPEC_ID> を表示
                    action = f"spec-weaver clear {spec}"
                table.add_row(spec, causes, action)
            for fpath in sorted(suspect_features):
                fname = Path(fpath).name
                causes = ", ".join(sorted(suspect_features[fpath])) or "不明"
                table.add_row(fname, causes, "feature ファイルを確認し、必要に応じてシナリオを更新")
            console.print(table)

        if unreviewed_specs or unreviewed_features:
            has_error = True
            console.print(
                "\n[bold yellow]📋 Unreviewed Changes — 未レビューの変更があります:[/bold yellow]"
            )
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Spec ID", style="dim")
            table.add_column("アクション", style="dim")
            for spec in sorted(unreviewed_specs):
                table.add_row(spec, "doorstop review / または spec-weaver review")
            for fpath in sorted(unreviewed_features):
                fname = Path(fpath).name
                try:
                    display_path = str(Path(fpath).relative_to(Path.cwd()))
                except ValueError:
                    display_path = fpath
                try:
                    display_fdir = str(feature_dir.relative_to(Path.cwd()))
                except ValueError:
                    display_fdir = str(feature_dir)
                action = f"spec-weaver review {display_path} -f {display_fdir}"
                table.add_row(fname, action)
            console.print(table)

        # stale チェック（終了コードには影響しない）
        if stale_days > 0:
            today = _date.today()
            stale_items: list[tuple[str, str, int]] = []
            for uid, item in raw_items.items():
                if prefix and not uid.startswith(prefix):
                    continue
                item_status = _get_custom_attribute(item, "status", None)
                if str(item_status or "") == "deprecated":
                    continue
                # Git 履歴 → YAML フォールバック
                file_path = getattr(item, "path", None)
                updated_at_val = None
                if file_path:
                    updated_at_val = _get_git_file_date(str(file_path), mode="latest")
                if not updated_at_val:
                    updated_at_val = _get_custom_attribute(item, "updated_at", None)
                if not updated_at_val:
                    continue
                try:
                    updated_at = _date.fromisoformat(str(updated_at_val))
                    delta = (today - updated_at).days
                    if delta > stale_days:
                        stale_items.append((str(uid), str(updated_at_val), delta))
                except ValueError:
                    pass

            if stale_items:
                console.print(
                    f"\n[bold yellow]⏰ Stale Items（{stale_days}日以上未更新）:[/bold yellow]"
                )
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("ID", style="bold cyan", no_wrap=True)
                table.add_column("タイトル")
                table.add_column("最終更新日", style="dim")
                table.add_column("経過日数", style="yellow")
                for uid, updated_at_str, delta in sorted(stale_items):
                    item = raw_items.get(uid)
                    title = (item.header or "").strip() if item else ""
                    table.add_row(uid, title, updated_at_str, f"{delta}日")
                console.print(table)

        # --check-impl: 実装ファイルリンク検証（QA-003）
        if check_impl:
            has_error = _run_impl_link_check(
                raw_items=raw_items,
                repo_root=repo_root,
                extensions=_parse_extensions(extensions),
                prefix=prefix,
                has_error=has_error,
            )

        # Behave ステップの整合性チェック
        with console.status("[bold cyan]Behave ステップの整合性を確認中...[/bold cyan]"):
            unused_defs, undefined_steps = check_behave_steps(feature_dir)

        if unused_defs:
            console.print(
                "\n[bold yellow]⚠️ 未使用のステップ定義 (Unused Step Definitions):[/bold yellow]"
            )
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Definition", style="dim")
            for d in sorted(unused_defs):
                table.add_row(d)
            console.print(table)

        if undefined_steps:
            has_error = True
            console.print(
                "\n[bold red]❌ 未定義のステップ (Undefined Steps):[/bold red]"
            )
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Undefined Step", style="dim")
            for s in sorted(undefined_steps):
                table.add_row(s)
            console.print(table)

        if not has_error:
            console.print(
                f"\n[bold green]✅ 完璧です！ {len(specs_in_db)} 件の仕様がすべてGherkinテストでカバーされています。[/bold green]"
            )
            raise typer.Exit(code=0)
        else:
            console.print(
                "\n[bold red]監査が失敗しました。仕様とテストの乖離を修正してください。[/bold red]"
            )
            raise typer.Exit(code=1)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(
            f"\n[bold white on red] 予期せぬ致命的なエラーが発生しました: {e} [/bold white on red]"
        )
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# 実装ファイルリンク検証ヘルパー（QA-003）
# ---------------------------------------------------------------------------


def _parse_extensions(extensions: Optional[str]) -> list[str] | None:
    """カンマ区切り拡張子文字列をリストに変換する。None または空の場合は None を返す。"""
    if not extensions:
        return None
    return [e.strip() for e in extensions.split(",") if e.strip()]


def _run_impl_link_check(
    raw_items: dict,
    repo_root: Path,
    extensions: list[str] | None,
    prefix: Optional[str],
    has_error: bool,
) -> bool:
    """実装ファイルリンクの検証を実行し、問題があれば出力する。has_error を更新して返す。"""
    console.print(
        "\n[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]"
    )
    console.print("[bold blue]🔗 実装ファイルリンクの検証[/bold blue]")
    console.print(
        "[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]"
    )

    with console.status("[bold cyan]実装ファイルをスキャン中...[/bold cyan]"):
        scanner = ImplScanner()
        annotation_map = scanner.scan(repo_root, extensions=extensions)

    # ref フィールドから {spec_id: [file_path, ...]} を構築
    ref_map: dict[str, list[str]] = {}
    for uid, item in raw_items.items():
        if prefix and not str(uid).startswith(prefix):
            continue
        refs = get_ref_files(item)
        if refs:
            ref_map[str(uid)] = refs

    # 全 spec_id の集合（ref または annotation のどちらかに存在するもの）
    all_spec_ids = set(ref_map.keys()) | set(annotation_map.keys())
    if prefix:
        all_spec_ids = {sid for sid in all_spec_ids if sid.startswith(prefix)}

    broken_refs: list[tuple[str, str]] = []  # (spec_id, path) — ファイル不在
    ref_only: list[tuple[str, str]] = []  # (spec_id, path) — ref のみ
    annotation_only: list[tuple[str, str]] = []  # (spec_id, path) — annotation のみ

    for spec_id in sorted(all_spec_ids):
        refs = set(ref_map.get(spec_id, []))
        annotations = annotation_map.get(spec_id, set())

        for path_str in sorted(refs):
            full_path = repo_root / path_str
            if not full_path.exists():
                broken_refs.append((spec_id, path_str))
            elif path_str not in annotations:
                ref_only.append((spec_id, path_str))

        for path_str in sorted(annotations - refs):
            annotation_only.append((spec_id, path_str))

    if broken_refs:
        has_error = True
        console.print("\n[bold red]❌ 存在しないファイルへの ref:[/bold red]")
        for spec_id, path_str in broken_refs:
            console.print(
                f"   [cyan]{spec_id}[/cyan] → [dim]{path_str}[/dim] [red](not found)[/red]"
            )

    if ref_only:
        console.print("\n[bold yellow]⚠️  ref のみ（アノテーションなし）:[/bold yellow]")
        for spec_id, path_str in ref_only:
            console.print(f"   [cyan]{spec_id}[/cyan] → [dim]{path_str}[/dim]")

    if annotation_only:
        console.print("\n[bold yellow]⚠️  アノテーションのみ（ref なし）:[/bold yellow]")
        for spec_id, path_str in annotation_only:
            console.print(f"   [cyan]{spec_id}[/cyan] ← [dim]{path_str}[/dim]")

    if not broken_refs and not ref_only and not annotation_only:
        console.print("\n[bold green]✅ リンク検証 完了 — 乖離なし[/bold green]")
    else:
        console.print(
            "\n[bold yellow]⚠️  リンク検証 完了 — 上記の乖離を確認してください[/bold yellow]"
        )

    return has_error


# ---------------------------------------------------------------------------
# scaffold コマンド
# ---------------------------------------------------------------------------


@app.command("scaffold")
def scaffold_cmd(
    feature_dir: Path = typer.Argument(
        ...,
        exists=True,
        resolve_path=True,
        help=".feature ファイルが格納されたディレクトリ",
    ),
    out_dir: Path = typer.Option(
        Path("specification/features/steps"),
        "--out-dir",
        "-o",
        resolve_path=True,
        help="テストコード出力先ディレクトリ",
    ),
    overwrite: bool = typer.Option(
        False,
        "--overwrite",
        help="既存ファイルを全上書きする",
    ),
    repo_root: Path = typer.Option(
        Path.cwd(),
        "--repo-root",
        "-r",
        resolve_path=True,
        help="Git dirty チェック用リポジトリルート（デフォルト: cwd）",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Git 未コミット変更の確認プロンプトをスキップして強制マージする",
    ),
) -> None:
    """Gherkin .feature ファイルから behave テストコードの雛形を生成・差分マージします。"""
    try:
        feature_files = sorted(feature_dir.rglob("*.feature"))
        if not feature_files:
            console.print(
                "[yellow]⚠️ .feature ファイルが見つかりませんでした。[/yellow]"
            )
            raise typer.Exit(0)

        generated = 0
        skipped = 0
        errors = 0

        def _display_path(p: Path) -> str:
            try:
                return str(p.relative_to(Path.cwd()))
            except ValueError:
                return str(p)

        # environment.py の生成
        try:
            res = generate_environment_file(feature_dir, overwrite=overwrite)
            if res:
                out_path, status, _ = res
                console.print(
                    f"  [green]✅ 環境設定作成[/green]: {_display_path(out_path)}"
                )
                generated += 1
            elif (feature_dir / "environment.py").exists():
                console.print(
                    f"  [dim]⏭️ スキップ[/dim]: {_display_path(feature_dir / 'environment.py')} (存在済み)"
                )
                skipped += 1
        except Exception as e:
            console.print(f"  [red]❌ 環境設定エラー[/red]: environment.py: {e}")
            errors += 1

        for fpath in feature_files:
            try:
                out_file = out_dir / f"step_{fpath.stem}.py"

                result = generate_test_file(
                    fpath, out_dir, feature_dir, overwrite=overwrite
                )

                if result is None:
                    console.print(
                        f"  [dim]⏭️ スキップ[/dim]: {_display_path(out_file)} (差分なし)"
                    )
                    skipped += 1
                else:
                    out_path, status, diff_text = result
                    if status == "created":
                        console.print(
                            f"  [green]✅ 新規作成[/green]: {_display_path(out_path)}"
                        )
                    else:
                        console.print(
                            f"\n  [blue]🔄 差分更新[/blue]: {_display_path(out_path)}"
                        )
                        console.print(
                            Syntax(diff_text, "diff", theme="monokai", padding=(0, 2))
                        )
                        console.print()
                    generated += 1

                    # Git dirty チェック: 既存ファイルに未コミット変更があれば確認
                    if out_file.exists() and not force and not overwrite:
                        if _is_file_dirty(out_file, repo_root):
                            console.print(
                                f"\n[bold yellow]⚠️  {_display_path(out_file)} "
                                f"に未コミットの変更があります。[/bold yellow]"
                            )
                            if not Confirm.ask("差分マージを続行しますか？"):
                                console.print(
                                    f"  [dim]⏭️ スキップ[/dim]: {_display_path(out_file)} (キャンセル)"
                                )
                                skipped += 1
                                continue

            except Exception as e:
                console.print(f"  [red]❌ エラー[/red]: {fpath.name}: {e}")
                errors += 1

        console.print()
        console.print(
            f"[bold green]生成/更新: {generated}[/bold green]  "
            f"[dim]スキップ: {skipped}[/dim]  "
            + (f"[bold red]エラー: {errors}[/bold red]" if errors else "")
        )

        if errors:
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ scaffold エラー: {e}[/bold red]")
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# review コマンド
# ---------------------------------------------------------------------------

@app.command("review")
def review_cmd(
    target_path: str = typer.Argument(
        ..., help="レビュー対象 ( .feature ファイルのパス, Doorstop アイテム ID, または .yml ファイルのパス )"
    ),
    feature_dir: Path = typer.Option(
        Path("specification/features"),
        "--feature-dir",
        "-f",
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
        help="Doorstop of the project root",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
) -> None:
    """
    指定したアイテムをレビュー済み状態にします。

    - .feature ファイルの場合: フィンガープリントを計算し書き込みます（QA-004）。
    - Doorstop アイテムの場合: doorstop review コマンドを呼び出します。
    """
    try:
        target = Path(target_path)

        # 1. .feature ファイルの場合（既存のフィンガープリント計算）
        if target.exists() and target.suffix == ".feature":
            with console.status(f"[bold cyan]{target_path} のハッシュを計算中...[/bold cyan]"):
                fp = compute_feature_file_hash(target)
                
                # 関連する Doorstop アイテムのスタンプを取得
                all_prefixes = get_all_prefixes(repo_root)
                tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
                raw_items = get_item_map(repo_root)
                
                linked_tags = set()
                try:
                    rel_target = str(target.relative_to(feature_dir.parent))
                except ValueError:
                    rel_target = str(target)
                    
                for tag, scenarios in tag_map.items():
                    for s in scenarios:
                        if Path(s["file"]).resolve() == target.resolve():
                            linked_tags.add(tag)
                            break
                            
                item_fps = {}
                for tag in linked_tags:
                    if tag in raw_items:
                        item = raw_items[tag]
                        item_fps[tag] = item.stamp() if hasattr(item, "stamp") else ""

            write_feature_fingerprints(target, fp, item_fps)

            console.print(f"[bold green]✅ フィンガープリントを書き込みました: {target_path}[/bold green]")
            console.print(f"[dim]ハッシュ: {fp}[/dim]")
            if item_fps:
                console.print(f"[dim]関連アイテム: {', '.join(item_fps.keys())}[/dim]")
            console.print()

        # 2. Doorstop アイテム（.yml ファイル）の場合
        elif target.exists() and target.suffix == ".yml":
            item_id = target.stem
            console.print(f"[bold cyan]Doorstop アイテム {item_id} をレビュー中...[/bold cyan]")

            # doorstop review -i <item_id> -f -j <repo_root>
            cmd = ["doorstop", "review", "-i", item_id, "-f", "-j", str(repo_root)]
            subprocess.run(cmd, check=True)

            console.print(f"[bold green]✅ アイテム {item_id} をレビューしました[/bold green]")
            console.print()

        # 3. ファイルパスではないが、アイテム ID の可能性がある場合
        else:
            # Doorstop のアイテムマップから ID を探す
            item_map = get_item_map(repo_root)
            if target_path in item_map:
                item_id = target_path
                console.print(f"[bold cyan]Doorstop アイテム {item_id} をレビュー中...[/bold cyan]")

                cmd = ["doorstop", "review", "-i", item_id, "-f", "-j", str(repo_root)]
                subprocess.run(cmd, check=True)

                console.print(f"[bold green]✅ アイテム {item_id} をレビューしました[/bold green]")
                console.print()
            else:
                if not target.exists():
                    console.print(f"[bold red]❌ ターゲットが見つかりません: {target_path}[/bold red]")
                else:
                    console.print(f"[bold red]❌ 未対応のファイル形式です: {target_path}[/bold red]")
                raise typer.Exit(1)

        # レビュー後に監査を実行
        audit_cmd(
            feature_dir=feature_dir,
            repo_root=repo_root,
            prefix=None,
            stale_days=90,
            check_impl=False,
            extensions=None,
        )

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ review エラー: {e}[/bold red]")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# clear コマンド
# ---------------------------------------------------------------------------


@app.command("clear")
def clear_cmd(
    item_id: str = typer.Argument(
        ..., help="test_fingerprint を更新するアイテムID、または .feature ファイルパス"
    ),
    feature_dir: Path = typer.Option(
        Path("specification/features"),
        "--feature-dir",
        "-f",
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
        help="Doorstopのプロジェクトルート",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
) -> None:
    """
    指定した仕様アイテムの Doorstop YAML の test_fingerprint を現在の Gherkin ハッシュで更新し、
    Suspect 状態を解除します（QA-005）。

    .feature ファイルが指定された場合は、ファイル内の全アイテムの test_fingerprint を一括更新します。
    """
    try:
        item_path = Path(item_id)

        # .feature ファイルが指定された場合
        if item_path.suffix == ".feature" and item_path.exists():
            all_prefixes = get_all_prefixes(repo_root)
            with console.status(f"[bold cyan]{item_id} に含まれる仕様IDを特定中...[/bold cyan]"):
                tags_in_file = get_tags(item_path, repo_root, all_prefixes)

            if not tags_in_file:
                console.print(
                    f"[bold yellow]⚠️ {item_id} に紐づく仕様IDが見つかりませんでした。[/bold yellow]"
                )
                raise typer.Exit(1)

            with console.status("[bold cyan]フィンガープリントを計算中...[/bold cyan]"):
                all_fingerprints = get_spec_fingerprints(feature_dir, repo_root, all_prefixes)

            tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
            feature_file_states = _compute_feature_file_states(feature_dir, repo_root)
            raw_items = get_item_map(repo_root)
            review_state = compute_review_state(
                {str(uid): it for uid, it in raw_items.items()},
                all_fingerprints,
                tag_map,
                feature_file_states,
            )

            updated_count = 0
            for tag in sorted(tags_in_file):
                status = review_state.get_status(tag)
                if tag in review_state.unreviewed_nodes:
                    console.print(
                        f"⚠️ [bold yellow]{tag}[/bold yellow] は未レビューです。スキップします。"
                    )
                    continue
                
                if "suspect-with-unreviewed" in status:
                    console.print(
                        f"⚠️ [bold yellow]{tag}[/bold yellow] は上位アイテムが未レビューです。スキップします。"
                    )
                    continue

                fps = all_fingerprints.get(tag)
                if fps:
                    with console.status(f"[bold cyan]{tag} の YAML を更新中...[/bold cyan]"):
                        # 新しい gherkin_fingerprints 属性をセット
                        update_item_attribute(repo_root, tag, "gherkin_fingerprints", fps)
                        # 旧属性を削除
                        try:
                            delete_item_attribute(repo_root, tag, "test_fingerprint")
                        except Exception:
                            pass

                    console.print(
                        f"✅ [bold]{tag}[/bold] の gherkin_fingerprints を更新しました。"
                    )
                    updated_count += 1
                # Doorstop ネイティブ suspect リンクも解除
                try:
                    if clear_doorstop_suspects(repo_root, tag):
                        console.print(
                            f"✅ [bold]{tag}[/bold] の Doorstop suspect リンクを解除しました。"
                        )
                except Exception:
                    pass

            if updated_count > 0:
                console.print(
                    f"\n[bold green]✨ 合計 {updated_count} 個のアイテムの gherkin_fingerprints を更新しました。[/bold green]"
                )
            return

        # アイテムID が指定された場合
        with console.status(f"[bold cyan]{item_id} の Gherkin フィンガープリントを計算中...[/bold cyan]"):
            all_prefixes = get_all_prefixes(repo_root)
            raw_items = get_item_map(repo_root)
            item = raw_items.get(item_id)
            if not item:
                console.print(f"[bold red]❌ アイテム {item_id} が見つかりません。[/bold red]")
                raise typer.Exit(1)

            # QA-001: suspect-with-unreviewed の状態では clear を実行できない
            # レビュー状態を計算
            gherkin_fingerprints = get_spec_fingerprints(feature_dir, repo_root, all_prefixes)
            tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
            feature_file_states = _compute_feature_file_states(feature_dir, repo_root)
            review_state = compute_review_state(
                {str(uid): it for uid, it in raw_items.items()},
                gherkin_fingerprints,
                tag_map,
                feature_file_states,
            )

            status = review_state.get_status(item_id)
            if item_id in review_state.unreviewed_nodes:
                console.print(
                    f"[bold red]❌ {item_id} は未レビューです。レビュー（doorstop review {item_id} / spec-weaver review {item_id}）してから clear を実行してください。[/bold red]"
                )
                raise typer.Exit(1)
            
            if "suspect-with-unreviewed" in status:
                console.print(
                    f"[bold red]❌ {item_id} は上位アイテムが未レビューです。上位アイテムを先にレビューしてから clear を実行してください。[/bold red]"
                )
                raise typer.Exit(1)

            actual_fps = gherkin_fingerprints.get(item_id)

        if actual_fps:
            with console.status(f"[bold cyan]{item_id} の YAML を更新中...[/bold cyan]"):
                update_item_attribute(repo_root, item_id, "gherkin_fingerprints", actual_fps)
                try:
                    delete_item_attribute(repo_root, item_id, "test_fingerprint")
                except Exception:
                    pass
            console.print(f"[bold green]✅ {item_id} の gherkin_fingerprints を更新しました。[/bold green]")
        else:
            # Gherkin シナリオがなくても Doorstop suspect リンクの解除は試みる
            pass

        # Doorstop ネイティブ suspect リンクも解除
        doorstop_cleared = False
        try:
            doorstop_cleared = clear_doorstop_suspects(repo_root, item_id)
        except Exception:
            pass
        if doorstop_cleared:
            console.print(f"[bold green]✅ {item_id} の Doorstop suspect リンクを解除しました。[/bold green]")
        elif not actual_fps:
            console.print(
                f"[bold red]❌ {item_id} に紐づく Gherkin シナリオが見つかりません。[/bold red]"
            )
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ clear エラー: {e}[/bold red]")
        raise typer.Exit(1)


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
    feature_dir: Path = typer.Option(
        Path("specification/features"),
        "--feature-dir",
        "-f",
        help="Gherkinの .feature ファイルが格納されているディレクトリのパス",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    filter_status: Optional[str] = typer.Option(
        None,
        "--filter",
        "-F",
        help="表示するステータスで絞り込む（draft / in-progress / implemented / deprecated）",
    ),
) -> None:
    """
    REQ・SPECの実装ステータス（status フィールド）を一覧表示します。
    """
    try:
        with console.status("[bold cyan]Doorstopデータを読み込み中...[/bold cyan]"):
            raw_items = get_item_map(repo_root=repo_root, include_inactive=True)
            all_items_str = {str(uid): item for uid, item in raw_items.items()}
            all_prefixes = get_all_prefixes(repo_root)

        with console.status(
            "[bold cyan]Gherkinのフィンガープリントを計算中...[/bold cyan]"
        ):
            try:
                gherkin_fingerprints = get_spec_fingerprints(feature_dir, repo_root, all_prefixes)
            except Exception:
                gherkin_fingerprints = {}

        try:
            tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
        except Exception:
            tag_map = {}

        feature_file_states = _compute_feature_file_states(feature_dir, repo_root)
        review_state = compute_review_state(
            all_items_str, gherkin_fingerprints, tag_map, feature_file_states
        )

        # プレフィックスごとにアイテムをグループ化
        grouped_items: dict[str, dict] = {p: {} for p in all_prefixes}
        for uid, item in all_items_str.items():
            prefix = _get_uid_prefix(uid)
            if prefix in grouped_items:
                grouped_items[prefix][uid] = item
            else:
                grouped_items.setdefault("OTHER", {})[uid] = item

        def _print_status_table(title: str, items: dict) -> int:
            if not items:
                return 0
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("ID", style="bold cyan", no_wrap=True)
            table.add_column("タイトル")
            table.add_column("活性", no_wrap=True)
            table.add_column("実装ステータス")
            table.add_column("レビューステータス")
            table.add_column("最終更新日", no_wrap=True)
            shown = 0
            for uid in sorted(items.keys()):
                item = items[uid]
                raw_status = _get_custom_attribute(item, "status", None)
                if filter_status and str(raw_status or "") != filter_status:
                    continue
                active_badge = "✅" if item.active else "[dim]⛔ 非活性[/dim]"
                badge = _impl_status_badge(item)
                review = _review_status_badge(uid, review_state=review_state)
                updated = _get_timestamp(item, "updated_at")
                title_text = (item.header or "").strip()
                if not item.active:
                    table.add_row(f"[dim]{uid}[/dim]", f"[dim]{title_text}[/dim]", active_badge, f"[dim]{badge}[/dim]", f"[dim]{review}[/dim]", f"[dim]{updated}[/dim]")
                else:
                    table.add_row(uid, title_text, active_badge, badge, review, updated)
                shown += 1
            if shown > 0:
                console.print(table)
            return shown

        total = 0
        # 優先して表示するプレフィックスの順序
        for prefix in ["REQ", "SPEC", "CORE", "QA", "VIS", "TRC", "AUT", "DESIGN", "PLAN", "ADR", "RESEARCH"]:
            if prefix in grouped_items:
                total += _print_status_table(
                    f"ドキュメント: {prefix}", grouped_items.pop(prefix)
                )

        # 残りのプレフィックスを表示
        for prefix, items in sorted(grouped_items.items()):
            total += _print_status_table(f"ドキュメント: {prefix}", items)

        # Gherkin Featureファイルのステータス表示
        try:
            tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
            feature_files = {}
            for uid, scenarios in tag_map.items():
                for sc in scenarios:
                    file_path = sc["file"]
                    if file_path not in feature_files:
                        feature_files[file_path] = {"scenarios": 0, "specs": set()}
                    feature_files[file_path]["scenarios"] += 1
                    feature_files[file_path]["specs"].add(uid)

            if (
                feature_files and not filter_status
            ):  # filter_status がある場合はfeatureはステータスを持たないので除外する
                table = Table(
                    title="振る舞い仕様 (Gherkin Features)",
                    show_header=True,
                    header_style="bold green",
                )
                table.add_column("ファイルパス", style="bold cyan")
                table.add_column("シナリオ数", justify="right")
                table.add_column("レビューステータス")
                table.add_column("関連仕様ID")
                for fpath in sorted(feature_files.keys()):
                    info = feature_files[fpath]
                    specs = sorted(info["specs"])
                    
                    file_status = review_state.get_status(fpath)
                    specs_str = ", ".join(specs)
                    table.add_row(fpath, str(info["scenarios"]), file_status, specs_str)
                console.print(table)
        except Exception:
            pass

        # Behave ステップの整合性チェック (status では概要のみ)
        try:
            unused_defs, undefined_steps = check_behave_steps(feature_dir)
            if unused_defs or undefined_steps:
                console.print("\n[bold magenta]Step Definitions Info:[/bold magenta]")
                if unused_defs:
                    console.print(f"  [yellow]⚠️  未使用のステップ定義: {len(unused_defs)} 件[/yellow]")
                if undefined_steps:
                    console.print(f"  [red]❌ 未定義のステップ: {len(undefined_steps)} 件[/red]")
                console.print("  [dim]詳細は `spec-weaver audit` で確認できます。[/dim]")
        except Exception:
            pass

        if total == 0:
            if filter_status:
                console.print(
                    f"[yellow]ステータス '{filter_status}' に一致するアイテムが見つかりませんでした。[/yellow]"
                )
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
    repo_root: Path = typer.Option(
        Path.cwd(), "--repo-root", "-r", exists=True, resolve_path=True
    ),
    out_dir: Path = typer.Option(
        Path(".specification"), "--out-dir", "-o", resolve_path=True
    ),
    prefix: str = typer.Option(
        "SPEC",
        "--prefix",
        "-p",
        help="Gherkinタグとして主に扱うデフォルトプレフィックス",
    ),
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
        _run_build(feature_dir, repo_root, out_dir, test_results_file, prefix)
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]❌ ビルドエラー: {e}[/bold red]")
        import traceback

        traceback.print_exc()
        raise typer.Exit(1)


def _run_build(
    feature_dir: Path,
    repo_root: Path,
    out_dir: Path,
    test_results_file: Path | None = None,
    prefix: str = "SPEC",
) -> None:
    """build コマンドのコアロジック。build / ci の両方から呼ばれる。"""
    with console.status("[bold cyan]データの分析と結合を開始...[/bold cyan]"):
        # 1. Doorstopから全アイテムと全プレフィックス取得（非活性アイテムも含む）
        raw_items = get_item_map(repo_root, include_inactive=True)
        all_items_str = {str(uid): item for uid, item in raw_items.items()}
        doorstop_tree = get_doorstop_tree(repo_root)
        all_prefixes = {str(doc.prefix) for doc in doorstop_tree}

        # 2. Gherkinタグマップ取得 (全プレフィックスを対象にする)
        tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
        gherkin_fingerprints = get_spec_fingerprints(feature_dir, repo_root, all_prefixes)
        feature_file_states = _compute_feature_file_states(feature_dir, repo_root)
        review_state = compute_review_state(
            all_items_str, gherkin_fingerprints, tag_map, feature_file_states
        )

        # feature_path -> 関連アイテムUID一覧（バックリンク用）
        _backlink_sets: dict[str, set[str]] = {}
        for _uid, _scenarios in tag_map.items():
            for _s in _scenarios:
                _backlink_sets.setdefault(_s["file"], set()).add(_uid)
        feature_backlink_map: dict[str, list[str]] = {
            k: sorted(v) for k, v in _backlink_sets.items()
        }

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
                console.print(
                    f"[bold red]❌ テスト結果の読み込みに失敗しました: {e}[/bold red]"
                )
                raise typer.Exit(1)

    # 出力ディレクトリ準備
    docs_dir = out_dir / "docs"
    items_dir = docs_dir / "items"
    features_md_dir = docs_dir / "features"
    items_dir.mkdir(parents=True, exist_ok=True)
    features_md_dir.mkdir(parents=True, exist_ok=True)

    # 6. Gherkin .feature → Markdown 変換
    step_resolver = StepResolver()
    # feature_dir と同じ階層、またはその下の steps/ を探す
    # behave は feature_dir/steps をデフォルトで探す
    step_resolver.load_steps(feature_dir / "steps")

    feature_md_map: dict[str, str] = {}
    for feature_file in feature_dir.rglob("*.feature"):
        try:
            rel = feature_file.relative_to(feature_dir)
            md_rel = rel.with_suffix(".md")
            out_path = features_md_dir / md_rel
            out_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                tag_rel = "./" + str(feature_file.relative_to(repo_root))
            except ValueError:
                tag_rel = str(feature_file)
            backlinks = feature_backlink_map.get(tag_rel, [])
            md_content = _feature_to_markdown(
                feature_file,
                backlinks=backlinks,
                step_resolver=step_resolver,
                review_state=review_state,
                all_items_str=all_items_str,
                feature_md_map=feature_md_map,
                node_id=tag_rel,
                test_result_map=test_result_map,
            )
            out_path.write_text(md_content, encoding="utf-8")
            feature_md_map[tag_rel] = f"../features/{md_rel.as_posix()}"
        except Exception as e:
            console.print(
                f"[yellow]⚠️ feature変換スキップ: {feature_file}: {e}[/yellow]"
            )

    # 7. 個別アイテムページ (items/*.md)
    for uid, item in all_items_str.items():
        content = _generate_item_markdown(
            uid,
            item,
            all_items_str,
            child_map,
            sibling_map,
            tag_map,
            feature_md_map,
            test_result_map=test_result_map,
            review_state=review_state,
        )
        (items_dir / f"{uid}.md").write_text(content, encoding="utf-8")

    # 8. 各ドキュメントの一覧ページ生成
    prefix_to_file = {}
    for doc in doorstop_tree:
        p = str(doc.prefix)
        doc_items = {
            uid: item for uid, item in all_items_str.items() if uid.startswith(p + "-")
        }
        # プレフィックスが完全に一致する場合（ハイフンなし）も考慮が必要な場合があるが、Doorstopの標準はハイフン区切り
        if not doc_items:
            doc_items = {
                uid: item for uid, item in all_items_str.items() if uid.startswith(p)
            }

        filename = f"{p.lower()}.md"
        table = _generate_index_table(
            f"ドキュメント: {p}",
            doc_items,
            all_items_str,
            child_map,
            sibling_map,
            tag_map,
            test_result_map=test_result_map,
            review_state=review_state,
        )
        (docs_dir / filename).write_text(table, encoding="utf-8")
        prefix_to_file[p] = filename

    # 9. index.md と mkdocs.yml
    _generate_basic_files(
        docs_dir,
        out_dir,
        repo_root.name,
        feature_md_map,
        all_items_str,
        child_map,
        tag_map,
        doorstop_tree,
        prefix_to_file,
        review_state,
    )

    console.print(f"[bold green]✅ ビルド成功！ [white]{out_dir}[/white][/bold green]")
    try:
        display_path = out_dir.relative_to(Path.cwd())
    except ValueError:
        display_path = out_dir
    console.print(
        f"閲覧: [bold magenta]mkdocs serve -f {display_path}/mkdocs.yml[/bold magenta]"
    )


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


def _spec_coverage(
    uid: str, tag_map: dict, item, all_items_str: dict
) -> tuple[int, int]:
    """
    SPEC単体のカバレッジを返す。
    Returns: (covered_scenario_count, 1) ただしnot testableなら(0, 0)
    """
    testable = _get_custom_attribute(item, "testable", True)
    if not testable:
        return (0, 0)
    scenarios = tag_map.get(uid, [])
    return (1 if scenarios else 0, 1)


def _scenario_count_badge(uid: str, tag_map: dict, item) -> str:
    """SPEC単体のシナリオ数を直接表示するバッジ。testable=falseなら '-'、0なら🔴、それ以上は🟢。"""
    testable = _get_custom_attribute(item, "testable", True)
    if not testable:
        return "-"
    count = len(tag_map.get(uid, []))
    if count == 0:
        return "🔴 0"
    return f"🟢 {count}"


# ---------------------------------------------------------------------------
# ヘルパー: Gherkin → Markdown 変換
# ---------------------------------------------------------------------------


def _feature_to_markdown(
    feature_file: Path,
    backlinks: list[str] | None = None,
    step_resolver: Optional[StepResolver] = None,
    review_state: Optional[ReviewState] = None,
    all_items_str: dict | None = None,
    feature_md_map: dict | None = None,
    node_id: str | None = None,
    test_result_map: Optional[TestResultMap] = None,
) -> str:
    """
    .featureファイルをGherkinパーサーで解析し、ブラウザで読みやすいMarkdownに変換する。
    backlinks: このfeatureを参照しているアイテムUID一覧（例: ["SPEC-003", "REQ-001"]）
    """
    from gherkin.parser import Parser
    from gherkin.token_scanner import TokenScanner

    if all_items_str is None:
        all_items_str = {}
    if feature_md_map is None:
        feature_md_map = {}

    with open(feature_file, "r", encoding="utf-8") as f:
        raw = f.read()

    parser = Parser()
    ast = parser.parse(TokenScanner(raw))
    feature_node = ast.get("feature", {})

    feature_name = feature_node.get("name", feature_file.stem)
    feature_desc = (feature_node.get("description") or "").strip()
    feature_tags = [t["name"] for t in feature_node.get("tags", [])]

    lines: list[str] = [f"# Feature: {feature_name}\n"]

    # ---- 警告バナー ----
    if review_state and node_id:
        status = review_state.get_status(node_id)
        if "unreviewed" in status:
            lines.append(
                "> 📋 **Unreviewed Changes**: このフィーチャーファイル自体に未レビューの変更があります。レビュー後に `review` コマンドで更新してください。\n"
            )
        if "suspect" in status:
            causes = review_state.suspect_causes.get(node_id, set())
            cause_links = []
            for c in causes:
                if c in all_items_str:
                    cause_links.append(f"[{c}](../items/{c}.md)")
                else:
                    # Feature file
                    md_link = feature_md_map.get(c)
                    if md_link:
                        # From features/ to features/
                        name = Path(c).name
                        cause_links.append(f"[{name}]({Path(md_link).name})")
                    else:
                        cause_links.append(f"`{c}`")
            
            causes_str = ", ".join(sorted(cause_links)) if causes else "不明"
            lines.append(
                f"> ⚠️ **Suspect**: 関連する仕様や他のテストが変更されました。影響範囲のレビューが必要です。\n> **原因 (Unreviewed)**: {causes_str}\n"
            )

    if feature_tags:
        lines.append("**タグ**: " + " ".join(f"`{t}`" for t in feature_tags) + "\n")

    if backlinks:
        links_str = " / ".join(f"[{uid}](../items/{uid}.md)" for uid in backlinks)
        lines.append(f"**関連アイテム**: {links_str}\n")

    if feature_desc:
        lines.append(f"{feature_desc}\n")

    def _resolve_step_prefixes(steps: list[dict]) -> list[tuple[str, str, str]]:
        """And / But キーワードを直前の Given/When/Then に解決して返す。
        Returns: (resolved_keyword, raw_keyword, text)
        """
        resolved: list[tuple[str, str, str]] = []
        current_prefix = "given"
        for step in steps:
            keyword = step.get("keyword", "").strip()
            text = step.get("text", "").strip()
            prefix = _step_keyword_to_prefix(keyword)
            if prefix:
                current_prefix = prefix
            resolved.append((current_prefix, keyword, text))
        return resolved

    for child in feature_node.get("children", []):
        # Background
        if "background" in child:
            bg = child["background"]
            lines.append("---\n## Background\n")
            resolved_steps = _resolve_step_prefixes(bg.get("steps", []))
            for res_kw, raw_kw, text in resolved_steps:
                lines.append(f"- **{raw_kw}** {text}")

            if step_resolver:
                step_codes = []
                for res_kw, raw_kw, text in resolved_steps:
                    step_def = step_resolver.resolve_step(res_kw, text)
                    if step_def:
                        step_codes.append((raw_kw, text, step_def.source))
                if step_codes:
                    lines.append(
                        "\n<details><summary><b>Step Definitions (Source Code)</b></summary>\n"
                    )
                    for rkw, txt, src in step_codes:
                        lines.append(f"#### {rkw} {txt}\n")
                        lines.append(f"```python\n{src}\n```\n")
                    lines.append("</details>\n")
            lines.append("")

        # Scenario / Scenario Outline
        if "scenario" in child:
            sc = child["scenario"]
            sc_name = sc.get("name", "")
            sc_keyword = (sc.get("keyword") or "Scenario").strip()
            sc_tags = [t["name"] for t in sc.get("tags", [])]
            sc_desc = (sc.get("description") or "").strip()
            sc_line = sc.get("location", {}).get("line", 0)

            tag_str = " ".join(f"`{t}`" for t in sc_tags) if sc_tags else ""
            # Add explicit anchor for auto-focusing from item pages
            lines.append(f"---\n## {sc_keyword}: {sc_name} {{: #line-{sc_line} }}\n")
            if tag_str:
                lines.append(f"**タグ**: {tag_str}\n")
            if sc_desc:
                lines.append(f"{sc_desc}\n")

            resolved_steps = _resolve_step_prefixes(sc.get("steps", []))
            for res_kw, raw_kw, text in resolved_steps:
                lines.append(f"- **{raw_kw}** {text}")

            if step_resolver:
                step_codes = []
                for res_kw, raw_kw, text in resolved_steps:
                    step_def = step_resolver.resolve_step(res_kw, text)
                    if step_def:
                        step_codes.append((raw_kw, text, step_def.source))
                if step_codes:
                    lines.append(
                        "\n<details><summary><b>Step Definitions (Source Code)</b></summary>\n"
                    )
                    # テスト失敗時のログがあれば表示 (REQ-005)
                    if test_result_map:
                        res = test_result_map.get((feature_file.stem, sc_name.strip()))
                        if res and res.get("error"):
                            lines.append("#### 📋 Execution Log (Failure)\n")
                            lines.append(f"```text\n{res['error']}\n```\n")

                    for rkw, txt, src in step_codes:
                        lines.append(f"#### {rkw} {txt}\n")
                        lines.append(f"```python\n{src}\n```\n")
                    lines.append("</details>\n")

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
    title,
    target_items,
    all_items_str,
    child_map,
    sibling_map,
    tag_map,
    test_result_map: "TestResultMap | None" = None,
    review_state: Optional[ReviewState] = None,
):
    """一覧ページのテーブルMarkdownを生成。"""
    has_results = test_result_map is not None

    # ID | タイトル | 活性 | 親 | 子 | 兄弟 | Gherkinカバレッジ | レビューステータス | 実装状況 | 作成日 | 更新日
    header = "| ID | タイトル | 活性 | 親 | 子 | 兄弟 | Gherkinカバレッジ | レビューステータス | 実装状況 | 作成日 | 更新日 |"
    sep = "| :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"

    lines = [f"# {title}\n", header, sep]

    for uid in sorted(target_items.keys(), key=lambda u: (target_items[u].level, u)):
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
        # -t あり: テスト結果バッジをカバレッジ列に表示
        # -t なし: シナリオ数バッジ
        if has_results:
            p, f, e, s, t = spec_result_summary(uid, tag_map, test_result_map)
            coverage_col = result_badge(p, f, e, s, t)
        else:
            coverage_col = _scenario_count_badge(uid, tag_map, item)

        review_status = _review_status_badge(uid, review_state=review_state)
        impl_col = _impl_status_badge(item)
        created_col = _get_timestamp(item, "created_at")
        updated_col = _get_timestamp(item, "updated_at")
        active_col = "✅" if item.active else "⛔"

        # 行の組み立て
        row = f"| [{uid}](items/{uid}.md) | {item.header} | {active_col} | {parents_col} | {children_col} | {siblings_col} | {coverage_col} | {review_status} | {impl_col} | {created_col} | {updated_col}"

        # 状態に応じた行ハイライト (attr_list 拡張用)
        # QA-001: Unreviewedは赤 (.unreviewed-row), Suspectは紫 (.suspect-row)
        # 非活性は専用クラス (.inactive-row)
        if not item.active:
            row += " {: .inactive-row } |"
        elif "unreviewed" in review_status:
            row += " {: .unreviewed-row } |"
        elif "suspect" in review_status:
            row += " {: .suspect-row } |"
        else:
            row += " |"

        lines.append(row)

    # 属性リストは空行を挟んで配置（attr_list拡張が解釈できない場合でもJS側でヘッダー判定する）
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# ヘルパー: 個別詳細ページ生成
# ---------------------------------------------------------------------------


def _generate_item_markdown(
    uid,
    item,
    all_items_str,
    child_map,
    sibling_map,
    tag_map,
    feature_md_map,
    test_result_map: "TestResultMap | None" = None,
    review_state: Optional[ReviewState] = None,
):
    """個別詳細Markdownを生成（兄弟リンク・カバレッジ割合・featureリンク付き）。"""
    testable = _get_custom_attribute(item, "testable", True)
    scenarios = tag_map.get(uid, [])
    children = child_map.get(uid, [])

    content: list[str] = [f"# [{uid}] {item.header}\n"]

    # ---- 非活性バナー ----
    if not item.active:
        migrated_to = _get_custom_attribute(item, "migrated_to", None)
        if migrated_to:
            content.append(
                f"> 🚫 **非活性 (active: false)**: このアイテムは非活性です。[{migrated_to}]({migrated_to}.md) に移行されました。\n"
            )
        else:
            content.append(
                "> 🚫 **非活性 (active: false)**: このアイテムは非活性です。\n"
            )

    # ---- 警告バナー ----
    if review_state:
        status = review_state.get_status(uid)
        if "unreviewed" in status:
            content.append(
                "> 📋 **Unreviewed Changes**: このアイテム自体または関連するテストに未レビューの変更があります。\n"
            )
        if "suspect" in status:
            causes = review_state.suspect_causes.get(uid, set())
            cause_links = []
            for c in causes:
                if c in all_items_str:
                    cause_links.append(f"[{c}]({c}.md)")
                else:
                    # Feature file
                    # We can try to make a link if it's in feature_md_map
                    md_link = feature_md_map.get(c)
                    if md_link:
                        cause_links.append(f"[{Path(c).name}]({md_link})")
                    else:
                        cause_links.append(f"`{c}`")
                        
            causes_str = ", ".join(sorted(cause_links)) if causes else "不明"
            content.append(
                f"> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。\n> **原因 (Unreviewed)**: {causes_str}\n"
            )

    # ---- 実装ステータス ----
    impl_badge = _impl_status_badge(item)
    content.append(f"**実装状況**: {impl_badge}\n")

    # ---- タイムスタンプ ----
    created_at = _get_timestamp(item, "created_at")
    updated_at = _get_timestamp(item, "updated_at")
    content.append(f"**作成日**: {created_at}　|　**更新日**: {updated_at}\n")

    # ---- リンクセクション（親・子・兄弟）----
    link_parts: list[str] = []

    # 親関係
    if item.links:
        parents = [str(l) for l in item.links if str(l) in all_items_str]
        if parents:
            link_parts.append(
                f"**上位アイテム**: {', '.join(f'[{p}]({p}.md)' for p in parents)}"
            )

    # 子関係
    if children:
        valid_children = [c for c in children if c in all_items_str]
        if valid_children:
            link_parts.append(
                f"**下位アイテム**: {', '.join(f'[{c}]({c}.md)' for c in valid_children)}"
            )

    # 兄弟関係
    siblings = sibling_map.get(uid, [])
    if siblings:
        sibling_links = ", ".join(
            f"[{s}]({s}.md)" for s in siblings if s in all_items_str
        )
        if sibling_links:
            link_parts.append(f"**兄弟アイテム**: {sibling_links}")

    if link_parts:
        content.append(" / ".join(link_parts) + "\n")

    # ---- カバレッジバッジ ----
    content.append(
        f"**テスト対象**: {'Yes' if testable else 'No'}"
    )
    if test_result_map is not None:
        p, f, e, s, t = spec_result_summary(uid, tag_map, test_result_map)
        summary = result_badge(p, f, e, s, t)
        content.append(
            f" / **テストカバレッジ**: {summary}\n"
        )

    # ---- 本文 ----
    content.append(f"---\n\n{item.text}\n")

    # ---- テスト実行結果サマリー ----
    if test_result_map is not None:
        if testable or scenarios:
            p, f, e, s, t = spec_result_summary(uid, tag_map, test_result_map)
            summary = result_badge(p, f, e, s, t)
            content.append(f"**テスト実行結果**: {summary}\n")

    # ---- 検証シナリオ ----
    if scenarios:
        content.append("### 🧪 検証シナリオ\n")
        for s in scenarios:
            file_path = s["file"]
            md_link = feature_md_map.get(file_path)
            if md_link:
                # Append line anchor for auto-focus
                loc = f"[{file_path}:{s['line']}]({md_link}#line-{s['line']})"
            else:
                loc = f"`{file_path}:{s['line']}`"
            # テスト結果がある場合はバッジを先頭に付与
            if test_result_map is not None:
                key = (Path(file_path).stem, s["name"].strip())
                res = test_result_map.get(key)
                status = res["status"] if res else None
                badge = format_status_badge(status) if status is not None else "-"
                content.append(f"- {badge} **{s['name']}** — {s['keyword']} （{loc}）")
                # エラーメッセージがあれば表示
                if res and res.get("error"):
                    content.append(f"\n```text\n{res['error']}\n```\n")
            else:
                content.append(f"- **{s['name']}** — {s['keyword']} （{loc}）")
    elif testable:
        content.append(
            "### 🧪 検証シナリオ\n\n❌ Gherkin シナリオが登録されていません。"
        )

    return "\n".join(content)


# ---------------------------------------------------------------------------
# ヘルパー: UID → ドキュメントプレフィックス変換
# ---------------------------------------------------------------------------


def _get_uid_prefix(uid: str) -> str:
    """'REQ-001' → 'REQ'、'AUTH-REQ-001' → 'AUTH-REQ'"""
    m = re.match(r"^(.*)-\d+$", uid)
    return m.group(1) if m else uid


# ---------------------------------------------------------------------------
# trace コマンド用ヘルパー
# ---------------------------------------------------------------------------


def _collect_all_ancestors(
    uid: str, all_items: dict, visited: set | None = None
) -> set[str]:
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


def _format_trace_node(
    uid: str, item, is_origin: bool = False, review_state: Optional[ReviewState] = None
) -> str:
    """Rich マークアップ付きのノードラベル文字列を返す。"""
    header = (item.header or "").strip() if item else ""
    impl_badge = _impl_status_badge(item) if item else "-"
    review_badge = _review_status_badge(item or uid, review_state)
    badge = f"{impl_badge} / {review_badge}"
    if is_origin:
        return f"[bold yellow]★[/bold yellow] [bold]{uid}[/bold] {header} {badge}"
    return f"[bold cyan]{uid}[/bold cyan] {header} {badge}"


def _add_impl_files_to_node(node, uid: str, impl_map: dict, repo_root: Path) -> None:
    """実装ファイルノードを Rich Tree ノードに追加する（TRC-004）。

    ref 由来は 📁、アノテーションのみは 📝、不在ファイルは ❌ で表示。
    """
    files = impl_map.get(uid)
    if not files:
        return
    for path_str in sorted(files):
        full_path = repo_root / path_str
        if not full_path.exists():
            node.add(f"❌ {path_str} [red](not found)[/red]")
        else:
            node.add(f"📁 {path_str}")


def _add_descendants_to_rich_node(
    node,
    uid: str,
    all_items: dict,
    child_map: dict,
    tag_map: dict,
    visited: set,
    impl_map: dict | None = None,
    repo_root: Path | None = None,
    review_state: Optional[ReviewState] = None,
) -> None:
    """子アイテム・Gherkinシナリオを再帰的にRich Treeノードへ追加する。"""
    # Gherkinシナリオをファイル別にグループ化して追加
    scenarios = tag_map.get(uid, [])
    if scenarios:
        file_scenarios: dict[str, list] = {}
        for sc in scenarios:
            fname = Path(sc["file"]).name
            file_scenarios.setdefault(fname, []).append(sc)
        for fname, scs in sorted(file_scenarios.items()):
            # get_tag_map で使っているキー（相対パス）を使ってレビューステータスを取得
            # シナリオの１つ目からファイルパスを復元する
            rel_path = scs[0]["file"]
            review_badge = _review_status_badge(rel_path, review_state)
            feature_node = node.add(f"🥒 {fname} {review_badge}")
            for sc in scs:
                feature_node.add(f"Scenario: {sc['name']}")

    # 実装ファイルノードを追加（--show-impl 時）
    if impl_map is not None and repo_root is not None:
        _add_impl_files_to_node(node, uid, impl_map, repo_root)

    # 子アイテムを再帰的に追加
    for child_uid in sorted(child_map.get(uid, [])):
        if child_uid in visited:
            continue
        child_item = all_items.get(child_uid)
        label = _format_trace_node(child_uid, child_item, review_state=review_state)
        child_node = node.add(label)
        new_visited = set(visited)
        new_visited.add(child_uid)
        _add_descendants_to_rich_node(
            child_node,
            child_uid,
            all_items,
            child_map,
            tag_map,
            new_visited,
            impl_map=impl_map,
            repo_root=repo_root,
            review_state=review_state,
        )


def _add_focused_path(
    node,
    current_uid: str,
    origin_uid: str,
    on_path: set[str],
    all_items: dict,
    child_map: dict,
    tag_map: dict,
    visited: set,
    expand_at_origin: bool = True,
    impl_map: dict | None = None,
    repo_root: Path | None = None,
    review_state: Optional[ReviewState] = None,
) -> None:
    """祖先からoriginまでのパスを辿り、originで全子孫を展開する（expand_at_origin=True 時）。"""
    if current_uid == origin_uid:
        if expand_at_origin:
            _add_descendants_to_rich_node(
                node,
                current_uid,
                all_items,
                child_map,
                tag_map,
                set(visited),
                impl_map=impl_map,
                repo_root=repo_root,
                review_state=review_state,
            )
        return

    # on_path に含まれる子のみを辿る
    for child_uid in sorted(child_map.get(current_uid, [])):
        if child_uid not in on_path or child_uid in visited:
            continue
        child_item = all_items.get(child_uid)
        is_origin = child_uid == origin_uid
        label = _format_trace_node(
            child_uid, child_item, is_origin=is_origin, review_state=review_state
        )
        child_node = node.add(label)
        new_visited = set(visited)
        new_visited.add(child_uid)
        _add_focused_path(
            child_node,
            child_uid,
            origin_uid,
            on_path,
            all_items,
            child_map,
            tag_map,
            new_visited,
            expand_at_origin,
            impl_map=impl_map,
            repo_root=repo_root,
            review_state=review_state,
        )


def _build_trace_rich_tree(
    origin_uid: str,
    all_items: dict,
    child_map: dict,
    tag_map: dict,
    direction: str,
    impl_map: dict | None = None,
    repo_root: Path | None = None,
    review_state: Optional[ReviewState] = None,
):
    """トレースツリーを構築して返す。複数ルート祖先がある場合はリストで返す。"""
    origin_item = all_items.get(origin_uid)

    if direction == "down":
        label = _format_trace_node(
            origin_uid, origin_item, is_origin=True, review_state=review_state
        )
        tree = Tree(label)
        _add_descendants_to_rich_node(
            tree,
            origin_uid,
            all_items,
            child_map,
            tag_map,
            {origin_uid},
            impl_map=impl_map,
            repo_root=repo_root,
            review_state=review_state,
        )
        return tree

    # up / both: 祖先を収集しルートから辿る
    ancestors = _collect_all_ancestors(origin_uid, all_items)
    if not ancestors:
        # 祖先なし: origin 自身がルート
        label = _format_trace_node(
            origin_uid, origin_item, is_origin=True, review_state=review_state
        )
        tree = Tree(label)
        if direction == "both":
            _add_descendants_to_rich_node(
                tree,
                origin_uid,
                all_items,
                child_map,
                tag_map,
                {origin_uid},
                impl_map=impl_map,
                repo_root=repo_root,
                review_state=review_state,
            )
        return tree

    on_path = ancestors | {origin_uid}
    expand_at_origin = direction == "both"

    # ルート祖先を特定: 祖先集合の中でさらに祖先を持たないもの
    root_ancestors: set[str] = set()
    for anc_uid in ancestors:
        anc_item = all_items.get(anc_uid)
        if anc_item is None:
            root_ancestors.add(anc_uid)
            continue
        parents_in_ancestors = [
            str(link) for link in anc_item.links if str(link) in ancestors
        ]
        if not parents_in_ancestors:
            root_ancestors.add(anc_uid)

    trees = []
    for root_uid in sorted(root_ancestors):
        root_item = all_items.get(root_uid)
        label = _format_trace_node(root_uid, root_item, review_state=review_state)
        tree = Tree(label)
        _add_focused_path(
            tree,
            root_uid,
            origin_uid,
            on_path,
            all_items,
            child_map,
            tag_map,
            {root_uid},
            expand_at_origin,
            impl_map=impl_map,
            repo_root=repo_root,
            review_state=review_state,
        )
        trees.append(tree)

    return trees if len(trees) > 1 else trees[0]


def _trace_flat_output(
    origin_uid: str,
    all_items_str: dict,
    child_map: dict,
    direction: str,
    review_state: Optional[ReviewState] = None,
) -> None:
    """flat形式でトレース結果をテーブル表示する。"""
    all_relevant: set[str] = set()
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

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("種別", style="bold")
    table.add_column("ID", style="bold cyan")
    table.add_column("タイトル")
    table.add_column("実装ステータス")
    table.add_column("レビューステータス")
    for uid in sorted(all_relevant):
        item = all_items_str.get(uid)
        prefix = _get_uid_prefix(uid)
        header = (item.header or "").strip() if item else ""
        impl_badge = _impl_status_badge(item) if item else "-"
        review_badge = _review_status_badge(item or uid, review_state)
        table.add_row(prefix, uid, header, impl_badge, review_badge)
    console.print(table)


# ---------------------------------------------------------------------------
# trace コマンド
# ---------------------------------------------------------------------------


@app.command("trace")
def trace_cmd(
    item_id: str = typer.Argument(
        ..., help="探索起点ID (例: REQ-001, SPEC-003, audit.feature)"
    ),
    feature_dir: Optional[Path] = typer.Option(
        None,
        "--feature-dir",
        "-f",
        help="Gherkin .featureファイルディレクトリ (direction=down/both で使用)",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    repo_root: Path = typer.Option(
        Path.cwd(),
        "--repo-root",
        "-r",
        help="Doorstopリポジトリのルート",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    direction: str = typer.Option(
        "both",
        "--direction",
        "-d",
        help="探索方向: up / down / both (デフォルト: both)",
    ),
    output_format: str = typer.Option(
        "tree",
        "--format",
        help="出力形式: tree (デフォルト) / flat",
    ),
    show_impl: bool = typer.Option(
        False,
        "--show-impl",
        help="実装ファイル（ref フィールド・コードアノテーション）をツリーに表示する",
    ),
    extensions: Optional[str] = typer.Option(
        None,
        "--extensions",
        help="アノテーションスキャン対象の拡張子（カンマ区切り。例: py,ts）。未指定時は全テキストファイルを対象とする。",
    ),
) -> None:
    """
    指定したアイテム（REQ/SPEC/Gherkin feature）を起点として、上位・下位のトレーサビリティツリーを表示します。
    """
    try:
        with console.status("[bold cyan]データを読み込み中...[/bold cyan]"):
            raw_items = get_item_map(repo_root)
            all_items_str = {str(uid): item for uid, item in raw_items.items()}

            # child_map 構築（parent_uid → [child_uid, ...]）
            child_map: dict[str, list[str]] = {}
            for uid, item in all_items_str.items():
                for link in item.links:
                    parent_uid = str(link)
                    child_map.setdefault(parent_uid, []).append(uid)

            # tag_map 構築
            tag_map: dict = {}
            if feature_dir is not None:
                all_prefixes = get_all_prefixes(repo_root)
                tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)

            # review_state 構築
            review_state: Optional[ReviewState] = None
            try:
                all_prefixes = get_all_prefixes(repo_root)
                gherkin_fingerprints = {}
                feature_file_states = None
                if feature_dir:
                    gherkin_fingerprints = get_spec_fingerprints(
                        feature_dir, repo_root, all_prefixes
                    )
                    feature_file_states = _compute_feature_file_states(feature_dir, repo_root)

                review_state = compute_review_state(
                    raw_items, gherkin_fingerprints, tag_map, feature_file_states
                )
            except Exception:
                pass

            # impl_map 構築（--show-impl 時のみ）
            impl_map: dict[str, set[str]] = {}
            if show_impl:
                ext_list = _parse_extensions(extensions)
                scanner = ImplScanner()
                annotation_map = scanner.scan(repo_root, extensions=ext_list)
                # ref フィールドと annotation を統合: {spec_id: set of paths}
                for uid, item in all_items_str.items():
                    refs = set(get_ref_files(item))
                    annotations = annotation_map.get(uid, set())
                    merged = refs | annotations
                    if merged:
                        impl_map[uid] = merged

        # 起点アイテムの解決
        origin_uid: str
        if item_id.endswith(".feature"):
            if feature_dir is None:
                console.print(
                    "[bold red]❌ .featureファイルを起点にするには --feature-dir を指定してください。[/bold red]"
                )
                raise typer.Exit(1)
            # tag_map からファイル名が一致するSPEC IDを探す
            found_uid = None
            for spec_uid, scenarios in tag_map.items():
                for sc in scenarios:
                    if Path(sc["file"]).name == item_id:
                        found_uid = spec_uid
                        break
                if found_uid:
                    break
            if found_uid is None:
                console.print(
                    f"[bold red]❌ Error: Item '{item_id}' not found[/bold red]"
                )
                raise typer.Exit(1)
            origin_uid = found_uid
        else:
            if item_id not in all_items_str:
                console.print(
                    f"[bold red]❌ Error: Item '{item_id}' not found[/bold red]"
                )
                raise typer.Exit(1)
            origin_uid = item_id

        # 出力
        if output_format == "flat":
            _trace_flat_output(
                origin_uid, all_items_str, child_map, direction, review_state=review_state
            )
        else:
            result = _build_trace_rich_tree(
                origin_uid,
                all_items_str,
                child_map,
                tag_map,
                direction,
                impl_map=impl_map if show_impl else None,
                repo_root=repo_root if show_impl else None,
                review_state=review_state,
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
        for child_tree in sorted(
            tree_node.children, key=lambda t: str(t.document.prefix)
        ):
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
    review_state: Optional[ReviewState] = None,
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
    
    feature_files = {}
    for tag, scenarios in tag_map.items():
        for s in scenarios:
            file_path = s["file"]
            if file_path not in feature_files:
                feature_files[file_path] = {"scenarios": 0, "specs": set()}
            feature_files[file_path]["scenarios"] += 1
            feature_files[file_path]["specs"].add(tag)

    table_lines = [
        "| ファイル | シナリオ数 | レビューステータス | 関連仕様ID |",
        "| :--- | :---: | :--- | :--- |"
    ]
    
    for tag_rel, md_url in sorted(feature_md_map.items()):
        info = feature_files.get(tag_rel, {"scenarios": 0, "specs": set()})
        scenarios_count = info["scenarios"]
        specs = sorted(info["specs"])
        
        # Use review_state if passed, else default to reviewed
        if review_state:
            file_status = review_state.get_status(tag_rel)
        else:
            file_status = "✅ reviewed"

        specs_str = "<br>".join(f"[{s}](../items/{s}.md)" for s in specs) or "-"
        
        row = f"| [{Path(tag_rel).name}]({Path(md_url).name}) | {scenarios_count} | {file_status} | {specs_str}"
        if "unreviewed" in file_status:
            row += " {: .unreviewed-row } |"
        elif "suspect" in file_status:
            row += " {: .suspect-row } |"
        else:
            row += " |"
            
        table_lines.append(row)

    feature_table = "\n".join(table_lines)
    
    features_index.write_text(
        f"# 振る舞い仕様一覧 (Gherkin Features)\n\n{feature_table}\n",
        encoding="utf-8",
    )

    # JS / CSS の配置 (テンプレートからコピー)
    js_dir = docs_dir / "javascripts"
    css_dir = docs_dir / "stylesheets"
    js_dir.mkdir(parents=True, exist_ok=True)
    css_dir.mkdir(parents=True, exist_ok=True)

    # テンプレートファイルを探索してコピー
    # importlib.resources.files は Python 3.9+ で利用可能
    template_root = resources.files("spec_weaver") / "templates"

    js_src = template_root / "javascripts" / "custom-table-filter.js"
    css_src = template_root / "stylesheets" / "extra.css"

    if js_src.exists():
        (js_dir / "custom-table-filter.js").write_text(
            js_src.read_text(encoding="utf-8"), encoding="utf-8"
        )

    if css_src.exists():
        (css_dir / "extra.css").write_text(
            css_src.read_text(encoding="utf-8"), encoding="utf-8"
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
        for uid in sorted(p_items, key=lambda u: (all_items_str[u].level, u)):
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
extra_javascript:
    - javascripts/custom-table-filter.js
extra_css:
    - stylesheets/extra.css
nav:
  - Home: index.md
{docs_nav_entries}
  - 振る舞い仕様 (Features):
      - features/index.md
{features_nav_entries}
markdown_extensions:
  - tables
  - attr_list
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
"""
    (out_dir / "mkdocs.yml").write_text(mkdocs_config, encoding="utf-8")


# ---------------------------------------------------------------------------
# semantic-review コマンド (AUT-003)
# ---------------------------------------------------------------------------

@app.command("semantic-review")
def semantic_review_cmd(
    item: Optional[str] = typer.Option(
        None,
        "--item",
        "-i",
        help="レビュー対象の仕様アイテムID（例: SPEC-003）。--all と排他。",
    ),
    all_items: bool = typer.Option(
        False,
        "--all",
        help="全仕様アイテムを並列レビューする。--item と排他。",
    ),
    feature_dir: Path = typer.Option(
        Path("specification/features"),
        "--feature-dir",
        "-f",
        help=".feature ファイル検索ディレクトリ",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
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
    output: str = typer.Option(
        "text",
        "--output",
        "-o",
        help="出力形式: text（Markdown） / json",
    ),
    min_severity: str = typer.Option(
        "low",
        "--min-severity",
        help="表示する finding の最低重大度: low / medium / high",
    ),
    fail_on: Optional[str] = typer.Option(
        None,
        "--fail-on",
        help="指定重大度以上の finding があれば終了コード 1 を返す: low / medium / high",
    ),
    max_workers: int = typer.Option(
        3,
        "--max-workers",
        help="--all 時の並列 Claude プロセス数",
    ),
    timeout: int = typer.Option(
        300,
        "--timeout",
        help="Claude プロセスの最大待機秒数（デフォルト: 300秒）",
    ),
) -> None:
    """
    仕様・Gherkin・実装コードの意味的整合性を Claude でレビューします。
    """
    from spec_weaver.review import (
        ReviewReport,
        ReviewResult,
        filter_findings,
        run_all_reviews,
        run_claude_review,
        severity_gte,
    )

    # --item / --all の排他チェック
    if item and all_items:
        console.print("[bold red]❌ --item と --all は同時に指定できません。[/bold red]")
        raise typer.Exit(code=2)
    if not item and not all_items:
        console.print("[bold red]❌ --item または --all のどちらかを指定してください。[/bold red]")
        raise typer.Exit(code=2)

    # feature_dir が存在しなければ cwd 相対で解決
    if not feature_dir.exists():
        candidate = repo_root / feature_dir
        if candidate.exists():
            feature_dir = candidate

    # --------------- 単一アイテム ---------------
    if item:
        try:
            if output != "json":
                with console.status(f"[bold cyan]🔍 {item} をレビュー中...[/bold cyan]"):
                    result = run_claude_review(item, feature_dir, repo_root, timeout=timeout)
            else:
                result = run_claude_review(item, feature_dir, repo_root, timeout=timeout)
        except FileNotFoundError as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
            raise typer.Exit(code=1)
        except ValueError as e:
            console.print(f"[bold red]❌ {e}[/bold red]")
            raise typer.Exit(code=1)

        visible = filter_findings(result.findings, min_severity)
        result.findings = visible

        if output == "json":
            print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        else:
            _print_review_result(console, result)

        if fail_on and any(severity_gte(f.severity, fail_on) for f in visible):
            raise typer.Exit(code=1)
        raise typer.Exit(code=0)

    # --------------- 全アイテム並列 ---------------
    try:
        if output != "json":
            from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

            from spec_weaver.doorstop import get_item_map as _get_item_map
            total = len(_get_item_map(repo_root))

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                MofNCompleteColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task_id = progress.add_task("[cyan]セマンティックレビュー実行中...[/cyan]", total=total)

                def _on_complete(iid: str, _result: "ReviewResult") -> None:
                    progress.advance(task_id)
                    progress.update(task_id, description=f"[cyan]完了: {iid}[/cyan]")

                report = run_all_reviews(
                    feature_dir, repo_root, max_workers=max_workers,
                    on_complete=_on_complete, timeout=timeout,
                )
        else:
            report = run_all_reviews(
                feature_dir, repo_root, max_workers=max_workers, timeout=timeout,
            )
    except FileNotFoundError as e:
        console.print(f"[bold red]❌ {e}[/bold red]")
        raise typer.Exit(code=1)

    # min_severity フィルタを適用
    for r in report.items:
        r.findings = filter_findings(r.findings, min_severity)

    if output == "json":
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        for r in report.items:
            _print_review_result(console, r)

    if fail_on:
        for r in report.items:
            if any(severity_gte(f.severity, fail_on) for f in r.findings):
                raise typer.Exit(code=1)
    raise typer.Exit(code=0)


def _print_review_result(console: Console, result: ReviewResult) -> None:
    """ReviewResult を Rich で Markdown 的に出力する。"""
    from rich.markdown import Markdown

    header = f"## {result.item_id} — {result.item_title}"
    console.print(Markdown(header))

    if not result.findings:
        console.print("[green]✅ finding なし[/green]")
    else:
        for f in result.findings:
            sev_color = {"high": "red", "medium": "yellow", "low": "cyan"}.get(f.severity, "white")
            console.print(
                f"  [{sev_color}][{f.severity.upper()}][/{sev_color}] "
                f"[bold]{f.title}[/bold] ({f.kind})"
            )
            if f.detail:
                console.print(f"    {f.detail}")
            if f.location:
                console.print(f"    → {f.location}")

    if result.summary:
        console.print(f"\n[dim]{result.summary}[/dim]\n")


if __name__ == "__main__":
    app()
