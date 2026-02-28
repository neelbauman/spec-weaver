"""behave steps for: scaffold コマンド"""

from behave import given, when, then, step

# ======================================================================
# Steps
# ======================================================================

@given('"{param0}" ファイルが存在するディレクトリがある')  # type: ignore
def given_488529e3(context, param0):
    """".feature" ファイルが存在するディレクトリがある

    Scenarios:
      - 基本的なテストコード生成
      - Docstring にシナリオリストを記載
    """
    raise NotImplementedError('STEP: "{param0}" ファイルが存在するディレクトリがある')


@when('scaffold コマンドを実行する')  # type: ignore
def when_4cda1d3b(context):
    """scaffold コマンドを実行する

    Scenarios:
      - 基本的なテストコード生成
      - ハッシュベースの関数名生成
      - ステップ関数の生成と重複排除
      - Docstring にシナリオリストを記載
    """
    raise NotImplementedError('STEP: scaffold コマンドを実行する')


@then('各 .feature に対応する "{param0}" が生成されること')  # type: ignore
def then_38f9dc8b(context, param0):
    """各 .feature に対応する "step_<stem>.py" が生成されること

    Scenarios:
      - 基本的なテストコード生成
    """
    raise NotImplementedError('STEP: 各 .feature に対応する "{param0}" が生成されること')


@then('各ステップに "{param0}", "{param1}", "{param2}" デコレータ付き関数が含まれること')  # type: ignore
def then_398bb2af(context, param0, param1, param2):
    """各ステップに "@given", "@when", "@then" デコレータ付き関数が含まれること

    Scenarios:
      - 基本的なテストコード生成
    """
    raise NotImplementedError('STEP: 各ステップに "{param0}", "{param1}", "{param2}" デコレータ付き関数が含まれること')


@given('日本語のシナリオ名を持つ .feature ファイルがある')  # type: ignore
def given_a87fa38a(context):
    """日本語のシナリオ名を持つ .feature ファイルがある

    Scenarios:
      - ハッシュベースの関数名生成
    """
    raise NotImplementedError('STEP: 日本語のシナリオ名を持つ .feature ファイルがある')


@then('生成されたステップ関数名が ASCII 文字のみで構成されること')  # type: ignore
def then_75178cb9(context):
    """生成されたステップ関数名が ASCII 文字のみで構成されること

    Scenarios:
      - ハッシュベースの関数名生成
    """
    raise NotImplementedError('STEP: 生成されたステップ関数名が ASCII 文字のみで構成されること')


@then('関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること')  # type: ignore
def then_3649a406(context):
    """関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること

    Scenarios:
      - ハッシュベースの関数名生成
    """
    raise NotImplementedError('STEP: 関数名にステップ文の SHA256 ハッシュ先頭8文字が使用されること')


@then('docstring にオリジナルのステップ文が記載されること')  # type: ignore
def then_c876ede8(context):
    """docstring にオリジナルのステップ文が記載されること

    Scenarios:
      - ハッシュベースの関数名生成
    """
    raise NotImplementedError('STEP: docstring にオリジナルのステップ文が記載されること')


@given('複数のシナリオで同一のステップ文が使用されている')  # type: ignore
def given_ae2a90a1(context):
    """複数のシナリオで同一のステップ文が使用されている

    Scenarios:
      - ステップ関数の生成と重複排除
    """
    raise NotImplementedError('STEP: 複数のシナリオで同一のステップ文が使用されている')


@then('同一ステップに対する関数は1回のみ生成されること')  # type: ignore
def then_67099eaf(context):
    """同一ステップに対する関数は1回のみ生成されること

    Scenarios:
      - ステップ関数の生成と重複排除
    """
    raise NotImplementedError('STEP: 同一ステップに対する関数は1回のみ生成されること')


@then('各ステップ関数の Docstring に "{param0}" セクションが含まれること')  # type: ignore
def then_5ab7d202(context, param0):
    """各ステップ関数の Docstring に "Scenarios:" セクションが含まれること

    Scenarios:
      - Docstring にシナリオリストを記載
    """
    raise NotImplementedError('STEP: 各ステップ関数の Docstring に "{param0}" セクションが含まれること')


@then('そのステップを使用するシナリオ名が列挙されること')  # type: ignore
def then_6fd54334(context):
    """そのステップを使用するシナリオ名が列挙されること

    Scenarios:
      - Docstring にシナリオリストを記載
    """
    raise NotImplementedError('STEP: そのステップを使用するシナリオ名が列挙されること')


@given('出力先に既存のテストファイルが存在する')  # type: ignore
def given_f54fe40f(context):
    """出力先に既存のテストファイルが存在する

    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 既存ファイルの上書き
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 出力先に既存のテストファイルが存在する')


@given('.feature に既存ファイルにないステップが追加されている')  # type: ignore
def given_63fcef57(context):
    """.feature に既存ファイルにないステップが追加されている

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: .feature に既存ファイルにないステップが追加されている')


@when('scaffold コマンドをデフォルトオプションで実行する')  # type: ignore
def when_7a9125c7(context):
    """scaffold コマンドをデフォルトオプションで実行する

    Scenarios:
      - 差分マージ（新規ステップ追記）
      - 差分なし時のスキップ
      - Git 未コミット変更の確認プロンプト
      - 差分マージ時の Duplicate スタブのコメント化
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: scaffold コマンドをデフォルトオプションで実行する')


@then('既存ファイルに新規ステップのみが追記されること')  # type: ignore
def then_84ae62d5(context):
    """既存ファイルに新規ステップのみが追記されること

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: 既存ファイルに新規ステップのみが追記されること')


