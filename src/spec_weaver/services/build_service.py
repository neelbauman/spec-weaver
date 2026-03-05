import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources  # type: ignore

from spec_weaver.adapters.codegen import _step_keyword_to_prefix
from spec_weaver.adapters.doorstop import (
    _build_child_index,
    _get_custom_attribute,
    get_all_prefixes,
    get_doorstop_tree,
    get_item_map,
)
from spec_weaver.adapters.gherkin import get_spec_fingerprints, get_tag_map
from spec_weaver.adapters.test_results import (
    TestResultMap,
    format_status_badge,
    load_test_results,
    result_badge,
    spec_result_summary,
)
from spec_weaver.core.review_state import ReviewState, compute_review_state
from spec_weaver.core.step_resolver import StepResolver
from spec_weaver.services.audit_service import AuditService
from spec_weaver.utils.formatters import (
    get_impl_status_badge,
    get_review_status_badge,
    get_timestamp,
    get_uid_prefix,
)


@dataclass
class BuildReport:
    """ビルドの実行結果を保持するデータクラス"""
    is_success: bool
    out_dir: Path
    generated_features_count: int = 0
    generated_items_count: int = 0
    bdd_generated_count: int = 0
    error_message: Optional[str] = None


class BuildService:
    """
    仕様とテスト結果から、静的ドキュメントサイト(MkDocs向けMarkdown)を生成するサービス。
    UI(Console出力)には依存せず、成果物のファイル出力とレポート作成のみを行う。
    """

    def run_build(
        self,
        feature_dir: Path,
        repo_root: Path,
        out_dir: Path,
        test_results_file: Optional[Path] = None,
        prefix: str = "SPEC"
    ) -> BuildReport:
        try:
            return self._execute_build(feature_dir, repo_root, out_dir, test_results_file, prefix)
        except Exception as e:
            return BuildReport(is_success=False, out_dir=out_dir, error_message=f"{e}\n{traceback.format_exc()}")

    def _execute_build(
        self, feature_dir: Path, repo_root: Path, out_dir: Path,
        test_results_file: Optional[Path], prefix: str
    ) -> BuildReport:
        # 0. BDD アイテムから .feature ファイルを生成（プレステップ）
        from spec_weaver.services.bdd_service import generate_feature_files

        bdd_result = generate_feature_files(
            repo_root=repo_root,
            out_dir=feature_dir,
            prefix="BDD",
        )

        # 1. Doorstopから全アイテムと全プレフィックス取得（非活性アイテムも含む）
        raw_items = get_item_map(repo_root, include_inactive=True)
        all_items_str = {str(uid): item for uid, item in raw_items.items()}
        doorstop_tree = get_doorstop_tree(repo_root)
        all_prefixes = get_all_prefixes(repo_root)

        # 2. Gherkinタグマップ・フィンガープリント取得
        tag_map = get_tag_map(feature_dir, repo_root, all_prefixes)
        gherkin_fingerprints = get_spec_fingerprints(feature_dir, repo_root, all_prefixes)
        
        audit_service = AuditService()
        feature_file_states = audit_service._compute_feature_file_states(feature_dir, repo_root)
        child_index = _build_child_index(doorstop_tree)
        review_state = compute_review_state(
            all_items_str, gherkin_fingerprints, tag_map, feature_file_states,
            multi_tree=doorstop_tree, child_index=child_index,
        )

        # feature_path -> 関連アイテムUID一覧（バックリンク用）
        _backlink_sets: Dict[str, Set[str]] = {}
        for _uid, _scenarios in tag_map.items():
            for _s in _scenarios:
                _backlink_sets.setdefault(_s["file"], set()).add(_uid)
        feature_backlink_map: Dict[str, List[str]] = {k: sorted(v) for k, v in _backlink_sets.items()}

        # 3. 子への逆引きマップと兄弟マップ
        child_map: Dict[str, List[str]] = {}
        for uid, item in all_items_str.items():
            for link in item.links:
                parent_uid = str(link)
                child_map.setdefault(parent_uid, []).append(uid)
        sibling_map = self._compute_sibling_map(all_items_str, child_map)

        # 4. テスト実行結果の読み込み
        test_result_map: Optional[TestResultMap] = None
        if test_results_file is not None and test_results_file.exists():
            test_result_map = load_test_results(test_results_file)

        # 出力ディレクトリ準備
        docs_dir = out_dir / "docs"
        items_dir = docs_dir / "items"
        features_md_dir = docs_dir / "features"
        items_dir.mkdir(parents=True, exist_ok=True)
        features_md_dir.mkdir(parents=True, exist_ok=True)

        report = BuildReport(
            is_success=True, out_dir=out_dir,
            bdd_generated_count=bdd_result.generated_count,
        )

        # 5. Gherkin .feature → Markdown 変換
        step_resolver = StepResolver()
        step_resolver.load_steps(feature_dir / "steps")

        feature_md_map: Dict[str, str] = {}
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
                md_content = self._feature_to_markdown(
                    feature_file, backlinks, step_resolver, review_state,
                    all_items_str, feature_md_map, tag_rel, test_result_map
                )
                out_path.write_text(md_content, encoding="utf-8")
                feature_md_map[tag_rel] = f"../features/{md_rel.as_posix()}"
                report.generated_features_count += 1
            except Exception as e:
                # 変換エラー時はスキップ（元実装を踏襲）
                print(f"DEBUG: Failed to process {feature_file}: {e}")
                import traceback
                traceback.print_exc()
                pass

        # 6. 個別アイテムページ (items/*.md)
        for uid, item in all_items_str.items():
            content = self._generate_item_markdown(
                uid, item, all_items_str, child_map, sibling_map,
                tag_map, feature_md_map, test_result_map, review_state
            )
            (items_dir / f"{uid}.md").write_text(content, encoding="utf-8")
            report.generated_items_count += 1

        # 7. 各ドキュメントの一覧ページ生成
        prefix_to_file = {}
        for doc in doorstop_tree:
            p = str(doc.prefix)
            doc_items = {uid: item for uid, item in all_items_str.items() if uid.startswith(p + "-") or uid.startswith(p)}
            filename = f"{p.lower()}.md"
            table = self._generate_index_table(
                f"ドキュメント: {p}", doc_items, all_items_str, child_map,
                sibling_map, tag_map, test_result_map, review_state
            )
            (docs_dir / filename).write_text(table, encoding="utf-8")
            prefix_to_file[p] = filename

        # 8. index.md と mkdocs.yml
        self._generate_basic_files(
            docs_dir, out_dir, repo_root.name, feature_md_map,
            all_items_str, child_map, tag_map, doorstop_tree, prefix_to_file, review_state
        )

        return report

    # ---------------------------------------------------------------------------
    # ヘルパー: 兄弟マップ計算
    # ---------------------------------------------------------------------------
    def _compute_sibling_map(self, all_items_str: dict, child_map: dict) -> dict[str, list[str]]:
        sibling_map: dict[str, list[str]] = {}
        for uid, item in all_items_str.items():
            my_prefix = get_uid_prefix(uid)
            siblings: set[str] = set()
            for link in item.links:
                parent_uid = str(link)
                for sibling_uid in child_map.get(parent_uid, []):
                    if sibling_uid != uid and get_uid_prefix(sibling_uid) == my_prefix:
                        siblings.add(sibling_uid)
            if siblings:
                sibling_map[uid] = sorted(siblings)
        return sibling_map

    def _scenario_count_badge(self, uid: str, tag_map: dict, item) -> str:
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
        self, feature_file: Path, backlinks: list[str], step_resolver: Optional[StepResolver],
        review_state: Optional[ReviewState], all_items_str: dict, feature_md_map: dict,
        node_id: str, test_result_map: Optional[TestResultMap]
    ) -> str:
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

        if review_state and node_id:
            status = review_state.get_status(node_id)
            if "unreviewed" in status:
                lines.append("> 📋 **Unreviewed Changes**: このフィーチャーファイル自体に未レビューの変更があります。レビュー後に `review` コマンドで更新してください。\n")
            if "suspect" in status:
                causes = review_state.suspect_causes.get(node_id, set())
                cause_links = []
                for c in causes:
                    if c in all_items_str:
                        cause_links.append(f"[{c}](../items/{c}.md)")
                    else:
                        md_link = feature_md_map.get(c)
                        if md_link:
                            cause_links.append(f"[{Path(c).name}]({Path(md_link).name})")
                        else:
                            cause_links.append(f"`{c}`")
                causes_str = ", ".join(sorted(cause_links)) if causes else "不明"
                lines.append(f"> ⚠️ **Suspect**: 関連する仕様や他のテストが変更されました。影響範囲のレビューが必要です。\n> **原因 (Unreviewed)**: {causes_str}\n")

        if feature_tags:
            lines.append("**タグ**: " + " ".join(f"`{t}`" for t in feature_tags) + "\n")

        if backlinks:
            links_str = " / ".join(f"[{uid}](../items/{uid}.md)" for uid in backlinks)
            lines.append(f"**関連アイテム**: {links_str}\n")

        if feature_desc:
            lines.append(f"{feature_desc}\n")

        def _resolve_step_prefixes(steps: list[dict]) -> list[tuple[str, str, str]]:
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
                        lines.append("\n<details><summary><b>Step Definitions (Source Code)</b></summary>\n")
                        for rkw, txt, src in step_codes:
                            lines.append(f"#### {rkw} {txt}\n")
                            lines.append(f"```python\n{src}\n```\n")
                        lines.append("</details>\n")
                lines.append("")

            if "scenario" in child:
                sc = child["scenario"]
                sc_name = sc.get("name", "")
                sc_keyword = (sc.get("keyword") or "Scenario").strip()
                sc_tags = [t["name"] for t in sc.get("tags", [])]
                sc_desc = (sc.get("description") or "").strip()
                sc_line = sc.get("location", {}).get("line", 0)

                tag_str = " ".join(f"`{t}`" for t in sc_tags) if sc_tags else ""
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
                        lines.append("\n<details><summary><b>Step Definitions (Source Code)</b></summary>\n")
                        if test_result_map:
                            res = test_result_map.get((feature_file.stem, sc_name.strip()))
                            if res and res.get("error"):
                                lines.append("#### 📋 Execution Log (Failure)\n")
                                lines.append(f"```text\n{res['error']}\n```\n")

                        for rkw, txt, src in step_codes:
                            lines.append(f"#### {rkw} {txt}\n")
                            lines.append(f"```python\n{src}\n```\n")
                        lines.append("</details>\n")

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

        lines.append("\n---\n<details><summary>Raw .feature source</summary>\n")
        lines.append(f"```gherkin\n{raw}\n```\n</details>")

        return "\n".join(lines)

    # ---------------------------------------------------------------------------
    # ヘルパー: 個別詳細ページ生成
    # ---------------------------------------------------------------------------
    def _generate_item_markdown(
        self, uid, item, all_items_str, child_map, sibling_map,
        tag_map, feature_md_map, test_result_map, review_state
    ) -> str:
        testable = _get_custom_attribute(item, "testable", True)
        scenarios = tag_map.get(uid, [])
        children = child_map.get(uid, [])

        content: list[str] = [f"# [{uid}] {item.header}\n"]

        if not item.active:
            migrated_to = _get_custom_attribute(item, "migrated_to", None)
            if migrated_to:
                content.append(f"> 🚫 **非活性 (active: false)**: このアイテムは非活性です。[{migrated_to}]({migrated_to}.md) に移行されました。\n")
            else:
                content.append("> 🚫 **非活性 (active: false)**: このアイテムは非活性です。\n")

        if review_state:
            status = review_state.get_status(uid)
            if "unreviewed" in status:
                content.append("> 📋 **Unreviewed Changes**: このアイテム自体または関連するテストに未レビューの変更があります。\n")
            if "suspect" in status:
                causes = review_state.suspect_causes.get(uid, set())
                cause_links = []
                for c in causes:
                    if c in all_items_str:
                        cause_links.append(f"[{c}]({c}.md)")
                    else:
                        md_link = feature_md_map.get(c)
                        if md_link:
                            cause_links.append(f"[{Path(c).name}]({md_link})")
                        else:
                            cause_links.append(f"`{c}`")
                causes_str = ", ".join(sorted(cause_links)) if causes else "不明"
                content.append(f"> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。\n> **原因 (Unreviewed)**: {causes_str}\n")

        impl_badge = get_impl_status_badge(item)
        content.append(f"**実装状況**: {impl_badge}\n")

        created_at = get_timestamp(item, "created_at")
        updated_at = get_timestamp(item, "updated_at")
        content.append(f"**作成日**: {created_at}　|　**更新日**: {updated_at}\n")

        link_parts: list[str] = []
        if item.links:
            parents = [str(l) for l in item.links if str(l) in all_items_str]
            if parents:
                link_parts.append(f"**上位アイテム**: {', '.join(f'[{p}]({p}.md)' for p in parents)}")
        if children:
            valid_children = [c for c in children if c in all_items_str]
            if valid_children:
                link_parts.append(f"**下位アイテム**: {', '.join(f'[{c}]({c}.md)' for c in valid_children)}")
        siblings = sibling_map.get(uid, [])
        if siblings:
            sibling_links = ", ".join(f"[{s}]({s}.md)" for s in siblings if s in all_items_str)
            if sibling_links:
                link_parts.append(f"**兄弟アイテム**: {sibling_links}")

        if link_parts:
            content.append(" / ".join(link_parts) + "\n")

        content.append(f"**テスト対象**: {'Yes' if testable else 'No'}")
        if test_result_map is not None:
            p, f, e, s, t = spec_result_summary(uid, tag_map, test_result_map)
            summary = result_badge(p, f, e, s, t)
            content.append(f" / **テストカバレッジ**: {summary}\n")

        content.append(f"---\n\n{item.text}\n")

        if test_result_map is not None and (testable or scenarios):
            p, f, e, s, t = spec_result_summary(uid, tag_map, test_result_map)
            summary = result_badge(p, f, e, s, t)
            content.append(f"**テスト実行結果**: {summary}\n")

        if scenarios:
            content.append("### 🧪 検証シナリオ\n")
            for s in scenarios:
                file_path = s["file"]
                md_link = feature_md_map.get(file_path)
                loc = f"[{file_path}:{s['line']}]({md_link}#line-{s['line']})" if md_link else f"`{file_path}:{s['line']}`"
                if test_result_map is not None:
                    key = (Path(file_path).stem, s["name"].strip())
                    res = test_result_map.get(key)
                    status = res["status"] if res else None
                    badge = format_status_badge(status) if status is not None else "-"
                    content.append(f"- {badge} **{s['name']}** — {s['keyword']} （{loc}）")
                    if res and res.get("error"):
                        content.append(f"\n```text\n{res['error']}\n```\n")
                else:
                    content.append(f"- **{s['name']}** — {s['keyword']} （{loc}）")
        elif testable:
            content.append("### 🧪 検証シナリオ\n\n❌ Gherkin シナリオが登録されていません。")

        return "\n".join(content)

    # ---------------------------------------------------------------------------
    # ヘルパー: 一覧ページ生成
    # ---------------------------------------------------------------------------
    def _generate_index_table(
        self, title, target_items, all_items_str, child_map,
        sibling_map, tag_map, test_result_map, review_state
    ) -> str:
        has_results = test_result_map is not None
        header = "| ID | タイトル | 活性 | 親 | 子 | 兄弟 | Gherkinカバレッジ | レビューステータス | 実装状況 | 作成日 | 更新日 |"
        sep = "| :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"

        lines = [f"# {title}\n", header, sep]

        for uid in sorted(target_items.keys(), key=lambda u: (target_items[u].level, u)):
            item = target_items[uid]
            parents = [str(l) for l in item.links if str(l) in all_items_str]
            children = child_map.get(uid, [])
            siblings = sibling_map.get(uid, [])

            parents_col = "<br>".join(f"[{p}](items/{p}.md)" for p in parents) or "-"
            children_col = "<br>".join(f"[{c}](items/{c}.md)" for c in children) or "-"
            siblings_col = "<br>".join(f"[{s}](items/{s}.md)" for s in siblings) or "-"

            if has_results:
                p, f, e, s, t = spec_result_summary(uid, tag_map, test_result_map)
                coverage_col = result_badge(p, f, e, s, t)
            else:
                coverage_col = self._scenario_count_badge(uid, tag_map, item)

            review_status = get_review_status_badge(uid, review_state=review_state)
            impl_col = get_impl_status_badge(item)
            created_col = get_timestamp(item, "created_at")
            updated_col = get_timestamp(item, "updated_at")
            active_col = "✅" if item.active else "⛔"

            row = f"| [{uid}](items/{uid}.md) | {item.header} | {active_col} | {parents_col} | {children_col} | {siblings_col} | {coverage_col} | {review_status} | {impl_col} | {created_col} | {updated_col}"

            classes = []
            if not item.active:
                classes.append(".inactive-row")
            else:
                if "suspect" in review_status:
                    classes.append(".suspect-row")
                if "unreviewed" in review_status:
                    classes.append(".unreviewed-row")

            if classes:
                row += " {: " + " ".join(classes) + " } |"
            else:
                row += " |"

            lines.append(row)

        return "\n".join(lines)

    # ---------------------------------------------------------------------------
    # ヘルパー: index.md / mkdocs.yml 生成
    # ---------------------------------------------------------------------------
    def _build_hierarchy_tree(self, doorstop_tree, prefix_to_file: dict) -> str:
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
            for child_tree in sorted(tree_node.children, key=lambda t: str(t.document.prefix)):
                render_tree_node(child_tree, depth + 1)

        # MultiTree の場合は各ルートツリーを個別にレンダリング
        trees = getattr(doorstop_tree, "trees", None)
        if trees is not None:
            for tree in trees:
                render_tree_node(tree, 0)
        else:
            render_tree_node(doorstop_tree, 0)
        return "\n".join(lines) if lines else "_（ドキュメント階層が見つかりません）_"

    def _generate_basic_files(
        self, docs_dir: Path, out_dir: Path, project_name: str, feature_md_map: dict,
        all_items_str: dict, child_map: dict, tag_map: dict, doorstop_tree,
        prefix_to_file: dict, review_state: Optional[ReviewState]
    ) -> None:
        index_path = docs_dir / "index.md"
        tree_md = self._build_hierarchy_tree(doorstop_tree, prefix_to_file)
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
            
            file_status = review_state.get_status(tag_rel) if review_state else "✅ reviewed"
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
        features_index.write_text(f"# 振る舞い仕様一覧 (Gherkin Features)\n\n{feature_table}\n", encoding="utf-8")

        js_dir = docs_dir / "javascripts"
        css_dir = docs_dir / "stylesheets"
        js_dir.mkdir(parents=True, exist_ok=True)
        css_dir.mkdir(parents=True, exist_ok=True)

        template_root = resources.files("spec_weaver") / "templates"
        js_src = template_root / "javascripts" / "custom-table-filter.js"
        css_src = template_root / "stylesheets" / "extra.css"

        if js_src.exists():
            (js_dir / "custom-table-filter.js").write_text(js_src.read_text(encoding="utf-8"), encoding="utf-8")
        if css_src.exists():
            (css_dir / "extra.css").write_text(css_src.read_text(encoding="utf-8"), encoding="utf-8")

        docs_nav_entries = ""
        for p, f in sorted(prefix_to_file.items()):
            docs_nav_entries += f"  - {p}:\n      - {p}一覧: {f}\n"
            p_items = [uid for uid in all_items_str if uid.startswith(f"{p}-") or uid.startswith(p)]
            for uid in sorted(p_items, key=lambda u: (all_items_str[u].level, u)):
                docs_nav_entries += f"      - {uid}: items/{uid}.md\n"

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
