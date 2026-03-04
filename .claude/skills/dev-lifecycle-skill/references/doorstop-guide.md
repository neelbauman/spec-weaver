# Doorstop 操作ガイド

## ⚠️ 重要: YAML は CLI で生成する

Doorstop の YAML ファイルは **手動作成禁止**。必ず `doorstop add` で生成し、
生成されたファイルの `text` フィールドのみを編集する。

```bash
doorstop add REQ    # → reqs/REQ-001.yml を自動生成
doorstop edit REQ-001  # → エディタが開く（$EDITOR に依存）
```

---

## 1. Doorstop CLI の使い方

### インストール

```bash
uv tool install doorstop
```

### ドキュメントの作成（`doorstop create`）

```bash
# ルートドキュメント（親なし）を作成
doorstop create REQ ./specification/reqs

# 子ドキュメントを作成（--parent で親プレフィックスを指定）
doorstop create SPEC ./specification/specs --parent REQ
```

これにより各ディレクトリに `.doorstop.yml` が自動生成される。Git リポジトリのルートで実行すること。

### アイテムの追加（`doorstop add`）

```bash
# REQ アイテムを追加（REQ-001.yml が自動生成される）
doorstop add REQ

# 生成された YAML ファイルをエディタで開いて text を編集する
doorstop edit REQ-001
```

### アイテムのリンク（`doorstop link`）

```bash
# SPEC-001 を REQ-001 にリンク
doorstop link SPEC-001 REQ-001
```

これにより `SPEC-001.yml` の `links` フィールドが自動更新される。

### 検証とレビュー

```bash
# ツリー全体の整合性チェック（リンク切れ・未レビュー検出）
doorstop

# アイテムをレビュー済みにする（fingerprint が記録される）
doorstop review all

# HTML として公開
doorstop publish all ./specification/public
```

---

## 2. ID 形式の設定（Spec-Weaver との連携）

Spec-Weaver はデフォルトで `SPEC-001` 形式（ダッシュ区切り）を想定している。
Doorstop 作成時は `.doorstop.yml` の `sep` を確認・修正する:

```yaml
settings:
  digits: 3
  prefix: SPEC
  sep: '-'     # ← Spec-Weaver に合わせてダッシュを使う
```

---

## 3. YAML テンプレートリファレンス

### Doorstop add で生成される YAML の初期構造

```yaml
active: true
derived: false
header: ''
level: 1.0
links: []
normative: true
ref: ''
reviewed: null
text: |
  （空欄 - ここを編集する）
```

### REQ（要件）の text の書き方

```yaml
text: |
  ## 概要
  （このビジネス要件の一文サマリー）

  ## 背景・動機
  （なぜこの要件が必要か。ビジネス上の課題や目標）

  ## ダイアグラム
  （フローチャートやシーケンス図など、Mermaid で必要があれば表現）

  ## 受け入れ基準
  - （測定可能な条件1）
  - （測定可能な条件2）
```

### SPEC（仕様）の text の書き方

```yaml
text: |
  ## 概要
  （このシステム仕様の一文サマリー）

  ## 詳細仕様

  ### ダイアグラム
  （フローチャートやシーケンス図など、Mermaid で必要があればロジックを表現）

  ### 入力
  - （入力パラメータや前提条件）

  ### 処理
  - （システムが行う処理の詳細）

  ### 出力・結果
  - （期待される出力や状態変化）
```

### カスタム属性

**`layer` 属性（仕様の層分類）:**

```yaml
active: true
layer: behavior       # ← 外部仕様（外部のアクターが結果を直接観察できる）
testable: true        #    または architecture（内部仕様）
status: draft
text: |
  ユーザーが正しい認証情報でログインするとアクセストークンが返る。
```

| 値 | 意味 | Gherkin との関係 |
|---|---|---|
| `behavior` | 外部仕様 | 振る舞い仕様（.feature）でテストすべき（推奨） |
| `architecture` | 内部仕様 | 振る舞い仕様は不適切（ユニットテスト等で検証） |

> **`testable` と `layer` の違い**: `testable` は「テスト可能かどうか」、`layer` は「仕様がどの層に属するか」を示す。
> `layer: architecture` でも `testable: true`（ユニットテストで検証可能）はあり得る。
> 詳細は `design-principles.md` の関係表を参照。

**Spec-Weaver のテスト除外設定:**

振る舞い仕様（.feature）でテストができない仕様の場合は `testable: false` を追加する。

```yaml
active: true
layer: architecture   # ← 内部構造に関する仕様
testable: false       # ← Spec-Weaver が監査から除外する
text: |
  ログインボタンの背景色は #1A73E8 とすること。
```

**実装ステータス管理:**

`doorstop add` でファイルを生成した後、`status` キーを手動で追記することで実装の進行状況を管理できる。

```yaml
active: true
status: in-progress   # ← 実装状況を追記する
text: |
  （仕様本文）
```

