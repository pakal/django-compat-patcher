from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_6_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="1.6",
    fixer_applied_from_version="1.6",
)


@django1_6_bc_fixer()
def fix_deletion_http_request_HttpRequest_raw_post_data(utils):
    """
    Preserve the request.raw_post_data alias for request.body.
    """
    from django.http.request import HttpRequest

    @property
    def raw_post_data(self):
        utils.emit_warning(
            "HttpRequest.raw_post_data has been deprecated. Use HttpRequest.body instead.",
            RemovedInDjango16Warning,
        )
        return self.body

    utils.inject_attribute(HttpRequest, "raw_post_data", raw_post_data)
