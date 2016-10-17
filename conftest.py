import copy
from _pytest.python import Function

import _test_utilities  # initializes django
from django_compat_patcher.registry import get_all_fixers

def ensure_all_fixers_have_a_test(config, items):
    all_fixers = get_all_fixers()
    all_tests_names = [test.name for test in items]
    for fixer in all_fixers:
        expected_test_name = "test_{}".format(fixer['fixer_callable'].__name__)
        if expected_test_name not in all_tests_names:

            error_message = "No test written for {} fixer '{}'".format(fixer['fixer_family'].title(), fixer['fixer_callable'].__name__)
            def missing_test():
                raise RuntimeError(error_message)

            mock_item = copy.copy(items[0])
            mock_item.parent.name = "test_{}_fixers.py".format(fixer['fixer_family'])  # FIXME parent node is not correclty named
            mock_item.parent.obj.name = "test_{}_fixers.py".format(fixer['fixer_family'])
            setattr(mock_item.parent.obj, "MISSING_"+expected_test_name, missing_test)
            items.append(Function(name="MISSING_"+expected_test_name, parent=mock_item.parent, config=config, session=mock_item.session))


def pytest_collection_modifyitems(config, items):
    ensure_all_fixers_have_a_test(config, items)
