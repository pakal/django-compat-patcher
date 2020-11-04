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