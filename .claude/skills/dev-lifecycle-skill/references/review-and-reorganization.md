# ドキュメントレビュー & 再編ガイド

Doorstop + Gherkin で管理された仕様ドキュメントの健全性を診断し、
問題があれば段階的に再整理する。

---

## 1. レビュー（診断のみ）手順

ドキュメントを変更せず、問題点を報告する。

### Step 1: 構造スキャン

```bash
# Doorstop ドキュメントツリーの全体像を把握
find ./specification -name ".doorstop.yml" | sort

# 各ドキュメントのアイテム数を確認
find ./specification -name "*.yml" ! -name ".doorstop.yml" | \
  awk -F'/' '{print $NF}' | sed 's/-[0-9]*.yml//' | sort | uniq -c | sort -rn
```

### Step 2: Doorstop バリデーション

```bash
# リンク切れ・未レビューアイテムを検出
doorstop

# 全アイテムのステータス一覧
spec-weaver status
```

### Step 3: Gherkin 整合性チェック

```bash
# SPEC と .feature の対応チェック
spec-weaver audit ./specification/features

# 孤立した SPEC（feature で参照されていないもの）を確認
spec-weaver audit ./specification/features --show-untested
```

### Step 4: ファイル内容の分析

以下を Grep / Read ツールで確認する:

```bash
# status フィールドが未設定のアイテム
grep -rL "^status:" ./specification/reqs ./specification/specs 2>/dev/null

# active: false なアイテム（廃止済み・整理候補）
grep -rl "^active: false" ./specification/

# links が空のアイテム（孤立アイテム候補）
grep -rA1 "^links:" ./specification/ | grep "links: \[\]"
```

---

## 2. レビューチェックリスト

### A. 構造チェック

#### A-1. ドキュメント一覧の把握

```bash
find ./specification -name ".doorstop.yml" | sort
```

確認すること:
- [ ] どのドキュメント（prefix）が存在するか
- [ ] 各ドキュメントの親子関係が意図通りか
- [ ] 孤立したディレクトリ（`.doorstop.yml` が missing）がないか

#### A-2. アイテム数の確認

```bash
for dir in $(find ./specification -name ".doorstop.yml" -exec dirname {} \;); do
  count=$(find "$dir" -maxdepth 1 -name "*.yml" ! -name ".doorstop.yml" | wc -l)
  echo "$count  $dir"
done | sort -rn
```

判断基準:
- [ ] 1ドキュメントに **10件以上** → サブドキュメント分割を推奨
- [ ] 1ドキュメントに **20件以上** → 分割が必要（見通しが著しく悪い）
- [ ] 1ドキュメントに **0件** → 空ドキュメント（削除候補）

#### A-3. `level` フィールドの利用状況

```bash
grep -rh "^level:" ./specification/reqs ./specification/specs | sort | uniq -c
```

確認すること:
- [ ] `normative: false` の `level: X.0` アイテムがセクション見出しとして機能しているか
- [ ] level が連番になっていて飛びがないか

### B. リンク整合性チェック

#### B-1. Doorstop バリデーション

```bash
doorstop
```

- [ ] エラー・警告が 0 件
- [ ] "WARNING" メッセージの内容を把握

#### B-2. 孤立アイテムの検出

```bash
grep -rl "^links: \[\]" ./specification/specs/ 2>/dev/null
grep -rl "^links: \[\]" ./specification/reqs/ 2>/dev/null
```

- [ ] SPEC で `links: []` → 親 REQ へのリンクが未設定（要修正）
- [ ] 拡張ドキュメント（DESIGN/PLAN/ADR）で `links: []` → SPEC へのリンクが未設定

#### B-3. active: false のアイテムへのリンク

- [ ] 非アクティブアイテムへのリンクが残っていないか

### C. 内容チェック

#### C-1. text フィールドの充足

```bash
grep -rA3 "^text:" ./specification/reqs ./specification/specs | \
  grep -B1 "text: ''" | grep "\.yml"
```

- [ ] `text: ''` のアイテム → 記述が未完了
- [ ] text の内容が 1行以下 → 不十分な可能性

#### C-2. status フィールドの管理

- [ ] `status` 未設定のアイテムが多数 → 一括更新を推奨
- [ ] `status: deprecated` なのに `active: true` → `active: false` に変更すべき

#### C-3. 重複・類似アイテムの検出

