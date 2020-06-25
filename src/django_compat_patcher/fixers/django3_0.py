from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_30_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="3.0",
    fixer_applied_from_version="3.0",
)


@django1_30_bc_fixer()
def fix_deletion_utils_six(utils):
    """Preserve the vendored copy of "six" compatibility utility, in django.utils"""
    import six
    utils.inject_module("django.utils.six", six)

