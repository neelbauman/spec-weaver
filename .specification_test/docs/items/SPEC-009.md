# [SPEC-009] build への実装状況統合

**実装状況**: ✅ implemented

**関連要件**: [REQ-006](REQ-006.md) / **兄弟仕様**: [SPEC-007](SPEC-007.md), [SPEC-008](SPEC-008.md)

**テスト対象**: No　**カバレッジ**: ⚪️ -


### 内容

## 概要
`spec-weaver build` で生成するMarkdownドキュメントに、
各アイテムの実装ステータスを反映する。

## 詳細仕様

### 一覧ページ（requirements.md / specifications.md）
- テーブルに「実装状況」列を追加する
- カバレッジ列の直後（状態列の前）に配置する
- 未設定の場合は `-` と表示する

### 個別詳細ページ（items/SPEC-XXX.md）
- Suspect警告バナーの直後に `**実装状況**: <バッジ>` を表示する
- カバレッジバッジより前（冒頭に近い位置）に配置する

### バッジ形式
| status 値 | 表示テキスト |
|---|---|
| `draft` | 📝 draft |
| `in-progress` | 🚧 in-progress |
| `implemented` | ✅ implemented |
| `deprecated` | 🗑️ deprecated |
| 未設定 | `-` |
