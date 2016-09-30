

import django_compat_patcher
django_compat_patcher.patch()

import django
django.setup()