```bash
# header フィールドの一覧（類似タイトルを探す）
grep -rh "^header:" ./specification/reqs ./specification/specs | sort
```

- [ ] 同じ機能を別の言葉で説明しているアイテムがないか
- [ ] 分割すべき複合要件がないか
- [ ] 統合すべき粒度の細かすぎるアイテムがないか

### D. Gherkin 連携チェック

#### D-1. Spec-Weaver 監査

```bash
spec-weaver audit ./specification/features
```

- [ ] `MISSING_SPEC` → feature のタグに対応する SPEC が存在しない
- [ ] `UNTESTED_SPEC` → SPEC に対応する feature シナリオがない

#### D-2. testable 設定の確認

- [ ] Gherkin でテストできない仕様に `testable: false` が付いているか
- [ ] `testable: false` が多すぎないか

#### D-3. feature ファイルのタグ確認

```bash
grep -rh "@[A-Z][A-Z0-9-]*" ./specification/features/ | \
  grep -o "@[A-Z][A-Z0-9-]*" | sort | uniq
```

- [ ] タグに対応する SPEC/REQ ID が実際に存在するか
- [ ] 古い ID のタグが残っていないか

### E. 鮮度チェック

```bash
spec-weaver audit ./specification/features --stale-days 90
```

- [ ] stale アイテムの内容が今も有効か
- [ ] `status: deprecated` かつ `active: true` → `active: false` への移行を検討

### F. layer 分類チェック

#### F-1. layer 属性の設定状況

```bash
find ./specification/specs -name "*.yml" ! -name ".doorstop.yml" -exec grep -L "^layer:" {} \;
grep -rh "^layer:" ./specification/specs/ 2>/dev/null | sort | uniq -c
```

- [ ] 新規アイテムに `layer` が設定されているか
- [ ] `layer` の値が `behavior` または `architecture` のいずれかか

#### F-2. layer と Gherkin タグの整合性

- [ ] `layer: architecture` の SPEC に `@SPEC-xxx` タグが付いた .feature がないか
- [ ] `layer: behavior` かつ `testable: true` の SPEC に対応する .feature があるか

#### F-3. layer 分類の妥当性

| 判断基準 | `behavior` が適切 | `architecture` が適切 |
|---|---|---|
| 外部アクターが結果を観察できるか | はい | いいえ |
| Given-When-Then で表現できるか | はい | いいえ |
| 受け入れ条件として書けるか | はい | いいえ |
| 内部構造・技術選定に関する記述か | いいえ | はい |

---

## 3. レビュー報告フォーマット

```markdown
## 仕様ドキュメント レビュー報告

### サマリー
- ドキュメント数: N
- 総アイテム数: N
- 問題アイテム数: N

### 問題一覧

#### 🔴 構造的問題（再編が必要）
- `REQ`: 20件がフラット。グループ化未実施 → 分割を推奨
- `OAUTH-REQ` と `AUTH-REQ` が少数ずつ混在 → 集約を推奨

#### 🟡 内容的問題（内容の修正が必要）
- `SPEC-003`, `VIS-003`: 類似した振る舞いを記述している（重複の可能性）
- `REQ-005`: text フィールドが空

#### 🟠 layer 分類の問題
- `CORE-002`: `layer` 属性が未設定（未分類）
- `VIS-005`: `layer: architecture` だが .feature でテストされている

#### 🟢 鮮度・管理上の問題（軽微）
- `VIS-007`: status フィールドが未設定
- `REQ-008`: active: false だがリンクが残っている

### 推奨アクション（優先順）
1. REQ を機能領域別サブドキュメントに分割（→ 分割操作）
2. OAUTH-REQ を AUTH-REQ に統合（→ 集約操作）
3. AUT-001 のリンク切れを修正（→ 個別修正）
```

| 重要度 | 基準 | 対応 |
|---|---|---|
| 🔴 構造的問題 | ドキュメント構造に起因する問題 | 再編操作で対応 |
| 🟡 内容的問題 | アイテムの記述・リンクに問題がある | 個別修正で対応 |
| 🟢 管理上の問題 | status 未設定・stale 等の軽微な問題 | 随時修正 |

---

## 4. 再編操作: 分割

フラットなドキュメントを機能ドメイン別サブドキュメントに分ける。

