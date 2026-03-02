# [SPEC-019] audit コマンドへの実装ファイルリンク検証の追加

> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: `./specification/features/impl_link.feature`

**実装状況**: ✅ implemented

**作成日**: 2026-02-27　|　**更新日**: 2026-03-02

**上位アイテム**: [REQ-012](REQ-012.md) / **下位アイテム**: [PLAN-001](PLAN-001.md) / **兄弟アイテム**: [SPEC-017](SPEC-017.md), [SPEC-018](SPEC-018.md), [SPEC-020](SPEC-020.md)

**テストカバレッジ**:  - （下位アイテムの集計）

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
`spec-weaver audit` コマンドに、DoorstopのYAML `ref` フィールドと
コードアノテーションの整合性を検証するセクションを追加する。

## 詳細仕様

### 新オプション
```
spec-weaver audit <feature-dir> [OPTIONS]
  --check-impl          実装ファイルリンクの検証を有効化（デフォルト: 無効）
  --extensions TEXT     スキャン対象の拡張子（カンマ区切り。例: py,ts）
                        未指定時は全テキストファイルを対象とする
```

### 検証ロジック

#### チェック1: refに記載されたファイルの存在確認
- `ref` リストに含まれるパスがリポジトリ内に実際に存在するか確認する
- 存在しないファイルは「壊れたリンク」として報告する

#### チェック2: refとアノテーションの双方向乖離検出
- YAML `ref` に記載されているがコードアノテーションがないファイル → 警告
- コードアノテーションがあるが YAML `ref` に記載されていないファイル → 警告

### 出力形式
既存の audit 出力に続いて、新しいセクションを追加する：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 実装ファイルリンクの検証
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 存在しないファイルへの ref:
   SPEC-001 → src/spec_weaver/old_file.py (not found)

⚠️  ref のみ（アノテーションなし）:
   SPEC-002 → src/spec_weaver/cli.py

⚠️  アノテーションのみ（ref なし）:
   SPEC-003 ← src/spec_weaver/gherkin.py

✅ リンク検証 完了
```

### 既存動作への影響
`--check-impl` が指定されない場合、既存の audit 動作は一切変わらない。

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