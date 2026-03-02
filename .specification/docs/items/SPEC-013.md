# [SPEC-013] タイムスタンプ鮮度の監査チェック

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-03-02

**上位アイテム**: [REQ-002](REQ-002.md), [REQ-010](REQ-010.md) / **兄弟アイテム**: [SPEC-002](SPEC-002.md), [SPEC-003](SPEC-003.md), [SPEC-011](SPEC-011.md), [SPEC-012](SPEC-012.md)

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
`spec-weaver audit` コマンドを拡張し、長期間更新されていないアイテムを
「stale（陳腐化の可能性）」として検出・警告する。

## 詳細仕様

### 1. Stale 判定ロジック

以下の条件をすべて満たすアイテムを stale と判定する。
- `active: true` である
- `status` が `deprecated` でない
- `updated_at` が設定されている
- `updated_at` から現在日付までの経過日数が閾値を超えている

**デフォルト閾値**: 90日

> `updated_at` が未設定のアイテムは stale 判定の対象外とする（警告しない）。
> タイムスタンプ運用が浸透していない既存アイテムへの過剰な警告を防ぐため。

### 2. CLI オプション

`spec-weaver audit` コマンドに以下のオプションを追加する。

| オプション | 型 | デフォルト | 説明 |
|---|---|---|---|
| `--stale-days` | int | 90 | stale 判定の閾値（日数）。0 で無効化 |

### 3. 出力形式

stale アイテムが検出された場合、既存の監査結果テーブルの後に
追加のテーブルを表示する。

```
⏰ Stale Items（90日以上未更新）
┌──────────┬────────────────────────┬────────────┬──────────┐
│ ID       │ タイトル               │ 最終更新日  │ 経過日数  │
├──────────┼────────────────────────┼────────────┼──────────┤
│ SPEC-002 │ データ抽出基盤          │ 2025-11-01 │ 117日    │
└──────────┴────────────────────────┴────────────┴──────────┘
```

### 4. 終了コードへの影響

- stale アイテムの検出のみでは終了コードを非ゼロにしない（警告扱い）。
- 既存の監査エラー（テスト漏れ・孤児タグ・Suspect）とは独立した報告とする。

### 🧪 検証シナリオ

- **stale アイテムの検出（Git履歴ベース）** — Scenario （[features/timestamp.feature:57](../features/timestamp.md)）
- **閾値内のアイテムは stale と判定されない** — Scenario （[features/timestamp.feature:65](../features/timestamp.md)）
- **Git情報もupdated_atもないアイテムは stale 判定の対象外** — Scenario （[features/timestamp.feature:71](../features/timestamp.md)）
- **deprecated アイテムは stale 判定の対象外** — Scenario （[features/timestamp.feature:77](../features/timestamp.md)）
- **--stale-days 0 で鮮度チェックを無効化** — Scenario （[features/timestamp.feature:84](../features/timestamp.md)）