from __future__ import absolute_import, print_function, unicode_literals

import os, sys, pytest, warnings

import _test_utilities

from django.test import override_settings

import django_compat_patcher.utilities
from django_compat_patcher.utilities import (inject_class, inject_callable, inject_attribute,
                                             inject_callable_alias, inject_module, emit_warning, emit_log, get_patcher_setting)


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


def test_DCP_ENABLE_WARNINGS():

    assert django_compat_patcher.utilities.DCP_ENABLE_WARNINGS == True  # default

    warnings.simplefilter("always", Warning)

    with warnings.catch_warnings(record=True) as w:
        emit_warning("this feature is obsolete!", DeprecationWarning)
    assert len(w) == 1
    warning = w[0]
    message = str(warning.message)
    assert "this feature is obsolete!" in message

    from django_compat_patcher.patcher import patch
    patch(settings=dict(DCP_INCLUDE_FIXER_IDS=[],
                        DCP_ENABLE_WARNINGS=False))
    patch()  # changes nothing

    with warnings.catch_warnings(record=True) as w:
        emit_warning("this feature is dead!", DeprecationWarning)
    assert len(w) == 0  # well disabled


def test_DCP_LOGGING_LEVEL(capsys):

    assert django_compat_patcher.utilities.DCP_LOGGING_LEVEL == "INFO"  # default

    # ensure specific assertions are OK
    get_patcher_setting("DCP_LOGGING_LEVEL", {"DCP_LOGGING_LEVEL": None})
    get_patcher_setting("DCP_LOGGING_LEVEL", {"DCP_LOGGING_LEVEL": "INFO"})
    with pytest.raises(AssertionError):
        get_patcher_setting("DCP_LOGGING_LEVEL", {"DCP_LOGGING_LEVEL": "badvalue"})

    emit_log("<DEBUGGING>", "DEBUG")
    emit_log("<INFORMATION>")  # default value

    out, err = capsys.readouterr()

    assert "<DEBUGGING>" not in err
    assert "<INFORMATION>" in err

    from django_compat_patcher.patcher import patch
    patch(settings=dict(DCP_LOGGING_LEVEL=None))
    patch()  # changes nothing

    emit_log("<DEBUGGING2>", "DEBUG")
    emit_log("<INFORMATION2>", "INFO")
    out, err = capsys.readouterr()
    assert "<DEBUGGING2>" not in err
    assert "<INFORMATION2>" not in err

    from django_compat_patcher.patcher import patch
    patch(settings=dict(DCP_LOGGING_LEVEL="DEBUG"))
    patch()  # changes nothing

    emit_log("<DEBUGGING3>", "DEBUG")
    emit_log("<INFORMATION3>", "INFO")
    out, err = capsys.readouterr()
    assert "<DEBUGGING3>" in err
    assert "<INFORMATION3>" in err


def test_no_stdlib_warnings():

    pkg_root = os.path.dirname(django_compat_patcher.__file__)

    # we authorize "warnings.warn", as long as it uses our custom WarningsProxy
    forbidden_phrases = ["import warnings", "from warnings", "django.utils.deprecation"]

    for root, subdirs, files in os.walk(pkg_root):
        for f in [x for x in files if x.endswith(".py")]:
            full_path = os.path.join(root, f)
            #print(">> ANALYSING PYTHON FILE", full_path)
            with open(full_path, "r") as s:
                data = s.read()
            for forbidden_phrase in forbidden_phrases:
                if forbidden_phrase in data:
                    if (f == "utilities.py") and ("import warnings as stdlib_warnings" in data):
                        continue  # the only case OK is our own warnings utility
                    raise Exception("ALERT, wrong phrase '%s' detected in %s" % (forbidden_phrase, full_path))
