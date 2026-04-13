
import _test_utilities


def test_fix_deletion_core_files_storage_get_storage_class(settings):

    from django.core.files.storage import get_storage_class

    klass = get_storage_class()
    assert klass.__name__ == "FileSystemStorage"

    # We override or create this (deprecated) setting
    settings.DEFAULT_FILE_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

    klass = get_storage_class()
    assert klass.__name__ == "StaticFilesStorage"

    klass = get_storage_class('django.core.files.storage.FileSystemStorage')
    assert klass.__name__ == "FileSystemStorage"


def test_fix_deletion_contrib_auth_base_user_make_random_password():
    from django.contrib.auth.base_user import BaseUserManager

    mgr = BaseUserManager()

    # Default length is 10
    password = mgr.make_random_password()
    assert len(password) == 10

    # Custom length
    password = mgr.make_random_password(length=20)
    assert len(password) == 20

    # Custom allowed chars
    password = mgr.make_random_password(length=8, allowed_chars="abc")
    assert len(password) == 8
    assert all(c in "abc" for c in password)


def test_fix_deletion_template_defaultfilters_length_is():
    from django.template.defaultfilters import length_is

    assert length_is([1, 2, 3], 3) is True
    assert length_is([1, 2, 3], 2) is False
    assert length_is("hello", 5) is True
    assert length_is("hello", 4) is False

    # Invalid arg returns empty string
    assert length_is("hello", "not-a-number") == ""

    # Also verify it works as a template filter
    from django.template import engines
    django_engine = engines["django"]
    template = django_engine.from_string('{% load i18n %}{{ value|length_is:3 }}')
    # length_is should be in the default filters
    from django.template.defaultfilters import register
    assert "length_is" in register.filters


def test_fix_deletion_test_SimpleTestCase_assertFormsetError():
    from django.test import SimpleTestCase

    assert hasattr(SimpleTestCase, "assertFormsetError")
    assert callable(SimpleTestCase.assertFormsetError)

    # Verify it's available on subclasses too
    from django.test import TestCase
    assert hasattr(TestCase, "assertFormsetError")


def test_fix_deletion_test_TransactionTestCase_assertQuerysetEqual():
    from django.test import TransactionTestCase

    assert hasattr(TransactionTestCase, "assertQuerysetEqual")
    assert callable(TransactionTestCase.assertQuerysetEqual)

    # Verify it's available on TestCase too (inherits from TransactionTestCase)
    from django.test import TestCase
    assert hasattr(TestCase, "assertQuerysetEqual")


def test_fix_behaviour_core_signing_Signer_positional_args():
    from django.core.signing import Signer, TimestampSigner

    # keyword args should still work (unchanged behavior)
    signer = Signer(key="my-key", sep=":", salt="my-salt")
    assert signer.key == "my-key"
    assert signer.sep == ":"
    assert signer.salt == "my-salt"

    # positional key argument
    signer = Signer("my-positional-key")
    assert signer.key == "my-positional-key"

    # positional key and sep
    signer = Signer("my-key", "|")
    assert signer.key == "my-key"
    assert signer.sep == "|"

    # positional key, sep, and salt
    signer = Signer("my-key", ":", "my-salt")
    assert signer.key == "my-key"
    assert signer.sep == ":"
    assert signer.salt == "my-salt"

    # Sign and unsign should still work
    signed = signer.sign("hello")
    assert signer.unsign(signed) == "hello"

    # TimestampSigner inherits from Signer — also accepts positional args
    ts_signer = TimestampSigner("my-ts-key")
    assert ts_signer.key == "my-ts-key"


def test_fix_deletion_db_models_options_index_together():
    from django.db import models

    # Model with index_together must not raise TypeError
    class SampleModel(models.Model):
        name = models.CharField(max_length=100)
        rank = models.IntegerField()

        class Meta:
            app_label = "django_compat_patcher"
            index_together = [["name", "rank"]]

    # The index_together fields must appear as an Index in _meta.indexes
    idx_fields = [tuple(idx.fields) for idx in SampleModel._meta.indexes if hasattr(idx, "fields")]
    assert ("name", "rank") in idx_fields

    # Models without index_together are not affected
    class CleanModel(models.Model):
        title = models.CharField(max_length=50)

        class Meta:
            app_label = "django_compat_patcher"

    assert CleanModel._meta.indexes == []

    # Multiple index groups are all converted
    class MultiIndexModel(models.Model):
        a = models.IntegerField()
        b = models.IntegerField()
        c = models.IntegerField()

        class Meta:
            app_label = "django_compat_patcher"
            index_together = [["a", "b"], ["b", "c"]]

    multi_fields = [tuple(idx.fields) for idx in MultiIndexModel._meta.indexes if hasattr(idx, "fields")]
    assert ("a", "b") in multi_fields
    assert ("b", "c") in multi_fields

    # Explicit Meta.indexes entries are not duplicated
    class NoDupModel(models.Model):
        x = models.IntegerField()
        y = models.IntegerField()

        class Meta:
            app_label = "django_compat_patcher"
            indexes = [models.Index(fields=["x", "y"])]
            index_together = [["x", "y"]]

    nodup_fields = [tuple(idx.fields) for idx in NoDupModel._meta.indexes if hasattr(idx, "fields")]
    assert nodup_fields.count(("x", "y")) == 1


def test_fix_deletion_conf_settings_DEFAULT_FILE_STORAGE(settings):
    from django.core.files.storage import StorageHandler

    # Without deprecated setting, default storage should be FileSystemStorage
    handler = StorageHandler()
    default = handler["default"]
    assert default.__class__.__name__ == "FileSystemStorage"

    # With DEFAULT_FILE_STORAGE set, it should override STORAGES["default"]
    settings.DEFAULT_FILE_STORAGE = "django.core.files.storage.InMemoryStorage"
    handler2 = StorageHandler()
    default2 = handler2["default"]
    assert default2.__class__.__name__ == "InMemoryStorage"
