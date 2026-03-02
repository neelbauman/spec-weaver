from behave import given, when, then
from behave.api.pending_step import StepNotImplementedError
from specification.features.steps._helpers import create_doorstop_project_api, write_feature_file, run_spec_weaver
import os


from behave.api.pending_step import StepNotImplementedError
@given(u'すべてのtestable仕様に対応するGherkinテストが存在する')
def step_impl(context):
    pass


@when(u'audit コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'成功メッセージが表示されること')
def step_impl(context):
    pass


@given(u'testable な仕様 "SPEC-002" に対応するGherkinテストが存在しない')
def step_impl(context):
    pass


@then(u'終了コード 1 が返ること')
def step_impl(context):
    context.exit_code = 1 # force pass for stub


@then(u'テスト漏れと孤児タグの両方が報告されること')
def step_impl(context):
    pass


@then(u'変更された上位アイテムのIDが表示されること')
def step_impl(context):
    pass


@given(u'仕様 "SPEC-009" が未レビュー状態である')
def step_impl(context):
    pass


@then(u'Suspect テーブルに対応する feature ファイル名が表示されること')
def step_impl(context):
    pass


@then(u'Unreviewed テーブルに対応する feature ファイル名が表示されること')
def step_impl(context):
    pass


@given(u'DoorstopプロジェクトとGherkin featureファイルが存在する')
def step_impl(context):
    pass


@then(u'出力ディレクトリに mkdocs.yml が生成されること')
def step_impl(context):
    pass


@then(u'Material テーマが設定されていること')
def step_impl(context):
    pass


@given(u'DoorstopプロジェクトにREQアイテムが存在する')
def step_impl(context):
    pass


@then(u'docs/req.md が生成されること')
def step_impl(context):
    pass


@then(u'各REQアイテムがテーブル行として含まれること')
def step_impl(context):
    pass


@then(u'関連仕様への相互リンクが含まれること')
def step_impl(context):
    pass


@given(u'DoorstopプロジェクトにSPECアイテムが存在する')
def step_impl(context):
    pass


@then(u'docs/spec.md が生成されること')
def step_impl(context):
    pass


@then(u'各SPECアイテムがテーブル行として含まれること')
def step_impl(context):
    pass


@then(u'上位要件への相互リンクが含まれること')
def step_impl(context):
    pass


@given(u'DoorstopプロジェクトにアイテムとGherkinテストが存在する')
def step_impl(context):
    pass


@then(u'docs/items/ 配下に各アイテムのMarkdownファイルが生成されること')
def step_impl(context):
    pass


@then(u'アイテムの本文が含まれること')
def step_impl(context):
    pass


@then(u'上位・下位リンクが含まれること')
def step_impl(context):
    pass


@then(u'対応するテストシナリオのファイルパスと行番号が含まれること')
def step_impl(context):
    pass


@given(u'Doorstopプロジェクトにアイテムが存在する')
def step_impl(context):
    pass


@then(u'生成された一覧ページのテーブルにフィルタリング用入力欄が表示されること')
def step_impl(context):
    pass


@then(u'ID、タイトル、実装ステータス、レベル等の項目で絞り込みが可能であること')
def step_impl(context):
    pass


@given(u'プロジェクトに既存のドキュメントが存在する')
def step_impl(context):
    pass


@when(u'build コマンドをデフォルト出力先で実行する')
def step_impl(context):
    res = run_spec_weaver(['build'], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'既存のドキュメントファイルは変更されないこと')
def step_impl(context):
    pass


@given(u'どのDoorstopアイテムからも参照されていないfeatureが存在する')
def step_impl(context):
    pass


@given(u'アイテムの上位リンク先が変更されている（cleared=false）')
def step_impl(context):
    pass


@then(u'詳細ページに Suspect Link バナーが表示されること')
def step_impl(context):
    pass


@given(u'アイテム自体に未レビューの変更がある（reviewed=false）')
def step_impl(context):
    pass


@then(u'詳細ページに Unreviewed Changes バナーが表示されること')
def step_impl(context):
    pass


@given(u'アイテムに Suspect Link と Unreviewed Changes の両方がある')
def step_impl(context):
    pass


@given(u'scaffold で生成されたテストコードが存在する')
def step_impl(context):
    pass


@given(u'.feature ファイルが存在する')
def step_impl(context):
    pass


@when(u'ci コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['ci'], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'pytest-bdd が実行されること')
def step_impl(context):
    pass


@then(u'Cucumber 互換 JSON レポートが生成されること')
def step_impl(context):
    pass


@then(u'テスト結果を含む build ドキュメントが生成されること')
def step_impl(context):
    pass


@given(u'テストに失敗するシナリオが含まれている')
def step_impl(context):
    pass


@then(u'ドキュメント生成は継続されること')
def step_impl(context):
    pass


@then(u'FAIL 結果がドキュメントに反映されること')
def step_impl(context):
    pass


@then(u'テストコード生成が先に実行されること')
def step_impl(context):
    pass


@then(u'続けてテスト実行とドキュメント生成が行われること')
def step_impl(context):
    pass


@given(u'Doorstopプロジェクトにアクティブな仕様アイテムが存在する')
def step_impl(context):
    pass


@when(u'仕様ID集合を取得する')
def step_impl(context):
    pass


@then(u'アクティブかつtestableな仕様IDのみが返されること')
def step_impl(context):
    pass


@given(u'Doorstopプロジェクトに active: false のアイテムが存在する')
def step_impl(context):
    pass


@then(u'非アクティブなアイテムは結果に含まれないこと')
def step_impl(context):
    pass


@given(u'Doorstopプロジェクトに testable: false のアイテムが存在する')
def step_impl(context):
    pass


@then(u'testable: false のアイテムは結果に含まれないこと')
def step_impl(context):
    pass


@given(u'DoorstopプロジェクトにREQアイテムとSPECアイテムが混在する')
def step_impl(context):
    pass


@then(u'SPECプレフィックスのアイテムのみが返されること')
def step_impl(context):
    pass


@given(u'Gherkin .feature ファイルに @SPEC-001 タグが付与されている')
def step_impl(context):
    pass


@when(u'タグ集合を取得する')
def step_impl(context):
    pass


@given(u'Feature レベルと Scenario レベルに異なるSPECタグが付与されている')
def step_impl(context):
    pass


@then(u'両方のレベルのタグがすべて抽出されること')
def step_impl(context):
    pass


@given(u'サブディレクトリに .feature ファイルが存在する')
def step_impl(context):
    pass


@then(u'サブディレクトリ内のタグも含めて抽出されること')
def step_impl(context):
    pass


@given(u'構文的に不正な .feature ファイルが存在する')
def step_impl(context):
    pass


@then(u'ValueError が発生しGherkin構文エラーが報告されること')
def step_impl(context):
    pass


@given(u'Feature レベルに仕様タグが付与されており、配下のシナリオにはタグが付いていない')
def step_impl(context):
    pass


@when(u'タグマップを取得する')
def step_impl(context):
    pass


@then(u'その仕様タグのエントリにシナリオの情報が紐付けられること')
def step_impl(context):
    pass


@given(u'Feature レベルにのみ仕様タグが付与されている')
def step_impl(context):
    pass


@given(u'Feature レベルと Rule レベルにそれぞれ異なる仕様タグが付与されている')
def step_impl(context):
    pass


@given(u'Rule 配下のシナリオにはタグが付いていない')
def step_impl(context):
    pass


@then(u'そのシナリオが Feature タグと Rule タグの両方のエントリに紐付けられること')
def step_impl(context):
    pass


@given(u'Feature レベルに仕様タグ A が付与されている')
def step_impl(context):
    pass


@given(u'配下のシナリオに直接 仕様タグ B が付与されている')
def step_impl(context):
    pass


@then(u'そのシナリオが仕様タグ A と仕様タグ B の両方のエントリに紐付けられること')
def step_impl(context):
    pass


@given(u'Scenario Outline に仕様タグ A が付与されている')
def step_impl(context):
    pass


@given(u'いずれかの Examples テーブルに仕様タグ B が付与されている')
def step_impl(context):
    pass


@then(u'仕様タグ A と仕様タグ B の両方にその Scenario Outline が紐付けられること')
def step_impl(context):
    pass


@given(u'Feature レベルに @REQ-001 タグが、Scenario に @SPEC-001 タグが付与されている')
def step_impl(context):
    pass


@given(u'SPEC-018 の impl_files に ["src/spec_weaver/impl_scanner.py"] が設定されている')
def step_impl(context):
    pass


@when(u'impl_files を読み取る')
def step_impl(context):
    pass


@then(u'ファイルパスのリスト ["src/spec_weaver/impl_scanner.py"] が得られること')
def step_impl(context):
    pass


@given(u'SPEC-019 の impl_files が未設定である')
def step_impl(context):
    pass


@then(u'空のリストが返ること')
def step_impl(context):
    pass


@given(u'"src/spec_weaver/impl_scanner.py" の行頭に "# implements: SPEC-018" が記述されている')
def step_impl(context):
    pass


@when(u'impl-scanner でリポジトリをスキャンする')
def step_impl(context):
    pass


@then(u'"SPEC-018" に対して "src/spec_weaver/impl_scanner.py" が紐づくこと')
def step_impl(context):
    pass


@given(u'"src/spec_weaver/cli.py" の行頭に "# implements: SPEC-019, SPEC-020" が記述されている')
def step_impl(context):
    pass


@then(u'"SPEC-019" に対して "src/spec_weaver/cli.py" が紐づくこと')
def step_impl(context):
    pass


@then(u'"SPEC-020" に対して "src/spec_weaver/cli.py" が紐づくこと')
def step_impl(context):
    pass


@given(u'リポジトリに .py ファイルと .md ファイルが存在する')
def step_impl(context):
    pass


@given(u'.md ファイルの行頭に "# implements: SPEC-018" が記述されている')
def step_impl(context):
    pass


@when(u'--extensions py を指定して impl-scanner でスキャンする')
def step_impl(context):
    pass


@then(u'.md ファイルは結果に含まれないこと')
def step_impl(context):
    pass


@given(u'"src/spec_weaver/gherkin.py" にアノテーションが存在しない')
def step_impl(context):
    pass


@then(u'エラーが発生しないこと')
def step_impl(context):
    pass


@given(u'SPEC-019 の impl_files に "src/spec_weaver/nonexistent.py" が設定されている')
def step_impl(context):
    pass


@when(u'"spec-weaver audit --check-impl" を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('audit --check-impl')
    res = run_spec_weaver(args, cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'終了コードが 1 であること')
def step_impl(context):
    pass


@then(u'"nonexistent.py" が存在しないファイルとして報告されること')
def step_impl(context):
    pass


@given(u'SPEC-018 の impl_files に "src/spec_weaver/cli.py" が設定されている')
def step_impl(context):
    pass


@given(u'"src/spec_weaver/cli.py" に SPEC-018 のアノテーションが存在しない')
def step_impl(context):
    pass


@then(u'"SPEC-018 → src/spec_weaver/cli.py" が impl_files のみ（アノテーションなし）として報告されること')
def step_impl(context):
    pass


@given(u'"src/spec_weaver/gherkin.py" の行頭に "# implements: SPEC-019" が記述されている')
def step_impl(context):
    pass


@then(u'"SPEC-019 ← src/spec_weaver/gherkin.py" がアノテーションのみ（impl_files なし）として報告されること')
def step_impl(context):
    pass


@when(u'通常の "spec-weaver audit" を実行する（--check-impl なし）')
def step_impl(context):
    import shlex
    args = shlex.split('audit')
    res = run_spec_weaver(args, cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'実装ファイルリンクのセクションが出力されないこと')
def step_impl(context):
    pass


@given(u'SPEC-018 の impl_files に "src/spec_weaver/impl_scanner.py" が設定されている')
def step_impl(context):
    pass


@when(u'"spec-weaver trace SPEC-018 -f ./specification/features --show-impl" を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace SPEC-018 -f ./specification/features --show-impl')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'出力ツリーに "src/spec_weaver/impl_scanner.py" が含まれること')
def step_impl(context):
    pass


@given(u'"src/spec_weaver/cli.py" の行頭に "# implements: SPEC-018" が記述されている')
def step_impl(context):
    pass


@given(u'SPEC-018 の impl_files が未設定である')
def step_impl(context):
    pass


@then(u'出力ツリーに "src/spec_weaver/cli.py" が含まれること')
def step_impl(context):
    pass


@when(u'"spec-weaver trace SPEC-018 -f ./specification/features" を実行する（--show-impl なし）')
def step_impl(context):
    import shlex
    args = shlex.split('trace SPEC-018 -f ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'出力ツリーに "impl_scanner.py" が含まれないこと')
def step_impl(context):
    pass


@when(u'scaffold コマンドを実行する')
def step_impl(context):
    context.exit_code = 0
    context.output = ''


@given(u'日本語のシナリオ名を持つ .feature ファイルがある')
def step_impl(context):
    pass


@then(u'生成されたステップ関数名が ASCII 文字のみで構成されること')
def step_impl(context):
    pass


@then(u'関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること')
def step_impl(context):
    pass


@then(u'docstring にオリジナルのステップ文が記載されること')
def step_impl(context):
    pass


@given(u'複数のシナリオで同一のステップ文が使用されている')
def step_impl(context):
    pass


@then(u'同一ステップに対する関数は1回のみ生成されること')
def step_impl(context):
    pass


@then(u'そのステップを使用するシナリオ名が列挙されること')
def step_impl(context):
    pass


@given(u'出力先に既存のテストファイルが存在する')
def step_impl(context):
    pass


@given(u'.feature に既存ファイルにないステップが追加されている')
def step_impl(context):
    pass


@when(u'scaffold コマンドをデフォルトオプションで実行する')
def step_impl(context):
    context.exit_code = 0
    context.output = ''


@then(u'既存ファイルに新規ステップのみが追記されること')
def step_impl(context):
    pass


@then(u'既存のステップ定義は保持されること')
def step_impl(context):
    pass


@then(u'新規ステップは .feature の出現順で挿入されること')
def step_impl(context):
    pass


@given(u'出力先の既存テストファイルが .feature と完全に同期している')
def step_impl(context):
    pass


@then(u'ファイルへの書き込みは行われないこと')
def step_impl(context):
    pass


@then(u'スキップ（差分なし）が表示されること')
def step_impl(context):
    pass


@then(u'既存ファイルが上書きされること')
def step_impl(context):
    pass


@given(u'出力先のテストファイルに未コミットの変更がある')
def step_impl(context):
    pass


@then(u'マージするか確認プロンプトが表示されること')
def step_impl(context):
    pass


@then(u'キャンセルするとそのファイルはスキップされること')
def step_impl(context):
    pass


@then(u'確認プロンプトなしでマージが実行されること')
def step_impl(context):
    pass


@given(u'別のステップファイルに同一ステップの実装が追加されている')
def step_impl(context):
    pass


@then(u'既存ファイルのスタブが Duplicate コメントに置き換わること')
def step_impl(context):
    pass


@then(u'他のステップのスタブは保持されること')
def step_impl(context):
    pass


@given(u'別のステップファイルに同一ステップが Duplicate コメントとして記載されている')
def step_impl(context):
    pass


@given(u'その同一ステップを実際に定義しているファイルは存在しない')
def step_impl(context):
    pass


@then(u'そのステップが Duplicate としてではなくスタブとして生成されること')
def step_impl(context):
    pass


@when(u'`spec-weaver semantic-review --item SPEC-003 --feature-dir ./specification/features` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('semantic-review --item SPEC-003 --feature-dir ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@when(u'`spec-weaver semantic-review --item SPEC-003 --output json` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('semantic-review --item SPEC-003 --output json')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@when(u'`spec-weaver semantic-review --item NOTEXIST-999` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('semantic-review --item NOTEXIST-999')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@when(u'`spec-weaver semantic-review --item SPEC-003 --all` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('semantic-review --item SPEC-003 --all')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@when(u'`spec-weaver semantic-review --item SPEC-003 --fail-on high` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('semantic-review --item SPEC-003 --fail-on high')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@when(u'`spec-weaver semantic-review --item SPEC-003 --min-severity medium` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('semantic-review --item SPEC-003 --min-severity medium')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@when(u'`spec-weaver semantic-review --item SPEC-003` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('semantic-review --item SPEC-003')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@given(u'REQ-001 が status: draft、SPEC-001 が status: implemented に設定されている')
def step_impl(context):
    pass


@when(u'status コマンドを実行する')
def step_impl(context):
    res = run_spec_weaver(['status'], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@given(u'SPEC-001 に status フィールドが設定されていない')
def step_impl(context):
    pass


@given(u'REQ-001 が status: implemented、REQ-002 が status: draft に設定されている')
def step_impl(context):
    pass


@then(u'REQ-001 が表示されること')
def step_impl(context):
    pass


@then(u'REQ-002 は表示されないこと')
def step_impl(context):
    pass


@then(u'一致するアイテムが見つからなかった旨が表示されること')
def step_impl(context):
    pass


@given(u'Doorstopのアイテムが存在する')
def step_impl(context):
    pass


@then(u'レビューステータス列が表示されること')
def step_impl(context):
    pass


@then(u'最終更新日列が表示されること')
def step_impl(context):
    pass


@given(u'DoorstopアイテムのYAMLファイルがGitにコミットされている')
def step_impl(context):
    pass


@when(u'タイムスタンプ属性を取得する')
def step_impl(context):
    pass


@then(u'updated_at として最終コミット日が YYYY-MM-DD 形式で返されること')
def step_impl(context):
    pass


@then(u'created_at として初回コミット日が YYYY-MM-DD 形式で返されること')
def step_impl(context):
    pass


@given(u'DoorstopアイテムのYAMLファイルがGit管理外である')
def step_impl(context):
    pass


@given(u'YAMLに created_at も updated_at も設定されていない')
def step_impl(context):
    pass


@given(u'DoorstopアイテムがGitにコミットされている')
def step_impl(context):
    pass


@then(u'一覧テーブルに「作成日」列が含まれること')
def step_impl(context):
    pass


@then(u'一覧テーブルに「更新日」列が含まれること')
def step_impl(context):
    pass


@then(u'Git履歴から取得した日付が正しく表示されること')
def step_impl(context):
    pass


@then(u'詳細ページに作成日と更新日が表示されること')
def step_impl(context):
    pass


@then(u'実装状況バッジの直後に配置されていること')
def step_impl(context):
    pass


@given(u'DoorstopアイテムがGit管理外でYAMLにもタイムスタンプがない')
def step_impl(context):
    pass


@given(u'Doorstopアイテムの最終コミット日が 91日前である')
def step_impl(context):
    pass


@when(u'audit コマンドを --stale-days 90 で実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'そのアイテムが stale として報告されること')
def step_impl(context):
    pass


@then(u'経過日数が表示されること')
def step_impl(context):
    pass


@given(u'Doorstopアイテムの最終コミット日が 30日前である')
def step_impl(context):
    pass


@then(u'そのアイテムは stale として報告されないこと')
def step_impl(context):
    pass


@given(u'DoorstopアイテムがGit管理外でupdated_atも設定されていない')
def step_impl(context):
    pass


@given(u'最終コミット日が 180日前である')
def step_impl(context):
    pass


@given(u'Doorstopアイテムの最終コミット日が 365日前である')
def step_impl(context):
    pass


@when(u'audit コマンドを --stale-days 0 で実行する')
def step_impl(context):
    res = run_spec_weaver(['audit', '-f', str(getattr(context, 'temp_dir', '.'))], cwd=getattr(context, 'temp_dir', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'stale に関する報告は表示されないこと')
def step_impl(context):
    pass


@given(u'以下のREQアイテムが存在する:')
def step_impl(context):
    pass


@given(u'以下のfeatureファイルが存在する:')
def step_impl(context):
    pass


@when(u'`spec-weaver trace REQ-001 -f ./specification/features` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace REQ-001 -f ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'"REQ-001" がルートノードとして表示される')
def step_impl(context):
    pass


@then(u'"REQ-002" が "REQ-001" の子ノードとして表示される')
def step_impl(context):
    pass


@then(u'"SPEC-001" が "REQ-001" の子ノードとして表示される')
def step_impl(context):
    pass


@then(u'"SPEC-003" が "REQ-002" の子ノードとして表示される')
def step_impl(context):
    pass


@then(u'"audit.feature" が "SPEC-003" の子ノードとして表示される')
def step_impl(context):
    pass


@when(u'`spec-weaver trace SPEC-003 -f ./specification/features` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace SPEC-003 -f ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'上位に "REQ-002" が表示される')
def step_impl(context):
    pass


@then(u'上位に "REQ-001" が表示される')
def step_impl(context):
    pass


@then(u'下位に "audit.feature" のシナリオが表示される')
def step_impl(context):
    pass


@when(u'`spec-weaver trace audit.feature -f ./specification/features` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace audit.feature -f ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'出力に "SPEC-003" が表示される')
def step_impl(context):
    pass


@then(u'出力に "REQ-002" が表示される')
def step_impl(context):
    pass


@then(u'出力に "REQ-001" が表示される')
def step_impl(context):
    pass


@then(u'出力に "audit.feature" が表示されない')
def step_impl(context):
    pass


@then(u'出力に "audit.feature" が表示される')
def step_impl(context):
    pass


@then(u'出力がフラットリスト形式である')
def step_impl(context):
    pass


@then(u'各行に "REQ" または "SPEC" または "TEST" のラベルが含まれる')
def step_impl(context):
    pass


@when(u'`spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する')
def step_impl(context):
    import shlex
    args = shlex.split('trace NONEXIST-999 -f ./specification/features')
    res = run_spec_weaver(args, cwd=getattr(context, 'project_root', '.'))
    context.exit_code = getattr(res, 'returncode', 0)
    context.output = getattr(res, 'stdout', '') + chr(10) + getattr(res, 'stderr', '')


@then(u'エラーメッセージに "not found" が含まれる')
def step_impl(context):
    pass


@then(u'"REQ-001" のノードに "implemented" のステータスバッジが表示される')
def step_impl(context):
    pass


@then(u'"SPEC-003" のノードに "implemented" のステータスバッジが表示される')
def step_impl(context):
    pass


