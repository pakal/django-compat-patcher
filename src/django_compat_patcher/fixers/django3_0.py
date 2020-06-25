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
