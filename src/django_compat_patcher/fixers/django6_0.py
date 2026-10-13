from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_60_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="6.0",
    fixer_applied_from_version="6.0",
)


@django1_60_bc_fixer()
def fix_behaviour_db_models_Model_save_positional_args(utils):
    """Restore support for positional arguments to Model.save() and Model.asave(), removed in Django 6.0"""
    from django.db.models import Model

    _orig_save = Model.save
    _orig_asave = Model.asave

    _POSITIONAL_ARG_NAMES = ("force_insert", "force_update", "using", "update_fields")

    def _merge_positional_args(args, kwargs):
        if args:
            warnings.warn(
                "Passing positional arguments to Model.save() and Model.asave() is deprecated.",
                RemovedInDjango60Warning,
                stacklevel=4,
            )
            for name, value in zip(_POSITIONAL_ARG_NAMES, args):
                kwargs.setdefault(name, value)
        return kwargs

    def patched_save(self, *args, **kwargs):
        kwargs = _merge_positional_args(args, kwargs)
        return _orig_save(self, **kwargs)

    patched_save.alters_data = True

    async def patched_asave(self, *args, **kwargs):
        kwargs = _merge_positional_args(args, kwargs)
        return await _orig_asave(self, **kwargs)

    patched_asave.alters_data = True

    utils.inject_callable(Model, "save", patched_save)
    utils.inject_callable(Model, "asave", patched_asave)


@django1_60_bc_fixer()
def fix_deletion_db_models_constraints_CheckConstraint_check_kwarg(utils):
    """Restore the check= keyword argument of CheckConstraint, superseded by condition= and removed in Django 6.0"""
    from django.db.models import CheckConstraint

    _orig_init = CheckConstraint.__init__

    def patched_init(self, *args, condition=None, check=None, **kwargs):
        if check is not None:
            warnings.warn(
                "CheckConstraint.check is deprecated in favor of condition.",
                RemovedInDjango60Warning,
                stacklevel=2,
            )
            if condition is None:
                condition = check
        _orig_init(self, *args, condition=condition, **kwargs)

    utils.inject_callable(CheckConstraint, "__init__", patched_init)


@django1_60_bc_fixer()
def fix_deletion_utils_html_format_html_without_args(utils):
    """Restore support for calling format_html() without passing args or kwargs, removed in Django 6.0"""
    from django.utils import html
    from django.utils.safestring import mark_safe

    _orig_format_html = html.format_html

    def patched_format_html(format_string, *args, **kwargs):
        if not args and not kwargs:
            warnings.warn(
                "Calling format_html() without passing args or kwargs is deprecated.",
                RemovedInDjango60Warning,
                stacklevel=2,
            )
            return mark_safe(format_string.format())
        return _orig_format_html(format_string, *args, **kwargs)

    utils.inject_callable(html, "format_html", patched_format_html)


