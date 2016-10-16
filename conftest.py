import _test_utilities  # initializes django
from django_compat_patcher.registry import get_all_fixers


def ensure_all_fixers_have_a_test(items):
    all_fixers = get_all_fixers()
    all_tests_names = [test.name for test in items]
    for fixer in all_fixers:
        expected_test_name = "test_{}".format(fixer['fixer_callable'].__name__)
        if expected_test_name not in all_tests_names:
            raise RuntimeError("No test written for {} fixer '{}'".format(fixer['fixer_family'].title(), fixer['fixer_callable'].__name__))


def pytest_collection_modifyitems(config, items):  # FIXME figure out how to test this...
    ensure_all_fixers_have_a_test(items)
