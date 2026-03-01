# [SPEC-005] Suspect（変更波及）対応

> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: [audit.feature](../features/audit.md), [build.feature](../features/build.md)

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-03-01

**上位アイテム**: [REQ-004](REQ-004.md)

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
DoorstopのSuspect機能を活用した変更波及の検知と可視化の仕様を定義する。

## 詳細仕様

### 処理
- Doorstop APIの `item.cleared`（suspect link 検出）および `item.reviewed`（未レビュー変更検出）属性を評価すること
- `audit` コマンド実行時に Suspect Link / Unreviewed Changes を分離して警告出力すること
- `build` コマンド実行時に一覧テーブルの行ハイライト（Suspectは赤、Unreviewedは紫）および詳細ページに警告バナーを動的に付与すること

### 出力・結果
- audit の警告出力: Suspect Link テーブル（変更された上位アイテムとアクションを表示）、Unreviewed Changes テーブル（対象 ID とアクションを表示）
- build の一覧テーブル: Suspect状態の行を赤色、Unreviewed状態の行を紫色でハイライト表示する。従来の状態列は廃止する。
- build の詳細ページ: Suspect Link バナー（対象リンク付き）、Unreviewed Changes バナーを表示

**テスト実行結果 (個別)**: ✅ 5/5 PASS

### 🧪 検証シナリオ

- ✅ PASS **Suspect Link の検出** — Scenario （[features/audit.feature:36](../features/audit.md)）
- ✅ PASS **Unreviewed Changes の検出** — Scenario （[features/audit.feature:44](../features/audit.md)）
- ✅ PASS **Suspect Link 警告の一覧テーブル表示** — Scenario （[features/build.feature:72](../features/build.md)）
- ✅ PASS **Unreviewed Changes 警告の一覧テーブル表示** — Scenario （[features/build.feature:79](../features/build.md)）
- ✅ PASS **複合警告の表示** — Scenario （[features/build.feature:86](../features/build.md)）