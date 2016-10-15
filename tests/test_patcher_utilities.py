import sys

import pytest
from django.test import override_settings

from django_compat_patcher.utilities import inject_class, inject_callable


def test__patch_injected_object():
    from django.contrib.admin import actions

    class TemplateResponse():
        pass

    inject_class(actions, 'TemplateResponse', TemplateResponse)
    assert getattr(actions.TemplateResponse, "__dcp_injected__") == True

    def delete_selected():
        pass

    inject_callable(actions, 'delete_selected', delete_selected)
    assert getattr(actions.delete_selected, "__dcp_injected__") == True


@override_settings(DCP_PATCH_INJECTED_OBJECT=False)
def test_DCP_PATCH_INJECTED_OBJECT_setting():

    def mock_function():
        pass

    class MockModule(object):
        @staticmethod
        def method(a, b):
            return a + b

    sys.modules["mock_module"] = MockModule

    import mock_module

    inject_callable(mock_module, 'method', MockModule.method)
    assert not hasattr(mock_module.method, "__dcp_injected__")