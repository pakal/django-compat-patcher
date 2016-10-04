
import warnings
from ..registry import register_backwards_compatibility_fixer

from ..deprecation import *


@register_backwards_compatibility_fixer()
def keep_templatetags_future_url(utils):
    from django.template import defaulttags
    from django.templatetags import future
    new_tag = utils.inject_function_alias(defaulttags, "url",
                                          future, "url")
    future.register.tag(new_tag)


@register_backwards_compatibility_fixer()
def keep_request_post_get_mergedict(utils):
    from django.core.handlers.wsgi import WSGIRequest
    from .. import datastructures
    def _get_request_compat(self):
        warnings.warn('`request.REQUEST` is deprecated, use `request.GET` or '
                      '`request.POST` instead.', RemovedInDjango19Warning, 2)
        if not hasattr(self, '_request'):
            self._request = datastructures.MergeDict(self.POST, self.GET)
        return self._request

    WSGIRequest._get_request = _get_request_compat
    WSGIRequest.REQUEST = property(_get_request_compat)
