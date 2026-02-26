# [SPEC-007] status カスタム属性の定義

**実装状況**: ✅ implemented

**関連要件**: [REQ-006](REQ-006.md) / **兄弟仕様**: [SPEC-008](SPEC-008.md), [SPEC-009](SPEC-009.md)

**テスト対象**: No　**カバレッジ**: ⚪️ -


### 内容

## 概要
DoorstopのYAMLファイルに `status` カスタム属性を追記することで、
各アイテムの実装進行状況を管理する。

## 詳細仕様

### フィールド定義
- キー名: `status`
- 型: 文字列
- 省略可（未設定のアイテムは `-` として扱う）

### 許容値
| 値 | バッジ | 意味 |
|---|---|---|
| `draft` | 📝 draft | 草案。まだ実装着手していない |
| `in-progress` | 🚧 in-progress | 実装中 |
| `implemented` | ✅ implemented | 実装済み |
| `deprecated` | 🗑️ deprecated | 廃止予定 |

### 書き方
`doorstop add` で生成したYAMLに手動で追記する:
```yaml
active: true
status: in-progress
text: |
  （仕様本文）
```

### 制約
- `status` フィールドはDoorstopが管理するフィールドではなくカスタム属性のため、
  `doorstop review` のfingerprintには影響しない
