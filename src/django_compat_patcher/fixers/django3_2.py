from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_31_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="3.2",
    fixer_applied_from_version="3.2",
)


@django1_31_bc_fixer()
def fix_deletion_http_response_HttpResponseBase_private_headers(utils):
    """Preserve HttpResponseBase._headers as an alias to the new HttpResponseBase.headers"""
    from django.http.response import HttpResponseBase

    @property
    def _headers(self):
        return self.headers._store  # Maps lower_case to (normal_case, value)

    utils.inject_attribute(HttpResponseBase, "_headers", _headers)
