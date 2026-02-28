# [SPEC-011] タイムスタンプ・カスタム属性の定義

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-02-26

**上位アイテム**: [REQ-010](REQ-010.md) / **兄弟アイテム**: [SPEC-012](SPEC-012.md), [SPEC-013](SPEC-013.md)

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
Doorstop YAMLにタイムスタンプ用のカスタム属性を定義し、アイテムの時系列情報を記録する。

## 詳細仕様

### 1. カスタム属性の定義

| 属性名 | 型 | 形式 | 省略 | デフォルト | 説明 |
|---|---|---|---|---|---|
| `created_at` | 文字列 | ISO 8601 (`YYYY-MM-DD`) | 可 | `null` | アイテム作成日 |
| `updated_at` | 文字列 | ISO 8601 (`YYYY-MM-DD`) | 可 | `null` | 最終更新日 |

### 2. YAMLでの記述例

```yaml
active: true
status: in-progress
created_at: '2026-01-15'
updated_at: '2026-02-20'
header: |
  ○○○○の仕様
text: |
  ...
```

### 3. 属性の自動取得（Git 履歴ベース）

`build` / `audit` 実行時に、Git コミット履歴からタイムスタンプを自動算出する。

- **`updated_at`**: `git log -1 --format=%aI -- <ファイルパス>` で最終コミット日を取得
- **`created_at`**: `git log --follow --diff-filter=A --format=%aI -- <ファイルパス>` で初回コミット日を取得
- 取得した値は `YYYY-MM-DD` に切り詰めて使用する

#### フォールバック順序

1. Git 履歴から取得（優先）
2. YAML の `created_at` / `updated_at` カスタム属性（Git 情報が取れない場合）
3. いずれもなければ `"-"` を表示

> YAML への手動記入は不要。Git リポジトリ外や未コミットファイルの場合のみ
> YAML 属性をフォールバックとして使用する。

### 4. 運用ルール

- **通常運用**: タイムスタンプは Git 履歴から自動取得されるため、手動管理は不要。
- **Git 外での利用**: YAML に `created_at` / `updated_at` を手動記入することで対応可能。
- **不変**: `created_at`（初回コミット日）は Git 履歴で自動的に不変となる。

**テスト実行結果 (個別)**: ✅ 12/12 PASS

### 🧪 検証シナリオ

- ✅ PASS **Git履歴から updated_at を自動取得する** — Scenario （[features/timestamp.feature:8](../features/timestamp.md)）
- ✅ PASS **Git履歴から created_at を自動取得する** — Scenario （[features/timestamp.feature:13](../features/timestamp.md)）
- ✅ PASS **Git情報がない場合はYAML属性にフォールバック** — Scenario （[features/timestamp.feature:18](../features/timestamp.md)）
- ✅ PASS **Git情報もYAML属性もない場合のフォールバック** — Scenario （[features/timestamp.feature:24](../features/timestamp.md)）
- ✅ PASS **一覧テーブルにタイムスタンプ列が表示される** — Scenario （[features/timestamp.feature:33](../features/timestamp.md)）
- ✅ PASS **詳細ページにタイムスタンプが表示される** — Scenario （[features/timestamp.feature:41](../features/timestamp.md)）
- ✅ PASS **Git情報がない場合の一覧テーブル表示** — Scenario （[features/timestamp.feature:48](../features/timestamp.md)）
- ✅ PASS **stale アイテムの検出（Git履歴ベース）** — Scenario （[features/timestamp.feature:56](../features/timestamp.md)）
- ✅ PASS **閾値内のアイテムは stale と判定されない** — Scenario （[features/timestamp.feature:64](../features/timestamp.md)）
- ✅ PASS **Git情報もupdated_atもないアイテムは stale 判定の対象外** — Scenario （[features/timestamp.feature:70](../features/timestamp.md)）
- ✅ PASS **deprecated アイテムは stale 判定の対象外** — Scenario （[features/timestamp.feature:76](../features/timestamp.md)）
- ✅ PASS **--stale-days 0 で鮮度チェックを無効化** — Scenario （[features/timestamp.feature:83](../features/timestamp.md)）