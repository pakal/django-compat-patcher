from __future__ import absolute_import, print_function, unicode_literals

import os
import sys



sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.minimal_settings"

os.environ.update(
    DCP_INCLUDE_FIXER_IDS = '["some_included_id"]',
    DCP_INCLUDE_FIXER_FAMILIES = '["some_included_family"]',

    DCP_EXCLUDE_FIXER_IDS = '["some_excluded_id"]',
    DCP_EXCLUDE_FIXER_FAMILIES = '["some_excluded_family"]',

    DCP_PATCH_INJECTED_OBJECTS = 'true',

    DCP_LOGGING_LEVEL = '"DEBUG"',
    DCP_ENABLE_WARNINGS = 'false',
)

import django
import django_compat_patcher

django_compat_patcher.patch()  # fixers which can't apply should be skipped, not crash

from django_compat_patcher.config import DjangoSettingsProvider

django_settings_provider = DjangoSettingsProvider(settings=None)

assert django_settings_provider["include_fixer_ids"] == ["some_included_id"]
assert django_settings_provider["include_fixer_families"] == ["some_included_family"]
assert django_settings_provider["exclude_fixer_ids"] == ["some_excluded_id"]
assert django_settings_provider["exclude_fixer_families"] == ["some_excluded_family"]
assert django_settings_provider["patch_injected_objects"] == True
assert django_settings_provider["logging_level"] == "DEBUG"
assert django_settings_provider["enable_warnings"] == False
