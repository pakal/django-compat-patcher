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
def fix_deletion_utils_datastructures_SortedDict(utils):
    """
    Preserve the SortedDict util datastructure
    """
    from django.utils import datastructures as dj_datastructures
    from ..removed.django19 import datastructures
    utils.inject_attribute(dj_datastructures, "SortedDict", datastructures.SortedDict)


@django19_bc_fixer()
def fix_deletion_utils_dictconfig(utils):
    """
    Preserve the dictconfig util file
    """
    from django import utils as dj_utils
    from ..removed.django19 import utils_dictconfig
    utils.inject_attribute(dj_utils, "dictconfig", utils_dictconfig)


@django19_bc_fixer()
def fix_deletion_utils_importlib(utils):
    """
    Preserve the importlib util file
    """
    from django import utils as dj_utils
    from ..removed.django19 import utils_importlib
    utils.inject_attribute(dj_utils, "importlib", utils_importlib)


@django19_bc_fixer()
def fix_deletion_utils_tzinfo(utils):
    """
    Preserve the tzinfo util file
    """
    from django import utils as dj_utils
    from ..removed.django19 import utils_tzinfo
    utils.inject_attribute(dj_utils, "tzinfo", utils_tzinfo)


@django19_bc_fixer()
def fix_deletion_utils_unittest(utils):
    """
    Preserve the unittest util file
    """
    from django import utils as dj_utils
    from ..removed.django19 import utils_unittest
    utils.inject_attribute(dj_utils, "unittest", utils_unittest)


@django19_bc_fixer()
def fix_deletion_request_post_get_mergedict(utils):  # TODO rename to fit new guidelines
    "Preserve the `request.REQUEST` attribute, merging parameters from GET "
    "and POST (the latter has precedence)."

    from django.core.handlers.wsgi import WSGIRequest
    from django.utils.datastructures import MergeDict  # Depends on a previous fixer
    def _get_request_compat(self):
        utils.emit_warning('`request.REQUEST` is deprecated, use `request.GET` or '
                           '`request.POST` instead.', RemovedInDjango19Warning, 2)
        if not hasattr(self, '_request'):
            self._request = MergeDict(self.POST, self.GET)
        return self._request

    utils.inject_method(WSGIRequest, "_get_request", _get_request_compat)
    utils.inject_attribute(WSGIRequest, "REQUEST", property(_get_request_compat))


@django19_bc_fixer()
def fix_deletion_contrib_admin_ModelAdmin_get_formsets(utils):
    """
    Preserve the get_formsets method of ModelAdmin
    """
    from django.contrib.admin import ModelAdmin

    def _get_formsets_compat(self, request, obj):
        """
        Helper function that exists to allow the deprecation warning to be
        executed while this function continues to return a generator.
        """
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)

    def get_formsets_compat(self, request, obj=None):
        warnings.warn(  # TODO change all warnings.warn to emit_warning util
            "ModelAdmin.get_formsets() is deprecated Use ModelAdmin.get_formsets_with_inlines() instead.",
            RemovedInDjango19Warning, stacklevel=2
        )
        return self._get_formsets(request, obj)

    utils.inject_method(ModelAdmin, "_get_formsets", _get_formsets_compat)
    utils.inject_method(ModelAdmin, "get_formsets", get_formsets_compat)


@django19_bc_fixer()
def fix_deletion_templatetags_future_url(utils):  # TODO rename to fit new guidelines
    "Preserve the `url` tag in the `future` templatetags library."
    from django.template import defaulttags
    from django.templatetags import future
    new_tag = utils.inject_function_alias(defaulttags, "url",
                                          future, "url")
    future.register.tag(new_tag)


def keep_templatetags_future_ssi(utils):
    "Preserve the `ssi` tag in the `future` templatetags library."
    from django.template import defaulttags
    from django.templatetags import future
    new_tag = utils.inject_function_alias(defaulttags, "ssi",
                                          future, "ssi")
    future.register.tag(new_tag)


@django19_bc_fixer()
def fix_deletion_forms_fields_IPAddressField(utils):
    """Preserve the IPAddressField model field, now superseded by GenericIPAddressField"""
    import django.forms.fields
    from django.forms.fields import CharField
    from django.core import validators

    class IPAddressFieldCompat(CharField):
        default_validators = [validators.validate_ipv4_address]

        def __init__(self, *args, **kwargs):
            utils.emit_warning("IPAddressField has been deprecated. Use GenericIPAddressField instead.",
                                RemovedInDjango19Warning)
            super(IPAddressFieldCompat, self).__init__(*args, **kwargs)

        def to_python(self, value):
            if value in self.empty_values:
                return ''
            return value.strip()

    utils.inject_class(django.forms.fields, "IPAddressField", IPAddressFieldCompat)

    from django.db.models.fields import IPAddressField as OriginalIPAddressField

    def formfield_compat(self, **kwargs):
        defaults = {'form_class': django.forms.fields.IPAddressField}
        defaults.update(kwargs)
        return super(OriginalIPAddressField, self).formfield(**defaults)

    utils.inject_attribute(OriginalIPAddressField, "formfield", formfield_compat)

