# src/spec_weaver/cli.py
import typer
from rich.console import Console

# 各コマンドモジュールからのインポート
from spec_weaver.cli.commands.audit_cmd import _audit_cmd
from spec_weaver.cli.commands.scaffold_cmd import _scaffold_cmd
from spec_weaver.cli.commands.review_cmd import _review_cmd
from spec_weaver.cli.commands.clear_cmd import _clear_cmd
from spec_weaver.cli.commands.status_cmd import _status_cmd
from spec_weaver.cli.commands.build_cmd import _build_cmd
from spec_weaver.cli.commands.trace_cmd import _trace_cmd
from spec_weaver.cli.commands.semantic_review_cmd import _semantic_review_cmd

# Typerアプリケーションの初期化
app = typer.Typer(
    help="Spec-Weaver: Doorstopの仕様とGherkinのテストをシームレスに統合・監査するツール",
    add_completion=False,
)
console = Console()

# コマンドの登録
app.command("audit")(_audit_cmd)
app.command("scaffold")(_scaffold_cmd)
app.command("review")(_review_cmd)
app.command("clear")(_clear_cmd)
app.command("status")(_status_cmd)
app.command("build")(_build_cmd)
app.command("trace")(_trace_cmd)
app.command("semantic-review")(_semantic_review_cmd)

if __name__ == "__main__":
    app()
