# [SPEC-012] build コマンドにおけるタイムスタンプ表示

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-02-26

**上位アイテム**: [REQ-010](REQ-010.md) / **兄弟アイテム**: [SPEC-011](SPEC-011.md), [SPEC-013](SPEC-013.md)

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
`spec-weaver build` で生成するドキュメントの一覧テーブルおよび詳細ページに
タイムスタンプ（作成日・更新日）を表示する。

## 詳細仕様

### 1. 一覧テーブルへの列追加

既存の一覧テーブル（`_generate_index_table`）に以下の2列を追加する。

| 追加列 | 表示内容 | 未設定時 |
|---|---|---|
| **作成日** | `created_at` の値（`YYYY-MM-DD`） | `-` |
| **更新日** | `updated_at` の値（`YYYY-MM-DD`） | `-` |

- 列の挿入位置: 「実装状況」列の後、「状態」列の前とする。

### 2. 詳細ページへの表示

個別アイテム詳細ページ（`_generate_item_markdown`）に以下を追加する。
- **表示位置**: 実装状況バッジの直後
- **表示形式**: `**作成日**: YYYY-MM-DD　|　**更新日**: YYYY-MM-DD`
- 未設定の場合は `"-"` を表示する。

### 3. 表示形式

- 日付は `YYYY-MM-DD` 形式でそのまま表示する（ロケール変換は行わない）。
- 両方未設定の場合でも列・行は表示し、`-` で埋める。

**テスト実行結果 (個別)**: ✅ 3/3 PASS

### 🧪 検証シナリオ

- ✅ PASS **一覧テーブルにタイムスタンプ列が表示される** — Scenario （[features/timestamp.feature:33](../features/timestamp.md)）
- ✅ PASS **詳細ページにタイムスタンプが表示される** — Scenario （[features/timestamp.feature:41](../features/timestamp.md)）
- ✅ PASS **Git情報がない場合の一覧テーブル表示** — Scenario （[features/timestamp.feature:48](../features/timestamp.md)）