from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_7_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="1.7",
    fixer_applied_from_version="1.7",
)
