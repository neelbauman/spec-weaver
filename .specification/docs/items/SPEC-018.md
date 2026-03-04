# [SPEC-018] コードアノテーションスキャンによる実装ファイル検出

> 🚫 **非活性 (active: false)**: このアイテムは非活性です。[TRC-003](TRC-003.md) に移行されました。

> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: `Doorstop native suspect link`

**実装状況**: ✅ implemented

**作成日**: 2026-02-27　|　**更新日**: 2026-03-03

**上位アイテム**: [REQ-012](REQ-012.md) / **兄弟アイテム**: [SPEC-017](SPEC-017.md), [SPEC-019](SPEC-019.md), [SPEC-020](SPEC-020.md)

**テスト対象**: Yes
 / **テストカバレッジ**: -

---

## 概要
ソースファイルに記述されたアノテーション（`# implements: SPEC-001` 等）を
スキャンし、仕様IDと実装ファイルの対応を自動抽出する機能を提供する。

## 詳細仕様

### アノテーション書式
ソースファイル内の任意の行に以下の形式で記述する。

```python
# implements: SPEC-001
# implements: SPEC-001, CORE-001
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
    "TRC-003": {"src/spec_weaver/impl_scanner.py"},
}
```

### 実装モジュール
`src/spec_weaver/impl_scanner.py` に `ImplScanner` クラスとして実装する。

**テスト実行結果**: -

### 🧪 検証シナリオ

❌ Gherkin シナリオが登録されていません。