| 値 | バッジ | 意味 |
|---|---|---|
| `draft` | 📝 draft | 草案。まだ実装着手していない |
| `in-progress` | 🚧 in-progress | 実装中 |
| `implemented` | ✅ implemented | 実装済み |
| `deprecated` | 🗑️ deprecated | 廃止予定 |

> フィールド未設定の場合は `-` として扱われる（エラーにはならない）。

**タイムスタンプ管理（Git 自動取得）:**

`build` / `audit` 実行時に、Git コミット履歴からタイムスタンプを自動算出する。
YAML への手動記入は不要。

| 属性 | 取得元 | 説明 |
|---|---|---|
| `created_at` | Git 初回コミット日 | ファイルが最初にコミットされた日付 |
| `updated_at` | Git 最終コミット日 | ファイルが最後にコミットされた日付 |

> Git 情報が取れない場合（未コミット、Git 管理外）は YAML の `created_at` / `updated_at` にフォールバック。
> いずれもなければ `-` として扱われる（エラーにはならない）。
> 最終コミット日から 90 日以上経過している場合、`audit --stale-days` で stale として検出される。

### フィールド説明

| フィールド | 意味 | 注意 |
|---|---|---|
| `active` | 有効な要件か | `false` にすると削除の代わりに非表示化できる |
| `level` | 階層番号 | `1.0`終わりの非 normative はセクション見出しになる |
| `links` | 親アイテムへの参照 | `doorstop link` コマンドで自動更新。手動編集不要 |
| `normative` | 規範的か | 通常 `true`。見出し用は `false` + level を `.0` 終わりに |
| `reviewed` | レビュー済み fingerprint ハッシュ | `doorstop review` で自動更新。手動編集不要 |
| `ref` | 外部参照（ファイルパスなど） | 通常は空でよい |
| `text` | 本文（Markdown） | 人間が直接編集するフィールド |
| `layer` | 仕様の層分類 | カスタム属性。`behavior` / `architecture` |
| `testable` | テスト対象か | カスタム属性。`false` で audit 除外 |
| `status` | 実装ステータス | カスタム属性。`draft` / `in-progress` / `implemented` / `deprecated` |
| `created_at` | 作成日 | Git 初回コミット日から自動取得。フォールバック: YAML カスタム属性 |
| `updated_at` | 最終更新日 | Git 最終コミット日から自動取得。フォールバック: YAML カスタム属性 |

### Mermaid や画像の挿入

Doorstop の `text:` フィールドは Markdown として解釈されるため、Mermaid コードや画像を記述できる。

```yaml
# 画像の挿入
text: |
  ![ログイン画面のモックアップ](../assets/images/login-mock.png)
```

```yaml
# Mermaid の記述
text: |
  ```mermaid
  sequenceDiagram
      User->>API: POST /login
      API->>DB: Query User
      DB-->>API: Return Hash
      API-->>User: JWT Token
  ```
```

> **注意**: Doorstop 標準の `publish` は Mermaid を描画できない。描画は別ツール（MkDocs 等）で行う。

---

## 4. `layer` 属性の導入ガイド

SPEC アイテムには `layer` カスタム属性を設定し、仕様が外部仕様か内部仕様かを明示する。

### 値の定義

| 値 | 意味 | Gherkin との関係 |
|---|---|---|
| `behavior` | 外部仕様 | 振る舞い仕様（.feature）でテストすべき（推奨） |
| `architecture` | 内部仕様 | 振る舞い仕様は不適切（ユニットテスト等で検証） |

### 判断基準（3問で決定）

1. **外部から観察可能か？** → Yes なら `behavior`
2. **Given-When-Then で表現できるか？** → Yes なら `behavior`
3. **受け入れ条件として書けるか？** → Yes なら `behavior`

3問とも No なら `architecture`。

### 段階的導入

- **新規アイテム**: 設計フェーズで設定必須
- **既存アイテム**: レビュー時に段階的付与
- **未設定**: エラーではなく「未分類」として許容

> 詳細（`testable` との関係表、フローチャート等）は `design-principles.md` を参照。

---

## 5. 階層化・グループ化の設計指針

Doorstop の REQ/SPEC は **複数レベルの階層** を自由に設計してよい。機能領域やドメインに応じて柔軟に構成すること。

### 階層化の例

```bash
# 機能グループ別にドキュメントを分ける
doorstop create REQ      ./specification/reqs              # ルート要件
doorstop create AUTH-REQ ./specification/reqs/auth --parent REQ    # 認証サブグループ
doorstop create PAY-REQ  ./specification/reqs/payment --parent REQ # 決済サブグループ

doorstop create SPEC     ./specification/specs             # ルート仕様
doorstop create AUTH     ./specification/specs/auth --parent AUTH-REQ
doorstop create PAY      ./specification/specs/payment --parent PAY-REQ
```

### グループ化の設計指針

- **ドメイン別**: 認証・決済・通知・ユーザー管理など機能ドメインで分ける
- **レイヤー別**: API 仕様・UI 仕様・DB 仕様など技術レイヤーで分ける
- **フェーズ別**: MVP 要件・拡張要件など開発フェーズで分ける
- **`level` フィールド活用**: 同一ドキュメント内でも `level: 1.1`, `level: 1.2` で論理的なグルーピングができる

