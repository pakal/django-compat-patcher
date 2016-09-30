# django-compat-patcher

A "magic" package which adds retro/forward compatibility patches to Django, so that your app ecosystem doesn't get broken by trivial changes in the core of the framework.

Add "django-compat-patcher" to your pip requirements, install it, and then activate it with::
    
    import django_compat_patcher
    django_compat_patcher.patch()
    
This code must be placed BEFORE any use of django (eg. in your manage.py or your wsgi script). 

However, the DJANGO_SETTINGS_MODULE environment variable must already be set.
