from __future__ import absolute_import, print_function, unicode_literals

import warnings
from functools import partial

from ..deprecation import *
from ..registry import register_compatibility_fixer

# for backward-compatibility fixers
django16_bc_fixer = partial(register_compatibility_fixer,
                            fixer_family="django16",
                            fixer_applied_from_django="1.6")

@django16_bc_fixer()
def fix_deletion_http_request_HttpRequest_raw_post_data(utils):
    """
    Preserve the request.raw_post_data alias for request.body.
    """
    from django.http.request import HttpRequest
    @property
    def raw_post_data(self):
        utils.emit_warning('HttpRequest.raw_post_data has been deprecated. Use HttpRequest.body instead.', RemovedInDjango16Warning)
        return self.body
    utils.inject_attribute(HttpRequest, "raw_post_data", raw_post_data)
