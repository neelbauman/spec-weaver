# src/spec_weaver/gherkin.py

from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Set

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

    Args:
        features_dir (Path): .feature ファイルが格納されているディレクトリ
        prefixes (Set[str] | str): 対象とするタグのプレフィックスまたはその集合（例: {"SPEC", "REQ", "AUTH"}）
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

            # ASTのルートから再帰的に探索し、tag_map に情報を蓄積する
            _extract_tag_map_recursive(ast, target_prefixes, rel_path, tag_map)
            
        except Exception as e:
            # 構文エラーの握り潰しは厳禁（フェイルファスト）
            raise ValueError(
                f"Gherkin構文エラー: {feature_file} のパースに失敗しました。\n詳細: {e}"
            ) from e

    # defaultdict を通常の dict に変換して返す
    return dict(tag_map)


def _extract_tag_map_recursive(node: Any, target_prefixes: Set[str], file_path: str, tag_map: TagMap) -> None:
    """
    ASTのノードツリーを再帰的に探索し、対象プレフィックスのいずれかに合致するタグと親ノードの情報を抽出します。
    """
    if isinstance(node, dict):
        # 現在のノードが 'tags' を持っている場合 (Feature, Scenario, Scenario Outline など)
        if "tags" in node and isinstance(node["tags"], list):
            
            # 親ノード（このタグが付けられているブロック）のメタデータを取得
            name = node.get("name", "Unnamed")
            keyword = node.get("keyword", "Unknown")
            # GherkinのASTでは、行番号は "location" 辞書の中に格納されている
            line = node.get("location", {}).get("line", 0)

            for tag_node in node["tags"]:
                tag_name: str = tag_node.get("name", "")
                clean_tag = tag_name.lstrip("@")
                
                # プレフィックスのいずれかが一致すれば、詳細情報と共にマッピングに追加
                for prefix in target_prefixes:
                    if clean_tag.upper().startswith(prefix):
                        tag_map[clean_tag].append({
                            "file": file_path,
                            "line": line,
                            "name": name,
                            "keyword": keyword
                        })
                        break

        # 辞書の各バリューに対してさらに再帰探索（ネストされたScenarioやExamplesを掘り下げる）
        for value in node.values():
            _extract_tag_map_recursive(value, target_prefixes, file_path, tag_map)

    elif isinstance(node, list):
        # リスト内の各要素に対して再帰探索
        for item in node:
            _extract_tag_map_recursive(item, target_prefixes, file_path, tag_map)


def get_tags(features_dir: Path, prefixes: Set[str] | str = "SPEC", **kwargs) -> Set[str]:
    """
    (後方互換性・監査用)
    仕様IDの文字列の集合（Set）のみを返します。auditコマンド等の差分検知で使用します。
    """
    tag_map = get_tag_map(features_dir, prefixes, **kwargs)
    return set(tag_map.keys())

