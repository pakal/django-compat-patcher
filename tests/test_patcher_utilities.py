import sys

import pytest
from django.test import override_settings

from django_compat_patcher.utilities import inject_class, inject_callable


def test__patch_object__name__():
    from django.contrib.admin import actions

    class TemplateResponse():
        pass

    class MockClass():
        pass

    inject_class(actions, 'TemplateResponse', TemplateResponse)
    assert actions.TemplateResponse.__name__ == 'TemplateResponse__DJANGO_COMPAT_PATCHER'

    with pytest.raises(AssertionError):
        inject_class(actions, 'TemplateResponse', MockClass)


    def mock_function():
        pass

    def delete_selected():
        pass

    inject_callable(actions, 'delete_selected', delete_selected)
    assert actions.delete_selected.__name__ == 'delete_selected__DJANGO_COMPAT_PATCHER'

    with pytest.raises(AssertionError):
        inject_callable(actions, "delete_selected", mock_function)


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

    inject_callable(mock_module, 'method', MockModule.method)
    assert mock_module.method.__name__ == 'method'