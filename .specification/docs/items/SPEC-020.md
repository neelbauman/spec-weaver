# [SPEC-020] trace コマンドへの実装ファイル表示の追加

**実装状況**: ✅ implemented

**作成日**: 2026-02-27　|　**更新日**: 2026-03-01

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