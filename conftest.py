import copy

import _test_utilities  # initializes django


def pytest_collection_modifyitems(config, items):
    from django_compat_patcher.registry import django_patching_registry
    from compat_patcher.utilities import ensure_all_fixers_have_a_test_under_pytest
    ensure_all_fixers_have_a_test_under_pytest(
        config=config, items=items, patching_registry=django_patching_registry
    )
