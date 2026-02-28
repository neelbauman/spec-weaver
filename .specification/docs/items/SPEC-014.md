# [SPEC-014] feature MDページのバックリンク生成

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-02-26

**上位アイテム**: [REQ-003](REQ-003.md) / **兄弟アイテム**: [SPEC-004](SPEC-004.md)

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
`build` コマンドが生成する `.feature` → Markdown 変換ページの冒頭に、
そのfeatureを参照しているDoorstopアイテム（SPEC, REQ等）への
バックリンクセクションを自動生成する。

## 背景・動機
Gherkinのfeatureファイルにはタグ（`@SPEC-003` 等）で仕様IDが紐付けられているが、
生成されたfeature MDページからは元のDoorstopアイテムへ戻る手段がなかった。
双方向のナビゲーションを提供することで、仕様書としての利便性を向上させる。

## 詳細仕様

### バックリンクマップの構築
- `tag_map`（`spec_id → [ScenarioInfo]`）を逆引きし、
  `feature_path → [uid, ...]` のマッピング（`feature_backlink_map`）を生成する
- 同一featureを参照する複数UIDは重複排除の上、ソートして格納する

### Markdown出力
- feature MDの冒頭（タグ行の直下）に「関連アイテム」行を追記する
- フォーマット: `**関連アイテム**: [UID](../items/UID.md) / [UID2](../items/UID2.md)`
- 関連アイテムが存在しない場合は当該行を出力しない

## 受け入れ基準
- `@SPEC-003` タグを持つfeatureのMDページに `[SPEC-003](../items/SPEC-003.md)` リンクが含まれること
- 複数アイテムが同一featureを参照する場合、全UIDのリンクが「/」区切りで表示されること
- どのアイテムにも参照されていないfeatureにはバックリンク行が表示されないこと

**テスト実行結果 (個別)**: ✅ 3/3 PASS

### 🧪 検証シナリオ

- ✅ PASS **feature MDページへのバックリンク生成** — Scenario （[features/build.feature:53](../features/build.md)）
- ✅ PASS **複数アイテムを参照するfeatureのバックリンク** — Scenario （[features/build.feature:60](../features/build.md)）
- ✅ PASS **タグのないfeatureにはバックリンクを表示しない** — Scenario （[features/build.feature:66](../features/build.md)）