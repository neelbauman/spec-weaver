# [SPEC-017] impl_files カスタム属性による実装ファイル参照の定義

> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: `./specification/features/impl_link.feature`

**実装状況**: ✅ implemented

**作成日**: 2026-02-27　|　**更新日**: 2026-03-02

**上位アイテム**: [REQ-012](REQ-012.md) / **下位アイテム**: [PLAN-001](PLAN-001.md) / **兄弟アイテム**: [SPEC-018](SPEC-018.md), [SPEC-019](SPEC-019.md), [SPEC-020](SPEC-020.md)

**テストカバレッジ**:  - （下位アイテムの集計）

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
DoorstopのYAMLアイテムにカスタム属性 `IMPL_FILES` を追加し、
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

- **impl_files にリスト形式でファイルパスを記述できる** — Scenario （`./specification/features/impl_link.feature:17`）
- **impl_files が未設定の場合はリンクなしとして扱われる** — Scenario （`./specification/features/impl_link.feature:23`）
- **アノテーションのスキャンで仕様IDとファイルの対応を抽出できる** — Scenario （`./specification/features/impl_link.feature:31`）
- **1行に複数の仕様IDを記述できる** — Scenario （`./specification/features/impl_link.feature:37`）
- **--extensions オプションでスキャン対象を絞れる** — Scenario （`./specification/features/impl_link.feature:44`）
- **アノテーションがないファイルはエラーにならない** — Scenario （`./specification/features/impl_link.feature:51`）
- **--check-impl オプションで存在しないファイルへの impl_files を検出する** — Scenario （`./specification/features/impl_link.feature:59`）
- **impl_files にあってアノテーションがない場合は警告を報告する** — Scenario （`./specification/features/impl_link.feature:66`）
- **アノテーションがあって impl_files がない場合は警告を報告する** — Scenario （`./specification/features/impl_link.feature:73`）
- **--check-impl なしでは実装リンク検証は実行されない** — Scenario （`./specification/features/impl_link.feature:80`）
- **--show-impl オプションで trace ツリーに実装ファイルを表示する** — Scenario （`./specification/features/impl_link.feature:88`）
- **アノテーション由来のファイルも trace ツリーに表示される** — Scenario （`./specification/features/impl_link.feature:94`）
- **--show-impl なしでは実装ファイルは表示されない** — Scenario （`./specification/features/impl_link.feature:101`）