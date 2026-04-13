from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_50_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="5.0",
    fixer_applied_from_version="5.0",
)


@django1_50_bc_fixer()
def fix_deletion_utils_baseconv(utils):
    """Preserve django.utils.baseconv module, removed in Django 5.0"""
    from django_compat_patcher.django_legacy.django5_0 import utils__baseconv
    import django.utils
    utils.inject_module("django.utils.baseconv", utils__baseconv)
    utils.inject_attribute(django.utils, "baseconv", utils__baseconv)


@django1_50_bc_fixer()
def fix_deletion_utils_datetime_safe(utils):
    """Preserve django.utils.datetime_safe module, removed in Django 5.0"""
    from django_compat_patcher.django_legacy.django5_0 import utils__datetime_safe
    import django.utils
    utils.inject_module("django.utils.datetime_safe", utils__datetime_safe)
    utils.inject_attribute(django.utils, "datetime_safe", utils__datetime_safe)


@django1_50_bc_fixer()
def fix_deletion_utils_timezone_utc(utils):
    """Restore django.utils.timezone.utc as an alias for datetime.timezone.utc, removed in Django 5.0"""
    import datetime as dt_module
    from django.utils import timezone
    utils.inject_attribute(timezone, "utc", dt_module.timezone.utc)


@django1_50_bc_fixer()
def fix_behaviour_utils_functional_cached_property_name_argument(utils):
    """Preserve the deprecated name argument of django.utils.functional.cached_property, removed in Django 5.0"""
    from django.utils.functional import cached_property
    original_init = cached_property.__init__

    def patched_init(self, func, name=None):
        if name is not None:
            warnings.warn(
                "The name argument is deprecated as it's unnecessary as of "
                "Python 3.6.",
                RemovedInDjango50Warning,
                stacklevel=2,
            )
        original_init(self, func)

    utils.inject_callable(cached_property, "__init__", patched_init)
