"""behave 共通ステップ定義 — 複数フィーチャーファイルで共有されるステップ。"""

from __future__ import annotations

from behave import then


@then("終了コードが{code:d}である")  # type: ignore
def then_exit_code(context, code):
    """終了コードが0である / 終了コードが1である

    Scenarios:
      - trace, review, semantic_review 各コマンドの共通ステップ
    """
    assert context.exit_code == code, (
        f"終了コード {code} を期待しましたが {context.exit_code} でした。\n出力:\n{context.output}"
    )


@then("出力にツリー構造が含まれる")  # type: ignore
def then_output_has_tree(context):
    """出力にツリー構造が含まれる

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - SPECを起点とした双方向のツリー表示
    """
    assert any(
        kw in context.output
        for kw in ["REQ-", "SPEC-", "├", "└", "│", "─"]
    ), f"ツリー構造が出力にありません:\n{context.output}"
