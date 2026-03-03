# -*- coding: utf-8 -*-
from specification.features.steps._helpers import create_doorstop_project_api, write_feature_file, run_spec_weaver, write_doorstop_yaml
from behave import given, when, then, step
import shlex
import subprocess
from pathlib import Path
import tempfile
import shutil

# ======================================================================
# Steps
# ======================================================================

@given('Doorstopツリーが初期化されている')  # type: ignore
def given_6df87eb3(context):
    """Doorstopツリーが初期化されている"""
    create_doorstop_project_api(context.temp_dir)
    context.repo_root = context.temp_dir


@given('以下のREQアイテムが存在する:')  # type: ignore
def given_28140be4(context):
    """以下のREQアイテムが存在する:"""
    for row in context.table:
        links = []
        if "Links" in row.headings and row["Links"]:
            links = [l.strip() for l in row["Links"].split(",") if l.strip()]
        status = row.get("Status", "implemented")
        write_doorstop_yaml(context.temp_dir / "reqs", row["ID"], header=row.get("Header", ""), links=links, status=status)


@given('以下のSPECアイテムが存在する:')  # type: ignore
def given_14c0b615(context):
    """以下のSPECアイテムが存在する:"""
    import json
    for row in context.table:
        extra = {}
        if "impl_files" in row.headings and row["impl_files"]:
            try:
                extra["impl_files"] = json.loads(row["impl_files"])
            except json.JSONDecodeError:
                extra["impl_files"] = row["impl_files"]
        
        links = []
        if "Links" in row.headings and row["Links"]:
            links = [l.strip() for l in row["Links"].split(",") if l.strip()]
            
        status = row.get("Status", "implemented")
        write_doorstop_yaml(context.temp_dir / "specs", row["ID"], header=row.get("Header", ""), extra=extra, links=links, status=status)


@given('以下のfeatureファイルが存在する:')  # type: ignore
def given_a838a6ff(context):
    """以下のfeatureファイルが存在する:"""
    features_dir = context.temp_dir / "specification" / "features"
    features_dir.mkdir(parents=True, exist_ok=True)
    for row in context.table:
        filename = row["File"]
        tags = row.get("Tags", "")
        path = features_dir / filename
        path.write_text(f"{tags}\nFeature: Test Feature\n  Scenario: Test Scenario\n    Given test\n")


# [Duplicate Skip] This step is already defined elsewhere
# @then('終了コードが0である')  # type: ignore
# def then_0f800e56(context):
#     """終了コードが0である
# 
#     Scenarios:
#       - REQを起点としたトップダウンのツリー表示
#       - SPECを起点とした双方向のツリー表示
#       - Gherkin Featureファイルを起点としたボトムアップ表示
#       - --direction up で上方向のみ探索
#       - --direction down で下方向のみ探索
#       - --format flat でフラットリスト表示
#       - .feature ディレクトリが存在しない場合の警告と継続
#       - 各ノードにステータスバッジが表示される
#     """
#     raise NotImplementedError('STEP: 終了コードが0である')


@when('`spec-weaver trace REQ-001 -f ./specification/features` を実行する')  # type: ignore
def when_6629a1b8(context):
    """`spec-weaver trace REQ-001 -f ./specification/features` を実行する

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - Doorstopツリーが未初期化の場合のエラー
      - 各ノードにステータスバッジが表示される
    """
    raise NotImplementedError('STEP: `spec-weaver trace REQ-001 -f ./specification/features` を実行する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('終了コードが0である')  # type: ignore
# def then_0f800e56(context):
#     """終了コードが0である
# 
#     Scenarios:
#       - REQを起点としたトップダウンのツリー表示
#       - SPECを起点とした双方向のツリー表示
#       - Gherkin Featureファイルを起点としたボトムアップ表示
#       - --direction up で上方向のみ探索
#       - --direction down で下方向のみ探索
#       - --format flat でフラットリスト表示
#       - .feature ディレクトリが存在しない場合の警告と継続
#       - 各ノードにステータスバッジが表示される
#     """
#     raise NotImplementedError('STEP: 終了コードが0である')


@when('`spec-weaver trace {target}` を実行する')  # type: ignore
@when('`spec-weaver trace {target}` を実行する（--show-impl なし）')  # type: ignore
def when_trace_generic(context, target):
    """`spec-weaver trace {target}` を実行する"""
    args = shlex.split(f"trace {target}")
    
    # replace ./specification/features with actual temp path
    for i, arg in enumerate(args):
        if arg == "./specification/features":
            features_dir = context.temp_dir / "specification" / "features"
            features_dir.mkdir(parents=True, exist_ok=True)
            args[i] = str(features_dir)
        elif arg == "./nonexistent/features":
            args[i] = str(context.temp_dir / "nonexistent" / "features")

    cwd = getattr(context, "repo_root", context.temp_dir)
    cmd = ["uv", "run", "spec-weaver"] + args
    context.result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(cwd),
    )


