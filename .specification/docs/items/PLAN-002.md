# [PLAN-002] scaffold コマンド 差分マージ・非対話モード実装計画

**実装状況**: -

**作成日**: 2026-02-27　|　**更新日**: 2026-02-27

**上位アイテム**: [SPEC-015](SPEC-015.md)


### 内容

## 概要

scaffold コマンドに差分マージ機能・インメモリ差分表示・Git dirty チェック・
非対話モード（--force）を追加する実装計画。

## タスク一覧

### T1: SPEC-015.yml 更新
- 依存: なし
- 完了条件: コマンドIF（--repo-root, --force）、マージ動作、Docstring 仕様が記述されている
- 対象: `specification/specs/SPEC-015.yml`

### T2: scaffold.feature 更新
- 依存: T1
- 完了条件: 5シナリオ追加（Docstringシナリオリスト、差分マージ、差分なしスキップ、dirty確認プロンプト、--force）
- 対象: `specification/features/scaffold.feature`

### T3: codegen.py — 戻り値・Docstring フォーマット変更
- 依存: なし（T1/T2 と並行可）
- 完了条件:
  - `generate_test_file` が `tuple[Path, str, str] | None` を返す
  - 新規生成時の Docstring に Scenarios セクションが含まれる
  - `import difflib` 追加済み
- 対象: `src/spec_weaver/codegen.py`

### T4: codegen.py — 仮想新規ファイル方式マージアルゴリズム実装
- 依存: T3
- 完了条件:
  - `overwrite=False` かつ既存ファイルあり のとき差分マージが動作する
  - 新規ステップが .feature の出現順で挿入される（仮想新規ファイル方式）
  - 既存 Docstring の Scenarios セクションに不足シナリオが追記される
  - 変更なしのとき None を返す
  - difflib.unified_diff で差分テキストが生成される
- 対象: `src/spec_weaver/codegen.py`

### T5: cli.py — scaffold コマンド更新
- 依存: T3, T4
- 完了条件:
  - `--repo-root` / `--force` オプションが追加されている
  - `_is_file_dirty()` ヘルパーが実装されている
  - dirty チェック → Confirm プロンプト（--force でスキップ）が動作する
  - 戻り値タプルに応じて "新規作成" / "差分更新" / "スキップ" を表示する
  - 差分更新時に `rich.Syntax` でハイライト表示する
- 対象: `src/spec_weaver/cli.py`

### T6: cli.py — ci コマンド更新
- 依存: T3
- 完了条件: `generate_test_file` の戻り値タプルを正しくアンパックしている
- 対象: `src/spec_weaver/cli.py`

### T7: tests/test_scaffold.py 更新
- 依存: T3, T4, T5, T6
- 完了条件:
  - 既存テストが新戻り値形式 (path, status, diff) に対応している
  - 差分マージ動作のテストが追加されている
  - dirty チェック・--force のテストが追加されている（subprocess モック使用）
  - pytest が全件通過する
- 対象: `tests/test_scaffold.py`

## 実行順序

```
T1 (SPEC更新)  ──┐
T2 (feature)  ──┤
T3 (戻り値/DS) ──┼──→ T4 (マージ) ──→ T5 (scaffold CLI) ──→ T7 (テスト)
                │                  └──→ T6 (ci CLI)    ──┘
                └──────────────────────────────────────────┘
```

T1・T2・T3 は並行実施可能。T4 は T3 完了後。T5・T6 は T4 完了後。T7 は T5・T6 完了後。
