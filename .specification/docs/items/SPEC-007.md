# [SPEC-007] 実装ステータス管理

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-02-26

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
- **表示**: ID / タイトル / 実装ステータス（絵文字バッジ付き）
- **フィルタリング**: `--filter` オプションで特定ステータスのみを表示可能

### 3. build コマンドへの統合
生成されるドキュメントにステータスを反映する。
- **一覧ページ**: テーブルに「実装状況」列を追加
- **詳細ページ**: カバレッジ情報の直前に `**実装状況**: <バッジ>` を表示

**テスト実行結果 (個別)**: ✅ 4/4 PASS

### 🧪 検証シナリオ

- ✅ PASS **全アイテムのステータスを一覧表示する** — Scenario （[features/status.feature:5](../features/status.md)）
- ✅ PASS **status 未設定のアイテムは "-" と表示される** — Scenario （[features/status.feature:12](../features/status.md)）
- ✅ PASS **--filter で特定ステータスに絞り込める** — Scenario （[features/status.feature:18](../features/status.md)）
- ✅ PASS **--filter に一致するアイテムが存在しない場合に通知される** — Scenario （[features/status.feature:25](../features/status.md)）