> **制約**: Doorstop の `--parent` は1つだけ指定可能（多重継承不可）。
> 複数ドメインにまたがる仕様は、上位 REQ へのリンクを複数張ることで対応する。

---

## 6. ディレクトリ構成テンプレート

```text
<project-root>/specification/
├── reqs/                  # 要件 [Doorstop: prefix=REQ]
│   ├── .doorstop.yml      # doorstop create REQ ./specification/reqs で自動生成
│   ├── REQ-001.yml
│   └── auth/              # サブグループ（認証ドメイン）
│       ├── .doorstop.yml  # doorstop create AUTH-REQ ... --parent REQ
│       └── AUTH-REQ-001.yml
├── specs/                 # 仕様 [Doorstop: prefix=SPEC, parent=REQ]
│   ├── .doorstop.yml
│   ├── SPEC-001.yml
│   └── auth/              # サブグループ（認証ドメイン）
│       ├── .doorstop.yml  # doorstop create AUTH ... --parent AUTH-REQ
│       └── AUTH-001.yml
└── features/              # 振る舞い仕様 [Gherkin]
    ├── auth.feature       # @AUTH-001 タグで紐付け
    └── payment.feature    # @PAY-001 タグで紐付け
```

---

## 7. 新規プロジェクトセットアップ手順

### セットアップ前の確認事項

- プロジェクトルートのパス（Git リポジトリのルートか確認）
- 主要な機能領域（例: 認証、決済、通知 など）

### Step 1: Doorstop 初期化

```bash
cd <project-root>
doorstop create REQ ./specification/reqs
doorstop create SPEC ./specification/specs --parent REQ

# .doorstop.yml の sep を '-' に修正（Spec-Weaver 対応）
```

### Step 2: 要件を追加・編集

```bash
doorstop add REQ   # → REQ-001.yml 生成
doorstop edit REQ-001  # エディタで text を記述
```

### Step 3: 仕様を追加・REQ にリンク

```bash
doorstop add SPEC         # → SPEC-001.yml 生成
doorstop link SPEC-001 REQ-001  # リンク設定
doorstop edit SPEC-001    # エディタで text を記述
```

### Step 4: Gherkin .feature の作成

詳細は `gherkin-guide.md` を参照。

### Step 5: 整合性チェック

```bash
doorstop            # Doorstop 内のリンク整合性
spec-weaver audit ./specification/features  # Doorstop ↔ Gherkin の整合性
```

---

## 8. 既存プロジェクト逆引き初期化手順

### 分析フロー

**1. コードベースのスキャン**
```bash
find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.tsx" \) | head -60
find . -name "README*" -o -name "*.md" | head -20
```

**2. 機能領域の推定**
- ルーティング定義（routes/, pages/, controllers/）からエンドポイントを抽出
- 既存テストの `describe`/`it` ブロックのテキストは Gherkin 化しやすい

**3. 仕様ドラフトの生成手順**
```bash
# まず Doorstop を初期化
doorstop create REQ ./specification/reqs
doorstop create SPEC ./specification/specs --parent REQ

# 機能ごとにアイテムを追加
doorstop add REQ  # 機能の数だけ繰り返す
```

その後、生成された YAML ファイルの `text` フィールドに分析した内容を記述し、
`doorstop link` で REQ-SPEC の紐付けを行う。

### 逆引き時の注意

- 実装から推測できるのは「何をしているか（SPEC）」まで。「なぜ（REQ）」はユーザーに必ず確認
- 完璧な仕様より「まず存在する仕様」を優先し、後から精緻化を提案する
- `testable: false` を付けるべき仕様（UI 見た目、設定値など）も整理する

---

## 9. 実装ステータス管理

### ステータス値

| 値 | バッジ | 意味 |
|---|---|---|
| `draft` | 📝 draft | 草案。まだ実装着手していない |
| `in-progress` | 🚧 in-progress | 実装中 |
| `implemented` | ✅ implemented | 実装済み |
| `deprecated` | 🗑️ deprecated | 廃止予定 |

### タスク終了時のステータス更新手順

1. **実装が完了した SPEC を確認する**
   ```bash
   spec-weaver status --filter in-progress
   ```

2. **完了した SPEC の YAML を更新する**
   ```yaml
   status: implemented
   ```

3. **ステータス一覧で確認**
   ```bash
   spec-weaver status
   ```

4. **build でドキュメントに反映**
   ```bash
   spec-weaver build ./specification/features --out-dir .specification
   ```

### よくある操作例

```bash
# 新しい要件を追加してリンク
doorstop add REQ          # REQ-002.yml 生成
doorstop add SPEC         # CORE-001.yml 生成
doorstop link CORE-001 REQ-002   # リンク設定

# アイテムを非アクティブ化（削除の代わり）
# → YAML の active: false に変更（doorstop edit で）

# 現在の状態を確認
doorstop               # バリデーション実行
doorstop publish all ./specification/public  # HTML 生成して確認
```
