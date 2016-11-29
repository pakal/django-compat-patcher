from __future__ import absolute_import, print_function, unicode_literals

import warnings
from functools import partial

from ..deprecation import *
from ..registry import register_compatibility_fixer


# for backward-compatibility fixers
django1_8_bc_fixer = partial(register_compatibility_fixer,
                             fixer_reference_version="1.8",
                             fixer_applied_from_django="1.8")



@django1_8_bc_fixer()
def fix_deletion_contrib_comments(utils):
    """
    Keep django.contrib.comments as alias for the now external package
    django_comments (django-contrib-comments on pypi).
    """
    utils.register_import_alias(alias_name="django.contrib.comments",
                                real_name="django_comments")
