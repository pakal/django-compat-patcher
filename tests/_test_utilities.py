from __future__ import absolute_import, print_function, unicode_literals

import os, logging, random

os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

logging.basicConfig()  # so that logging works before django LOGGING kicks in

import django

early_django_setup = random.choice((True, False))
if early_django_setup:
    django.setup()

import django_compat_patcher

django_compat_patcher.patch()

django.setup()  # idempotent
