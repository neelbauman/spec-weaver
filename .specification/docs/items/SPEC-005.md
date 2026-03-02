# [SPEC-005] Suspect（変更波及）対応

> 🚫 **非活性 (active: false)**: このアイテムは非活性です。[QA-001](QA-001.md) に移行されました。

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-03-03

**上位アイテム**: [REQ-004](REQ-004.md) / **兄弟アイテム**: [SPEC-024](SPEC-024.md), [SPEC-025](SPEC-025.md)

**テスト対象**: Yes　**個別カバレッジ**: 🔴 0


### 内容

## 概要
DoorstopのSuspect機能を活用した変更波及の検知と可視化の仕様を定義する。

## 詳細仕様

### 処理
- Doorstop APIの `item.cleared`（suspect link 検出）および `item.reviewed`（未レビュー変更検出）属性を評価すること
  - item.reviewed is true and item.cleared is true, then review status is **reviewed**
  - item.reviewed is true and item.cleared is false, and related items is reviewed,  then review status is **suspect-with-reviewed**
  - item.reviewed is true and item.cleared is false, and related items have unreviewed ones,  then review status is **suspect-with-unreviewed**
  - item.reviewed is false and item.cleared is true, then review status is **unreviewed**
  - item.reviewed is false and item.cleared is false, and related items is reviewed,  then review status is **unreviewed, suspect-with-reviewed**
  - item.reviewed is false and item.cleared is false, and related items have unreviewed ones,  then review status is **unreviewed, suspect-with-unreviewed**
- `audit` コマンド実行時に Suspect Link / Unreviewed Changes を分離して警告出力すること
- `build` コマンド実行時に一覧テーブルの行ハイライト（Suspectは紫、Unreviewedは赤）および詳細ページに警告バナーを動的に付与すること
- Doorstop アイテムに加え、`.feature` ファイルも Unreviewed の対象とする:
  - Unreviewed:
    存在しない、または現在のファイル内容のハッシュと一致しない場合、
    その `.feature` ファイルを Unreviewed として audit テーブルに報告する

### `.feature` ファイルの Unreviewed 判定ロジック
1. ファイル先頭から `# spec-weaver-fingerprint: <hash>` コメントを読み取る
2. Feature / Background / 全 Scenario の構造コンテンツから現在のハッシュを計算する
   （コメント行自体はハッシュ計算から除外する）
3. 保存されたハッシュと現在のハッシュを比較し、不一致 or コメント未存在 → Unreviewed

### Doorstop アイテムの Suspect 判定ロジック（gherkin_fingerprints）
- SPEC YAML の `gherkin_fingerprints`（リスト）と、現在の Gherkin タグ付きシナリオのハッシュ（ファイル単位）を比較する
- 不一致の場合、またはリスト内のファイルパスと現在のタグマップが不整合な場合、その SPEC アイテムを Suspect として報告する
- Suspect 状態はレビュー状態（reviewed）に応じて以下の2種類に分類される：
  - **suspect-with-unreviewed**: アイテムが Suspect かつ `reviewed:
    この状態では `spec-weaver clear` を実行できない。まず `doorstop review` または `spec-weaver review` でレビューを完了させる必要がある。
  - **suspect-with-reviewed**: アイテムが Suspect かつ `reviewed:
    この状態でのみ `spec-weaver clear` による Suspect 解除が可能となる。
- `spec-weaver clear <SPEC_ID>` を実行することで `gherkin_fingerprints` が更新され Suspect が解除される

### 出力・結果
- audit の警告出力: Suspect Link テーブル（変更された上位アイテムとアクションを表示）、Unreviewed Changes テーブル（対象 ID とアクションを表示）
  - `.feature` ファイルも同テーブルに表示する（表示名はファイル名のみ、例: `scaffold.feature`）
  - Suspect の原因アイテムには、変更された SPEC ID を表示する
  - Unreviewed の `.feature` のアクションには、`spec-weaver review <feature_file>` を表示する
  - Suspect の SPEC のアクションには、`spec-weaver clear <SPEC_ID>` を表示する
- build の一覧テーブル: Suspect状態の行を紫色、Unreviewed状態の行を赤色でハイライト表示する。従来の状態列は廃止する。
- build の詳細ページ: Suspect Link バナー（対象リンク付き）、Unreviewed Changes バナーを表示

### 🧪 検証シナリオ

❌ まだ Gherkin シナリオが登録されていません。