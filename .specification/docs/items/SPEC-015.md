# [SPEC-015] scaffold コマンド —  behave テストコード自動生成

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-03-02

**上位アイテム**: [REQ-011](REQ-011.md) / **下位アイテム**: [PLAN-002](PLAN-002.md) / **兄弟アイテム**: [SPEC-016](SPEC-016.md)

**テストカバレッジ**:  - （下位アイテムの集計）

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
`spec-weaver scaffold` コマンドにより、`.feature` ファイルから
behave 互換のテストコード雛形を自動生成・差分マージする。

## 詳細仕様

### コマンドインターフェース
```
spec-weaver scaffold <feature_dir>
  --out-dir <path>       # テストコード出力先（デフォルト: tests/features/）
  --overwrite            # 既存ファイルを全上書きする
  --repo-root <path>     # Git dirty チェック用リポジトリルート（デフォルト: cwd）
  --force                # 確認プロンプトをスキップして強制マージ（非対話モード）
```

### テストコード生成ロジック
1. 指定ディレクトリの `.feature` ファイルを Gherkin AST で解析する
2. 各 Feature に対して `step_<feature_stem>.py` を生成・マージする
3. 各ステップ（Given/When/Then）に対して以下を生成する:
   - `@given` / `@when` / `@then` デコレータ付きのステップ関数
   - 関数名はステップ文のハッシュ先頭8文字: `<prefix>_<hash8>`
   - docstring にオリジナルのステップ文と Scenarios セクションを記載
4. 同一ステップ文が複数シナリオで使われる場合、関数は1回のみ生成する（重複排除）
5. Docstring の Scenarios セクションには、そのステップを使用する全シナリオを列挙する
6. 出力先ディレクトリの他ファイルに同一ステップが定義済みの場合（スタブを含む）、
   そのステップは通常のスタブではなく Duplicate コメントブロックとして出力する。
   behave はステップをグローバルに解決するため、同一パターンが複数定義されると
   AmbiguousStep エラーになる。これを防ぐための措置。
   - 判定対象: `@given/@when/@then/@step` デコレータが付いた有効な行のみ
   - コメント行（`#` 始まり）内のデコレータは判定対象外とする

### 差分マージ動作（既存ファイルあり・--overwrite なし）
1. `.feature` から「仮想新規ファイル」を生成し、理想的な関数順序を得る
2. 既存ファイルの関数名リストと照合する:
   - 既存関数が存在する → Docstring の Scenarios セクションに不足シナリオを追記
   - 存在しない新規関数 → `.feature` の出現順を維持した位置に挿入する
      （直前に存在する関数の直後、アンカーがなければヘッダー直後）
3. 変更がない場合はファイルへの書き込みを行わない（スキップ）
4. 変更がある場合は unified diff を生成してコンソールに表示する
5. 他ファイルに実装済みのステップ（スタブ含む）が新たに追加された場合、
   既存ファイル内の対応スタブを Duplicate コメントブロックへ置き換える

### 戻り値（`generate_test_file` 関数）
- `(Path, "created", "")` — 新規ファイル作成
- `(Path, "updated", diff_text)` — 既存ファイルへの差分マージ
- `None` — 変更なし（スキップ）

### Git dirty チェック
- 既存ファイルに未コミットの変更がある場合、確認プロンプトを表示する
- `--force` を指定するとプロンプトをスキップして強制マージする

## 受け入れ基準
- `.feature` ファイルから behave テストコードが生成されること
- 生成された関数名に日本語が含まれないこと（ハッシュベース命名）
- 生成されたコードが構文的に正しい Python であること
- 同一ステップが重複生成されないこと
- 各ステップ関数の Docstring に Scenarios セクションが含まれること
- 既存ファイルに差分がない場合はスキップされること
- 新規ステップが .feature の出現順で既存ファイルに挿入されること
- Git 未コミット変更がある場合に確認プロンプトを表示すること
- `--force` でプロンプトなしにマージが実行されること
- 他のステップファイルに定義済みのステップ（スタブ含む）は Duplicate コメントとして生成されること
- Duplicate コメント行内のデコレータは重複判定に使用されないこと

### 🧪 検証シナリオ

- **基本的なテストコード生成** — Scenario （[features/scaffold.feature:6](../features/scaffold.md)）
- **ハッシュベースの関数名生成** — Scenario （[features/scaffold.feature:12](../features/scaffold.md)）
- **ステップ関数の生成と重複排除** — Scenario （[features/scaffold.feature:19](../features/scaffold.md)）
- **Docstring にシナリオリストを記載** — Scenario （[features/scaffold.feature:24](../features/scaffold.md)）
- **差分マージ（新規ステップ追記）** — Scenario （[features/scaffold.feature:30](../features/scaffold.md)）
- **差分なし時のスキップ** — Scenario （[features/scaffold.feature:38](../features/scaffold.md)）
- **既存ファイルの上書き** — Scenario （[features/scaffold.feature:44](../features/scaffold.md)）
- **Git 未コミット変更の確認プロンプト** — Scenario （[features/scaffold.feature:49](../features/scaffold.md)）
- **--force オプションで確認プロンプトをスキップ** — Scenario （[features/scaffold.feature:55](../features/scaffold.md)）
- **差分マージ時の Duplicate スタブのコメント化** — Scenario （[features/scaffold.feature:60](../features/scaffold.md)）
- **差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない** — Scenario （[features/scaffold.feature:67](../features/scaffold.md)）