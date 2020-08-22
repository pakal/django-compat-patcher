import os

import pytest
from django.conf import settings
from django_compat_patcher.config import DjangoSettingsProvider

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


def test_dcp_settings_overrides():

    old_environ = os.environ.copy()

    assert not hasattr(settings, "DCP_INCLUDE_FIXER_IDS")
    settings.DCP_INCLUDE_FIXER_IDS = ["some_django_setting_for_included_ids"]

    try:

        django_settings_provider = DjangoSettingsProvider(settings=dict(DCP_INCLUDE_FIXER_FAMILIES="*"))
        assert django_settings_provider["include_fixer_families"] == "*"
        assert django_settings_provider["include_fixer_ids"] == "*"  # DEFAULT DCP VALUE, no fallback to Django-level setting

        django_settings_provider = DjangoSettingsProvider(settings=None)
        assert django_settings_provider["include_fixer_ids"] == ["some_django_setting_for_included_ids"]

        os.environ.update(
            DCP_INCLUDE_FIXER_IDS = '["some_included_id"]',
            DCP_INCLUDE_FIXER_FAMILIES = '["some_included_family"]',

            DCP_EXCLUDE_FIXER_IDS = '["some_excluded_id"]',
            DCP_EXCLUDE_FIXER_FAMILIES = '["some_excluded_family"]',

            DCP_PATCH_INJECTED_OBJECTS = 'true',

            DCP_LOGGING_LEVEL = '"DEBUG"',
            DCP_ENABLE_WARNINGS = 'false',
        )

        assert django_settings_provider["include_fixer_ids"] == ["some_included_id"]
        assert django_settings_provider["include_fixer_families"] == ["some_included_family"]
        assert django_settings_provider["exclude_fixer_ids"] == ["some_excluded_id"]
        assert django_settings_provider["exclude_fixer_families"] == ["some_excluded_family"]
        assert django_settings_provider["patch_injected_objects"] == True
        assert django_settings_provider["logging_level"] == "DEBUG"
        assert django_settings_provider["enable_warnings"] == False

        del os.environ["DCP_INCLUDE_FIXER_IDS"]
        assert django_settings_provider["include_fixer_ids"] == ["some_django_setting_for_included_ids"]  # Fallback to django-level setting

        os.environ.update(
            DCP_INCLUDE_FIXER_IDS = "['some_included_id']"  # NOT real json due to quotes
        )
        with pytest.raises(ValueError, match="Abnormal json"):
            django_settings_provider["include_fixer_ids"]
    finally:
        os.environ.clear()
        os.environ.update(old_environ)
        del settings.DCP_INCLUDE_FIXER_IDS