> Doorstop はアイテムの「移動」コマンドを持たない。
> 再編とは「新ドキュメントに新アイテムを作り、旧アイテムを非アクティブ化する」プロセスである。

### 計画フォーマット

```markdown
## 分割計画

### 現状
REQ（20件フラット）→ SPEC（18件フラット）

### 提案する新構造
REQ（横断的要件のみ 3件）
├── AUTH-REQ（認証ドメイン 6件）
├── PAY-REQ（決済ドメイン 7件）
└── NTF-REQ（通知ドメイン 4件）

### マイグレーション対象
- REQ-002, REQ-005, REQ-008 → AUTH-REQ へ
- REQ-003, REQ-009, REQ-011 → PAY-REQ へ
```

**⛔ STOP: 計画をユーザーに提示し、承認を得てから実行する。**

### 実行手順

#### フェーズ1: 準備

移行対象アイテムのマッピング表を作成する:

```
旧ID     → 新ドキュメント  新ID（連番）
REQ-002  → AUTH-REQ      AUTH-REQ-001
REQ-005  → AUTH-REQ      AUTH-REQ-002
```

影響範囲を確認:
```bash
spec-weaver trace REQ-002 -f ./specification/features
grep -rn "@REQ-002" ./specification/features/
```

#### フェーズ2: 新ドキュメントの作成

```bash
doorstop create AUTH-REQ ./specification/reqs/auth --parent REQ
# .doorstop.yml の sep: '-' を確認
```

#### フェーズ3: アイテムのマイグレーション

各旧アイテムを1件ずつ移行する:

```bash
# Step A: 新ドキュメントにアイテムを追加
doorstop add AUTH-REQ   # → AUTH-REQ-001.yml が生成される

# Step B: 旧アイテムの内容を新アイテムにコピー
# （level, header, status 等のカスタム属性もコピーする）

# Step C: 旧アイテムを非アクティブ化
# REQ-002.yml: active: false, migrated_to: AUTH-REQ-001
```

> **注意**: アイテムを削除（ファイルごと削除）すると Git 履歴が失われる。
> `active: false` で非アクティブ化して残すことを推奨。

#### フェーズ4: SPEC のリンク張り直し

```bash
# 旧リンクを YAML 直接編集で削除
# 新しいリンクを張る
doorstop link QA-001 AUTH-REQ-001
doorstop  # バリデーション
```

#### フェーズ5: feature タグの更新

```bash
grep -rn "@REQ-002" ./specification/features/
# @REQ-002 → @AUTH-REQ-001 に置換
```

#### フェーズ6: 検証

```bash
doorstop
spec-weaver audit ./specification/features
spec-weaver status
```

### level セクション化（分割の軽量版）

ドメイン分割までは不要だが、同一ドキュメント内で整理したい場合。
`normative: false` のセクション見出しアイテムを挿入する。

```yaml
# セクション見出し用アイテム
active: true
level: 1.0        # ← セクション番号.0
normative: false  # ← false でヘッダー扱い
header: '認証機能'
text: ''
links: []
```

---

## 5. 再編操作: 集約

### ドキュメント集約（複数ドキュメントを1つに統合）

別々のドキュメントに分散しているが、実態は同一ドメインである場合に統合する。

#### 計画フォーマット

```markdown
## 集約計画

### 現状
AUTH-REQ（3件）と OAUTH-REQ（2件）が別ドキュメントだが内容が密接に関連

### 提案する新構造
AUTH-REQ（5件：従来の AUTH-REQ + OAUTH-REQ を統合）
OAUTH-REQ ドキュメントは廃止

### マイグレーション対象
- OAUTH-REQ-001 → AUTH-REQ-004 へ統合
- OAUTH-REQ-002 → AUTH-REQ-005 へ統合
```

**⛔ STOP: 計画をユーザーに提示し、承認を得てから実行する。**

#### 実行手順

```bash
# 1. 統合先ドキュメントに新アイテムを追加
doorstop add AUTH-REQ   # → AUTH-REQ-004.yml 生成
# OAUTH-REQ-001.yml の内容（text, status, header 等）をコピー

# 2. 統合元アイテムを非アクティブ化
# OAUTH-REQ-001.yml: active: false, migrated_to: AUTH-REQ-004, status: deprecated

# 3. SPEC のリンクを張り直す
doorstop link SPEC-xxx AUTH-REQ-004
# YAML から OAUTH-REQ-001 を削除

# 4. feature タグを更新
# @OAUTH-REQ-001 → @AUTH-REQ-004

# 5. 空になったドキュメントの処理
# 選択肢A（推奨）: .doorstop.yml は残し、active アイテム 0 件の状態にする
# 選択肢B: ディレクトリごと削除（rm -rf ./specification/reqs/oauth/）

# 6. バリデーション
doorstop && spec-weaver audit ./specification/features
```

