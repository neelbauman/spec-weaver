# src/spec_weaver/gherkin.py
# implements: SPEC-021
# implements: SPEC-002

from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Generator, List, Set, Tuple

from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner

# 型エイリアス: 1つのテストシナリオが持つ詳細情報
ScenarioInfo = Dict[str, Any]  # keys: "file", "line", "name", "keyword"

# 型エイリアス: 仕様IDをキーとし、関連するシナリオ情報のリストを値とする辞書
TagMap = Dict[str, List[ScenarioInfo]]


def get_tag_map(features_dir: Path, prefixes: Set[str] | str = "SPEC", **kwargs) -> TagMap:
    """
    指定ディレクトリ以下の .feature ファイルを解析し、
    仕様ID（タグ）と、それに紐づくシナリオ（テスト）情報のマッピングを取得します。

    Gherkin のタグ継承ルール（SPEC-021）に従い、Feature / Rule レベルのタグは
    配下のすべての Scenario / Scenario Outline に継承されます。
    tag_map の各エントリは必ず Scenario 系のキーワードを持つ ScenarioInfo になります。

    Args:
        features_dir (Path): .feature ファイルが格納されているディレクトリ
        prefixes (Set[str] | str): 対象とするタグのプレフィックスまたはその集合（例: {"SPEC", "REQ"}）
        **kwargs: 後方互換性のため、'prefix' 引数を受け入れます。

    Returns:
        TagMap: { "SPEC-001": [{"file": "features/login.feature", "line": 5, "name": "...", "keyword": "Scenario"}, ...] }
    """
    # 後方互換性のための処理
    if "prefix" in kwargs:
        prefixes = kwargs["prefix"]

    if isinstance(prefixes, str):
        target_prefixes = {prefixes.upper()}
    else:
        target_prefixes = {p.upper() for p in prefixes}

    parser = Parser()
    tag_map: TagMap = defaultdict(list)

    # 対象ディレクトリ内のすべての .feature ファイルを再帰的に検索
    for feature_file in features_dir.rglob("*.feature"):
        try:
            with open(feature_file, "r", encoding="utf-8") as f:
                content = f.read()

            # テキストをトークン化し、AST（抽象構文木）辞書に変換
            ast = parser.parse(TokenScanner(content))

            # ファイルパスは、ターミナルやMarkdown上で見やすいように相対パスに変換
            try:
                rel_path = str(feature_file.relative_to(features_dir.parent))
            except ValueError:
                rel_path = str(feature_file)

            # コアジェネレータで (effective_tag_set, scenario_info) を取得し、
            # プレフィックスフィルタを適用してから tag_map に登録する（SPEC-021）
            for effective_tags, scenario_info in _extract_scenarios_with_inherited_tags(ast, rel_path):
                for tag in effective_tags:
                    for prefix in target_prefixes:
                        if tag.upper().startswith(prefix):
                            tag_map[tag].append(scenario_info)
                            break

        except Exception as e:
            # 構文エラーの握り潰しは厳禁（フェイルファスト）
            raise ValueError(
                f"Gherkin構文エラー: {feature_file} のパースに失敗しました。\n詳細: {e}"
            ) from e

    # defaultdict を通常の dict に変換して返す
    return dict(tag_map)


def _extract_scenarios_with_inherited_tags(
    ast: Any,
    file_path: str,
) -> Generator[Tuple[Set[str], ScenarioInfo], None, None]:
    """
    GherkinのASTをトップダウンで再帰的に探索し、各シナリオの
    「Effective Tags（有効タグ）」と ScenarioInfo のタプルを生成するコアジェネレータ。

    タグ継承ルール（SPEC-021）:
    - Feature のタグはすべての直下 Scenario および Rule 配下の Scenario に継承される
    - Rule のタグは Feature タグと合わせて配下のすべての Scenario に継承される
    - Scenario Outline の場合、全 Examples テーブルのタグの和集合を effective_tags に加算
    - Background セクションはテスト実行単位ではないため対象外
    - タグ継承はすべてのタグに適用し、プレフィックスフィルタは呼び出し側で行う

    Yields:
        Tuple[Set[str], ScenarioInfo]:
            effective_tags: そのシナリオの有効タグ集合（@ なし）
            scenario_info: {"file", "line", "name", "keyword"}
    """
    feature = ast.get("feature")
    if not feature:
        return

    feature_tags = _collect_tags(feature)

    for child in feature.get("children", []):
        if "rule" in child:
            rule = child["rule"]
            rule_tags = feature_tags | _collect_tags(rule)
            for rule_child in rule.get("children", []):
                yield from _process_scenario_node(rule_child, rule_tags, file_path)
        elif "scenario" in child:
            yield from _process_scenario_node(child, feature_tags, file_path)
        # background は無視


def _process_scenario_node(
    child: Any,
    inherited_tags: Set[str],
    file_path: str,
) -> Generator[Tuple[Set[str], ScenarioInfo], None, None]:
    """
    Scenario または Scenario Outline のノードを処理し、
    (effective_tag_set, ScenarioInfo) を yield する。

    Scenario Outline の場合、全 Examples テーブルのタグを effective_tags に集約し、
    1エントリとして扱う（SPEC-021: ScenarioOutline は1エントリ）。
    """
    scenario = child.get("scenario")
    if not scenario:
        return

    keyword = scenario.get("keyword", "Scenario").strip()
    own_tags = _collect_tags(scenario)

    # Scenario Outline: 全 Examples テーブルのタグの和集合を加算
    examples_tags: Set[str] = set()
    for examples in scenario.get("examples", []):
        examples_tags |= _collect_tags(examples)

    effective_tags = inherited_tags | own_tags | examples_tags

    scenario_info: ScenarioInfo = {
        "file": file_path,
        "line": scenario.get("location", {}).get("line", 0),
        "name": scenario.get("name", "Unnamed"),
        "keyword": keyword,
    }
    yield effective_tags, scenario_info


def _collect_tags(node: Any) -> Set[str]:
    """ノードの 'tags' リストから '@' を除去したタグ名の集合を返す。"""
    return {tag["name"].lstrip("@") for tag in node.get("tags", [])}


def get_tags(features_dir: Path, prefixes: Set[str] | str = "SPEC", **kwargs) -> Set[str]:
    """
    (後方互換性・監査用)
    仕様IDの文字列の集合（Set）のみを返します。auditコマンド等の差分検知で使用します。
    """
    tag_map = get_tag_map(features_dir, prefixes, **kwargs)
    return set(tag_map.keys())
