from __future__ import absolute_import, print_function, unicode_literals

import os
os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

import django_compat_patcher
django_compat_patcher.patch()

import django
django.setup()
