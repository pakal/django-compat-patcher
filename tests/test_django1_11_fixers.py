from __future__ import absolute_import, print_function, unicode_literals

import pytest

import _test_utilities


def test_fix_behaviour_widget_build_attrs():
    from django.forms.widgets import Select

    select = Select({"someattr": "somevalue"})

    attrs = select.build_attrs({"other": "yes"}, multiple="multiple")  # old behavior
    assert attrs == {"someattr": "somevalue", "multiple": "multiple", "other": "yes"}

    try:
        attrs = select.build_attrs({"this": "no"}, {"other": "yes"})  # new behavior
        assert attrs == {"this": "no", "other": "yes"}
    except TypeError:  # old (unpatched) signature, with only 2 positional arguments including "self"
        attrs = select.build_attrs(extra_attrs={"this": "no"})
        assert attrs == {"someattr": "somevalue", "this": "no"}
    else:
        attrs = select.build_attrs({"this": "no"})  # new behavior
        assert attrs == {"this": "no"}  # no self.attrs added


def test_fix_incoming_test_utils_setup_test_environment_signature_change():
    from django.test.utils import setup_test_environment

    try:
        setup_test_environment(debug=True)
    except RuntimeError:
        pass  # Ok for recent Django