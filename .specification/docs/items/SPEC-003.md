# [SPEC-003] audit コマンド仕様

> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: [audit.feature](../features/audit.md)

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-03-01

**上位アイテム**: [REQ-002](REQ-002.md) / **兄弟アイテム**: [SPEC-002](SPEC-002.md), [SPEC-013](SPEC-013.md)

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
仕様とテストの乖離を静的に検知する `audit` コマンドの仕様を定義する。

## 詳細仕様

### 入力
- `feature_dir` (必須): Gherkin `.feature` ファイルが格納されたディレクトリパス
- `--repo-root` / `-r` (オプション): Doorstopプロジェクトルート（デフォルト: カレントディレクトリ）
- `--prefix` / `-p` (オプション): 仕様IDプレフィックス（デフォルト: "SPEC"）

### 処理
- DoorstopのID集合とGherkinのタグ集合の差分（集合演算）を算出する
- `untested_specs = specs_in_db - tags_in_code`（テスト漏れ）
- `orphaned_tags = tags_in_code - specs_in_db`（孤児タグ）
- `testable: false` のアイテムは集合から除外する

### 出力・結果
- 乖離がある場合: 終了コード `1`（CI失敗）を返し、テーブルで乖離内容を出力
- 完全一致の場合: 終了コード `0`（成功）を返し、成功メッセージを出力

**テスト実行結果 (個別)**: ✅ 7/7 PASS

### 🧪 検証シナリオ

- ✅ PASS **完全一致時の監査成功** — Scenario （[features/audit.feature:5](../features/audit.md)）
- ✅ PASS **テスト漏れの検出** — Scenario （[features/audit.feature:11](../features/audit.md)）
- ✅ PASS **孤児タグの検出** — Scenario （[features/audit.feature:17](../features/audit.md)）
- ✅ PASS **テスト漏れと孤児タグの同時検出** — Scenario （[features/audit.feature:23](../features/audit.md)）
- ✅ PASS **testable: false の仕様はスキップされる** — Scenario （[features/audit.feature:29](../features/audit.md)）
- ✅ PASS **Suspect Link の検出** — Scenario （[features/audit.feature:36](../features/audit.md)）
- ✅ PASS **Unreviewed Changes の検出** — Scenario （[features/audit.feature:44](../features/audit.md)）