from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_51_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="5.1",
    fixer_applied_from_version="5.1",
)


@django1_51_bc_fixer()
def fix_deletion_core_files_storage_get_storage_class(utils):
    """Preserve get_storage_class() in django.core.files.storage, superseded by STORAGES"""
    from django.utils.module_loading import import_string
    from django.conf import settings

    GET_STORAGE_CLASS_DEPRECATED_MSG = (
        "django.core.files.storage.get_storage_class is deprecated in favor of "
        "using django.core.files.storage.storages."
    )

    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    def get_storage_class(import_path=None):
        warnings.warn(GET_STORAGE_CLASS_DEPRECATED_MSG, RemovedInDjango51Warning)
        return import_string(import_path or getattr(settings, 'DEFAULT_FILE_STORAGE', None) or DEFAULT_FILE_STORAGE)

    from django.core.files import storage
    utils.inject_callable(storage, "get_storage_class", get_storage_class)

