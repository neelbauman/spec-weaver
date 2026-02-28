"""behave steps for: test bug 2"""

from behave import given

@given('an implemented step')  # type: ignore
def given_321e4bcc(context):
    """an implemented step

    Scenarios:
      - a
    """
    raise NotImplementedError('STEP: an implemented step')
@given('an implemented step')
def given_abcdef(context):
    print("I am completely custom implemented!")
    # No scenarios block here
