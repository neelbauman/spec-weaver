import os
import shutil
import tempfile
import subprocess
import sys
from behave import fixture, use_fixture

# Add src and features/steps to sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(base_dir, "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "steps"))

@fixture
def workspace(context):
    context.temp_dir = tempfile.mkdtemp()
    context.cwd = os.getcwd()
    os.chdir(context.temp_dir)
    # Initialize git repo as doorstop requires it
    subprocess.run(["git", "init"], capture_output=True)
    yield context.temp_dir
    os.chdir(context.cwd)
    shutil.rmtree(context.temp_dir)

def before_scenario(context, scenario):
    use_fixture(workspace, context)
    context.stdout = None
    context.stderr = None
    context.exit_code = None
