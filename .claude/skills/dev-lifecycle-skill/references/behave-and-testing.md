# BDD テスト実装ガイド（Gherkin × behave）

## 1. テストの3層構造（Spec-Glue-Execution）

BDD テストは以下の3層に分離する。依存方向は上から下への一方向のみ。

```
 Spec 層 ──── .feature（Gherkin）
    ↓          ビジネスの振る舞いを自然言語で宣言
 Glue 層 ──── Step 定義（Python / behave）
    ↓          Spec の翻訳・委譲のみ（ロジック禁止）
 Execution 層 ── ヘルパー / クライアント（context.xxx）
                 実際のシステム操作（API呼び出し、DB操作等）
```

| 層 | ファイル | 責務 | 含めてよいもの | 含めてはいけないもの |
|---|---|---|---|---|
| **Spec** | `.feature` | ビジネスの振る舞いを宣言 | Given/When/Then、ドメイン用語 | 実装詳細、技術用語 |
| **Glue** | `steps/*.py` | Spec → Execution への翻訳・委譲 | パラメータ受け渡し、assert | if/for、計算、ビジネスロジック |
| **Execution** | ヘルパークラス | 実際のシステム操作 | API呼び出し、DB操作、状態管理 | Gherkin の知識、assert |

**依存の方向**: Spec → Glue → Execution（逆方向の依存は禁止）

---

## 2. Gherkin の適用範囲

Gherkin は **`layer: behavior` の SPEC（外部から観察可能な振る舞い）** にのみ適用する。

| SPEC の layer | テスト手段 |
|---|---|
| `behavior` | Gherkin + behave（本ガイドの対象） |
| `architecture` | ユニットテスト / 統合テスト（本ガイドの対象外） |

`layer: architecture` の SPEC に対して .feature を書いてはならない。

---

## 3. spec-weaver trace による情報収集ワークフロー

テストを書く前に、必ず spec-weaver trace で仕様・設計・実装の関連情報を収集すること。

### なぜ trace から始めるのか

BDD テストを書くには「何を証明するか」が明確でなければならない。
spec-weaver trace はその問いに答えるための情報を、単一コマンドで収集できる。

- **REQ** → なぜこの振る舞いが必要か（背景・目的）
- **SPEC** → 何を実装すべきか（仕様本文）
- **`.feature`** → 既にどんな振る舞いがテストされているか
- **実装ファイル** → 現在どう実装されているか

### 起点の特定

```bash
# SPEC ID がわかっている場合
uv run spec-weaver trace TRC-001 -f ./specification/features --show-impl

# Feature ファイルを起点にする場合
uv run spec-weaver trace checkout.feature -f ./specification/features --direction up

# 全体像を把握したい場合
uv run spec-weaver trace REQ-001 -f ./specification/features --direction down
```

### trace 出力の読み方

```
REQ-005 決済フローの整合性保証 ✅ implemented
└── ★ TRC-001 送料計算ルール ✅ implemented
    ├── 🥒 checkout.feature
    │   ├── Scenario Outline: VIPユーザーの購入金額別送料 -- @1.1 通常送料
    │   └── Scenario Outline: VIPユーザーの購入金額別送料 -- @1.2 送料無料ライン到達
    ├── 📁 src/checkout/shipping.py
    └── 📝 src/checkout/cart.py
```

| 記号 | 確認すべきこと |
|---|---|
| `★ TRC-001` | この SPEC の `text` フィールドを読んで仕様本文を把握する |
| 親 REQ | なぜこのルールが必要かの文脈を確認する |
| `🥒` + シナリオ | 既存のシナリオで何がカバーされているか確認する |
| `📁` `📝` 実装ファイル | 現在の実装を読んで仕様との乖離を確認する |

### Doorstop YAML の仕様本文を読む

trace で SPEC ID が判明したら、YAML を直接読んで仕様本文を確認する。
**この `text` が「あるべき振る舞い」の唯一の根拠**。
実装ファイルではなく、この YAML を基準にテストを設計する。

### 既存テストとのギャップ分析

trace で確認できた既存シナリオと仕様本文を照合する。

