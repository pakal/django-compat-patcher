from __future__ import absolute_import, print_function, unicode_literals

import warnings
from functools import partial

from ..deprecation import *
from ..registry import register_compatibility_fixer

# for backward-compatibility fixers
django19_bc_fixer = partial(register_compatibility_fixer,
                            fixer_family="django19",
                            fixer_applied_from_django="1.9")



@django19_bc_fixer()
def fix_deletion_utils_datastructures_MergeDict(utils):
    """
    Preserve the MergeDict util datastructure
    """
    from django.utils import datastructures as dj_datastructures
    from ..django_legacy.django19.datastructures import MergeDict as MergeDictCompat
    utils.inject_class(dj_datastructures, "MergeDict", MergeDictCompat)


@django19_bc_fixer()
def fix_deletion_utils_datastructures_SortedDict(utils):
    """
    Preserve the SortedDict util datastructure
    """
    from django.utils import datastructures as dj_datastructures
    from ..django_legacy.django19.datastructures import SortedDict as SortedDictCompat
    utils.inject_class(dj_datastructures, "SortedDict", SortedDictCompat)


@django19_bc_fixer()
def fix_deletion_utils_dictconfig(utils):
    """
    Preserve the dictconfig util file
    """
    from django_compat_patcher.django_legacy.django19.utils import dictconfig
    utils.inject_module("django.utils.dictconfig", dictconfig)


@django19_bc_fixer()
def fix_deletion_utils_importlib(utils):
    """
    Preserve the importlib util file
    """
    from django_compat_patcher.django_legacy.django19.utils import importlib
    utils.inject_module("django.utils.importlib", importlib)


@django19_bc_fixer()
def fix_deletion_utils_tzinfo(utils):
    """
    Preserve the tzinfo util file
    """
    from django_compat_patcher.django_legacy.django19.utils import tzinfo
    utils.inject_module("django.utils.tzinfo", tzinfo)


@django19_bc_fixer()
def fix_deletion_utils_unittest(utils):
    """
    Preserve the unittest util file
    """
    from django_compat_patcher.django_legacy.django19.utils import unittest
    utils.inject_module("django.utils.unittest", unittest)


@django19_bc_fixer()
def fix_deletion_core_handlers_wsgi_WSGIRequest_REQUEST(utils):
    "Preserve the `request.REQUEST` attribute, merging parameters from GET "
    "and POST (the latter has precedence)."

    from django.core.handlers.wsgi import WSGIRequest
    from django.utils.datastructures import MergeDict  # Depends on a previous fixer
    def _get_request(self):
        utils.emit_warning('`request.REQUEST` is deprecated, use `request.GET` or '
                           '`request.POST` instead.', RemovedInDjango19Warning, 2)
        if not hasattr(self, '_request'):
            self._request = MergeDict(self.POST, self.GET)
        return self._request

    utils.inject_callable(WSGIRequest, "_get_request", _get_request)
    utils.inject_attribute(WSGIRequest, "REQUEST", property(_get_request))


@django19_bc_fixer()
def fix_deletion_contrib_admin_ModelAdmin_get_formsets(utils):
    """
    Preserve the get_formsets method of ModelAdmin
    """
    from django.contrib.admin import ModelAdmin

    def _get_formsets(self, request, obj):
        """
        Helper function that exists to allow the deprecation warning to be
        executed while this function continues to return a generator.
        """
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)

    def get_formsets(self, request, obj=None):
        warnings.warn(  # TODO change all warnings.warn to emit_warning util
            "ModelAdmin.get_formsets() is deprecated Use ModelAdmin.get_formsets_with_inlines() instead.",
            RemovedInDjango19Warning, stacklevel=2
        )
        return self._get_formsets(request, obj)

    utils.inject_callable(ModelAdmin, "_get_formsets", _get_formsets)
    utils.inject_callable(ModelAdmin, "get_formsets", get_formsets)


@django19_bc_fixer()
def fix_deletion_templatetags_future_url(utils):  # TODO rename to fit new guidelines
    "Preserve the `url` tag in the `future` templatetags library."
    from django.template import defaulttags
    from django.templatetags import future
    new_tag = utils.inject_function_alias(defaulttags, "url",
                                          future, "url")
    future.register.tag(new_tag)


@django19_bc_fixer()
def fix_deletion_templatetags_future_ssi(utils):
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

    class IPAddressField(CharField):
        default_validators = [validators.validate_ipv4_address]

        def __init__(self, *args, **kwargs):
            utils.emit_warning("IPAddressField has been deprecated. Use GenericIPAddressField instead.",
                                RemovedInDjango19Warning)
            super(IPAddressField, self).__init__(*args, **kwargs)

        def to_python(self, value):
            if value in self.empty_values:
                return ''
            return value.strip()

    utils.inject_class(django.forms.fields, "IPAddressField", IPAddressField)

    from django.db.models.fields import IPAddressField as OriginalIPAddressField

    def formfield(self, **kwargs):
        defaults = {'form_class': django.forms.fields.IPAddressField}
        defaults.update(kwargs)
        return super(OriginalIPAddressField, self).formfield(**defaults)

    utils.inject_callable(OriginalIPAddressField, "formfield", formfield)

@django19_bc_fixer()
def fix_deletion_django_core_management_base_AppCommand_handle_app(utils):
    """Preserve the fallback to AppCommand.handle_app() method in django management commands."""

    from django.core.management.base import CommandError, AppCommand

    def handle_app_config(self, app_config, **options):
        """
        Perform the command's actions for app_config, an AppConfig instance
        corresponding to an application label given on the command line.
        """
        try:
            # During the deprecation path, keep delegating to handle_app if
            # handle_app_config isn't implemented in a subclass.
            handle_app = self.handle_app
        except AttributeError:
            # Keep only this exception when the deprecation completes.
            raise NotImplementedError(
                "Subclasses of AppCommand must provide "
                "a handle_app_config() method.")
        else:
            utils.emit_warning(
                "AppCommand.handle_app() is superseded by "
                "AppCommand.handle_app_config().",
                RemovedInDjango19Warning, stacklevel=2)
            if app_config.models_module is None:
                raise CommandError(
                    "AppCommand cannot handle app '%s' in legacy mode "
                    "because it doesn't have a models module."
                    % app_config.label)
            return handle_app(app_config.models_module, **options)

    utils.inject_attribute(AppCommand, "handle_app_config", handle_app_config)
