# [PLAN-001] 実装ファイルリンク管理機能の実装計画

**実装状況**: ✅ implemented

**作成日**: 2026-02-27　|　**更新日**: 2026-03-02

**上位アイテム**: [SPEC-017](SPEC-017.md), [SPEC-018](SPEC-018.md), [SPEC-019](SPEC-019.md), [SPEC-020](SPEC-020.md)


### 内容

## 概要
仕様アイテムと実装ファイルのリンク管理機能を実装する計画。
SPEC-017〜020 に対応する。

## 実装タスク（実行順）

### Task 1: impl_scanner.py の新規作成（SPEC-017, SPEC-018）
**ファイル**: `src/spec_weaver/impl_scanner.py`
**内容**:
- `get_ref_files(item) -> list[str]`:
  ref フィールドを読み取り、文字列・リスト・空文字を統一的に処理して返す
- `ImplScanner` クラス:
  - `scan(repo_root, extensions=None) -> dict[str, set[str]]`
    正規表現 `r'(?:#|//|--)\s*implements:\s*(.+)'` でアノテーションを抽出
    `.git/`, `__pycache__/`, `.venv/` 等を除外
    extensions が指定された場合はその拡張子のみ対象

### Task 2: doorstop.py への ref 読み取り関数追加（SPEC-017）
**ファイル**: `src/spec_weaver/doorstop.py`
**内容**:
- impl_scanner.py に get_ref_files を集約するため doorstop.py への追加は最小限とする
- get_item_map の import を impl_scanner から呼べるよう整理

### Task 3: audit コマンドの拡張（SPEC-019）
**ファイル**: `src/spec_weaver/cli.py`
**追加オプション**:
- `--check-impl` (bool, default: False): 実装ファイルリンク検証を有効化
- `--extensions TEXT` (str, default: None): スキャン拡張子のカンマ区切り指定
**処理フロー**（--check-impl 時）:
1. get_item_map で全 SPEC の ref を収集
2. ImplScanner.scan() でアノテーションを収集
3. 3種の乖離を検出・表示:
   a. ref のファイルが存在しない（❌）
   b. ref にあってアノテーションなし（⚠️）
   c. アノテーションあって ref なし（⚠️）

### Task 4: trace コマンドの拡張（SPEC-020）
**ファイル**: `src/spec_weaver/cli.py`
**追加オプション**:
- `--show-impl` (bool, default: False): 実装ファイルをツリー表示
- `--extensions TEXT` (str, default: None): アノテーションスキャン拡張子
**処理**:
- `_add_descendants_to_rich_node` にパラメータを追加
- SPEC ノード直下に 📁（ref 由来）/ 📝（annotation のみ）を表示
- ファイル不在は ❌ で表示

### Task 5: テストの追加
**ファイル**: `tests/test_impl_scanner.py`（新規）
**内容**:
- get_ref_files のユニットテスト（list/string/空文字の各形式）
- ImplScanner.scan のユニットテスト（単一ID, 複数ID, extensions フィルタ）
**ファイル**: `tests/test_cli.py` or `tests/test_impl_link.py`（追記 or 新規）
- audit --check-impl のテスト
- trace --show-impl のテスト

### Task 6: dev-lifecycle スキルの更新
**ファイル**: `.claude/skills/dev-lifecycle-skill/skill.md`
**内容**:
Phase 4（実装）の末尾に以下のステップを追加:
> #### 実装ファイルの ref 記述
> コードを変更したら、対象 SPEC の YAML `ref` フィールドに
> 実装ファイルパスをリスト形式で記述すること:
> ```yaml
> ref:
>   - src/your_module.py
> ```
> ソースファイルにもアノテーションを記述すること:
> ```python
> # implements: SPEC-XXX
> ```

## 依存関係
Task 1 → Task 2（impl_scanner が doorstop に依存）
Task 1 → Task 3（audit が impl_scanner を使う）
Task 1 → Task 4（trace が impl_scanner を使う）
Task 3, Task 4 → Task 5（テストは実装後）
Task 1〜5 → Task 6（スキル更新は最後）

## 完了条件
- uv run pytest tests/ -q が全て通過
- uv run spec-weaver audit --check-impl ./specification/features が正常終了
- uv run spec-weaver trace SPEC-018 -f ./specification/features --show-impl が正常表示
- uv run spec-weaver audit ./specification/features が従来通り動作