チェックリスト:
- [ ] 仕様に記載されたすべての条件分岐がシナリオでカバーされているか
- [ ] 境界値が含まれているか
- [ ] 異常系が記述されているか
- [ ] `testable: true` の仕様に `.feature` タグが付いているか

### 仕様と実装の乖離の扱い方

| 状況 | 対応 |
|---|---|
| 実装が仕様通りに動いていない | テストで乖離を固定化する（テストを失敗させる） |
| 実装が仕様を超えた振る舞いをしている | 仕様にない振る舞いもテストに加えるが SPEC の更新を提案する |
| 仕様が曖昧で実装と合わせるしかない | 仕様の明確化をユーザーに確認する。憶測でテストを書かない |
| `testable: false` の仕様 | Gherkin でのテストは不要 |

**重要**: trace 結果に合わせて仕様を歪めてはならない。
仕様に反する実装が見つかった場合、その乖離を **テスト失敗として固定化する**。

### trace コマンド クイックリファレンス

```bash
# 基本（both: 上位+下位を展開）
uv run spec-weaver trace SPEC-xxx -f ./specification/features

# 上位のみ（REQ まで遡る）
uv run spec-weaver trace SPEC-xxx -f ./specification/features --direction up

# 下位のみ（シナリオまで展開）
uv run spec-weaver trace REQ-xxx -f ./specification/features --direction down

# 実装ファイルも表示
uv run spec-weaver trace SPEC-xxx -f ./specification/features --show-impl

# テーブル形式で出力
uv run spec-weaver trace SPEC-xxx -f ./specification/features --format flat

# .feature ファイルを起点に遡る
uv run spec-weaver trace target.feature -f ./specification/features --direction up
```

---

## 4. Gherkin 記述ルール

- Gherkin v6 に準拠する（Rule キーワードを活用）
- Feature は「業務上の関心事」単位で定義する
- ビジネスルールは `Rule` で明示する
- 共通前提は `Background` に集約する

### データ表現ルール

| 用途 | 構文 |
|---|---|
| 複数レコードの初期データ | Data Table |
| 境界値・網羅的なバリエーション | Scenario Outline + Examples |
| 長文の期待値・メッセージ | Doc String (`"""`) |

- 意味の異なる Examples を1つにまとめない
- Examples 名は「業務的な意味」を持たせる

### Feature ファイルと SPEC のリンク

```gherkin
@SPEC-001
Feature: ショッピングカートの振る舞い
```

- Feature タグに `@SPEC-xxx` を付与して Doorstop とリンクさせる
- spec-weaver audit でリンク整合性を確認できる

### Scenario Outline のパターン

```gherkin
# ✅ 良い: 境界値ごとに Examples を分割し、名前で意味を表現する
Scenario Outline: ユーザーランク別割引率
  Given ユーザーのランクは "<ランク>" である
  Then 割引率は <割引率> ％であること

  Examples: 一般会員
    | ランク  | 割引率 |
    | NORMAL  | 0      |

  Examples: 優良会員
    | ランク  | 割引率 |
    | SILVER  | 5      |
    | GOLD    | 10     |

  Examples: VIP会員（特別扱い）
    | ランク  | 割引率 |
    | VIP     | 20     |
```

```gherkin
# ❌ 悪い: 意味の異なるケースを1つの Examples に混在させる
Examples: パターン
  | ランク  | 割引率 |
  | NORMAL  | 0      |
  | VIP     | 20     |   # ← 区別ができない
```

---

## 5. behave 実装ルール

### Thin Wrapper 原則（絶対）

Step 関数は **委譲のみ**。以下を **禁止** する。

- `if` / `for` / `while`
- 条件分岐
- 計算・変換ロジック
- ビジネスルールの再実装
- 仕様の再解釈

### 許可される Step の責務

1. Gherkin から値を受け取る
2. `context.xxx` にそのまま渡す
3. 結果を `assert` で比較する

### データ受け取りの正規ルート

| データ形式 | 受け取り方 |
|---|---|
| 単一の値 | 型付きパラメータ `{count:d}`, `{name}` |
| 複数レコード | `context.table` |
| 長文テキスト | `context.text` |

**正規表現による独自パースは禁止。** 型付きパラメータと公式構文を使うこと。

---

## 6. scaffold の使い方と肉付けワークフロー

