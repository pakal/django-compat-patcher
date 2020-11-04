from __future__ import absolute_import, print_function, unicode_literals

import _test_utilities


def test_fix_deletion_utils_translation_string_concat():
    from django.utils.translation import string_concat

    assert string_concat("a", "b", "c") == "abc"


def test_fix_behaviour_widget_render_forced_renderer():

    from django import forms
    try:
        from django.forms import BoundField
    except ImportError:
        from django.forms.forms import BoundField  # not propagated in django1.8

    class MyForm(forms.Form):
        my_field = forms.CharField(label="My field", max_length=100)

    class OldWidget(forms.Widget):
        def render(self, name, value, attrs=None):  # no "renderer" parameter expected
            return "All is ok 1"

    class NewWidget(forms.Widget):
        def render(self, name, value, attrs=None, renderer=None):
            return "All is ok 2"

    form = MyForm()

    my_field = form["my_field"]
    assert isinstance(my_field, BoundField)

    res = my_field.as_widget(OldWidget())
    assert res == "All is ok 1"

    res = my_field.as_widget(NewWidget())
    assert res == "All is ok 2"

    res = my_field.as_widget()  # implicit CharField widget
    assert "<input " in res
