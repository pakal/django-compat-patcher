from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_11_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="1.11",
    fixer_applied_from_version="1.11",
)


@django1_11_bc_fixer()
def fix_behaviour_widget_build_attrs(utils):
    """
    Preserve the "future" templatetags library, with its improved `firstof` and `cycle` tags.
    """
    from django.forms.widgets import Widget

    # original_build_attrs = Widget.build_attrs  UNUSED

    def build_attrs(self, base_attrs=None, extra_attrs=None, **kwargs):
        if kwargs:
            # old version
            assert not extra_attrs
            attrs = dict(self.attrs, **kwargs)
            if base_attrs:  # actually the old "extra_attrs"
                attrs.update(base_attrs)
        else:
            # new version
            attrs = base_attrs.copy()
            if extra_attrs is not None:
                attrs.update(extra_attrs)
        return attrs

    utils.inject_callable(Widget, "build_attrs", build_attrs)


""" CHANGED UTILITY:

def build_attrs(self, extra_attrs=None, **kwargs):
    "Helper function for building an attribute dictionary."
    attrs = dict(self.attrs, **kwargs)
    if extra_attrs:
        attrs.update(extra_attrs)
    return attrs

def build_attrs(self, base_attrs, extra_attrs=None):
    "Helper function for building an attribute dictionary."
    attrs = base_attrs.copy()
    if extra_attrs is not None:
        attrs.update(extra_attrs)
    return attrs
"""