### Step 1: trace で情報収集する

```bash
uv run spec-weaver trace SPEC-xxx -f ./specification/features --show-impl
```

Doorstop YAML の `text` を読み、「あるべき振る舞い」を確認する。

### Step 2: `.feature` ファイルを設計する

仕様ファースト・実装無視で Feature / Scenario を書く。
`@SPEC-xxx` タグを付けて Doorstop とリンクさせる。

### Step 3: scaffold で雛形を生成する（必須）

**`.feature` を書いたら、必ず最初に `spec-weaver scaffold` を実行すること。**
手でゼロから Step 定義を書き始めてはならない。

```bash
uv run spec-weaver scaffold ./specification/features --out-dir specification/features/steps
```

生成されるファイル: `specification/features/steps/step_<feature名>.py`

生成されたコードの特徴:
- 各 Step は `raise NotImplementedError('STEP: ...')` を本体とする雛形
- `"quoted string"` は自動的に `{param0}`, `{param1}` にパラメータ化される
- 他のファイルに定義済みの Step はコメントアウトされてスキップされる
- 関数名は Step 文の SHA256 ハッシュ（非 ASCII 文字回避のため）

既存の Step ファイルを再生成したい場合:
```bash
uv run spec-weaver scaffold ./specification/features --out-dir specification/features/steps --overwrite
```

### Step 4: 雛形を仕様に従って肉付けする

`raise NotImplementedError` を `context.xxx` への委譲と `assert` に置き換える。
scaffold が生成した型なしパラメータ `{param0}` を、
仕様の意味に合わせた型付きパラメータ（`{count:d}` 等）へ修正する。

**以下は絶対に削除しないこと:**

| 要素 | 理由 |
|---|---|
| `# type: ignore` （デコレータ末尾） | Pyright の誤検知を防ぐ |
| `# 使用されるシナリオ:` / `# - シナリオ名` | どのシナリオから呼ばれるかのトレーサビリティ |
| docstring（元ステップ文） | Gherkin の原文を保持し、将来の読者への文脈を提供する |

```python
# scaffold が生成した雛形
# 使用されるシナリオ:
# - VIPユーザーの購入金額別送料
@when('カートに "{param0}" を追加する')  # type: ignore
def when_a1b2c3d4(context, param0):
    """カートに "高級イヤホン" を追加する"""
    raise NotImplementedError('STEP: カートに "{param0}" を追加する')

# ↓ 仕様に合わせて肉付けする（コメント・type: ignore・docstring は残す）
# 使用されるシナリオ:
# - VIPユーザーの購入金額別送料
@when('カートに {count:d} 個の "{item}" (単価: {price:d}円) を追加する')  # type: ignore
def when_a1b2c3d4(context, count, item, price):
    """カートに "高級イヤホン" を追加する"""
    context.api_client.add_items_to_cart(name=item, unit_price=price, quantity=count)
```

Step は「1文 = 1委譲」に分解する。テスト失敗を前提に完了とする。

### Step 5: audit でリンク整合性を確認する

```bash
uv run spec-weaver audit ./specification/features
```

---

## 7. Step 定義パターン集

### 型付きパラメータ（Typed Parameters）

```python
# 整数
@then('残高は {amount:d} 円であること')
def step_impl(context, amount):
    assert context.account.balance == amount

# 浮動小数点
@then('割引率は {rate:f} ％であること')
def step_impl(context, rate):
    assert context.discount.rate == rate

# 文字列（デフォルト）
@given('ステータスが "{status}" のユーザーとしてログインしている')
def step_impl(context, status):
    context.api_client.login_as(status=status)
```

### Data Table の受け取り

```python
# context.table でそのままアクセスする
@given('システムに以下のユーザーが登録されている:')
def step_impl(context):
    users = [
        {"username": row["username"], "status": row["status"]}
        for row in context.table
    ]
    context.api_client.setup_users(users)

# ヘッダーなしの場合（rows）
@when('以下のアイテムをカートに追加する:')
def step_impl(context):
    items = [row[0] for row in context.table.rows]
    context.api_client.add_items(items)
```

### Doc String の受け取り

