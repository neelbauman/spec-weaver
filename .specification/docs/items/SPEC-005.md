# [SPEC-005] Suspect（変更波及）対応

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-03-02

**上位アイテム**: [REQ-004](REQ-004.md) / **下位アイテム**: [PLAN-005](PLAN-005.md) / **兄弟アイテム**: [SPEC-024](SPEC-024.md), [SPEC-025](SPEC-025.md)

**テストカバレッジ**:  - （下位アイテムの集計）

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
DoorstopのSuspect機能を活用した変更波及の検知と可視化の仕様を定義する。

## 詳細仕様

### 処理
- Doorstop APIの `item.cleared`（suspect link 検出）および `item.reviewed`（未レビュー変更検出）属性を評価すること
- `audit` コマンド実行時に Suspect Link / Unreviewed Changes を分離して警告出力すること
- `build` コマンド実行時に一覧テーブルの行ハイライト（Suspectは紫、Unreviewedは赤）および詳細ページに警告バナーを動的に付与すること
- Doorstop アイテムに加え、`.feature` ファイルも Suspect / Unreviewed の対象とする:
  - Suspect: 対応 SPEC が未レビュー状態になった場合、その SPEC にタグ付けされた
    `.feature` ファイルも Suspect として audit テーブルに報告する
  - Unreviewed: `.feature` ファイル先頭の `# spec-weaver-fingerprint:` コメントが
    存在しない、または現在のファイル内容のハッシュと一致しない場合、
    その `.feature` ファイルを Unreviewed として audit テーブルに報告する

### `.feature` ファイルの Unreviewed 判定ロジック
1. ファイル先頭から `# spec-weaver-fingerprint: <hash>` コメントを読み取る
2. Feature / Background / 全 Scenario の構造コンテンツから現在のハッシュを計算する
   （コメント行自体はハッシュ計算から除外する）
3. 保存されたハッシュと現在のハッシュを比較し、不一致 or コメント未存在 → Unreviewed

### Doorstop アイテムの Suspect 判定ロジック（test_fingerprint）
- SPEC YAML の `test_fingerprint` と、現在の Gherkin タグ付きシナリオのハッシュを比較する
- 不一致の場合、その SPEC アイテムを Suspect として報告する
- `spec-weaver clear <SPEC_ID>` を実行することで `test_fingerprint` が更新され Suspect が解除される

### 出力・結果
- audit の警告出力: Suspect Link テーブル（変更された上位アイテムとアクションを表示）、Unreviewed Changes テーブル（対象 ID とアクションを表示）
  - `.feature` ファイルも同テーブルに表示する（表示名はファイル名のみ、例: `scaffold.feature`）
  - Suspect の原因アイテムには、変更された SPEC ID を表示する
  - Unreviewed の `.feature` のアクションには、`spec-weaver review <feature_file>` を表示する
  - Suspect の SPEC のアクションには、`spec-weaver clear <SPEC_ID>` を表示する
- build の一覧テーブル: Suspect状態の行を紫色、Unreviewed状態の行を赤色でハイライト表示する。従来の状態列は廃止する。
- build の詳細ページ: Suspect Link バナー（対象リンク付き）、Unreviewed Changes バナーを表示

**テスト実行結果 (集計)**: -

**テスト実行結果 (個別)**: ✅ 5/7 PASS

### 🧪 検証シナリオ

- ✅ PASS **Suspect Link 警告の一覧テーブル表示** — Scenario （[features/build.feature:73](../features/build.md)）
- ✅ PASS **Unreviewed Changes 警告の一覧テーブル表示** — Scenario （[features/build.feature:80](../features/build.md)）
- ✅ PASS **複合警告の表示** — Scenario （[features/build.feature:87](../features/build.md)）
- ✅ PASS **Suspect Link の検出** — Scenario （[features/audit.feature:37](../features/audit.md)）
- ✅ PASS **Unreviewed Changes の検出** — Scenario （[features/audit.feature:45](../features/audit.md)）
- - **feature ファイルが Suspect として検出される** — Scenario （[features/audit.feature:52](../features/audit.md)）
- - **feature ファイルが Unreviewed として検出される** — Scenario （[features/audit.feature:59](../features/audit.md)）