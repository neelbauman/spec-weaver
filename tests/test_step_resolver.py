# tests/test_step_resolver.py

from pathlib import Path
from spec_weaver.step_resolver import StepResolver

def test_step_resolver_load_and_resolve(tmp_path):
    steps_dir = tmp_path / "steps"
    steps_dir.mkdir()
    step_file = steps_dir / "test_steps.py"
    step_file.write_text("""
from behave import given, when, then

@given('a user "{user}" exists')
def step_impl(context, user):
    pass

@when('I login as "{user}"')
def step_impl(context, user):
    print(f"Logging in as {user}")
""", encoding="utf-8")

    resolver = StepResolver()
    resolver.load_steps(steps_dir)

    assert len(resolver.steps) == 2

    # Match Given
    step_def = resolver.resolve_step("Given", 'a user "admin" exists')
    assert step_def is not None
    assert step_def.keyword == "given"
    assert 'def step_impl(context, user):' in step_def.source

    # Match When
    step_def = resolver.resolve_step("When", 'I login as "admin"')
    assert step_def is not None
    assert step_def.keyword == "when"
    assert 'print(f"Logging in as {user}")' in step_def.source

    # No match
    assert resolver.resolve_step("Then", "nothing matches") is None

def test_step_resolver_loose_matching(tmp_path):
    steps_dir = tmp_path / "steps"
    steps_dir.mkdir()
    step_file = steps_dir / "test_steps.py"
    step_file.write_text("""
from behave import step

@step('a generic step')
def step_impl(context):
    pass
""", encoding="utf-8")

    resolver = StepResolver()
    resolver.load_steps(steps_dir)

    # Match with any keyword
    assert resolver.resolve_step("Given", "a generic step") is not None
    assert resolver.resolve_step("When", "a generic step") is not None
    assert resolver.resolve_step("Then", "a generic step") is not None
