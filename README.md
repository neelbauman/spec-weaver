# Spec-Weaver

Spec-Weaverは、**Doorstop**（テキストベースの要件管理）と **Gherkin**（実行可能な振る舞い駆動テスト）をシームレスに統合し、仕様と実装の完全なトレーサビリティを保証するCLIツールです。

仕様書とテストコードの乖離（リンク切れ、実装漏れ、不要なテストの残留）を CI/CD やローカル環境で瞬時に検知します。

## ✨ 特徴

- **堅牢なAST解析**: 正規表現への依存を排除。公式のGherkinパーサーを使用して抽象構文木（AST）から安全にタグを抽出します。
- **高速な差分検知**: Doorstopの仕様データベースとテストコードのタグを集合演算で比較し、「未実装の仕様」と「孤児となったテスト」を即座に割り出します。
- **美しいターミナルUI**: `Rich` ライブラリによる見やすいエラーレポートで、開発者の体験（DX）を向上させます。
- **柔軟な除外設定**: 自動テストが不可能な非機能要件などを、YAMLのカスタム属性で柔軟に監査対象から除外できます。
- **実装ステータス管理**: YAMLの `status` 属性で実装状況を追跡し、`status` コマンドで一覧・フィルタリング表示します。
- **トレーサビリティ探索**: `trace` コマンドで任意のアイテムを起点に上位要件〜下位仕様〜Gherkinシナリオを階層ツリー表示します。
- **Living Documentation**: `build` コマンドでカバレッジ・テスト結果・相互リンクを統合したドキュメントサイトを自動生成します。

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
links:
- REQ-001
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

### 2. 監査（`audit`）コマンド

仕様とテストの乖離をチェックします。終了コード0（問題なし）/ 1（乖離あり）を返すため、CIに組み込めます。

```bash
# 基本的な実行
spec-weaver audit ./features

# プロジェクトルートが別の場所にある場合
spec-weaver audit ./backend/tests/features --repo-root ./docs/doorstop

# プレフィックスを限定する場合
spec-weaver audit ./features --prefix REQ
```

乖離がある場合の出力例：

```
❌ テストが実装されていない仕様 (Untested Specs):
  SPEC-002

⚠️ 仕様書に存在しない孤児タグ (Orphaned Tags):
  @SPEC-003
```

### 3. 実装ステータス管理（`status`）コマンド

DoorstopのYAMLに `status` カスタム属性を追記することで、実装状況を管理できます。

```yaml
# SPEC-001.yml
active: true
status: in-progress
text: |
  ...
```

```bash
# 全アイテムのステータス一覧
spec-weaver status

# 特定のステータスで絞り込み
spec-weaver status --filter in-progress
```

利用可能なステータス値: `draft` / `in-progress` / `implemented` / `deprecated`

### 4. ドキュメントビルド（`build`）コマンド

カバレッジ・相互リンク・テスト結果を統合したドキュメントサイトを生成します。

```bash
# 基本的な実行
spec-weaver build ./specification/features --out-dir .specification

# Cucumber互換のテスト実行結果（JSON）を組み込む場合
spec-weaver build ./specification/features --out-dir .specification \
    --test-results test-results.json

# MkDocsでブラウザ表示
mkdocs serve -f .specification/mkdocs.yml
```

生成されるサイトには、各アイテムの詳細ページ・一覧テーブル・Gherkin feature のMarkdown変換が含まれます。テスト結果JSONを指定すると、各シナリオに ✅/❌ バッジが付与されます。

### 5. トレーサビリティ探索（`trace`）コマンド

任意のアイテム（REQ / SPEC / `.feature` ファイル）を起点として、上位要件〜下位仕様〜Gherkinシナリオを階層ツリーで可視化します。

```bash
# REQを起点に全子孫を展開（both = 上位+下位）
spec-weaver trace REQ-001 -f ./specification/features

# SPECを起点に、上位REQと下位シナリオを同時表示
spec-weaver trace SPEC-003 -f ./specification/features

# .featureファイルを起点に、紐づくSPECとREQを遡る
spec-weaver trace audit.feature -f ./specification/features --direction up

# 探索方向の指定
spec-weaver trace REQ-001 -f ./specification/features --direction down  # 下位のみ
spec-weaver trace SPEC-003 -f ./specification/features --direction up   # 上位のみ

# テーブル形式で出力
spec-weaver trace REQ-001 -f ./specification/features --format flat
```

**ツリー出力例（`SPEC-003` を起点、`both`）:**

```
REQ-001 仕様と実装のトレーサビリティ保証 ✅ implemented
└── REQ-002 監査による品質の継続的担保 ✅ implemented
    └── ★ SPEC-003 audit コマンド仕様 ✅ implemented
        └── 🥒 audit.feature
            └── Scenario: audit コマンド
```

`★` は探索起点のアイテムを示します。`🥒` は関連するGherkinフィーチャーファイルです。

## ⚙️ 高度な設定

### テスト対象外の仕様

「UIのカラーコード」や「ライセンス表記」など、Gherkinでの振る舞いテストが不可能な仕様は、DoorstopのYAMLに `testable: false` を追記することで監査対象から除外できます。

```yaml
# SPEC-005.yml
active: true
testable: false
text: |
  ログインボタンの背景色は青色とすること。
```

## 🛠 開発者向け情報

```bash
# テストの実行
uv run pytest tests/ -q

# 各コマンドの動作確認
uv run spec-weaver audit ./specification/features
uv run spec-weaver status
uv run spec-weaver build ./specification/features --out-dir .specification
uv run spec-weaver trace REQ-001 -f ./specification/features
```
