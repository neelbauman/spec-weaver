# src/spec_weaver/gherkin.py
# implements: CORE-002
# implements: CORE-001
# implements: QA-004

from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Set, Tuple

from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner

# 型エイリアス: 1つのテストシナリオが持つ詳細情報
ScenarioInfo = Dict[str, Any]  # keys: "file", "line", "name", "keyword", "fingerprint"

# 型エイリアス: 仕様IDをキーとし、関連するシナリオ情報のリストを値とする辞書
TagMap = Dict[str, List[ScenarioInfo]]


def get_spec_fingerprints(
    features_dir: Path, repo_root: Path, prefixes: Set[str] | str = "SPEC"
) -> Dict[str, List[Dict[str, str]]]:
    """
    各仕様IDに対して、紐づく全シナリオのフィンガープリントをファイルごとにハッシュ化したリストを返します。
    形式: {"SPEC-001": [{"./specification/features/audit.feature": "hash1"}, ...]}
    """
    import hashlib

    tag_map = get_tag_map(features_dir, repo_root, prefixes)
    result = {}

    for tag, scenarios in tag_map.items():
        # scenarios in tag_map already have "file" (relative path to repo_root)
        scenarios_by_file = defaultdict(list)
        for s in scenarios:
            scenarios_by_file[s["file"]].append(s)

        file_fingerprints = []
        for file_path in sorted(scenarios_by_file.keys()):
            scs = sorted(scenarios_by_file[file_path], key=lambda x: x["line"])
            combined = "".join(x["fingerprint"] for x in scs)
            file_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
            file_fingerprints.append({file_path: file_hash})
        result[tag] = file_fingerprints

    return result


def get_tag_map(
    features_dir: Path, repo_root: Path, prefixes: Set[str] | str = "SPEC", **kwargs
) -> TagMap:
    """
    指定ディレクトリ以下の .feature ファイルを解析し、
    仕様ID（タグ）と、それに紐づくシナリオ（テスト）情報のマッピングを取得します。

    Gherkin のタグ継承ルール（CORE-002）に従い、Feature / Rule レベルのタグは
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
    if features_dir.is_file():
        files = [features_dir]
    else:
        files = list(features_dir.rglob("*.feature"))

    for feature_file in files:
        try:
            with open(feature_file, "r", encoding="utf-8") as f:
                content = f.read()

            # テキストをトークン化し、AST（抽象構文木）辞書に変換
            ast = parser.parse(TokenScanner(content))

            # ファイルパスは repo_root からの相対パスに変換 (./ から始める)
            try:
                rel_path = "./" + str(feature_file.relative_to(repo_root))
            except ValueError:
                rel_path = str(feature_file)

            # コアジェネレータで (effective_tag_set, scenario_info) を取得し、
            # プレフィックスフィルタを適用してから tag_map に登録する（CORE-002）
            for effective_tags, scenario_info in _extract_scenarios_with_inherited_tags(
                ast, rel_path
            ):
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

    タグ継承ルール（CORE-002）:
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
    feature_hash = _get_node_hash_content(feature)

    bg_hash = ""
    for child in feature.get("children", []):
        if "background" in child:
            bg_hash += _get_node_hash_content(child["background"])

    base_hash = feature_hash + bg_hash

    for child in feature.get("children", []):
        if "rule" in child:
            rule = child["rule"]
            rule_tags = feature_tags | _collect_tags(rule)
            rule_hash = base_hash + _get_node_hash_content(rule)

            rule_bg_hash = ""
            for rule_child in rule.get("children", []):
                if "background" in rule_child:
                    rule_bg_hash += _get_node_hash_content(rule_child["background"])
            
            rule_base_hash = rule_hash + rule_bg_hash

            for rule_child in rule.get("children", []):
                yield from _process_scenario_node(rule_child, rule_tags, file_path, rule_base_hash)
        elif "scenario" in child:
            yield from _process_scenario_node(child, feature_tags, file_path, base_hash)


def _process_scenario_node(
    child: Any,
    inherited_tags: Set[str],
    file_path: str,
    base_hash_content: str = "",
) -> Generator[Tuple[Set[str], ScenarioInfo], None, None]:
    """
    Scenario または Scenario Outline のノードを処理し、
    (effective_tag_set, ScenarioInfo) を yield する。

    Scenario Outline の場合、全 Examples テーブルのタグを effective_tags に集約し、
    1エントリとして扱う（CORE-002: ScenarioOutline は1エントリ）。
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

    # フィンガープリントの計算（Feature情報、Background、名前、キーワード、ステップ、Examples）
    import hashlib

    f_content = base_hash_content + scenario.get("name", "") + keyword
    for step in scenario.get("steps", []):
        f_content += step.get("keyword", "") + step.get("text", "")
    for example in scenario.get("examples", []):
        f_content += example.get("name", "")
        header = example.get("tableHeader", {})
        if header:
            f_content += "".join(c["value"] for c in header.get("cells", []))
        for row in example.get("tableBody", []):
            f_content += "".join(c["value"] for c in row.get("cells", []))
    fingerprint = hashlib.sha256(f_content.encode("utf-8")).hexdigest()

    scenario_info: ScenarioInfo = {
        "file": file_path,
        "line": scenario.get("location", {}).get("line", 0),
        "name": scenario.get("name", "Unnamed"),
        "keyword": keyword,
        "fingerprint": fingerprint,
    }
    yield effective_tags, scenario_info


