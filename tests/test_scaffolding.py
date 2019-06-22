import os

import pytest
from compat_patcher_core.scaffolding import ensure_no_stdlib_warnings


def test_ensure_no_stdlib_warnings_in_package():
    import warnings  # This line will trigger checker error
    del warnings

    import django_compat_patcher

    pkg_root = os.path.dirname(django_compat_patcher.__file__)
    analysed_files = ensure_no_stdlib_warnings(pkg_root)
    assert len(analysed_files) >= 3, analysed_files

    test_root = os.path.dirname(__file__)
    with pytest.raises(ValueError, match="wrong phrase.*test_scaffolding.py"):
        ensure_no_stdlib_warnings(test_root)


def test_no_package_shadowing_in_tox():
    import django_compat_patcher

    package_dir = os.path.dirname(os.path.abspath(django_compat_patcher.__file__))
    if os.getenv("INSIDE_TOX_FOR_DCP") and ".tox" not in package_dir:
        raise RuntimeError("Wrong django_compat_patcher package used in Tox")
