"""Common behave steps"""

from behave import then, step

@then('終了コード {code:d} が返ること')
def then_exit_code(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"

@then('終了コードが{code:d}である')
def then_exit_code_alt(context, code):
    assert context.exit_code == code, f"Expected exit code {code}, but got {context.exit_code}.\nStdout: {context.stdout}\nStderr: {context.stderr}"

@step('出力に "{text}" が表示されること')
def step_output_contains(context, text):
    assert text in context.stdout or text in context.stderr

@step('出力に "{text}" が表示される')
def step_output_contains_alt(context, text):
    assert text in context.stdout or text in context.stderr

@step('出力に "{text}" が表示されないこと')
def step_output_not_contains(context, text):
    assert text not in context.stdout and text not in context.stderr

@step('出力に "{text}" が表示されない')
def step_output_not_contains_alt(context, text):
    assert text not in context.stdout and text not in context.stderr
