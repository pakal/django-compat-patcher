from __future__ import absolute_import, print_function, unicode_literals

import warnings
from functools import partial

from ..registry import register_compatibility_fixer
from ..deprecation import *


# for backward-compatibility fixers
django19_bc_fixer = partial(register_compatibility_fixer,
                            fixer_family="django19",
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
        utils.emit_warning('`request.REQUEST` is deprecated, use `request.GET` or '
                       '`request.POST` instead.', RemovedInDjango19Warning, 2)
        if not hasattr(self, '_request'):
            self._request = datastructures.MergeDict(self.POST, self.GET)
        return self._request

    utils.inject_method(WSGIRequest, "_get_request", _get_request_compat)
    utils.inject_attribute(WSGIRequest, "REQUEST", property(_get_request_compat))

@django19_bc_fixer()
def keep_modeladmin_get_formsets(utils):
    from django.contrib.admin import ModelAdmin

    def _get_formsets_compat(self, request, obj):
        """
        Helper function that exists to allow the deprecation warning to be
        executed while this function continues to return a generator.
        """
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)

    def get_formsets_compat(self, request, obj=None):
        warnings.warn(
            "ModelAdmin.get_formsets() is deprecated Use ModelAdmin.get_formsets_with_inlines() instead.",
            RemovedInDjango19Warning, stacklevel=2
        )
        return self._get_formsets(request, obj)

    utils.inject_method(ModelAdmin, "_get_formsets", _get_formsets_compat)
    utils.inject_method(ModelAdmin, "get_formsets", get_formsets_compat)


@django19_bc_fixer()
def keep_utils_dictconfig(utils):
    from django import utils as dj_utils
    from ..removed.django19 import utils_dictconfig
    utils.inject_attribute(dj_utils, "dictconfig", utils_dictconfig)


@django19_bc_fixer()
def keep_utils_importlib(utils):
    from django import utils as dj_utils
    from ..removed.django19 import utils_importlib
    utils.inject_attribute(dj_utils, "importlib", utils_importlib)


@django19_bc_fixer()
def keep_utils_tzinfo(utils):
    from django import utils as dj_utils
    from ..removed.django19 import utils_tzinfo
    utils.inject_attribute(dj_utils, "tzinfo", utils_tzinfo)


@django19_bc_fixer()
def keep_utils_unittest(utils):
    from django import utils as dj_utils
    from ..removed.django19 import utils_unittest
    utils.inject_attribute(dj_utils, "unittest", utils_unittest)

