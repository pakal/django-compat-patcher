


def test_fix_deletion_utils_six():
    import django.utils.six
    from django.utils import six as six2
    assert django.utils.six.string_types
    assert six2.string_types


def test_fix_deletion_utils_upath_npath_abspathu():
    from os.path import abspath
    from django.utils._os import abspathu, upath, npath

    assert abspathu(".") == abspath(".")
    assert upath("/something/file.txt") == "/something/file.txt"  # No-op
    assert npath("/something2/file.txt") == "/something2/file.txt"  # No-op


def test_fix_deletion_utils_decorators_ContextDecorator():
    from django.utils.decorators import ContextDecorator
    from contextlib import ContextDecorator as ContextDecoratorOriginal
    assert isinstance(ContextDecorator, type)
    assert ContextDecorator is ContextDecoratorOriginal


def test_fix_deletion_utils_decorators_available_attrs():
    from django.utils.decorators import available_attrs
    from functools import WRAPPER_ASSIGNMENTS

    def func():
        pass

    assert available_attrs(func) == WRAPPER_ASSIGNMENTS
