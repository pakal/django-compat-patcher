from __future__ import absolute_import, print_function, unicode_literals

import os, logging, random

os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

logging.basicConfig()  # so that logging works before django LOGGING kicks in

import django
import django_compat_patcher

# this MUST happen BEFORE django is setup(), else import proxies can't be installed
django_compat_patcher.patch()

django.setup()  # idempotent
