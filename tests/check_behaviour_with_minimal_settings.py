from __future__ import absolute_import, print_function, unicode_literals

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.minimal_settings"

import django
import django_compat_patcher

django_compat_patcher.patch()  # fixers which can't apply should be skipped, not crash

django.setup()  # idempotent

from django.conf import settings

assert settings.INSTALLED_APPS == []  # we ensure that we haven't mixed django confs
