from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_51_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="5.1",
    fixer_applied_from_version="5.1",
)


@django1_51_bc_fixer()
def fix_deletion_core_files_storage_get_storage_class(utils):
    """Preserve get_storage_class() in django.core.files.storage, superseded by STORAGES"""
    from django.utils.module_loading import import_string
    from django.conf import settings

    GET_STORAGE_CLASS_DEPRECATED_MSG = (
        "django.core.files.storage.get_storage_class is deprecated in favor of "
        "using django.core.files.storage.storages."
    )

    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    def get_storage_class(import_path=None):
        warnings.warn(GET_STORAGE_CLASS_DEPRECATED_MSG, RemovedInDjango51Warning)
        return import_string(import_path or getattr(settings, 'DEFAULT_FILE_STORAGE', None) or DEFAULT_FILE_STORAGE)

    from django.core.files import storage
    utils.inject_callable(storage, "get_storage_class", get_storage_class)


@django1_51_bc_fixer(fixer_delayed=True)
def fix_deletion_contrib_auth_base_user_make_random_password(utils):
    """Restore BaseUserManager.make_random_password(), removed in Django 5.1"""
    from django.utils.crypto import get_random_string
    from django.contrib.auth.base_user import BaseUserManager

    def make_random_password(
        self,
        length=10,
        allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789",
    ):
        warnings.warn(
            "BaseUserManager.make_random_password() is deprecated.",
            RemovedInDjango51Warning,
            stacklevel=2,
        )
        return get_random_string(length, allowed_chars)

    utils.inject_callable(BaseUserManager, "make_random_password", make_random_password)


@django1_51_bc_fixer()
def fix_deletion_template_defaultfilters_length_is(utils):
    """Restore the length_is template filter, removed in Django 5.1"""
    from django.template import defaultfilters

    def length_is(value, arg):
        """Return a boolean of whether the value's length is the argument."""
        warnings.warn(
            "The length_is template filter is deprecated in favor of the length "
            "template filter and the == operator within an {% if %} tag.",
            RemovedInDjango51Warning,
        )
        try:
            return len(value) == int(arg)
        except (ValueError, TypeError):
            return ""

    defaultfilters.register.filter("length_is", length_is)
    utils.inject_callable(defaultfilters, "length_is", length_is)


@django1_51_bc_fixer()
def fix_deletion_test_SimpleTestCase_assertFormsetError(utils):
    """Restore lowercase assertFormsetError() as an alias for assertFormSetError() on SimpleTestCase, removed in Django 5.1"""
    from django.test import SimpleTestCase

    def assertFormsetError(self, *args, **kw):
        warnings.warn(
            "assertFormsetError() is deprecated in favor of assertFormSetError().",
            RemovedInDjango51Warning,
            stacklevel=2,
        )
        return self.assertFormSetError(*args, **kw)

    utils.inject_callable(SimpleTestCase, "assertFormsetError", assertFormsetError)


@django1_51_bc_fixer()
def fix_deletion_test_TransactionTestCase_assertQuerysetEqual(utils):
    """Restore lowercase assertQuerysetEqual() as an alias for assertQuerySetEqual() on TransactionTestCase, removed in Django 5.1"""
    from django.test import TransactionTestCase

    def assertQuerysetEqual(self, *args, **kw):
        warnings.warn(
            "assertQuerysetEqual() is deprecated in favor of assertQuerySetEqual().",
            RemovedInDjango51Warning,
            stacklevel=2,
        )
        return self.assertQuerySetEqual(*args, **kw)

    utils.inject_callable(TransactionTestCase, "assertQuerysetEqual", assertQuerysetEqual)


@django1_51_bc_fixer()
def fix_behaviour_core_signing_Signer_positional_args(utils):
    """Restore support for positional arguments to Signer and TimestampSigner, removed in Django 5.1"""
    from django.core.signing import Signer

    original_init = Signer.__init__

    def patched_Signer_init(self, *args, key=None, sep=":", salt=None, algorithm=None, fallback_keys=None):
        if args:
            warnings.warn(
                "Passing positional arguments to %s is deprecated." % self.__class__.__name__,
                RemovedInDjango51Warning,
                stacklevel=2,
            )
            for arg, attr_name in zip(args, ["key", "sep", "salt", "algorithm", "fallback_keys"]):
                if arg or attr_name == "sep":
                    if attr_name == "key":
                        key = arg
                    elif attr_name == "sep":
                        sep = arg
                    elif attr_name == "salt":
                        salt = arg
                    elif attr_name == "algorithm":
                        algorithm = arg
                    elif attr_name == "fallback_keys":
                        fallback_keys = arg
        original_init(self, key=key, sep=sep, salt=salt, algorithm=algorithm, fallback_keys=fallback_keys)

    utils.inject_callable(Signer, "__init__", patched_Signer_init)


@django1_51_bc_fixer()
def fix_deletion_conf_settings_DEFAULT_FILE_STORAGE(utils):
    """Preserve DEFAULT_FILE_STORAGE and STATICFILES_STORAGE settings, superseded by STORAGES and removed in Django 5.1"""
    from django.conf import settings
    from django.core.files.storage import StorageHandler

    def patched_backends(self):
        if self._backends is not None:
            return self._backends
        result = settings.STORAGES.copy()
        try:
            default_storage = settings.DEFAULT_FILE_STORAGE
            warnings.warn(
                "The DEFAULT_FILE_STORAGE setting is deprecated in favor of "
                "STORAGES['default'].",
                RemovedInDjango51Warning,
            )
            result["default"] = {"BACKEND": default_storage}
        except AttributeError:
            pass
        try:
            staticfiles_storage = settings.STATICFILES_STORAGE
            warnings.warn(
                "The STATICFILES_STORAGE setting is deprecated in favor of "
                "STORAGES['staticfiles'].",
                RemovedInDjango51Warning,
            )
            result["staticfiles"] = {"BACKEND": staticfiles_storage}
        except AttributeError:
            pass
        return result

    utils.inject_attribute(StorageHandler, "backends", property(patched_backends))

