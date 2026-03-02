# [PLAN-003] SPEC-021 実装計画：Gherkinタグ継承（Effective Tags）

**実装状況**: 📝 draft

**作成日**: 2026-02-27　|　**更新日**: 2026-02-27

**上位アイテム**: [SPEC-021](SPEC-021.md)


### 内容

## 概要

SPEC-021「Gherkinタグ継承（Effective Tags）」の実装タスクを分解する。
規模は中規模（主要変更は gherkin.py の1モジュール）。

## 実装タスク

### Task 1: コアジェネレータの実装（gherkin.py）

**目的**: `_extract_scenarios_with_inherited_tags` を新設し、
AST を再帰的に探索して Effective Tags を算出する。

**実装内容**:
- `_collect_tags(node)`: ノードから @を除去したタグ名集合を返すヘルパー
- `_process_scenario_node(child, inherited_tags, file_path)`: Scenario / ScenarioOutline の処理
- `_extract_scenarios_with_inherited_tags(ast, file_path)`: コアジェネレータ
  - Feature → 直下 Scenario → `_process_scenario_node` に委譲
  - Feature → Rule → 各 Scenario → `_process_scenario_node` に委譲
  - Background は無視

**完了条件**: `_extract_scenarios_with_inherited_tags` が (effective_tag_set, ScenarioInfo) を yield できる

**依存**: なし（新設関数）

---

### Task 2: get_tag_map / get_tags の書き換え（gherkin.py）

**目的**: 既存の公開 API がコアジェネレータを利用するよう内部ロジックを置き換える。

**実装内容**:
- `get_tag_map()` の内部ループを `_extract_scenarios_with_inherited_tags` の呼び出しに変更
  - 各 (effective_tag_set, info) について prefix フィルタを適用し tag_map に追記
- `_extract_tag_map_recursive()` を削除

**完了条件**:
- 型シグネチャが変わらない
- `_extract_tag_map_recursive` が完全に削除されている

**依存**: Task 1 の完了

---

### Task 3: tests/test_gherkin.py への継承テスト追加

**目的**: Effective Tags の算出ロジックを pytest でユニットテストとして固定化する。

**テストケース**:
1. Feature タグのみ → 配下 Scenario が tag_map に登録され、keyword が "Scenario"
2. Feature + Rule + Scenario の多段継承 → 両方の SPEC に Scenario が登録される
3. Scenario 直接タグ + 継承タグの共存 → Effective Tags の和集合
4. Scenario Outline の全 Examples タグが集約される
5. プレフィックスフィルタが Effective Tags 算出後に適用される

**完了条件**: `uv run pytest tests/test_gherkin.py -q` がすべて PASS

**依存**: Task 2 の完了

---

### Task 4: BDDステップ定義の更新（scaffold → 肉付け）

**目的**: data_extraction.feature に追加した @SPEC-021 シナリオのステップ定義を実装する。

**実装内容**:
- `uv run spec-weaver scaffold ./specification/features --out-dir features/steps` を実行
- 生成された NotImplementedError を仕様に従って肉付け

**完了条件**: `uv run behave --no-capture` で @SPEC-021 シナリオが PASS または FAILED（仕様と実装の乖離が可視化されている）

**依存**: Task 2 の完了

---

### Task 5: SPEC-002 の更新と SPEC-021 のステータス更新

**目的**: 仕様書と実装の整合性を保つ。

**実装内容**:
- SPEC-002 の text に「タグ継承の詳細は SPEC-021 を参照」旨を追記
- SPEC-021 の `status` を `implemented` に更新

**完了条件**: `uv run spec-weaver audit ./specification/features` がエラーなし

**依存**: Task 1〜4 の完了

## タスク実行順序

```
Task 1 (コアジェネレータ)
  └── Task 2 (get_tag_map/get_tags 書き換え)
        ├── Task 3 (pytest テスト追加)
        └── Task 4 (BDD ステップ定義)
              └── Task 5 (仕様書ステータス更新)
```