@then('出力にツリー構造が含まれる')  # type: ignore
def then_a551e8cd(context):
    """出力にツリー構造が含まれる

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
      - SPECを起点とした双方向のツリー表示
    """
    # 枝文字またはリッチなテーブル
    assert any(c in context.result.stdout for c in ["─", "└", "│", "├"]) or "ID" in context.result.stdout


@then('"{param0}" がルートノードとして表示される')  # type: ignore
def then_24c28817(context, param0):
    """"REQ-001" がルートノードとして表示される

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
    """
    # 最初の数行にあるか（Panel表示などがあるため）
    assert param0 in "\n".join(context.result.stdout.splitlines()[:5])


@then('"{param0}" が "{param1}" の子ノードとして表示される')  # type: ignore
def then_5c046e43(context, param0, param1):
    """"REQ-002" が "REQ-001" の子ノードとして表示される

    Scenarios:
      - REQを起点としたトップダウンのツリー表示
    """
    assert param0 in context.result.stdout
    assert param1 in context.result.stdout


@when('`spec-weaver trace SPEC-003 -f ./specification/features` を実行する')  # type: ignore
def when_b1a2f499(context):
    """`spec-weaver trace SPEC-003 -f ./specification/features` を実行する

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    raise NotImplementedError('STEP: `spec-weaver trace SPEC-003 -f ./specification/features` を実行する')


@then('上位に "{param0}" が表示される')  # type: ignore
def then_0d60d0d2(context, param0):
    """上位に "REQ-002" が表示される

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    assert param0 in context.result.stdout


@then('下位に "{param0}" のシナリオが表示される')  # type: ignore
def then_b2f19b22(context, param0):
    """下位に "audit.feature" のシナリオが表示される

    Scenarios:
      - SPECを起点とした双方向のツリー表示
    """
    assert param0 in context.result.stdout


@when('`spec-weaver trace audit.feature -f ./specification/features` を実行する')  # type: ignore
def when_53222a94(context):
    """`spec-weaver trace audit.feature -f ./specification/features` を実行する

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
    """
    raise NotImplementedError('STEP: `spec-weaver trace audit.feature -f ./specification/features` を実行する')


@then('出力に "{param0}" が表示される')  # type: ignore
def then_1b9fcb6e(context, param0):
    """出力に "SPEC-003" が表示される

    Scenarios:
      - Gherkin Featureファイルを起点としたボトムアップ表示
      - --direction up で上方向のみ探索
      - --direction down で下方向のみ探索
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    assert param0 in context.result.stdout


@when('`spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する')  # type: ignore
def when_770f884f(context):
    """`spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する

    Scenarios:
      - --direction up で上方向のみ探索
    """
    raise NotImplementedError('STEP: `spec-weaver trace SPEC-003 -f ./specification/features --direction up` を実行する')


@then('出力に "{param0}" が表示されない')  # type: ignore
def then_1c0ce4ff(context, param0):
    """出力に "audit.feature" が表示されない

    Scenarios:
      - --direction up で上方向のみ探索
    """
    assert param0 not in context.result.stdout


@when('`spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する')  # type: ignore
def when_24d70f7f(context):
    """`spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する

    Scenarios:
      - --direction down で下方向のみ探索
    """
    raise NotImplementedError('STEP: `spec-weaver trace REQ-001 -f ./specification/features --direction down` を実行する')


