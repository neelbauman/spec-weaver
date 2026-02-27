# [SPEC-018] コードアノテーションスキャンによる実装ファイル検出

**実装状況**: 🚧 in-progress

**作成日**: 2026-02-27　|　**更新日**: 2026-02-27

**上位アイテム**: [REQ-012](REQ-012.md) / **下位アイテム**: [PLAN-001](PLAN-001.md) / **兄弟アイテム**: [SPEC-017](SPEC-017.md), [SPEC-019](SPEC-019.md), [SPEC-020](SPEC-020.md)

**テストカバレッジ**:  - （下位アイテムの集計）

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
ソースファイルに記述されたアノテーション（`# implements: SPEC-001` 等）を
スキャンし、仕様IDと実装ファイルの対応を自動抽出する機能を提供する。

## 詳細仕様

### アノテーション書式
ソースファイル内の任意の行に以下の形式で記述する。

```python
# implements: SPEC-001
# implements: SPEC-001, SPEC-002
# implements: SPEC-001, REQ-012
```

- コメント記号（`#`, `//`, `--` 等）の後に `implements:` キーワード
- スペースで区切り、仕様IDをカンマ区切りで列挙
- 複数IDの記述を許容する
- アノテーションのないファイルは警告なしとして扱う（エラーでない）

### スキャン対象
- デフォルト: リポジトリ内の全テキストファイル
- `--extensions` オプション: 拡張子でフィルタリング可能（例: `--extensions py,ts,tsx`）
- `.gitignore` 相当のパターンは除外対象とする（`.git/`, `__pycache__/` 等）

### 出力データ構造
スキャン結果は「仕様ID → ファイルパスのセット」のマッピングとして保持する。

```python
# 例
{
    "SPEC-001": {"src/spec_weaver/cli.py", "src/spec_weaver/doorstop.py"},
    "SPEC-018": {"src/spec_weaver/impl_scanner.py"},
}
```

### 実装モジュール
`src/spec_weaver/impl_scanner.py` に `ImplScanner` クラスとして実装する。

### 🧪 検証シナリオ

- **仕様アイテムと実装ファイルのリンク管理** — Feature （[features/impl_link.feature:2](../features/impl_link.md)）
- **アノテーションのスキャンで仕様IDとファイルの対応を抽出できる** — Scenario （[features/impl_link.feature:30](../features/impl_link.md)）
- **1行に複数の仕様IDを記述できる** — Scenario （[features/impl_link.feature:36](../features/impl_link.md)）
- **--extensions オプションでスキャン対象を絞れる** — Scenario （[features/impl_link.feature:43](../features/impl_link.md)）
- **アノテーションがないファイルはエラーにならない** — Scenario （[features/impl_link.feature:50](../features/impl_link.md)）