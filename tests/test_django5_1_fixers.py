

def test_fix_deletion_core_files_storage_get_storage_class(settings):

    from django.core.files.storage import get_storage_class

    klass = get_storage_class()
    assert klass.__name__ == "FileSystemStorage"

    # We override or create this (deprecated) setting
    settings.DEFAULT_FILE_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

    klass = get_storage_class()
    assert klass.__name__ == "StaticFilesStorage"

    klass = get_storage_class('django.core.files.storage.FileSystemStorage')
    assert klass.__name__ == "FileSystemStorage"