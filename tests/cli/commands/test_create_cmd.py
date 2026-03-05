import subprocess
from unittest.mock import MagicMock, patch

import typer
from typer.testing import CliRunner

from spec_weaver.cli.main import app

runner = CliRunner()


@patch("spec_weaver.cli.commands.create_cmd.subprocess.run")
def test_create_cmd_success(mock_run, tmp_path):
    mock_run.return_value = MagicMock(returncode=0)
    
    result = runner.invoke(app, ["create", "REQ", str(tmp_path)])
    
    assert result.exit_code == 0
    mock_run.assert_called_once_with(
        ["doorstop", "create", "REQ", str(tmp_path), "--digits", "3", "--separator", "-"]
    )


@patch("spec_weaver.cli.commands.create_cmd.subprocess.run")
def test_create_cmd_with_options(mock_run, tmp_path):
    mock_run.return_value = MagicMock(returncode=0)
    
    result = runner.invoke(app, [
        "create", "SPEC", str(tmp_path), 
        "--parent", "REQ", 
        "--digits", "4", 
        "--separator", "_"
    ])
    
    assert result.exit_code == 0
    mock_run.assert_called_once_with(
        ["doorstop", "create", "SPEC", str(tmp_path), "--digits", "4", "--separator", "_", "--parent", "REQ"]
    )