@then('既存のステップ定義は保持されること')  # type: ignore
def then_0cdc5832(context):
    """既存のステップ定義は保持されること

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: 既存のステップ定義は保持されること')


@then('新規ステップは .feature の出現順で挿入されること')  # type: ignore
def then_5c2cc2d3(context):
    """新規ステップは .feature の出現順で挿入されること

    Scenarios:
      - 差分マージ（新規ステップ追記）
    """
    raise NotImplementedError('STEP: 新規ステップは .feature の出現順で挿入されること')


@given('出力先の既存テストファイルが .feature と完全に同期している')  # type: ignore
def given_fdb17660(context):
    """出力先の既存テストファイルが .feature と完全に同期している

    Scenarios:
      - 差分なし時のスキップ
    """
    raise NotImplementedError('STEP: 出力先の既存テストファイルが .feature と完全に同期している')


@then('ファイルへの書き込みは行われないこと')  # type: ignore
def then_834cd5e1(context):
    """ファイルへの書き込みは行われないこと

    Scenarios:
      - 差分なし時のスキップ
    """
    raise NotImplementedError('STEP: ファイルへの書き込みは行われないこと')


@then('スキップ（差分なし）が表示されること')  # type: ignore
def then_f45c0000(context):
    """スキップ（差分なし）が表示されること

    Scenarios:
      - 差分なし時のスキップ
    """
    raise NotImplementedError('STEP: スキップ（差分なし）が表示されること')


@when('scaffold コマンドを "{param0}" オプション付きで実行する')  # type: ignore
def when_b42c7e05(context, param0):
    """scaffold コマンドを "--overwrite" オプション付きで実行する

    Scenarios:
      - 既存ファイルの上書き
      - --force オプションで確認プロンプトをスキップ
    """
    raise NotImplementedError('STEP: scaffold コマンドを "{param0}" オプション付きで実行する')


@then('既存ファイルが上書きされること')  # type: ignore
def then_6f27dfe3(context):
    """既存ファイルが上書きされること

    Scenarios:
      - 既存ファイルの上書き
    """
    raise NotImplementedError('STEP: 既存ファイルが上書きされること')


@given('出力先のテストファイルに未コミットの変更がある')  # type: ignore
def given_3f60de62(context):
    """出力先のテストファイルに未コミットの変更がある

    Scenarios:
      - Git 未コミット変更の確認プロンプト
      - --force オプションで確認プロンプトをスキップ
    """
    raise NotImplementedError('STEP: 出力先のテストファイルに未コミットの変更がある')


@then('マージするか確認プロンプトが表示されること')  # type: ignore
def then_fe932c66(context):
    """マージするか確認プロンプトが表示されること

    Scenarios:
      - Git 未コミット変更の確認プロンプト
    """
    raise NotImplementedError('STEP: マージするか確認プロンプトが表示されること')


@then('キャンセルするとそのファイルはスキップされること')  # type: ignore
def then_c8096039(context):
    """キャンセルするとそのファイルはスキップされること

    Scenarios:
      - Git 未コミット変更の確認プロンプト
    """
    raise NotImplementedError('STEP: キャンセルするとそのファイルはスキップされること')


@then('確認プロンプトなしでマージが実行されること')  # type: ignore
def then_4b7c11ee(context):
    """確認プロンプトなしでマージが実行されること

    Scenarios:
      - --force オプションで確認プロンプトをスキップ
    """
    raise NotImplementedError('STEP: 確認プロンプトなしでマージが実行されること')
@given('別のステップファイルに同一ステップの実装が追加されている')  # type: ignore
def given_b99b973a(context):
    """別のステップファイルに同一ステップの実装が追加されている

    Scenarios:
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 別のステップファイルに同一ステップの実装が追加されている')


@then('既存ファイルのスタブが Duplicate コメントに置き換わること')  # type: ignore
def then_df56f0cc(context):
    """既存ファイルのスタブが Duplicate コメントに置き換わること

    Scenarios:
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 既存ファイルのスタブが Duplicate コメントに置き換わること')


@then('他のステップのスタブは保持されること')  # type: ignore
def then_d0e8d8d6(context):
    """他のステップのスタブは保持されること

    Scenarios:
      - 差分マージ時の Duplicate スタブのコメント化
    """
    raise NotImplementedError('STEP: 他のステップのスタブは保持されること')


@given('別のステップファイルに同一ステップが Duplicate コメントとして記載されている')  # type: ignore
def given_e0006816(context):
    """別のステップファイルに同一ステップが Duplicate コメントとして記載されている

    Scenarios:
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: 別のステップファイルに同一ステップが Duplicate コメントとして記載されている')


@given('その同一ステップを実際に定義しているファイルは存在しない')  # type: ignore
def given_0e535b1f(context):
    """その同一ステップを実際に定義しているファイルは存在しない

    Scenarios:
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: その同一ステップを実際に定義しているファイルは存在しない')


@then('そのステップが Duplicate としてではなくスタブとして生成されること')  # type: ignore
def then_35ff3425(context):
    """そのステップが Duplicate としてではなくスタブとして生成されること

    Scenarios:
      - 差分マージ時の他ファイルコメント行を Duplicate 判定に使用しない
    """
    raise NotImplementedError('STEP: そのステップが Duplicate としてではなくスタブとして生成されること')
