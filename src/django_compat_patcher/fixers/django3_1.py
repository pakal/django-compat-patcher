from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_31_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="3.1",
    fixer_applied_from_version="3.1",
)

@django1_31_bc_fixer()
def fix_deletion_db_models_submodules_EmptyResultSet(utils):
    """Preserve compatibility imports of django.core.exceptions.EmptyResultSet in
    django.db.models.query, django.db.models.sql, and django.db.models.sql.datastructures
    """
    from django.core.exceptions import EmptyResultSet
    from django.db.models import query
    from django.db.models import sql
    from django.db.models.sql import datastructures

    utils.inject_class(query, "EmptyResultSet", EmptyResultSet)
    utils.inject_class(sql, "EmptyResultSet", EmptyResultSet)
    utils.inject_class(datastructures, "EmptyResultSet", EmptyResultSet)

    sql.__all__.append("EmptyResultSet")  # Preserve star import


@django1_31_bc_fixer()
def fix_deletion_db_models_fields_FieldDoesNotExist(utils):
    """
    Preserve compatibility import of django.core.exceptions.FieldDoesNotExist in django.db.models.fields
    """
    from django.core.exceptions import FieldDoesNotExist
    from django.db.models import fields

    utils.inject_class(fields, "FieldDoesNotExist", FieldDoesNotExist)
    fields.__all__.append("FieldDoesNotExist")  # Preserve star import


@django1_31_bc_fixer()
def fix_deletion_forms_forms_pretty_name_BoundField(utils):
    """
    Preserve the compatibility imports of django.forms.utils.pretty_name() and
    django.forms.boundfield.BoundField in django.forms.forms
    """
    from django.forms import forms

    from django.forms.boundfield import BoundField
    from django.forms.utils import pretty_name

    utils.inject_class(forms, "BoundField", BoundField)
    utils.inject_callable(forms, "pretty_name", pretty_name)


@django1_31_bc_fixer()
def fix_deletion_forms_fields_EMPTY_VALUES(utils):
    """
    Preserve the compatibility import of django.core.validators.EMPTY_VALUES in django.forms.fields
    """
    from django.core.validators import EMPTY_VALUES
    from django.forms import fields
    utils.inject_attribute(fields, "EMPTY_VALUES", EMPTY_VALUES)


@django1_31_bc_fixer()
def fix_deletion_template_base_Context_classes(utils):
    """
    Preserve the compatibility imports django.template.Context, django.template.RequestContext
    and django.template.ContextPopException
    """
    from django.template.context import (Context, RequestContext, ContextPopException)
    from django.template import base
    utils.inject_class(base, "Context", Context)
    utils.inject_class(base, "RequestContext", RequestContext)
    utils.inject_class(base, "ContextPopException", ContextPopException)


@django1_31_bc_fixer()
def fix_deletion_core_management_commands_runserver(utils):
    """
    Preserve the compatibility alias django.core.management.commands.runserver.BaseRunserverCommand
    """
    from django.core.management.commands import runserver
    utils.inject_class(runserver, "BaseRunserverCommand", runserver.Command)


@django1_31_bc_fixer()
def fix_deletion_utils_decorators_classproperty(utils):
    """
    Preserve django.utils.decorators.classproperty as alias of new django.utils.functional.classproperty
    """
    from django.utils.functional import classproperty
    from django.utils import decorators
    utils.inject_class(decorators, "classproperty", classproperty)


@django1_31_bc_fixer()
def fix_deletion_contrib_admin_ACTION_CHECKBOX_NAME(utils):
    """
    Preserve import of ACTION_CHECKBOX_NAME in django.contrib.admin
    """
    from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
    from django.contrib import admin

    utils.inject_attribute(admin, "ACTION_CHECKBOX_NAME", ACTION_CHECKBOX_NAME)
    admin.__all__.append("ACTION_CHECKBOX_NAME")


@django1_31_bc_fixer()
def fix_deletion_views_debug_ExceptionReporterFilter(utils):
    """
    Preserve undocumented ExceptionReporterFilter class
    """
    from django.views import debug as debug_module

    class ExceptionReporterFilter:
        """
        Base for all exception reporter filter classes. All overridable hooks
        contain lenient default behaviors.
        """

        def get_post_parameters(self, request):
            if request is None:
                return {}
            else:
                return request.POST

        def get_traceback_frame_variables(self, request, tb_frame):
            return list(tb_frame.f_locals.items())

    # Beware, it's not the parent of SafeExceptionReporterFilter anymore, but it shouldn't be a problem
    utils.inject_class(debug_module, "ExceptionReporterFilter", ExceptionReporterFilter)


@django1_31_bc_fixer()
def fix_deletion_contrib_postgres_forms_jsonb_InvalidJSONInput_JSONString(utils):
    """[UNSAFE] Preserve undocumented InvalidJSONInput and JSONString classes in django.contrib.postgres.forms.jsonb

    Requires psycopg2 to be installed.
    """

    from django.contrib.postgres.forms import jsonb
    from django.forms.fields import InvalidJSONInput, JSONString

    utils.inject_class(jsonb, "InvalidJSONInput", InvalidJSONInput)
    utils.inject_class(jsonb, "JSONString", JSONString)
    # We do not alter __all__ here, these were private utilities!


@django1_31_bc_fixer()
def fix_deletion_contrib_postgres_fields_jsonb_JsonAdapter(utils):
    """[UNSAFE] Preserve undocumented JsonAdapter class in django.contrib.postgres.fields.jsonb

    Requires psycopg2 to be installed.
    """
    from django.contrib.postgres.fields import jsonb

    import json
    from psycopg2.extras import Json

    class JsonAdapter(Json):
        """
        Customized psycopg2.extras.Json to allow for a custom encoder.
        """

        def __init__(self, adapted, dumps=None, encoder=None):
            self.encoder = encoder
            super().__init__(adapted, dumps=dumps)

        def dumps(self, obj):
            options = {'cls': self.encoder} if self.encoder else {}
            return json.dumps(obj, **options)

    utils.inject_class(jsonb, "JsonAdapter", JsonAdapter)
    # We do not alter __all__ here, it was a private utility!
