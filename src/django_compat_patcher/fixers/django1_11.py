from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_11_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="1.11",
    fixer_applied_from_version="1.11",
)


@register_django_compatibility_fixer(
    fixer_reference_version="1.11", fixer_applied_upto_version="1.11"
)
def fix_incoming_test_utils_setup_test_environment_signature_change(utils):
    """
    Set a forward compatibility wrapper for setup_test_environment() which takes a "debug" argument later.
    """
    import inspect
    from django.test import utils as django_utils

    original_setup_test_environment = django_utils.setup_test_environment

    # Sanity check
    argspec = inspect.getargspec(original_setup_test_environment)
    assert not argspec.args, argspec

    def setup_test_environment(debug=None):
        return original_setup_test_environment()  # No params

    utils.inject_callable(django_utils, "setup_test_environment", setup_test_environment)


@django1_11_bc_fixer()
def fix_behaviour_widget_build_attrs(utils):
    """
    Preserve compatibility with the old signature of Widget.build_attrs(): extra_attrs=None, **kwargs.
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