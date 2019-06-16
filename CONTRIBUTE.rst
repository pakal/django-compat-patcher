===============================================================
Django-compat-patcher warmly welcomes new fixers, and bugfixes
===============================================================


See "django_deprecation_timeline_notes.rst" for a list of breaking changes in Django history, and their current status in DCP.



Example of fixer
-------------------

Reverting the removal of the :code:`get_formsets()` method from django's :code:`ModelAdmin` (in submodule :code:`django.contrib.admin`) looks like this:

:code:`fix_deletion_contrib_admin_ModelAdmin_get_formsets`



