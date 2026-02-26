# [SPEC-003] audit コマンド仕様

**実装状況**: ✅ implemented

**上位アイテム**: [REQ-002](REQ-002.md) / **兄弟アイテム**: [SPEC-002](SPEC-002.md)

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

### 🧪 検証シナリオ

- **audit コマンド** — Feature （[features/audit.feature:2](../features/audit.md)）