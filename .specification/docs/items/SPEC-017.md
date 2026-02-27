# [SPEC-017] impl_files カスタム属性による実装ファイル参照の定義

**実装状況**: 🚧 in-progress

**作成日**: 2026-02-27　|　**更新日**: 2026-02-27

**上位アイテム**: [REQ-012](REQ-012.md) / **下位アイテム**: [PLAN-001](PLAN-001.md) / **兄弟アイテム**: [SPEC-018](SPEC-018.md), [SPEC-019](SPEC-019.md), [SPEC-020](SPEC-020.md)

**テストカバレッジ**:  - （下位アイテムの集計）

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
DoorstopのYAMLアイテムにカスタム属性 `impl_files` を追加し、
実装ファイルパスのリストを記録する規約を定める。

## 詳細仕様

### なぜ `ref` ではなく `impl_files` を使うか
Doorstopの組み込み `ref` フィールドは文字列専用（内部で `.strip()` 等を呼ぶ）のため、
リスト形式を格納するとエラーになる。
独自のカスタム属性 `impl_files` を用いることで Doorstop と共存できる。

### impl_files フィールドの形式
`impl_files` フィールドには、YAML リスト形式で実装ファイルのパスを記述する。
パスはリポジトリルートからの相対パスとする。

```yaml
# 単一ファイル
impl_files:
  - src/spec_weaver/cli.py

# 複数ファイル
impl_files:
  - src/spec_weaver/cli.py
  - src/spec_weaver/doorstop.py

# 記述なし（リンクなし）— エラーにしない
# impl_files フィールド自体を省略してよい
```

### バリデーション
- `impl_files` に記載されたパスが実際にリポジトリ内に存在するかを検証できること
- 存在しないパスは `audit --check-impl` 実行時に警告として報告すること

### 後方互換性
- `impl_files` フィールドがない（既存アイテム）場合は「リンクなし」として扱い、エラーにしないこと
- 文字列形式で記述されている場合は、単一要素リストとして解釈すること

### 🧪 検証シナリオ

- **仕様アイテムと実装ファイルのリンク管理** — Feature （[features/impl_link.feature:2](../features/impl_link.md)）
- **impl_files にリスト形式でファイルパスを記述できる** — Scenario （[features/impl_link.feature:16](../features/impl_link.md)）
- **impl_files が未設定の場合はリンクなしとして扱われる** — Scenario （[features/impl_link.feature:22](../features/impl_link.md)）