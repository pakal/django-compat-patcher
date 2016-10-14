import sys

from django.test import override_settings

from django_compat_patcher.utilities import inject_class, inject_callable


def test__patch_object__name__():
    from django.contrib.admin import actions

    class MockClass():
        pass

    inject_class(actions, 'TemplateResponse', MockClass)
    assert actions.TemplateResponse.__name__ == 'MockClass__DJANGO_COMPAT_PATCHER'

    def mock_function():
        pass

    inject_callable(actions, 'delete_selected', mock_function)
    assert actions.delete_selected.__name__ == 'mock_function__DJANGO_COMPAT_PATCHER'


@override_settings(DCP_MONKEY_PATCH_NAME=False)
def test_DCP_MONKEY_PATCH_NAME_setting():

    def mock_function():
        pass

    class MockModule(object):
        @staticmethod
        def method(a, b):
            return a + b

    sys.modules["mock_module"] = MockModule

    import mock_module

    inject_callable(mock_module, 'method', mock_function)
    assert mock_module.method.__name__ == 'method'