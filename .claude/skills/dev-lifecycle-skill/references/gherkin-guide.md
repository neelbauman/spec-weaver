# Gherkin .feature 作成ガイド

## 振る舞い仕様（.feature）の適用範囲

振る舞い仕様（.feature）は **外部仕様（`layer: behavior` の SPEC）** に対してのみ記述する。
内部仕様（`layer: architecture`）の SPEC には振る舞い仕様を書かない。

### 書くべきもの（外部仕様の検証）

| 仕様の内容 | Gherkin で表現する理由 |
|---|---|
| API にリクエストすると正しいレスポンスが返る | 外部から観察可能な入出力 |
| 無効な入力でエラーメッセージが表示される | ユーザーが観察可能な結果 |
| 条件を満たすと状態が変化する | ビジネスルールに基づく振る舞い |
| コマンドを実行すると期待する出力が得られる | CLI の外部インターフェース |

### 書くべきでないもの（内部仕様の領域）

| 仕様の内容 | 理由 | 代替テスト手段 |
|---|---|---|
| DB テーブルのスキーマ定義 | 内部実装の詳細 | マイグレーションテスト |
| クラス間の依存関係 | 内部構造 | ユニットテスト |
| フレームワークの選定理由 | 技術的決定 | ADR として記録 |
| レスポンスタイム < 100ms | 非機能要件 | 性能テスト |
| ログ出力の形式 | 内部観測性 | ユニットテスト |

### タグ付けと `layer` の関係ルール

- 外部仕様（`layer: behavior`）の SPEC → `@SPEC-xxx` タグで振る舞い仕様にリンク（推奨）
- 内部仕様（`layer: architecture`）の SPEC → 振る舞い仕様にリンクしない（タグを付けない）
- `layer` 未設定の SPEC → 従来通り `testable` 属性で判断（後方互換）

---

## 基本構造

```gherkin
@SPEC-001         ← DoorstopのSPEC IDをタグとして付与（必須）
Feature: ユーザー認証
  ユーザーが自分のアカウントに安全にアクセスできること。

  Background:       ← 各シナリオの前提（オプション）
    Given システムが起動している

  Scenario: 正しい認証情報でのログイン成功
    Given 登録済みユーザー "alice@example.com" が存在する
    When  正しいパスワードで "/api/login" にPOSTする
    Then  ステータスコード 200 が返る
    And   レスポンスにアクセストークンが含まれる

  Scenario: 誤ったパスワードでのログイン失敗
    Given 登録済みユーザー "alice@example.com" が存在する
    When  誤ったパスワードで "/api/login" にPOSTする
    Then  ステータスコード 401 が返る
```

---

## タグの付け方

```gherkin
@SPEC-001                    # 単一SPECに対応
Feature: ...

@CORE-001 @SPEC-003           # 複数SPECにまたがる場合
Feature: ...

@SPEC-001
  @smoke                    # 追加タグ（テスト分類）と併用可
  Scenario: ...
```

**ルール:**
- `Feature` には必ず対応する `@SPEC-xxx` タグを付ける
- 1つのfeatureファイルは原則1つの機能領域（Feature）
- Scenarioにも個別のSPECタグを付けてよい（より細かく紐づける場合）

---

## Given-When-Then の書き方原則

| キーワード | 意味 | 書き方 |
|---|---|---|
| `Given` | 前提条件・初期状態 | 「〜が存在する」「〜の状態で」 |
| `When` | 操作・イベント | 「〜する」「〜をPOSTする」 |
| `Then` | 期待結果 | 「〜が返る」「〜になる」「〜を含む」 |
| `And` / `But` | 前のキーワードの継続 | Given/When/Thenの補足 |

---

## Scenario Outline（パラメータ化）

複数の入力パターンを1つのシナリオで表現:

```gherkin
@SPEC-001
Scenario Outline: さまざまな入力での検証
  Given ユーザーが "<role>" の権限を持つ
  When  "<endpoint>" にアクセスする
  Then  ステータスコード <status> が返る

  Examples:
    | role  | endpoint      | status |
    | admin | /api/admin    | 200    |
    | user  | /api/admin    | 403    |
    | guest | /api/profile  | 401    |
```

---

## ファイル命名規則

```
features/
├── auth.feature          # 認証系
├── payment.feature       # 決済系
├── user_profile.feature  # ユーザープロフィール系
└── notification.feature  # 通知系
```

- スネークケース
- 機能ドメイン名でファイルを分割
- 1ファイルに複数のScenarioは許容（同一Featureなら）

---

## 既存コードからのGherkin逆引き例

既存テストコード（例: pytest, Jest）から変換する場合:

```python
# 既存テスト（pytest）
def test_login_success():
    response = client.post("/api/login", json={"email": "...", "password": "..."})
    assert response.status_code == 200
```

↓ Gherkin に変換

```gherkin
Scenario: ログイン成功
  Given 登録済みユーザーが存在する
  When  正しい認証情報で "/api/login" にPOSTする
  Then  ステータスコード 200 が返る
```

**変換のコツ:**
- `describe`/`context` → `Feature` または `Scenario` のグループ
- `test`/`it` → `Scenario`
- `beforeEach`/`setup` → `Background` または `Given`
- `assert`/`expect` → `Then`
