from __future__ import absolute_import, print_function, unicode_literals

import os, sys
import pytest

import _test_utilities


def test_fix_behaviour_widget_build_attrs():
    from django.forms.widgets import Select
    select = Select({'someattr': 'somevalue'})

    attrs = select.build_attrs({'other': 'yes'}, multiple="multiple")  # old behavior
    assert attrs == {'someattr': 'somevalue', 'multiple': 'multiple', 'other': 'yes'}

    try:
        attrs = select.build_attrs({'this': 'no'}, {'other': 'yes'})   # new behavior
        assert attrs == {'this': 'no', 'other': 'yes'}
    except TypeError:  # old (unpatched) signature, with only 2 positional arguments including "self"
        attrs = select.build_attrs(extra_attrs={'this': 'no'})
        assert attrs == {'someattr': 'somevalue', 'this': 'no'}
    else:
        attrs = select.build_attrs({'this': 'no'})   # new behavior
        assert attrs == {'this': 'no'}  # no self.attrs added
