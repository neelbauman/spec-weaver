# [SPEC-005] Suspect（変更波及）対応

**関連要件**: [REQ-004](REQ-004.md)

**テスト対象**: No

### 内容

## 概要
DoorstopのSuspect機能を活用した変更波及の検知と可視化の仕様を定義する。

## 詳細仕様

### 処理
- Doorstop APIの `item.suspect` または `link.suspect` 属性を評価すること
- `audit` コマンド実行時にSuspect状態の仕様を警告として出力すること
- `build` コマンド実行時にテーブルのステータスや詳細ページに警告バッジを動的に付与すること

### 出力・結果
- auditの警告出力例: 「レビューが必要なSuspect仕様: SPEC-xxx」
- buildの詳細ページ: 警告バッジの表示

## ステータス
Phase 1（次期開発）- is_suspect() 判定ロジックは実装済み
