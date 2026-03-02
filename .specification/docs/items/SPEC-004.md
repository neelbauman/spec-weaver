# [SPEC-004] build コマンド仕様

> ⚠️ **Suspect**: 関連するアイテムやテストが変更されました。影響範囲のレビューが必要です。
> **原因 (Unreviewed)**: `./specification/features/build.feature`

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

### 🧪 検証シナリオ

- **MkDocs設定ファイルの生成** — Scenario （`./specification/features/build.feature:7`）
- **要件一覧ページの生成** — Scenario （`./specification/features/build.feature:13`）
- **仕様一覧ページの生成** — Scenario （`./specification/features/build.feature:20`）
- **個別アイテム詳細ページの生成** — Scenario （`./specification/features/build.feature:27`）
- **一覧テーブルのフィルタリング機能** — Scenario （`./specification/features/build.feature:36`）
- **出力ディレクトリの独立性** — Scenario （`./specification/features/build.feature:42`）
- **カスタム出力ディレクトリの指定** — Scenario （`./specification/features/build.feature:48`）
- **feature MDページへのバックリンク生成** — Scenario （`./specification/features/build.feature:54`）
- **複数アイテムを参照するfeatureのバックリンク** — Scenario （`./specification/features/build.feature:61`）
- **タグのないfeatureにはバックリンクを表示しない** — Scenario （`./specification/features/build.feature:67`）
- **Suspect Link 警告の一覧テーブル表示** — Scenario （`./specification/features/build.feature:73`）
- **Unreviewed Changes 警告の一覧テーブル表示** — Scenario （`./specification/features/build.feature:80`）
- **複合警告の表示** — Scenario （`./specification/features/build.feature:87`）