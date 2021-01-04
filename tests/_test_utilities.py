from __future__ import absolute_import, print_function, unicode_literals

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

import django
import django_compat_patcher

# This MUST happen BEFORE django is setup(), else import proxies can't be installed
settings = dict(DCP_EXCLUDE_FIXER_IDS=[])  # REMOVE the disabling of unsafe fixers, for tests!
django_compat_patcher.patch(settings)

django.setup()  # idempotent

DJANGO_VERSION_TUPLE = django.VERSION




