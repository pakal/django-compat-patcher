from __future__ import absolute_import, print_function, unicode_literals

import warnings
from functools import partial

from ..deprecation import *
from ..registry import register_compatibility_fixer


# for backward-compatibility fixers
django1_8_bc_fixer = partial(register_compatibility_fixer,
                             fixer_reference_version="1.8",
                             fixer_applied_from_django="1.8")