```python
# context.text で受け取る
@then('エラーメッセージは以下であること:')
def step_impl(context):
    expected = context.text.strip()
    actual = context.api_client.get_last_error()
    assert actual == expected
```

### 正しい Step（Thin Wrapper の例）

```python
from behave import given, when, then

# ✅ 良い: 受け取って渡すだけ
@given('ユーザー "{username}" としてログインしている')
def step_impl(context, username):
    context.api_client.login(username)

# ✅ 良い: 型付きパラメータで受け取る
@when('カートに {count:d} 個の "{item}" を追加する')
def step_impl(context, count, item):
    context.api_client.add_to_cart(item, quantity=count)

# ✅ 良い: assert だけ
@then('注文総額は {expected:d} 円であること')
def step_impl(context, expected):
    actual = context.api_client.get_order_total()
    assert actual == expected
```

### 禁止パターン（Anti-Pattern）

```python
# ❌ 悪い: Step 内で計算している
@then('送料無料になること')
def step_impl(context):
    total = context.cart_items * context.unit_price   # ← 計算はここでしない
    shipping = 0 if total >= 10000 else 500            # ← ビジネスロジックの再実装
    assert context.api_client.get_shipping() == shipping

# ❌ 悪い: 条件分岐がある
@when('カートを確認する')
def step_impl(context):
    if context.user_status == 'VIP':   # ← if は禁止
        context.api_client.apply_vip_discount()
    context.api_client.view_cart()

# ❌ 悪い: 正規表現パースを使っている
import re

@when('"{item}" を {count} 個追加して合計 {total} 円になる場合')
def step_impl(context, item, count, total):
    count = int(re.sub(r'[^\d]', '', count))   # ← 自前パースは禁止
```

---

## 8. Execution 層の設計パターン

Step 定義（Glue 層）が委譲する先（`context.xxx`）の設計パターン。

### API Client パターン

REST API テストにおける最も一般的なパターン。

```python
# execution/api_client.py
import requests


class ApiClient:
    """Execution 層: 実際の HTTP 通信を担当する"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.last_response = None

    def login(self, username: str, password: str = "default"):
        self.last_response = self.session.post(
            f"{self.base_url}/api/login",
            json={"username": username, "password": password},
        )

    def add_items_to_cart(self, name: str, unit_price: int, quantity: int):
        self.last_response = self.session.post(
            f"{self.base_url}/api/cart/items",
            json={"name": name, "unit_price": unit_price, "quantity": quantity},
        )

    def calculate_shipping(self) -> int:
        resp = self.session.get(f"{self.base_url}/api/cart/shipping")
        return resp.json()["shipping"]

    def setup_users(self, users: list[dict]):
        for user in users:
            self.session.post(f"{self.base_url}/api/users", json=user)

    def reset(self):
        self.session.post(f"{self.base_url}/api/test/reset")

    def cleanup(self):
        self.session.close()
```

### Step → Execution 委譲の対比

```python
# ❌ 悪い: Step（Glue層）に実装詳細が漏れている
@when('ユーザー "{username}" でログインする')  # type: ignore
def step_impl(context, username):
    response = requests.post(
        f"{context.base_url}/api/login",
        json={"username": username, "password": "default"},
    )
    context.last_response = response
    context.token = response.json().get("token")

# ✅ 良い: Step は Execution 層に委譲するだけ
@when('ユーザー "{username}" でログインする')  # type: ignore
def step_impl(context, username):
    context.api_client.login(username)
```

### その他のパターン概要

| パターン | 適用場面 | context に設定するもの |
|---|---|---|
| **Page Object** | ブラウザ UI テスト | `context.login_page = LoginPage(driver)` |
| **Service Facade** | 結合テスト（API を介さない） | `context.order_service = OrderService(db)` |
| **Fixture Builder** | 複雑なテストデータ準備 | `context.fixture = FixtureBuilder(db)` |

---

## 9. environment.py のパターン

### 標準構成

```python
# features/environment.py
from execution.api_client import ApiClient


def before_all(context):
    """テスト全体の初期化"""
    context.base_url = "http://localhost:8000"
    context.api_client = ApiClient(base_url=context.base_url)


def before_scenario(context, scenario):
    """シナリオごとのリセット"""
    context.api_client.reset()


def after_all(context):
    """テスト終了後のクリーンアップ"""
    context.api_client.cleanup()
```

