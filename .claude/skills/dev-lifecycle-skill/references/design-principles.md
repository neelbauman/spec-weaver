# 設計原則リファレンス

3つの学術的考察（BDD/Cucumberの3層構造、階層的トレーサビリティ、DX/AXツール選定）を
凝縮した、spec-weaver仕様管理の設計原則。全スキルから参照される基盤ドキュメント。

---

## 原則1: 4層トレーサビリティモデル

仕様は「Why → What → How → Detail」の4層で階層化する。
各層には明確な問い・形式・責任者が存在する。

```
Why    ── REQ（ビジネス要件）     「なぜ作るのか」
What   ── SPEC（システム仕様）    「何を作るのか」
How    ── .feature（振る舞い仕様） 「外部からどう振る舞うか」
Detail ── DESIGN / PLAN / ADR     「内部をどう構築するか」
```

| 層 | ドキュメント | 問い | ツール |
|---|---|---|---|
| Why | REQ | なぜ作るのか | Doorstop |
| What | SPEC | 何を作るのか | Doorstop |
| How | .feature | 外部からどう振る舞うか | Gherkin |
| Detail | DESIGN / PLAN / ADR | 内部をどう構築するか | Doorstop |

**Spec-Weaverの役割**: Why〜How 層のトレーサビリティ・ブリッジ。
層をまたいだ整合性を保証するが、各層の内容自体は管理しない。

---

## 原則2: Gherkin の適用範囲限定

Gherkin（.feature）は **外部から観察可能な振る舞い** のみを記述する。
内部構造・技術的制約・アーキテクチャ決定は Gherkin の対象外。

### 書くべきもの（behavior 層）

| 例 | 理由 |
|---|---|
| ユーザーがログインすると200が返る | 外部から観察可能な入出力 |
| 無効なトークンでアクセスすると401が返る | エラー時の振る舞い |
| カートに商品を追加すると合計が更新される | 状態変化の観察 |
| 90日以上更新がないアイテムをstaleと検出する | ルールに基づく判定結果 |

### 書くべきでないもの（architecture 層以下）

| 例 | 理由 | 代替手段 |
|---|---|---|
| データベースのテーブル構造 | 内部実装の詳細 | DESIGN ドキュメント |
| 使用するフレームワークの選定理由 | 技術的決定 | ADR |
| クラス間の依存関係 | 内部構造 | DESIGN + ユニットテスト |
| パフォーマンス要件（レスポンス < 100ms） | 非機能要件 | SPEC + 性能テスト |
| ログ出力フォーマット | 内部観測性 | SPEC + ユニットテスト |

---

## 原則3: テストの3層分離（Spec-Glue-Execution）

BDD テストは以下の3層に分離する。依存方向は上から下への一方向のみ。

```
 Spec 層 ──── .feature（Gherkin）
    ↓          ビジネスの振る舞いを自然言語で宣言
 Glue 層 ──── Step 定義（Python）
    ↓          Spec の翻訳・委譲のみ（ロジック禁止）
 Execution 層 ── ヘルパー / クライアント
                 実際のシステム操作（API呼び出し、DB操作等）
```

| 層 | 責務 | 含めてよいもの | 含めてはいけないもの |
|---|---|---|---|
| **Spec** (.feature) | ビジネスの振る舞いを宣言 | Given/When/Then、ドメイン用語 | 実装詳細、技術用語 |
| **Glue** (Step定義) | Spec → Execution への翻訳・委譲 | パラメータ受け渡し、assert | if/for、計算、ビジネスロジック |
| **Execution** (ヘルパー) | 実際のシステム操作 | API呼び出し、DB操作、状態管理 | Gherkin の知識、assert |

**依存の方向**: Spec → Glue → Execution（逆方向の依存は禁止）

---

## 原則4: ツールスコープの分別

各ツールには明確なスコープがあり、スコープ外の役割を押し付けてはならない。

| ツール | スコープ | スコープ外 |
|---|---|---|
| **Doorstop** | 要件/仕様のID管理、リンク、バージョン管理 | テスト実行、ドキュメント描画 |
| **Gherkin** | 外部から観察可能な振る舞いの宣言 | 内部設計、非機能要件 |
| **Spec-Weaver** | Doorstop ↔ Gherkin のトレーサビリティ・ブリッジ | テスト実行、仕様作成 |
| **behave** | Gherkin シナリオの実行 | 仕様管理、トレーサビリティ |

---

## `layer` 属性

### 定義

Doorstop SPEC アイテムに付与するカスタム属性。仕様が記述する対象の「層」を明示する。

| 値 | 意味 | 例 |
|---|---|---|
| `behavior` | 外部から観察可能な振る舞い | API応答、ユーザー操作の結果、ビジネスルール |
| `architecture` | 内部構造・技術的制約 | データモデル、コンポーネント分割、非機能要件 |

### 判断基準フローチャート

```
この仕様は「外部のアクター（ユーザー/API呼び出し元）が
結果を直接観察できるか？」
  │
  ├── はい → layer: behavior
  │
  └── いいえ ──→「システム内部の構造・制約・技術選定に関するものか？」
                  │
                  ├── はい → layer: architecture
                  │
                  └── いいえ → 仕様の記述を見直す（どちらにも分類できない場合、
                               仕様が曖昧な可能性がある）
```

### 判断基準3問

1. **外部から観察可能か？** → Yes なら `behavior`
2. **Given-When-Then で表現できるか？** → Yes なら `behavior`
3. **ユーザーストーリーの受け入れ条件として書けるか？** → Yes なら `behavior`

3問とも No なら `architecture`。

### `testable` と `layer` の関係

| testable | layer | 意味 | テスト手段 |
|---|---|---|---|
| `true` | `behavior` | Gherkin でテストすべき（推奨） | .feature シナリオ |
| `true` | `architecture` | テスト可能だが Gherkin は不適切 | ユニットテスト / 統合テスト |
| `false` | `behavior` | 稀（UI の見た目など） | 手動確認 / VRT |
| `false` | `architecture` | テスト不要な技術方針 | レビューのみ |

### YAML での記述

```yaml
active: true
layer: behavior       # ← behavior または architecture
testable: true
status: draft
text: |
  （仕様本文）
```

### 段階的導入ルール

- **新規アイテム**: Phase 2（設計）で設定必須
- **既存アイテム**: レビュー時に段階的に付与
- **未設定**: エラーではなく「未分類」として許容（既存ワークフローを壊さない）

---

## スキル間の参照関係

一方向のみ。循環参照は禁止。

```
design-principles.md（本ドキュメント：基盤）
  ↑
spec-weaver-skill ← python-behave-expert-skill
  ↑
dev-lifecycle-skill
  ↑
requirements-specifications-organize-skill
  ↑
semantic-review-skill
```
