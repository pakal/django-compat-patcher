from __future__ import absolute_import, print_function, unicode_literals

import django_compat_patcher
django_compat_patcher.patch()

import django
django.setup()
