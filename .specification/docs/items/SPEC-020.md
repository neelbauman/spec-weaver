# [SPEC-020] trace コマンドへの実装ファイル表示の追加

**実装状況**: ✅ implemented

**作成日**: 2026-02-27　|　**更新日**: 2026-03-02

**上位アイテム**: [REQ-012](REQ-012.md) / **下位アイテム**: [PLAN-001](PLAN-001.md) / **兄弟アイテム**: [SPEC-017](SPEC-017.md), [SPEC-018](SPEC-018.md), [SPEC-019](SPEC-019.md)

**テストカバレッジ**:  - （下位アイテムの集計）

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
`spec-weaver trace` コマンドの出力ツリーに、SPECアイテムに紐づく
実装ファイル（`impl_files` フィールドおよびコードアノテーション）を表示する。

## 詳細仕様

### 新オプション
```
spec-weaver trace <ITEM-ID> [OPTIONS]
  --show-impl           実装ファイルをツリーに表示（デフォルト: 無効）
  --extensions TEXT     アノテーションスキャン対象の拡張子（カンマ区切り）
```

### 表示形式
SPECノードの子要素として、実装ファイルを `📁` アイコンで表示する。

```
REQ-012 仕様アイテムと実装ファイルのリンク管理 🚧 in-progress
└── ★ SPEC-018 コードアノテーションスキャン 🚧 in-progress
    ├── 🥒 impl_link.feature
    │   └── Scenario: アノテーションのスキャン
    └── 📁 src/spec_weaver/impl_scanner.py   ← impl_files フィールド由来
        └── 📁 src/spec_weaver/cli.py         ← アノテーション由来（アノテーションのみ）
```

### ファイルノードの表示情報
- `📁 <相対パス>` — impl_files フィールド由来
- `📝 <相対パス>` — コードアノテーション由来（impl_files に未記載）
- ファイルが存在しない場合は `❌ <パス> (not found)` と表示する

### 集約ルール
- `impl_files` フィールドとアノテーション両方に存在するファイルは `📁` として一度だけ表示する
- アノテーションのみのファイルは `📝` として表示する

### 🧪 検証シナリオ

- **impl_files にリスト形式でファイルパスを記述できる** — Scenario （[features/impl_link.feature:17](../features/impl_link.md)）
- **impl_files が未設定の場合はリンクなしとして扱われる** — Scenario （[features/impl_link.feature:23](../features/impl_link.md)）
- **アノテーションのスキャンで仕様IDとファイルの対応を抽出できる** — Scenario （[features/impl_link.feature:31](../features/impl_link.md)）
- **1行に複数の仕様IDを記述できる** — Scenario （[features/impl_link.feature:37](../features/impl_link.md)）
- **--extensions オプションでスキャン対象を絞れる** — Scenario （[features/impl_link.feature:44](../features/impl_link.md)）
- **アノテーションがないファイルはエラーにならない** — Scenario （[features/impl_link.feature:51](../features/impl_link.md)）
- **--check-impl オプションで存在しないファイルへの impl_files を検出する** — Scenario （[features/impl_link.feature:59](../features/impl_link.md)）
- **impl_files にあってアノテーションがない場合は警告を報告する** — Scenario （[features/impl_link.feature:66](../features/impl_link.md)）
- **アノテーションがあって impl_files がない場合は警告を報告する** — Scenario （[features/impl_link.feature:73](../features/impl_link.md)）
- **--check-impl なしでは実装リンク検証は実行されない** — Scenario （[features/impl_link.feature:80](../features/impl_link.md)）
- **--show-impl オプションで trace ツリーに実装ファイルを表示する** — Scenario （[features/impl_link.feature:88](../features/impl_link.md)）
- **アノテーション由来のファイルも trace ツリーに表示される** — Scenario （[features/impl_link.feature:94](../features/impl_link.md)）
- **--show-impl なしでは実装ファイルは表示されない** — Scenario （[features/impl_link.feature:101](../features/impl_link.md)）