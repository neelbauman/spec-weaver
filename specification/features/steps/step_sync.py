import os
from pathlib import Path
from behave import given, when, then
from spec_weaver.cli.main import app
from typer.testing import CliRunner

runner = CliRunner()

@given('Sync用Doorstopツリーが初期化されている')
def step_impl_sync_doorstop_init(context):
    from specification.features.steps._helpers import create_doorstop_project_yaml
    # SPEC-001 と SPEC-002 を用意する
    docs = [
        {
            "dir": "specs",
            "prefix": "SPEC",
            "items": [
                {"uid": "SPEC-001", "header": "Dummy Spec 1"},
                {"uid": "SPEC-002", "header": "Dummy Spec 2"},
            ]
        }
    ]
    create_doorstop_project_yaml(context.temp_dir, docs)
    os.chdir(context.temp_dir) # typser CLI runner works in cwd
    context.repo_root = context.temp_dir

@given('"{file_path}" に "{tag}" タグを持つシナリオが存在する')
def step_impl_sync_feature_file(context, file_path, tag):
    path = context.temp_dir / file_path
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"""
{tag}
Feature: Dummy
  Scenario: Dummy scenario
    Given dummy step
"""
    path.write_text(content, encoding="utf-8")

@when('"{command}" を実行する（sync用）')
def step_impl_sync_run_cmd_specific(context, command):
    args = command.replace("spec-weaver ", "").split()
    # Add repo root implicitly to avoid relying on chdir alone
    args.extend(["--repo-root", str(context.temp_dir)])
    context.result = runner.invoke(app, args)
    assert context.result.exit_code == 0, f"Command failed: {context.result.stdout}"

@then('"{item_id}" のYAMLファイルに "{attr_name}" 属性が追加されること')
def step_impl_sync_yaml_attr_added(context, item_id, attr_name):
    from spec_weaver.adapters.doorstop import get_item_map
    item_map = get_item_map(context.temp_dir)
    item = item_map.get(item_id)
    assert item is not None, f"Item {item_id} not found"
    
    val = item.get(attr_name)
    assert val is not None, f"Attribute {attr_name} not found in {item_id}"
    context.last_item = item
    context.last_attr_name = attr_name

@then('その属性に "{file_path}" が含まれること')
def step_impl_sync_attr_contains(context, file_path):
    attr_value = context.last_item.get(context.last_attr_name)
    assert file_path in attr_value, f"File {file_path} not found in {attr_value}"

@given('"{file_path}" に "{annotation}" アノテーションが存在する')
def step_impl_sync_annotation(context, file_path, annotation):
    path = context.temp_dir / file_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{annotation}\n", encoding="utf-8")
