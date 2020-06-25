


def test_fix_deletion_utils_six():
    import django.utils.six
    from django.utils import six as six2
    assert django.utils.six.string_types
    assert six2.string_types

