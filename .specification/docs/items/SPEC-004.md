# [SPEC-004] build コマンド仕様

> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: [build.feature](../features/build.md)

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-03-01

**上位アイテム**: [REQ-003](REQ-003.md) / **兄弟アイテム**: [SPEC-014](SPEC-014.md)

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
相互リンク付きのMkDocsドキュメントサイトを自動生成する `build` コマンドの仕様を定義する。

## 詳細仕様

### 入力
- `feature_dir` (必須): Gherkin `.feature` ファイルが格納されたディレクトリパス
- `--repo-root` / `-r` (オプション): Doorstopプロジェクトルート（デフォルト: カレントディレクトリ）
- `--out-dir` / `-o` (オプション): 出力ディレクトリ（デフォルト: `.specification`）
- `--prefix` / `-p` (オプション): 仕様IDプレフィックス（デフォルト: "SPEC"）

### 出力構造
- プロジェクトの既存ドキュメントを汚染しないよう、指定ディレクトリに独立したMkDocs環境一式を生成する
- 1アイテム1Markdownファイルの分散構成（ファイル肥大化の防止）

### 生成されるファイル
- `mkdocs.yml`: MkDocs設定ファイル（Material テーマ、Mermaid対応）
- `docs/index.md`: トップページ。プロジェクトのドキュメント階層（REQ, SPECなど）を表示し、それぞれの一覧ページへのリンクを提供する。具体的なアイテム一覧は表示せず、階層構造のみを示す。
- `docs/{prefix}.md`: 各ドキュメントの一覧テーブル（例: `req.md`, `spec.md`）。相互リンク付き。
- `docs/items/{ID}.md`: 各アイテムの詳細ページ（本文、上位/下位リンク、テストファイルパス）

**テスト実行結果 (個別)**: ✅ 13/13 PASS

### 🧪 検証シナリオ

- ✅ PASS **MkDocs設定ファイルの生成** — Scenario （[features/build.feature:6](../features/build.md)）
- ✅ PASS **要件一覧ページの生成** — Scenario （[features/build.feature:12](../features/build.md)）
- ✅ PASS **仕様一覧ページの生成** — Scenario （[features/build.feature:19](../features/build.md)）
- ✅ PASS **個別アイテム詳細ページの生成** — Scenario （[features/build.feature:26](../features/build.md)）
- ✅ PASS **一覧テーブルのフィルタリング機能** — Scenario （[features/build.feature:35](../features/build.md)）
- ✅ PASS **出力ディレクトリの独立性** — Scenario （[features/build.feature:41](../features/build.md)）
- ✅ PASS **カスタム出力ディレクトリの指定** — Scenario （[features/build.feature:47](../features/build.md)）
- ✅ PASS **feature MDページへのバックリンク生成** — Scenario （[features/build.feature:53](../features/build.md)）
- ✅ PASS **複数アイテムを参照するfeatureのバックリンク** — Scenario （[features/build.feature:60](../features/build.md)）
- ✅ PASS **タグのないfeatureにはバックリンクを表示しない** — Scenario （[features/build.feature:66](../features/build.md)）
- ✅ PASS **Suspect Link 警告の一覧テーブル表示** — Scenario （[features/build.feature:72](../features/build.md)）
- ✅ PASS **Unreviewed Changes 警告の一覧テーブル表示** — Scenario （[features/build.feature:79](../features/build.md)）
- ✅ PASS **複合警告の表示** — Scenario （[features/build.feature:86](../features/build.md)）