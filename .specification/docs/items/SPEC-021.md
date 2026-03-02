# [SPEC-021] Gherkinタグ継承（Effective Tags）

> 🚫 **非活性 (active: false)**: このアイテムは非活性です。[CORE-002](CORE-002.md) に移行されました。

**実装状況**: ✅ implemented

**作成日**: 2026-02-27　|　**更新日**: 2026-03-02

**上位アイテム**: [REQ-001](REQ-001.md) / **兄弟アイテム**: [SPEC-001](SPEC-001.md), [SPEC-002](SPEC-002.md)

**テスト対象**: Yes　**個別カバレッジ**: 🔴 0/1 (0%)


### 内容

## 概要
GherkinのASTをトップダウンで再帰的に探索し、上位要素（Feature / Rule）のタグを
下位要素（Scenario / Scenario Outline）へ継承することで、各シナリオが持つ
「Effective Tags（有効タグ）」を正確に算出する。

## 背景・動機
従来の実装では、タグが付与されたノード（Feature / Rule / Scenario）をそのままタグマップに
登録していたため、Featureレベルに記述された仕様タグ（例: `@SPEC-001`）が
配下の個別シナリオとは紐付けられていなかった。
これにより「シナリオが存在するのに仕様カバレッジが 0」という False Positive が発生していた。

## Effective Tags の定義

各テスト実行単位（Scenario / Scenario Outline）の Effective Tags は以下の通り定義される：

```
Effective Tags(scenario) =
    Tags(Feature)
  ∪ Tags(Rule)          # Rule 内にある場合のみ
  ∪ Tags(Scenario)
  ∪ Tags(Examples[all]) # Scenario Outline の場合、全 Examples タグの和集合
```

## 継承ルール

1. **Feature → Scenario**: Featureに付与されたタグはすべての直下 Scenario に継承される
2. **Feature + Rule → Scenario**: Featureタグ ∪ Ruleタグ が Rule配下のすべてのScenarioに継承される
3. **Scenario Outline**: Scenario Outline 自身のタグと、全 Examples テーブルのタグの和集合を
   1つの ScenarioInfo エントリとして扱う
4. **Background は除外**: Background セクションはテスト実行単位ではないため、
   tag_map への登録対象外とする
5. **タグ継承はすべてのタグに適用**: プレフィックスフィルタ（SPEC, REQ など）は
   Effective Tags 算出後に適用する（Gherkin公式仕様に準拠）

## コアジェネレータのインターフェース

```python
def _extract_scenarios_with_inherited_tags(
    ast: Any,
    file_path: str,
) -> Generator[Tuple[Set[str], ScenarioInfo], None, None]:
    """
    ASTを再帰的に探索し、(effective_tag_set, scenario_info) のタプルを yield する。
    プレフィックスフィルタは適用しない（呼び出し側の責務）。
    """
```

## get_tag_map / get_tags との統合

- `get_tag_map()` はコアジェネレータを呼び出し、effective_tag_set に対して
  プレフィックスフィルタを適用してから tag_map に登録する
- `get_tags()` は `get_tag_map()` のキー集合を返す（既存インターフェース維持）
- 両関数の引数・戻り値の型シグネチャに変更はない

## 既存インターフェースとの互換性

| 関数 | 引数の変化 | 戻り値の型の変化 | 振る舞いの変化 |
|---|---|---|---|
| `get_tags()` | なし | なし | Featureタグも継承されてScenario経由で集約される |
| `get_tag_map()` | なし | なし | tag_map[id] の各エントリが必ず Scenario の情報になる |

## 削除対象

- `_extract_tag_map_recursive()`: 本仕様実装後、コアジェネレータに完全に置き換えられ不要となる

### 🧪 検証シナリオ

❌ まだ Gherkin シナリオが登録されていません。