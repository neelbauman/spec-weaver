# Gherkin .feature ファイル管理ガイド

> **このガイドの担当範囲**: `.feature` ファイルの**管理面**（配置・命名・`@SPEC-xxx` タグ付け）のみ。
> シナリオの内容（何を書くか・宣言的記述の品質・Given-When-Then の設計）は **bdd-behave-expert-skill** を参照すること。

---

## 基本構造（Doorstop 連携に必要な要素）

```gherkin
@SPEC-001         ← DoorstopのSPEC IDをタグとして付与（必須）
Feature: ユーザー認証
  ユーザーが自分のアカウントに安全にアクセスできること。

  Scenario: 正しい認証情報でのログイン成功
    Given 登録済みユーザーが存在する
    When  正しいパスワードでログインする
    Then  ログインに成功する

  Scenario: 誤ったパスワードでのログイン失敗
    Given 登録済みユーザーが存在する
    When  誤ったパスワードでログインを試みる
    Then  ログインが拒否される
```

> **注意**: シナリオ本文でAPIエンドポイント・HTTPステータスコード・DB操作などの実装詳細を書かないこと（宣言的記述の原則 → bdd-behave-expert-skill を参照）。

---

## タグの付け方（Doorstop との紐付け）

```gherkin
@SPEC-001                    # 単一SPECに対応
Feature: ...

@SPEC-002 @SPEC-003           # 複数SPECにまたがる場合
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

## ファイル命名規則

```
specification/features/
├── auth.feature          # 認証系
├── payment.feature       # 決済系
├── user_profile.feature  # ユーザープロフィール系
└── notification.feature  # 通知系
```

- スネークケース
- 機能ドメイン名でファイルを分割
- 1ファイルに複数のScenarioは許容（同一Featureなら）

---

## 既存コードからの逆引き時のタグ付け

既存テストコード（pytest, Jest等）から `.feature` を逆引きする際は、
対応する SPEC を特定し、必ず `@SPEC-xxx` タグを付与すること。

```bash
# SPECが未作成の場合は先にDoorstopで作成する
doorstop add SPEC
# その後 .feature に @SPEC-xxx タグを付与
```

Gherkin の記述内容（シナリオの設計・変換ルール）は **bdd-behave-expert-skill** を参照すること。
