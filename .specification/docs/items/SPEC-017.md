# [SPEC-017] impl_files カスタム属性による実装ファイル参照の定義

> 📋 **Unreviewed Changes**: このアイテム自体または関連するテストに未レビューの変更があります。

> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: [impl_link.feature](../features/impl_link.md)

**実装状況**: ✅ implemented

**作成日**: 2026-02-27　|　**更新日**: 2026-03-01

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

**テスト実行結果 (集計)**: -

**テスト実行結果 (個別)**: ✅ 13/13 PASS

### 🧪 検証シナリオ

- ✅ PASS **impl_files にリスト形式でファイルパスを記述できる** — Scenario （[features/impl_link.feature:16](../features/impl_link.md)）
- ✅ PASS **impl_files が未設定の場合はリンクなしとして扱われる** — Scenario （[features/impl_link.feature:22](../features/impl_link.md)）
- ✅ PASS **アノテーションのスキャンで仕様IDとファイルの対応を抽出できる** — Scenario （[features/impl_link.feature:30](../features/impl_link.md)）
- ✅ PASS **1行に複数の仕様IDを記述できる** — Scenario （[features/impl_link.feature:36](../features/impl_link.md)）
- ✅ PASS **--extensions オプションでスキャン対象を絞れる** — Scenario （[features/impl_link.feature:43](../features/impl_link.md)）
- ✅ PASS **アノテーションがないファイルはエラーにならない** — Scenario （[features/impl_link.feature:50](../features/impl_link.md)）
- ✅ PASS **--check-impl オプションで存在しないファイルへの impl_files を検出する** — Scenario （[features/impl_link.feature:58](../features/impl_link.md)）
- ✅ PASS **impl_files にあってアノテーションがない場合は警告を報告する** — Scenario （[features/impl_link.feature:65](../features/impl_link.md)）
- ✅ PASS **アノテーションがあって impl_files がない場合は警告を報告する** — Scenario （[features/impl_link.feature:72](../features/impl_link.md)）
- ✅ PASS **--check-impl なしでは実装リンク検証は実行されない** — Scenario （[features/impl_link.feature:79](../features/impl_link.md)）
- ✅ PASS **--show-impl オプションで trace ツリーに実装ファイルを表示する** — Scenario （[features/impl_link.feature:87](../features/impl_link.md)）
- ✅ PASS **アノテーション由来のファイルも trace ツリーに表示される** — Scenario （[features/impl_link.feature:93](../features/impl_link.md)）
- ✅ PASS **--show-impl なしでは実装ファイルは表示されない** — Scenario （[features/impl_link.feature:100](../features/impl_link.md)）