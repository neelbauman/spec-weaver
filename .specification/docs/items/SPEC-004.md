# [SPEC-004] build コマンド仕様

**関連要件**: [REQ-003](REQ-003.md)

**テスト対象**: Yes

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
- `docs/index.md`: トップページ
- `docs/requirements.md`: 要件一覧テーブル（相互リンク付き）
- `docs/specifications.md`: 仕様一覧テーブル（相互リンク付き）
- `docs/items/{ID}.md`: 各アイテムの詳細ページ（本文、上位/下位リンク、テストファイルパス）

### 🧪 検証シナリオ
- **build コマンド** (`specification/features/build.feature:2`)