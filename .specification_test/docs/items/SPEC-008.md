# [SPEC-008] status コマンド仕様

**実装状況**: ✅ implemented

**関連要件**: [REQ-006](REQ-006.md) / **兄弟仕様**: [SPEC-007](SPEC-007.md), [SPEC-009](SPEC-009.md)

**テスト対象**: Yes　**カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
`spec-weaver status` コマンドで、リポジトリ内の全REQ・SPECの
実装ステータスをRichテーブル形式で一覧表示する。

## 詳細仕様

### コマンドシグネチャ
```
spec-weaver status [OPTIONS]
```

### オプション
| オプション | 短縮 | デフォルト | 説明 |
|---|---|---|---|
| `--repo-root PATH` | `-r` | カレントディレクトリ | Doorstopのプロジェクトルート |
| `--filter TEXT` | `-f` | なし | 表示するステータスで絞り込む |

### 出力仕様
- REQ・SPECそれぞれ別テーブルで表示する
- 各行: ID / タイトル / 実装ステータス（絵文字バッジ付き）
- `status` 未設定のアイテムは `-` と表示する
- `--filter` 指定時は一致するステータスのアイテムのみ表示する
- 一致するアイテムが0件の場合はその旨を通知する
- 末尾にステータス更新方法のヒントを表示する

### 🧪 検証シナリオ

- **status コマンド** — Feature （[features/status.feature:2](../features/status.md)）