from __future__ import absolute_import, print_function, unicode_literals

import sys, pytest, warnings

import _test_utilities

from django.test import override_settings

from django_compat_patcher.utilities import (inject_class, inject_callable, inject_attribute,
                                             inject_callable_alias, inject_module, emit_warning)


def test_patch_injected_object():
    from django.contrib.admin import actions
    import csv

    class TemplateResponse():
        pass

    inject_class(actions, 'TemplateResponse', TemplateResponse)
    assert getattr(actions.TemplateResponse, "__dcp_injected__") == True
    del actions.TemplateResponse.__dcp_injected__

    response = TemplateResponse()

    inject_attribute(actions, '_response_', response)
    assert getattr(response, "__dcp_injected__") == True

    def delete_selected():
        pass

    inject_callable(actions, 'delete_selected', delete_selected)
    assert getattr(actions.delete_selected, "__dcp_injected__") == True  # TODO Module check

    inject_module("new_csv", csv)
    import new_csv
    assert getattr(new_csv, "__dcp_injected__") == True


    def mycallable():
        pass

    source_object = TemplateResponse()
    source_object.my_attr = mycallable
    target_object = TemplateResponse()
    inject_callable_alias(source_object, "my_attr",
                          target_object, "other_attr")
    assert getattr(target_object.other_attr, "__dcp_injected__") == True



@override_settings(DCP_PATCH_INJECTED_OBJECTS=False)
def test_DCP_PATCH_INJECTED_OBJECTS_setting():

    from django.conf import settings as django_settings
    assert not django_settings.DCP_PATCH_INJECTED_OBJECTS

    def mock_function():
        pass

    class MockModule(object):
        @staticmethod
        def method(a, b):
            return a + b

    sys.modules["mock_module"] = MockModule

    import mock_module

    from django.conf import settings as django_settings2
    assert not django_settings2.DCP_PATCH_INJECTED_OBJECTS

    inject_callable(mock_module, 'method', mock_function)
    assert not hasattr(mock_module.method, "__dcp_injected__") # FIXME USE GLOBAL VARIABLE


def test_DCP_ENABLE_WARNINGS(capsys):

    warnings.simplefilter("always", Warning)

    with warnings.catch_warnings(record=True) as w:
        emit_warning("this feature is obsolete!", DeprecationWarning)
    assert len(w) == 1
    assert "this feature is obsolete!" in w[0].message

    from django_compat_patcher.patcher import patch
    patch(settings=dict(DCP_INCLUDE_FIXER_IDS=[],
                        DCP_ENABLE_WARNINGS=False))

    with warnings.catch_warnings(record=True) as w:
        emit_warning("this feature is dead!", DeprecationWarning)
    assert len(w) == 0  # well disabled


'''
def ___test_DCP_ENABLE_DEPRECATION_WARNINGS(capsys):
    capsys.readouterr()  # discarded
    emit_warning("this feature is obsolete!", DeprecationWarning)
    out, err = capsys.readouterr()
    assert "this feature is obsolete!" in err
'''
