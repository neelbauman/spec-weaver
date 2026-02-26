# Spec-Weaver

Spec-Weaverは、**Doorstop**（テキストベースの要件管理）と **Gherkin**（実行可能な振る舞い駆動テスト）をシームレスに統合し、仕様と実装の完全なトレーサビリティを保証するCLIツールです。

仕様書とテストコードの乖離（リンク切れ、実装漏れ、不要なテストの残留）を CI/CD やローカル環境で瞬時に検知します。

## ✨ 特徴

- **堅牢なAST解析**: 正規表現への依存を排除。公式のGherkinパーサーを使用して抽象構文木（AST）から安全にタグを抽出します。
- **高速な差分検知**: Doorstopの仕様データベースとテストコードのタグを集合演算で比較し、「未実装の仕様」と「孤児となったテスト」を即座に割り出します。
- **美しいターミナルUI**: `Rich` ライブラリによる見やすいエラーレポートで、開発者の体験（DX）を向上させます。
- **柔軟な除外設定**: 自動テストが不可能な非機能要件などを、YAMLのカスタム属性で柔軟に監査対象から除外できます。

## 📦 インストール

現在、ソースコードからのインストールに対応しています。Python 3.10以上が必要です。

```bash
# リポジトリをクローンまたはダウンロードし、ディレクトリへ移動
git clone <your-repo-url>
cd spec-weaver

# 開発モードでインストール（実行可能コマンドがパスに追加されます）
uv tool install .

```

## 🚀 使い方

### 1. 仕様とテストの紐付けルール

Doorstopの仕様書（YAML）で発番されたIDを、Gherkin（`.feature`）の **タグ** として記述することで両者を紐付けます。

**Doorstop側 (`specs/SPEC-001.yml`)**

```yaml
active: true
testable: true
text: |
  パスワードはハッシュ化して保存すること。

```

**Gherkin側 (`features/login.feature`)**

```gherkin
@SPEC-001
Feature: ユーザー認証
  Scenario: 正しいパスワードでのログイン
    Given ...

```

### 2. 監査（Audit）コマンドの実行

`audit` コマンドを使用して、仕様とテストの乖離をチェックします。

```bash
# 基本的な実行（カレントディレクトリをプロジェクトルートとする場合）
spec-weaver audit ./features

# モノレポ環境などで、Doorstopのルートディレクトリが別にある場合
spec-weaver audit ./backend/tests/features --repo-root ./docs/doorstop

# プレフィックスを変更する場合（デフォルトは "SPEC"）
spec-weaver audit ./features --prefix REQ

```

### 3. 出力例

仕様と実装に乖離がある場合、エラー（終了コード1）と共に詳細な表が出力されます。

```text
❌ テストが実装されていない仕様 (Untested Specs):
Missing Spec ID
---------------
SPEC-002

⚠️ 仕様書に存在しない孤児タグ (Orphaned Tags):
Orphaned Tag
---------------
@SPEC-003

```

乖離がない場合は、成功メッセージ（終了コード0）が出力されます。

## ⚙️ 高度な設定（テスト対象外の仕様）

「UIのカラーコード」や「ライセンス表記」など、Gherkinでの振る舞いテストが不可能な仕様は、DoorstopのYAMLファイルに `testable: false` 属性を追記することで、Spec-Weaverの監査対象から除外できます。

```yaml
# SPEC-005.yml
active: true
testable: false
text: |
  ログインボタンの背景色は青色とすること。

```

## 🛠 開発者向け情報

テストの実行には `pytest` を使用します。

```bash
# 開発用依存ライブラリのインストール
pip install -e ".[dev]"

# テストの実行
pytest -v tests/

```
