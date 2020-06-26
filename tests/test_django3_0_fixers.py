


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


def test_fix_deletion_utils_lru_cache_lru_cache():
    from django.utils.lru_cache import lru_cache as django_lru_cache_function
    from functools import lru_cache
    assert callable(django_lru_cache_function)
    assert django_lru_cache_function is lru_cache


def test_fix_deletion_utils_safestring_SafeBytes():
    from django.utils.safestring import SafeBytes
    assert SafeBytes("abc", "ascii") == bytes("abc", "ascii")


def test_fix_deletion_test_utils_str_prefix():
    from django.test.utils import str_prefix
    assert str_prefix("%(_)shello") == "hello"


def test_fix_deletion_test_utils_patch_logger():
    import logging
    from django.test.utils import patch_logger
    with patch_logger("django", "info") as calls:
        logging.getLogger("django").info("Patch-logger context manager seems to work %s", "fine")
    assert len(calls) == 1
    assert calls == ["Patch-logger context manager seems to work fine"]
