from __future__ import absolute_import, print_function, unicode_literals

import os, sys, logging, random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings_no_db")

import django
import django_compat_patcher  # ensure its folder is in your PYTHONPATH, if not found

# this MUST happen BEFORE django is setup(), else import proxies can't be installed
django_compat_patcher.patch()

django.setup()  # idempotent

DJANGO_VERSION_TUPLE = django.VERSION