def _collect_tags(node: Any) -> Set[str]:
    """ノードの 'tags' リストから '@' を除去したタグ名の集合を返す。"""
    return {tag["name"].lstrip("@") for tag in node.get("tags", [])}


def _get_node_hash_content(node: Any) -> str:
    """ノード（Feature, Rule, Background等）のハッシュ計算用コンテンツ文字列を生成する。"""
    content = node.get("keyword", "") + node.get("name", "") + (node.get("description", "") or "").strip()
    for step in node.get("steps", []):
        content += step.get("keyword", "") + step.get("text", "")
    return content


# ---------------------------------------------------------------------------
# .feature ファイル単位フィンガープリント（QA-004）
# ---------------------------------------------------------------------------

_FINGERPRINT_PREFIX = "# spec-weaver-fingerprint: "


def compute_feature_file_hash(feature_file: Path) -> str:
    """
    .feature ファイル全体の構造コンテンツ（Feature / Background / Scenario）の
    SHA-256 ハッシュを計算して返します。

    Gherkin パーサーで AST を生成するため、# spec-weaver-fingerprint: コメント行は
    自動的に除外されます（コメントは Gherkin AST に含まれません）。
    """
    import hashlib

    with open(feature_file, "r", encoding="utf-8") as f:
        content = f.read()

    parser = Parser()
    ast = parser.parse(TokenScanner(content))
    feature = ast.get("feature")
    if not feature:
        return hashlib.sha256(b"").hexdigest()

    combined = _get_node_hash_content(feature)

    for child in feature.get("children", []):
        if "background" in child:
            combined += _get_node_hash_content(child["background"])
        elif "rule" in child:
            rule = child["rule"]
            combined += _get_node_hash_content(rule)
            for rule_child in rule.get("children", []):
                if "background" in rule_child:
                    combined += _get_node_hash_content(rule_child["background"])
                elif "scenario" in rule_child:
                    combined += _get_scenario_hash_content(rule_child["scenario"])
        elif "scenario" in child:
            combined += _get_scenario_hash_content(child["scenario"])

    return hashlib.sha256(combined.encode("utf-8")).hexdigest()


def read_stored_fingerprints(feature_file: Path) -> Dict[str, str]:
    """
    .feature ファイルの先頭から spec-weaver-fingerprint および
    関連アイテムのフィンガープリント（# spec-weaver-fingerprint-<ID>: <hash>）
    を読み取り、辞書として返します。
    ファイル自身のハッシュは空文字キー ("") に格納します。
    """
    fps = {}
    try:
        with open(feature_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(_FINGERPRINT_PREFIX):
                    fps[""] = line[len(_FINGERPRINT_PREFIX):].strip()
                elif line.startswith("# spec-weaver-fingerprint-"):
                    parts = line.split(":", 1)
                    if len(parts) == 2:
                        key = parts[0][len("# spec-weaver-fingerprint-"):].strip()
                        val = parts[1].strip()
                        fps[key] = val
                else:
                    break
    except OSError:
        pass
    return fps


def read_stored_fingerprint(feature_file: Path) -> Optional[str]:
    """後方互換性用ラッパー"""
    return read_stored_fingerprints(feature_file).get("")


def write_feature_fingerprints(feature_file: Path, file_fingerprint: str, item_fingerprints: Dict[str, str] = None) -> None:
    """
    .feature ファイルの先頭に spec-weaver-fingerprint コメントと、
    関連アイテムのフィンガープリントを書き込みます。
    """
    if item_fingerprints is None:
        item_fingerprints = {}

    with open(feature_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 既存のフィンガープリント行を削除
    while lines and (lines[0].startswith(_FINGERPRINT_PREFIX) or lines[0].startswith("# spec-weaver-fingerprint-")):
        lines.pop(0)

    # 新しいフィンガープリント行を作成
    new_lines = [f"{_FINGERPRINT_PREFIX}{file_fingerprint}\n"]
    for tag in sorted(item_fingerprints.keys()):
        if item_fingerprints[tag]:
            new_lines.append(f"# spec-weaver-fingerprint-{tag}: {item_fingerprints[tag]}\n")

    lines = new_lines + lines

    with open(feature_file, "w", encoding="utf-8") as f:
        f.writelines(lines)


def write_feature_fingerprint(feature_file: Path, fingerprint: str) -> None:
    """後方互換性用ラッパー"""
    write_feature_fingerprints(feature_file, fingerprint)


def _get_scenario_hash_content(scenario: Any) -> str:
    """シナリオノード（steps + examples 含む）のハッシュ計算用コンテンツ文字列を生成する。"""
    keyword = scenario.get("keyword", "Scenario").strip()
    content = scenario.get("name", "") + keyword
    for step in scenario.get("steps", []):
        content += step.get("keyword", "") + step.get("text", "")
    for example in scenario.get("examples", []):
        content += example.get("name", "")
        header = example.get("tableHeader", {})
        if header:
            content += "".join(c["value"] for c in header.get("cells", []))
        for row in example.get("tableBody", []):
            content += "".join(c["value"] for c in row.get("cells", []))
    return content


def get_tags(
    features_dir: Path, repo_root: Path, prefixes: Set[str] | str = "SPEC", **kwargs
) -> Set[str]:
    """
    (後方互換性・監査用)
    仕様IDの文字列の集合（Set）のみを返します。auditコマンド等の差分検知で使用します。
    """
    tag_map = get_tag_map(features_dir, repo_root, prefixes, **kwargs)
    return set(tag_map.keys())
