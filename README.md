![ロゴ画像](./logo.png)

# Spec-Weaver

Spec-Weaverは、**Doorstop**（テキストベースの要件管理）と **Gherkin**（実行可能な振る舞い駆動テスト）をシームレスに統合し、仕様と実装の完全なトレーサビリティを保証するCLIツールです。

仕様書とテストコードの乖離（リンク切れ、実装漏れ、不要なテストの残留）を CI/CD やローカル環境で瞬時に検知します。

## 特徴

- **堅牢なAST解析**: 正規表現への依存を排除。公式のGherkinパーサーを使用して抽象構文木（AST）から安全にタグを抽出します。
- **高速な差分検知**: Doorstopの仕様データベースとテストコードのタグを集合演算で比較し、「未実装の仕様」と「孤児となったテスト」を即座に割り出します。
- **美しいターミナルUI**: `Rich` ライブラリによる見やすいエラーレポートで、開発者の体験（DX）を向上させます。
- **柔軟な除外設定**: 自動テストが不可能な非機能要件などを、YAMLのカスタム属性で柔軟に監査対象から除外できます。
- **実装ステータス管理**: YAMLの `status` 属性で実装状況を追跡し、`status` コマンドで一覧・フィルタリング表示します。
- **トレーサビリティ探索**: `trace` コマンドで任意のアイテムを起点に上位要件〜下位仕様〜Gherkinシナリオを階層ツリー表示します。
- **Living Documentation**: `build` コマンドでカバレッジ・テスト結果・相互リンクを統合したドキュメントサイトを自動生成します。
- **実装ファイルリンク管理**: `impl_files` カスタム属性とコードアノテーション（`# implements: SPEC-001`）を組み合わせ、仕様と実装ファイルの双方向トレーサビリティを実現します。
- **テストコード自動生成**: `scaffold` コマンドで `.feature` ファイルから behave テストコードの雛形を自動生成・差分マージします。
- **レビュー管理**: `review` / `clear` コマンドで `.feature` ファイルと Doorstop アイテムのレビュー状態・Suspect 状態を管理します。
- **意味的レビュー**: `semantic-review` コマンドで仕様・Gherkin・実装コードの意味的整合性を Claude で自動レビューします。

## インストール

現在、ソースコードからのインストールに対応しています。Python 3.10以上が必要です。

```bash
# リポジトリをクローンまたはダウンロードし、ディレクトリへ移動
git clone <your-repo-url>
cd spec-weaver

# 開発モードでインストール（実行可能コマンドがパスに追加されます）
uv tool install .
```

## 使い方

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

# 実装ファイルリンクの検証も行う場合
spec-weaver audit ./specification/features --check-impl

# 特定の拡張子のみスキャンする場合
spec-weaver audit ./specification/features --check-impl --extensions py,ts
```

乖離がある場合の出力例：

```
❌ テストが実装されていない仕様 (Untested Specs):
  CORE-001

⚠️ 仕様書に存在しない孤児タグ (Orphaned Tags):
  @SPEC-003
```

`--check-impl` 付きの追加出力例：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 実装ファイルリンクの検証
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ 存在しないファイルへの impl_files:
   SPEC-001 → src/spec_weaver/old_file.py (not found)

⚠️  impl_files のみ（アノテーションなし）:
   CORE-001 → src/spec_weaver/cli.py

⚠️  アノテーションのみ（impl_files なし）:
   SPEC-003 ← src/spec_weaver/gherkin.py

✅ リンク検証 完了
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

# 実装ファイルもツリーに表示する
spec-weaver trace TRC-003 -f ./specification/features --show-impl

# 特定の拡張子のみスキャンする場合
spec-weaver trace TRC-003 -f ./specification/features --show-impl --extensions py,ts
```

**ツリー出力例（`SPEC-003` を起点、`both`）:**

```
REQ-001 仕様と実装のトレーサビリティ保証 ✅ implemented
└── REQ-002 監査による品質の継続的担保 ✅ implemented
    └── ★ SPEC-003 audit コマンド仕様 ✅ implemented
        └── 🥒 audit.feature
            └── Scenario: audit コマンド
```

**`--show-impl` 付きのツリー出力例（`TRC-003` を起点）:**

```
REQ-012 仕様アイテムと実装ファイルのリンク管理 ✅ implemented
└── ★ TRC-003 コードアノテーションスキャン ✅ implemented
    ├── 🥒 impl_link.feature
    │   └── Scenario: アノテーションのスキャン
    ├── 📁 src/spec_weaver/impl_scanner.py
    └── 📝 src/spec_weaver/cli.py
```