### アイテム集約（複数アイテムを1つに統合）

粒度が細かすぎる複数のアイテムを、1つの包括的なアイテムにまとめる。

```bash
# 1. 統合先アイテムの text を更新（両方の内容を包含する形で記述）
# 2. 統合元を非アクティブ化: active: false, migrated_to: SPEC-003, status: deprecated
# 3. 統合元を参照するリンクを更新
# 4. feature タグを更新
# 5. バリデーション
doorstop && spec-weaver audit ./specification/features
```

---

## 6. 再編操作: 階層変更

ドキュメントの親子関係（`--parent`）を変更する。

### 親の変更

Doorstop の親子関係は `.doorstop.yml` の `parent` フィールドで管理される:

```yaml
settings:
  digits: 3
  parent: REQ      # ← この parent を変更する
  prefix: NOTIFY-REQ
  sep: '-'
```

#### 手順

```bash
# 1. 中間ドキュメントが必要なら作成
doorstop create MESSAGING-REQ ./specification/reqs/messaging --parent REQ

# 2. 移動するドキュメントの .doorstop.yml を編集
# parent: REQ → parent: MESSAGING-REQ

# 3. バリデーション
doorstop
```

### サブドキュメントをルートに昇格

```bash
# .doorstop.yml を編集: parent: REQ → parent: '' （親なし）
doorstop  # バリデーション
```

> **注意**: ルートドキュメントが複数になる場合、Doorstop はそれぞれ独立したツリーとして扱う。

### フラットな兄弟ドキュメントを階層化

中間層を挿入して多数の兄弟ドキュメントをグループ化する:

```bash
# 1. 中間ドキュメントを作成
doorstop create IDENTITY-REQ ./specification/reqs/identity --parent REQ

# 2. 各子ドキュメントの .doorstop.yml の parent を変更
# auth/.doorstop.yml: parent: IDENTITY-REQ
# oauth/.doorstop.yml: parent: IDENTITY-REQ

# 3. バリデーション
doorstop
```

---

## 7. 再編後の共通確認手順

どの操作を行った後も必ず実施する:

```bash
# Doorstop 全体バリデーション
doorstop

# Spec-Weaver 整合性チェック
spec-weaver audit ./specification/features

# ステータス確認
spec-weaver status
```

**⛔ STOP: 全チェックが通過したことを確認し、ユーザーに報告する。**

### コミット

```bash
git add ./specification/
git commit -m "refactor(spec): <操作の概要を記述>"
# 例: refactor(spec): AUTH-REQ と OAUTH-REQ を統合
# 例: refactor(spec): REQ をドメイン別サブドキュメントに分割
```

### よくある問題と対処法

| 問題 | 対処法 |
|---|---|
| `doorstop link` で "already linked" エラー | 旧リンクを YAML の `links` フィールドを直接編集して削除 |
| 新 ID と旧 ID が混在して混乱する | 旧アイテムに `migrated_to: <新ID>` カスタム属性を追記 |
| feature タグが多数あって一括置換したい | `sed -i 's/@REQ-002/@AUTH-REQ-001/g' ./specification/features/*.feature` |
| doorstop バリデーションが通らない | `doorstop --verbose` で詳細確認 |

---

## 8. 個別アイテムの整合性修正パターン

構造変更は不要だが、個々のアイテムに問題がある場合に使う。

### リンク切れの修正

```bash
doorstop link AUT-001 REQ-010
doorstop edit AUT-001  # 古いリンクを YAML から削除
```

### 孤立アイテムへのリンク追加

```bash
doorstop link VIS-003 REQ-003
```

### 廃止アイテムのクリーンアップ

```bash
doorstop edit REQ-008  # → active: false に変更
```

### 重複アイテムの統合

1. どちらのアイテムを残すか決める
2. 残す方に両方の内容を統合して記述
3. 統合元のアイテムを `active: false` にする
4. 統合先のアイテムに関連する全リンクを確認・更新
