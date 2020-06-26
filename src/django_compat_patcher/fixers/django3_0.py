from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_30_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="3.0",
    fixer_applied_from_version="3.0",
)


@django1_30_bc_fixer()
def fix_deletion_utils_six(utils):
    """Preserve the vendored copy of "six" compatibility utility, in django.utils"""
    import six
    utils.inject_import_alias(alias_name="django.utils.six", real_name="six")


@django1_30_bc_fixer()
def fix_deletion_utils_upath_npath_abspathu(utils):
    """Preserve python2 path normalization functions."""

    from os.path import abspath as abspathu  # For backwards-compatibility in Django 2.0

    def upath(path):
        """Always return a unicode path (did something for Python 2)."""
        return path

    def npath(path):
        """
        Always return a native path, that is unicode on Python 3 and bytestring on
        Python 2. Noop for Python 3.
        """
        return path

    from django.utils import _os
    utils.inject_callable(_os, "abspathu", abspathu)
    utils.inject_callable(_os, "upath", upath)
    utils.inject_callable(_os, "npath", npath)


@django1_30_bc_fixer()
def fix_deletion_utils_decorators_ContextDecorator(utils):
    """Preserve django.utils.decorators.ContextDecorator, alias of contextlib.ContextDecorator."""
    from contextlib import ContextDecorator
    from django.utils import decorators
    utils.inject_class(decorators, "ContextDecorator", ContextDecorator)


@django1_30_bc_fixer()
def fix_deletion_utils_decorators_available_attrs(utils):
    """Preserve django.utils.decorators.available_attrs, which just returns functools.WRAPPER_ASSIGNMENTS."""

    def available_attrs(fn):  # For backwards compatibility in Django 2.0.
        """
        Return the list of functools-wrappable attributes on a callable.
        This was required as a workaround for https://bugs.python.org/issue3445
        under Python 2.
        """
        from functools import WRAPPER_ASSIGNMENTS
        return WRAPPER_ASSIGNMENTS

    from django.utils import decorators
    utils.inject_callable(decorators, "available_attrs", available_attrs)


@django1_30_bc_fixer()
def fix_deletion_django_utils_lru_cache_lru_cache(utils):
    """Perserve django.utils.lru_cache.lru_cache(), alias of functools.lru_cache(), and its containing module."""
    from ..django_legacy.django3_0 import lru_cache as django_lru_cache_module
    utils.inject_module("django.utils.lru_cache", django_lru_cache_module)


@django1_30_bc_fixer()
def fix_deletion_django_utils_safestring_SafeBytes(utils):
    """Perserve django.utils.safestring.SafeBytes class."""
    from django.utils.safestring import SafeData, SafeText
    from django.utils import safestring

    class SafeBytes(bytes, SafeData):
        """
        A bytes subclass that has been specifically marked as "safe" (requires no
        further escaping) for HTML output purposes.

        Kept in Django 2.0 for usage by apps supporting Python 2. Shouldn't be used
        in Django anymore.
        """
        def __add__(self, rhs):
            """
            Concatenating a safe byte string with another safe byte string or safe
            string is safe. Otherwise, the result is no longer safe.
            """
            t = super(SafeBytes, self).__add__(rhs)
            if isinstance(rhs, SafeText):
                return SafeText(t)
            elif isinstance(rhs, SafeBytes):
                return SafeBytes(t)
            return t

    utils.inject_class(safestring, "SafeBytes", SafeBytes)
