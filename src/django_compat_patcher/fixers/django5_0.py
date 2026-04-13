from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_50_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="5.0",
    fixer_applied_from_version="5.0",
)


@django1_50_bc_fixer()
def fix_deletion_utils_baseconv(utils):
    """Preserve django.utils.baseconv module, removed in Django 5.0"""
    from django_compat_patcher.django_legacy.django5_0 import utils__baseconv
    import django.utils
    utils.inject_module("django.utils.baseconv", utils__baseconv)
    utils.inject_attribute(django.utils, "baseconv", utils__baseconv)


@django1_50_bc_fixer()
def fix_deletion_utils_datetime_safe(utils):
    """Preserve django.utils.datetime_safe module, removed in Django 5.0"""
    from django_compat_patcher.django_legacy.django5_0 import utils__datetime_safe
    import django.utils
    utils.inject_module("django.utils.datetime_safe", utils__datetime_safe)
    utils.inject_attribute(django.utils, "datetime_safe", utils__datetime_safe)


@django1_50_bc_fixer()
def fix_deletion_utils_timezone_utc(utils):
    """Restore django.utils.timezone.utc as an alias for datetime.timezone.utc, removed in Django 5.0"""
    import datetime as dt_module
    from django.utils import timezone
    utils.inject_attribute(timezone, "utc", dt_module.timezone.utc)


@django1_50_bc_fixer()
def fix_behaviour_utils_functional_cached_property_name_argument(utils):
    """Preserve the deprecated 'name' argument of django.utils.functional.cached_property, removed in Django 5.0"""
    from django.utils.functional import cached_property
    original_init = cached_property.__init__

    def patched_init(self, func, name=None):
        if name is not None:
            warnings.warn(
                "The name argument is deprecated as it's unnecessary as of "
                "Python 3.6.",
                RemovedInDjango50Warning,
                stacklevel=2,
            )
        original_init(self, func)

    utils.inject_callable(cached_property, "__init__", patched_init)


@django1_50_bc_fixer()
def fix_deletion_utils_timezone_make_aware_is_dst(utils):
    """Restore the is_dst argument to make_aware(), TruncBase.__init__(), and QuerySet.datetimes(), removed in Django 5.0 (it has no effect with zoneinfo time zones)."""
    _SENTINEL = object()

    # --- make_aware ---
    from django.utils import timezone as tz_module
    _orig_make_aware = tz_module.make_aware

    def patched_make_aware(value, timezone=None, is_dst=_SENTINEL):
        if is_dst is not _SENTINEL:
            warnings.warn(
                "The is_dst argument to make_aware() is deprecated and has no effect "
                "since pytz support was removed in Django 5.0.",
                RemovedInDjango50Warning,
                stacklevel=2,
            )
        return _orig_make_aware(value, timezone)

    utils.inject_callable(tz_module, "make_aware", patched_make_aware)

    # --- TruncBase (covers TruncYear, TruncMonth, TruncDay, TruncHour, etc.) ---
    from django.db.models.functions.datetime import TruncBase
    _orig_trunc_init = TruncBase.__init__

    def patched_trunc_init(self, expression, output_field=None, tzinfo=None, is_dst=_SENTINEL, **extra):
        if is_dst is not _SENTINEL:
            warnings.warn(
                "The is_dst argument to Trunc functions is deprecated and has no effect "
                "since pytz support was removed in Django 5.0.",
                RemovedInDjango50Warning,
                stacklevel=2,
            )
        _orig_trunc_init(self, expression, output_field=output_field, tzinfo=tzinfo, **extra)

    utils.inject_callable(TruncBase, "__init__", patched_trunc_init)

    # --- QuerySet.datetimes ---
    from django.db.models.query import QuerySet
    _orig_datetimes = QuerySet.datetimes

    def patched_datetimes(self, field_name, kind, order="ASC", tzinfo=None, is_dst=_SENTINEL):
        if is_dst is not _SENTINEL:
            warnings.warn(
                "The is_dst argument to QuerySet.datetimes() is deprecated and has no effect "
                "since pytz support was removed in Django 5.0.",
                RemovedInDjango50Warning,
                stacklevel=2,
            )
        return _orig_datetimes(self, field_name, kind, order=order, tzinfo=tzinfo)

    utils.inject_callable(QuerySet, "datetimes", patched_datetimes)


@django1_50_bc_fixer()
def fix_deletion_conf_settings_USE_L10N(utils):
    """Preserve the USE_L10N setting, removed in Django 5.0 (localization is now always enabled)"""
    from django.conf import settings
    from django.utils import formats

    _orig_get_format = formats.get_format

    def patched_get_format(format_type, lang=None, use_l10n=None):
        if use_l10n is None:
            try:
                use_l10n = settings.USE_L10N
                warnings.warn(
                    "The USE_L10N setting is deprecated. Localization is always enabled "
                    "in Django 5.0+. Remove USE_L10N from your settings.",
                    RemovedInDjango50Warning,
                )
            except AttributeError:
                pass  # USE_L10N not in user settings; use Django default (always True)
        return _orig_get_format(format_type, lang=lang, use_l10n=use_l10n)

    utils.inject_callable(formats, "get_format", patched_get_format)


@django1_50_bc_fixer()
def fix_deletion_forms_BaseForm_html_output(utils):
    """Restore the undocumented BaseForm._html_output() method, removed in Django 5.0"""
    from django.forms.forms import BaseForm
    from django.utils.html import conditional_escape
    from django.utils.safestring import mark_safe
    from django.utils.translation import gettext as _

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        """Render form fields as HTML rows. Private API restored by django-compat-patcher."""
        warnings.warn(
            "BaseForm._html_output() was removed in Django 5.0. "
            "Override render() or use a custom form renderer instead.",
            RemovedInDjango50Warning,
            stacklevel=2,
        )
        top_errors = self.non_field_errors()
        output, hidden_fields = [], []

        for name, field in self.fields.items():
            bf = self[name]
            bf_errors = self.error_class(bf.errors)
            if bf.is_hidden:
                if bf_errors:
                    top_errors += [
                        _("(Hidden field %(name)s) %(error)s") % {"name": name, "error": str(e)}
                        for e in bf_errors
                    ]
                hidden_fields.append(str(bf))
            else:
                css_classes = bf.css_classes()
                html_class_attr = ' class="%s"' % css_classes if css_classes else ""
                if errors_on_separate_row and bf_errors:
                    output.append(error_row % str(bf_errors))
                label = conditional_escape(bf.label) if bf.label else ""
                label = bf.label_tag(label) or ""
                help_text = help_text_html % field.help_text if field.help_text else ""
                output.append(
                    normal_row % {
                        "errors": bf_errors,
                        "label": label,
                        "field": bf,
                        "help_text": help_text,
                        "html_class_attr": html_class_attr,
                        "css_classes": css_classes,
                        "field_name": bf.html_name,
                    }
                )

        if top_errors:
            output.insert(0, error_row % top_errors)

        if hidden_fields:
            str_hidden = "".join(hidden_fields)
            if output:
                last_row = output[-1]
                if last_row.endswith(row_ender):
                    output[-1] = last_row[: -len(row_ender)] + str_hidden + row_ender
                else:
                    output.append(str_hidden)
            else:
                output.append(str_hidden)

        return mark_safe("\n".join(output))

    utils.inject_callable(BaseForm, "_html_output", _html_output)