@django1_60_bc_fixer()
def fix_behaviour_contrib_admin_ChangeList_get_filters_lookup_allowed_request_arg(utils):
    """Restore support for ModelAdmin.lookup_allowed() overrides not accepting a request
    argument, by reinstating the signature-introspection shim of ChangeList.get_filters()
    that was removed in Django 6.0"""
    from django.contrib.admin.views import main as main_module
    from django.utils.inspect import func_supports_parameter

    ChangeList = main_module.ChangeList

    def patched_get_filters(self, request):
        lookup_params = self.get_filters_params()
        may_have_duplicates = False
        has_active_filters = False

        supports_request = func_supports_parameter(self.model_admin.lookup_allowed, "request")
        if not supports_request:
            warnings.warn(
                "`request` must be added to the signature of "
                "%s.lookup_allowed()." % self.model_admin.__class__.__qualname__,
                RemovedInDjango60Warning,
            )
        for key, value_list in lookup_params.items():
            for value in value_list:
                params = (key, value, request) if supports_request else (key, value)
                if not self.model_admin.lookup_allowed(*params):
                    raise main_module.DisallowedModelAdminLookup(
                        "Filtering by %s not allowed" % key
                    )

        filter_specs = []
        for list_filter in self.list_filter:
            lookup_params_count = len(lookup_params)
            if callable(list_filter):
                # This is simply a custom list filter class.
                spec = list_filter(request, lookup_params, self.model, self.model_admin)
            else:
                field_path = None
                if isinstance(list_filter, (tuple, list)):
                    # This is a custom FieldListFilter class for a given field.
                    field, field_list_filter_class = list_filter
                else:
                    # This is simply a field name, so use the default
                    # FieldListFilter class that has been registered for the
                    # type of the given field.
                    field, field_list_filter_class = list_filter, main_module.FieldListFilter.create
                if not isinstance(field, main_module.Field):
                    field_path = field
                    field = main_module.get_fields_from_path(self.model, field_path)[-1]

                spec = field_list_filter_class(
                    field,
                    request,
                    lookup_params,
                    self.model,
                    self.model_admin,
                    field_path=field_path,
                )
                # field_list_filter_class removes any lookup_params it
                # processes. If that happened, check if duplicates should be
                # removed.
                if lookup_params_count > len(lookup_params):
                    may_have_duplicates |= main_module.lookup_spawns_duplicates(
                        self.lookup_opts,
                        field_path,
                    )
            if spec and spec.has_output():
                filter_specs.append(spec)
                if lookup_params_count > len(lookup_params):
                    has_active_filters = True

        if self.date_hierarchy:
            # Create bounded lookup parameters so that the query is more
            # efficient.
            from datetime import datetime, timedelta

            year = lookup_params.pop("%s__year" % self.date_hierarchy, None)
            if year is not None:
                month = lookup_params.pop("%s__month" % self.date_hierarchy, None)
                day = lookup_params.pop("%s__day" % self.date_hierarchy, None)
                try:
                    from_date = datetime(
                        int(year[-1]),
                        int(month[-1] if month is not None else 1),
                        int(day[-1] if day is not None else 1),
                    )
                except ValueError as e:
                    raise main_module.IncorrectLookupParameters(e) from e
                if day:
                    to_date = from_date + timedelta(days=1)
                elif month:
                    # In this branch, from_date will always be the first of a
                    # month, so advancing 32 days gives the next month.
                    to_date = (from_date + timedelta(days=32)).replace(day=1)
                else:
                    to_date = from_date.replace(year=from_date.year + 1)
                if main_module.settings.USE_TZ:
                    from_date = main_module.make_aware(from_date)
                    to_date = main_module.make_aware(to_date)
                lookup_params.update(
                    {
                        "%s__gte" % self.date_hierarchy: [from_date],
                        "%s__lt" % self.date_hierarchy: [to_date],
                    }
                )

        # At this point, all the parameters used by the various ListFilters
        # have been removed from lookup_params, which now only contains other
        # parameters passed via the query string. We now loop through the
        # remaining parameters both to ensure that all the parameters are valid
        # fields and to determine if at least one of them spawns duplicates. If
        # the lookup parameters aren't real fields, then bail out.
        try:
            for key, value in lookup_params.items():
                lookup_params[key] = main_module.prepare_lookup_value(key, value)
                may_have_duplicates |= main_module.lookup_spawns_duplicates(self.lookup_opts, key)
            return (
                filter_specs,
                bool(filter_specs),
                lookup_params,
                may_have_duplicates,
                has_active_filters,
            )
        except main_module.FieldDoesNotExist as e:
            raise main_module.IncorrectLookupParameters(e) from e

    utils.inject_callable(ChangeList, "get_filters", patched_get_filters)


@django1_60_bc_fixer()
def fix_deletion_db_models_enums_ChoicesMeta(utils):
    """Restore the ChoicesMeta alias to django.db.models.enums.ChoicesType, removed in Django 6.0"""
    from django.db.models import enums

    utils.inject_class(enums, "ChoicesMeta", enums.ChoicesType)
