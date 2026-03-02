# [SPEC-003] audit コマンド仕様

> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: `test_fingerprint mismatch`

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-03-02

**上位アイテム**: [REQ-002](REQ-002.md) / **兄弟アイテム**: [CORE-001](CORE-001.md), [QA-002](QA-002.md)

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

**テスト実行結果 (個別)**: ✅ 5/9 PASS

### 🧪 検証シナリオ

- - **完全一致で、監査が成功する** — Scenario （[features/audit.feature:6](../features/audit.md)）
- ✅ PASS **テスト漏れの検出** — Scenario （[features/audit.feature:12](../features/audit.md)）
- - **orphanタグの検出** — Scenario （[features/audit.feature:18](../features/audit.md)）
- ✅ PASS **テスト漏れと孤児タグの同時検出** — Scenario （[features/audit.feature:24](../features/audit.md)）
- ✅ PASS **testable: false の仕様はスキップされる** — Scenario （[features/audit.feature:30](../features/audit.md)）
- ✅ PASS **Suspect Link の検出** — Scenario （[features/audit.feature:37](../features/audit.md)）
- ✅ PASS **Unreviewed Changes の検出** — Scenario （[features/audit.feature:45](../features/audit.md)）
- - **feature ファイルが Suspect として検出される** — Scenario （[features/audit.feature:52](../features/audit.md)）
- - **feature ファイルが Unreviewed として検出される** — Scenario （[features/audit.feature:59](../features/audit.md)）