表示記号: `★` 探索起点 / `🥒` Gherkin feature / `📁` `impl_files` 属性由来の実装ファイル / `📝` アノテーション由来の実装ファイル

### 6. テストコード雛形生成（`scaffold`）コマンド

`.feature` ファイルから behave テストコードの雛形を自動生成します。既存のステップ定義ファイルとの差分マージにも対応しています。

```bash
# 基本的な実行
spec-weaver scaffold ./specification/features --out-dir tests/features

# 既存ファイルを全上書きする場合
spec-weaver scaffold ./specification/features --out-dir tests/features --overwrite

# Git未コミット変更の確認をスキップして強制マージ
spec-weaver scaffold ./specification/features --out-dir tests/features --force
```

### 7. レビュー管理（`review` / `clear`）コマンド

仕様変更後のレビュー状態と Suspect 状態を管理します。

**`review`** — アイテムをレビュー済み状態にします。

```bash
# .feature ファイルのレビュー（フィンガープリント計算・書き込み）
spec-weaver review specification/features/audit.feature

# Doorstop アイテムID のレビュー
spec-weaver review SPEC-003
```

**`clear`** — Doorstop YAML の gherkin_fingerprints を更新し Suspect 状態を解除します。

```bash
# アイテムIDを指定して解除
spec-weaver clear SPEC-003 --feature-dir ./specification/features

# .feature ファイルを指定して一括解除
spec-weaver clear specification/features/audit.feature --feature-dir ./specification/features
```

**典型的なワークフロー:**

```
1. 仕様変更 → .feature ファイルを修正
2. spec-weaver review <feature_file>   → フィンガープリント更新
3. spec-weaver clear <feature_file>    → Suspect 状態を解除
4. spec-weaver audit <feature_dir>     → 整合性確認
```

### 8. 意味的レビュー（`semantic-review`）コマンド

仕様・Gherkin・実装コードの意味的整合性を Claude で自動レビューします。

```bash
# 特定のアイテムをレビュー
spec-weaver semantic-review --item SPEC-003

# 全仕様アイテムを並列レビュー
spec-weaver semantic-review --all

# high以上のfindingがあれば終了コード1を返す（CI連携）
spec-weaver semantic-review --all --fail-on high
```

> **注意**: このコマンドの実行には Claude API アクセスが必要です。

### 9. 実装ファイルリンク管理（`impl_files` + アノテーション）

仕様アイテムと実装ファイルを双方向でリンクする仕組みです。

**YAML側: `impl_files` カスタム属性**

```yaml
# TRC-003.yml
active: true
status: implemented
impl_files:
- src/spec_weaver/impl_scanner.py
- src/spec_weaver/doorstop.py
ref: ''
text: |
  （仕様本文）
```

> **注意**: Doorstopの組み込み `ref` フィールドは文字列専用のため、`impl_files` カスタム属性を使います。

**実装ファイル側: コードアノテーション**

```python
# implements: TRC-003
# implements: TRC-003, QA-003   # 複数IDをカンマ区切りで記述可
```

`#`, `//`, `--` のコメント記号をサポートします。

**`audit --check-impl` で乖離を検証し、`trace --show-impl` でツリーに可視化**することで、仕様と実装の双方向トレーサビリティを確保できます。

---

## 高度な設定

### テスト対象外の仕様

「UIのカラーコード」や「ライセンス表記」など、Gherkinでの振る舞いテストが不可能な仕様は、DoorstopのYAMLに `testable: false` を追記することで監査対象から除外できます。

```yaml
# QA-001.yml
active: true
testable: false
text: |
  ログインボタンの背景色は青色とすること。
```

## 開発者向け情報

```bash
# テストの実行
uv run pytest tests/ -q

# 各コマンドの動作確認
uv run spec-weaver audit ./specification/features
uv run spec-weaver audit ./specification/features --check-impl
uv run spec-weaver status
uv run spec-weaver build ./specification/features --out-dir .specification
uv run spec-weaver trace REQ-001 -f ./specification/features
uv run spec-weaver trace TRC-003 -f ./specification/features --show-impl
uv run spec-weaver scaffold ./specification/features --out-dir tests/features
uv run spec-weaver review specification/features/audit.feature
uv run spec-weaver clear SPEC-003 --feature-dir ./specification/features
uv run spec-weaver semantic-review --item SPEC-003
```
