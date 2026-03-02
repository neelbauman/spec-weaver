# [SPEC-007] 実装ステータス管理

> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: [REQ-001](REQ-001.md), [REQ-003](REQ-003.md)

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-03-01

**上位アイテム**: [REQ-006](REQ-006.md)

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
各アイテムの実装進行状況を定義し、CLIおよびドキュメントで可視化する。

## 詳細仕様

### 1. status カスタム属性の定義
DoorstopのYAMLファイルに `status` キーを追記することで、実装状況を記録する。
- **型**: 文字列（省略可。未設定時は `-`）
- **許容値と表示形式**:
  | 値 | バッジ | 意味 |
  |---|---|---|
  | `draft` | 📝 draft | 草案。まだ実装着手していない |
  | `in-progress` | 🚧 in-progress | 実装中 |
  | `implemented` | ✅ implemented | 実装済み |
  | `deprecated` | 🗑️ deprecated | 廃止予定 |

### 2. status コマンド
`spec-weaver status` コマンドにより、全アイテムのステータスを一覧表示する。
- **表示**: ID / タイトル / 実装ステータス（絵文字バッジ付き）/ レビューステータス / 最終更新日
- **レビューステータス**: Doorstopの `reviewed` / `cleared` 属性を評価し `⚠️ suspect` / `📋 unreviewed` / `✅ reviewed` を表示
- **最終更新日**: Gitの最終コミット日付を優先し、未取得時は YAML の `updated_at` 属性にフォールバック。どちらもない場合は `-` を表示
- **フィルタリング**: `--filter` オプションで特定ステータスのみを表示可能

### 3. build コマンドへの統合
生成されるドキュメントにステータスを反映する。
- **一覧ページ**: テーブルに「実装状況」列を追加
- **詳細ページ**: カバレッジ情報の直前に `**実装状況**: <バッジ>` を表示

### 🧪 検証シナリオ

- **全アイテムのステータスを一覧表示する** — Scenario （[features/status.feature:6](../features/status.md)）
- **status 未設定のアイテムは "-" と表示される** — Scenario （[features/status.feature:13](../features/status.md)）
- **--filter で特定ステータスに絞り込める** — Scenario （[features/status.feature:19](../features/status.md)）
- **--filter に一致するアイテムが存在しない場合に通知される** — Scenario （[features/status.feature:26](../features/status.md)）
- **レビューステータスと最終更新日が表示される** — Scenario （[features/status.feature:32](../features/status.md)）