### ルール: environment.py に書くもの

| 書いてよいもの | 書いてはいけないもの |
|---|---|
| クライアントの初期化 | ビジネスロジック |
| DB 接続 / リセット | アサーション |
| 認証トークンの設定 | テストデータの準備（Step に書く） |

---

## 10. Anti-Patterns 一覧

| 禁止 | 理由 |
|---|---|
| テストが通るように仕様を弱める | 設計の裏切り |
| Step に `if` / `for` を書く | ロジックの混入 |
| 実装の都合を Gherkin に持ち込む | 関心の逆転 |
| 失敗するテストを削除する | 設計の意思の消滅 |
| `context` に中間計算結果を詰め込む | Step の責務超過 |
| Step 関数を共有しすぎる | 暗黙の依存 |

### テスト失敗の扱い

- 実装が未完成でテストが落ちる → **正常。実装を直すべき**
- 仕様が変わってテストが落ちる → **正常。仕様の変更を反映すべき**
- テストが間違っていてテストが落ちる → **テストを修正する（仕様に合わせる）**

### @wip タグによる段階的実装

```gherkin
@wip
Scenario: まだ実装されていないシナリオ
  Given 未実装の前提条件
  When 未実装のアクション
  Then 未実装の期待結果
```

```bash
# @wip タグ付きだけ実行する
behave --tags=wip

# @wip タグを除外して実行する
behave --tags=~wip
```

`@wip` は「実装予定」を示す一時的なタグ。実装が完了したら必ず削除すること。

---

## 11. 完全実装例

### Gherkin Feature

`specification/features/checkout.feature`

```gherkin
@TRC-001
Feature: ショッピングカートと決済の制御

  Background:
    Given システムに以下のユーザーが登録されている:
      | username | status |
      | alice    | VIP    |
      | bob      | NORMAL |

  Rule: VIPユーザーは一定金額以上で送料無料になる

    Scenario Outline: VIPユーザーの購入金額別送料
      Given ユーザー "alice" としてログインしている
      When カートに <品数> 個の "高級イヤホン" (単価: <単価>円) を追加する
      Then 送料は <送料> 円になること

      Examples: 通常送料
        | 品数 | 単価 | 送料 |
        | 1    | 5000 | 500  |

      Examples: 送料無料ライン到達
        | 品数 | 単価 | 送料 |
        | 2    | 5000 | 0    |
```

### Python Step 定義

```python
from behave import given, when, then


@given('システムに以下のユーザーが登録されている:')
def step_impl(context):
    users = [
        {"username": row["username"], "status": row["status"]}
        for row in context.table
    ]
    context.api_client.setup_users(users)


@given('ユーザー "{username}" としてログインしている')
def step_impl(context, username):
    context.api_client.login(username)


@when('カートに {count:d} 個の "{item}" (単価: {price:d}円) を追加する')
def step_impl(context, count, item, price):
    context.api_client.add_items_to_cart(
        name=item,
        unit_price=price,
        quantity=count,
    )


@then('送料は {expected:d} 円になること')
def step_impl(context, expected):
    actual = context.api_client.calculate_shipping()
    assert actual == expected
```

### Step 定義ファイルの分割ルール

```
features/
├── steps/
│   ├── common_steps.py      # 複数 Feature で共通する Given
│   ├── checkout_steps.py    # checkout.feature 専用
│   ├── auth_steps.py        # auth.feature 専用
│   └── inventory_steps.py   # inventory.feature 専用
└── environment.py
```

- 複数の Feature でまったく同じ文言の Step が必要な場合のみ共有する
- 文言が似ていても意味が違う場合は別の Step として定義する
- Step を共有する場合は `common_steps.py` に集約し、ファイル名で明示する

### behave の実行コマンド

```bash
# 全シナリオ実行
uv run behave specification/features/

# 特定の .feature だけ実行
uv run behave specification/features/checkout.feature

# タグ指定で実行
uv run behave --tags=TRC-001 specification/features/

# 詳細出力
uv run behave --no-capture specification/features/

# Cucumber JSON 出力（spec-weaver build で使用）
uv run behave --format json -o test-results.json specification/features/
```
