from __future__ import absolute_import, print_function, unicode_literals

import warnings
from functools import partial

from ..deprecation import *
from ..registry import register_compatibility_fixer

# for backward-compatibility fixers
django1_10_bc_fixer = partial(register_compatibility_fixer,
                             fixer_family="django1.10",
                             fixer_applied_from_django="1.10")



@django1_10_bc_fixer()
def fix_deletion_templatetags_future(utils):
    """
    Preserve the "future" templatetags library, with its improved `firstof` and `cycle` tags.
    """
    import django.templatetags
    from ..django_legacy.django1_10.templatetags import future
    utils.inject_module("django.templatetags.future", future)
    utils.inject_attribute(django.templatetags, "future", future)
