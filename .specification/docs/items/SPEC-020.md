# [SPEC-020] trace コマンドへの実装ファイル表示の追加

**実装状況**: 🚧 in-progress

**作成日**: 2026-02-27　|　**更新日**: 2026-02-27

**上位アイテム**: [REQ-012](REQ-012.md) / **下位アイテム**: [PLAN-001](PLAN-001.md) / **兄弟アイテム**: [SPEC-017](SPEC-017.md), [SPEC-018](SPEC-018.md), [SPEC-019](SPEC-019.md)

**テストカバレッジ**:  - （下位アイテムの集計）

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
`spec-weaver trace` コマンドの出力ツリーに、SPECアイテムに紐づく
実装ファイル（`ref` フィールドおよびコードアノテーション）を表示する。

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
    └── 📁 src/spec_weaver/impl_scanner.py   ← ref フィールド由来
        └── 📁 src/spec_weaver/cli.py         ← アノテーション由来（アノテーションのみ）
```

### ファイルノードの表示情報
- `📁 <相対パス>` — ref フィールド由来
- `📝 <相対パス>` — コードアノテーション由来（ref に未記載）
- ファイルが存在しない場合は `❌ <パス> (not found)` と表示する

### 集約ルール
- `ref` フィールドとアノテーション両方に存在するファイルは `📁` として一度だけ表示する
- アノテーションのみのファイルは `📝` として表示する

### 🧪 検証シナリオ

- **仕様アイテムと実装ファイルのリンク管理** — Feature （[features/impl_link.feature:2](../features/impl_link.md)）
- **--show-impl オプションで trace ツリーに実装ファイルを表示する** — Scenario （[features/impl_link.feature:87](../features/impl_link.md)）
- **アノテーション由来のファイルも trace ツリーに表示される** — Scenario （[features/impl_link.feature:93](../features/impl_link.md)）
- **--show-impl なしでは実装ファイルは表示されない** — Scenario （[features/impl_link.feature:100](../features/impl_link.md)）