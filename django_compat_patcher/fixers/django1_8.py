from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_8_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="1.8",
    fixer_applied_from_version="1.8",
)


@django1_8_bc_fixer()
def fix_outsourcing_contrib_comments(utils):
    """
    Keep 'django.contrib.comments' as an import alias for the now external package
    'django_comments' (django-contrib-comments on pypi) ; the latter must be installed separately.
    """
    utils.inject_import_alias(
        alias_name="django.contrib.comments", real_name="django_comments"
    )
