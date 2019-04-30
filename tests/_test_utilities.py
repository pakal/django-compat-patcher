from __future__ import absolute_import, print_function, unicode_literals

import os, sys, logging, random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

import django
import django_compat_patcher

# this MUST happen BEFORE django is setup(), else import proxies can't be installed
django_compat_patcher.patch()

django.setup()  # idempotent

DJANGO_VERSION_TUPLE = django.VERSION
