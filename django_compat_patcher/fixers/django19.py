from __future__ import absolute_import, print_function, unicode_literals

import warnings
from functools import partial

from ..registry import register_compatibility_fixer
from ..deprecation import *


django19_bc_fixer = partial(register_compatibility_fixer,
                            fixer_applied_from_django="1.9")


@django19_bc_fixer()
def keep_templatetags_future_url(utils):
    "Preserve the `url` tag in the `future` templatetags library."

    from django.template import defaulttags
    from django.templatetags import future
    new_tag = utils.inject_function_alias(defaulttags, "url",
                                          future, "url")
    future.register.tag(new_tag)


@django19_bc_fixer()
def keep_request_post_get_mergedict(utils):
    "Preserve the `request.REQUEST` attribute, merging parameters from GET "
    "and POST (the latter has precedence)."

    from django.core.handlers.wsgi import WSGIRequest
    from .. import datastructures
    def _get_request_compat(self):
        utils.warn('`request.REQUEST` is deprecated, use `request.GET` or '
                       '`request.POST` instead.', RemovedInDjango19Warning, 2)
        if not hasattr(self, '_request'):
            self._request = datastructures.MergeDict(self.POST, self.GET)
        return self._request

    utils.inject_method(WSGIRequest, "_get_request", _get_request_compat)
    utils.inject_attribute(WSGIRequest, "REQUEST", property(_get_request_compat))
