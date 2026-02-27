# [SPEC-016] CI/CD パイプライン統合 — テスト実行・結果反映の自動化

**実装状況**: ✅ implemented

**作成日**: 2026-02-26　|　**更新日**: 2026-02-27

**上位アイテム**: [REQ-011](REQ-011.md) / **兄弟アイテム**: [SPEC-015](SPEC-015.md)

**テスト対象**: Yes　**個別カバレッジ**: 🟢 1/1 (100%)


### 内容

## 概要
scaffold で生成した BDD テストの実行から、Cucumber JSON レポート出力、
`build` ドキュメントへの結果反映までを CI/CD パイプラインとして
一貫実行する仕組みを提供する。

## 詳細仕様

### spec-weaver ci コマンド
```
spec-weaver ci <feature_dir>
  --test-dir <path>         # テストコード格納先（デフォルト: tests/features/）
  --out-dir <path>          # build 出力先（デフォルト: .specification/）
  --report <path>           # Cucumber JSON 出力先（デフォルト: test-results.json）
  --scaffold                # テスト生成も実行する
```

### 処理フロー
1. `--scaffold` 指定時: `scaffold` と同等の処理でテストコードを生成
2. pytest-bdd を実行し、Cucumber 互換 JSON レポートを生成する
   - `pytest <test_dir> --cucumber-json-report=<report>`
3. 生成された JSON レポートを使用して `build` を実行する
   - `spec-weaver build <feature_dir> --test-results <report> --out-dir <out_dir>`
4. 各ステップの成否をコンソールに報告する

### エラーハンドリング
- テスト失敗時もドキュメント生成は継続する（FAIL 結果がドキュメントに反映される）
- pytest 自体の実行エラー（import エラー等）はエラーとして報告する

## 受け入れ基準
- `ci` コマンドでテスト実行→ドキュメント生成が一気通貫で実行されること
- テスト失敗時もドキュメント生成が行われ、FAIL 結果が反映されること
- `--scaffold` オプションでテストコード生成も含められること

### 🧪 検証シナリオ

- **ci コマンド** — Feature （[features/ci.feature:2](../features/ci.md)）