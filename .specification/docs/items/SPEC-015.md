# [SPEC-015] scaffold コマンド —  behave テストコード自動生成

> 📋 **Unreviewed Changes**: このアイテム自体に未レビューの変更があります。

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-02-27

**上位アイテム**: [REQ-011](REQ-011.md) / **兄弟アイテム**: [SPEC-016](SPEC-016.md)

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
`spec-weaver scaffold` コマンドにより、`.feature` ファイルから
behave 互換のテストコード雛形を自動生成する。

## 詳細仕様

### コマンドインターフェース
```
spec-weaver scaffold <feature_dir>
  --out-dir <path>       # テストコード出力先（デフォルト: tests/features/）
  --overwrite            # 既存ファイルの上書きを許可
```

### テストコード生成ロジック
1. 指定ディレクトリの `.feature` ファイルを Gherkin AST で解析する
2. 各 Feature に対して `test_<feature_stem>.py` を生成する
3. 各 Scenario に対して以下を生成する:
   - `@scenario` デコレータ付きのテスト関数
   - 関数名はシナリオ名の SHA256 ハッシュ先頭8文字を使用: `test_<hash8>`
   - docstring にオリジナルのシナリオ名を記載（可読性確保）
4. 各ステップ（Given/When/Then）に対して以下を生成する:
   - `@given` / `@when` / `@then` デコレータ付きのステップ関数
   - 関数名はステップ文のハッシュ先頭8文字: `<prefix>_<hash8>`
   - docstring にオリジナルのステップ文を記載
5. 同一ステップ文が複数シナリオで使われる場合、関数は1回のみ生成する（重複排除）

### 上書き制御
- デフォルトでは既存ファイルをスキップし、警告メッセージを表示する
- `--overwrite` フラグで既存ファイルの上書きを許可する

## 受け入れ基準
- `.feature` ファイルから behave テストコードが生成されること
- 生成された関数名に日本語が含まれないこと（ハッシュベース命名）
- 生成されたコードが構文的に正しい Python であること
- 同一ステップが重複生成されないこと
- 既存ファイルはデフォルトでスキップされること

### 🧪 検証シナリオ

- **scaffold コマンド** — Feature （[features/scaffold.feature:2](../features/scaffold.md)）