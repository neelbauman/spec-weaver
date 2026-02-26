# 仕様一覧 (SPEC)

| ID | タイトル | 関連要件 (REQ) | 兄弟 | カバレッジ | 実装状況 | 状態 |
| :--- | :--- | :--- | :--- | :--- | :--- | :---|
| [SPEC-001](items/SPEC-001.md) | コア・アーキテクチャ | [REQ-001](items/REQ-001.md) | [SPEC-002](items/SPEC-002.md) | ⚪️ - | ✅ implemented | ⚪️ |
| [SPEC-002](items/SPEC-002.md) | データ抽出基盤 | [REQ-001](items/REQ-001.md)<br>[REQ-002](items/REQ-002.md) | [SPEC-001](items/SPEC-001.md)<br>[SPEC-003](items/SPEC-003.md) | 🟢 1/1 (100%) | ✅ implemented | 🟢 |
| [SPEC-003](items/SPEC-003.md) | audit コマンド仕様 | [REQ-002](items/REQ-002.md) | [SPEC-002](items/SPEC-002.md) | 🟢 1/1 (100%) | ✅ implemented | 🟢 |
| [SPEC-004](items/SPEC-004.md) | build コマンド仕様 | [REQ-003](items/REQ-003.md) | - | 🟢 1/1 (100%) | ✅ implemented | 🟢 |
| [SPEC-005](items/SPEC-005.md) | Suspect（変更波及）対応 | [REQ-004](items/REQ-004.md) | - | ⚪️ - | ✅ implemented | ⚪️ |
| [SPEC-006](items/SPEC-006.md) | テスト結果統合 | [REQ-005](items/REQ-005.md) | - | ⚪️ - | ✅ implemented | ⚪️ |
| [SPEC-007](items/SPEC-007.md) | status カスタム属性の定義 | [REQ-006](items/REQ-006.md) | [SPEC-008](items/SPEC-008.md)<br>[SPEC-009](items/SPEC-009.md) | ⚪️ - | ✅ implemented | ⚪️ |
| [SPEC-008](items/SPEC-008.md) | status コマンド仕様 | [REQ-006](items/REQ-006.md) | [SPEC-007](items/SPEC-007.md)<br>[SPEC-009](items/SPEC-009.md) | 🟢 1/1 (100%) | ✅ implemented | 🟢 |
| [SPEC-009](items/SPEC-009.md) | build への実装状況統合 | [REQ-006](items/REQ-006.md) | [SPEC-007](items/SPEC-007.md)<br>[SPEC-008](items/SPEC-008.md) | ⚪️ - | ✅ implemented | ⚪️ |