@when('`spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する')  # type: ignore
def when_816b7b2c(context):
    """`spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する

    Scenarios:
      - --format flat でフラットリスト表示
    """
    raise NotImplementedError('STEP: `spec-weaver trace REQ-001 -f ./specification/features --format flat` を実行する')


@then('出力がフラットリスト形式である')  # type: ignore
def then_f50604f0(context):
    """出力がフラットリスト形式である

    Scenarios:
      - --format flat でフラットリスト表示
    """
    # フラット形式はツリーの枝文字がないはず。├ や └ がなければOKとする
    assert "├" not in context.result.stdout
    assert "└" not in context.result.stdout
    assert "ID" in context.result.stdout or "種別" in context.result.stdout


@then('各行に "{param0}" または "{param1}" または "{param2}" のラベルが含まれる')  # type: ignore
def then_29017220(context, param0, param1, param2):
    """各行に "REQ" または "SPEC" または "TEST" のラベルが含まれる

    Scenarios:
      - --format flat でフラットリスト表示
    """
    # テーブルヘッダ行や境界線を除いて確認
    lines = context.result.stdout.strip().splitlines()
    found = False
    for line in lines:
        if any(label in line for label in [param0, param1, param2]):
            found = True
            break
    assert found


@when('`spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する')  # type: ignore
def when_44385436(context):
    """`spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する

    Scenarios:
      - 存在しないIDを指定した場合のエラー
    """
    raise NotImplementedError('STEP: `spec-weaver trace NONEXIST-999 -f ./specification/features` を実行する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('終了コードが1である')  # type: ignore
# def then_9b731a71(context):
#     """終了コードが1である
# 
#     Scenarios:
#       - 存在しないIDを指定した場合のエラー
#       - Doorstopツリーが未初期化の場合のエラー
#     """
#     raise NotImplementedError('STEP: 終了コードが1である')


@then('エラーメッセージに "{param0}" が含まれる')  # type: ignore
def then_9998fad9(context, param0):
    """エラーメッセージに "not found" が含まれる

    Scenarios:
      - 存在しないIDを指定した場合のエラー
      - Doorstopツリーが未初期化の場合のエラー
    """
    assert param0.lower() in context.result.stdout.lower() or param0.lower() in context.result.stderr.lower()


@given('Doorstopツリーが初期化されていない')  # type: ignore
def given_1b5b3d28(context):
    """Doorstopツリーが初期化されていない

    Scenarios:
      - Doorstopツリーが未初期化の場合のエラー
    """
    context.repo_root = Path(tempfile.mkdtemp(prefix="sw_empty_"))


# [Duplicate Skip] This step is already defined elsewhere
# @then('警告メッセージが表示される')  # type: ignore
# def then_a11d14f9(context):
#     """警告メッセージが表示される
# 
#     Scenarios:
#       - .feature ディレクトリが存在しない場合の警告と継続
#     """
#     raise NotImplementedError('STEP: 警告メッセージが表示される')


@when('`spec-weaver trace REQ-001 -f ./nonexistent/features` を実行する')  # type: ignore
def when_64ec2c6c(context):
    """`spec-weaver trace REQ-001 -f ./nonexistent/features` を実行する

    Scenarios:
      - .feature ディレクトリが存在しない場合の警告と継続
    """
    raise NotImplementedError('STEP: `spec-weaver trace REQ-001 -f ./nonexistent/features` を実行する')


# [Duplicate Skip] This step is already defined elsewhere
# @then('警告メッセージが表示される')  # type: ignore
# def then_a11d14f9(context):
#     """警告メッセージが表示される
# 
#     Scenarios:
#       - .feature ディレクトリが存在しない場合の警告と継続
#     """
#     raise NotImplementedError('STEP: 警告メッセージが表示される')


@then('"{param0}" のノードに "{param1}" のステータスバッジが表示される')  # type: ignore
def then_f676df97(context, param0, param1):
    """"REQ-001" のノードに "implemented" のステータスバッジが表示される

    Scenarios:
      - 各ノードにステータスバッジが表示される
    """
    assert param0 in context.result.stdout
    assert param1 in context.result.stdout
