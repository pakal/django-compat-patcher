
import pytest

import _test_utilities

from django_compat_patcher import default_settings
from django_compat_patcher.registry import django_patching_registry


def test_fix_deletion_db_models_submodules_EmptyResultSet():
    from django.db.models.query import EmptyResultSet as EmptyResultSet1
    from django.db.models.sql import EmptyResultSet as EmptyResultSet2
    from django.db.models.sql.datastructures import EmptyResultSet as EmptyResultSet3

    assert EmptyResultSet1 is EmptyResultSet2
    assert EmptyResultSet2 is EmptyResultSet3

    import django.db.models.sql
    assert "EmptyResultSet" in django.db.models.sql.__all__


def test_fix_deletion_db_models_fields_FieldDoesNotExist():
    from django.db.models.fields import FieldDoesNotExist
    assert FieldDoesNotExist

    from django.db.models import fields
    assert "FieldDoesNotExist" in fields.__all__


def test_fix_deletion_forms_forms_pretty_name_BoundField():
    from django.forms.forms import BoundField
    assert BoundField
    from django.forms.forms import pretty_name
    assert pretty_name("my_dog") == "My dog"


def test_fix_deletion_forms_fields_EMPTY_VALUES():
    from django.forms.fields import EMPTY_VALUES
    assert EMPTY_VALUES


def test_fix_deletion_template_base_Context_classes():
    from django.template.base import (Context, RequestContext, ContextPopException)
    assert Context
    assert RequestContext
    assert ContextPopException


def test_fix_deletion_core_management_commands_runserver():
    from django.core.management.commands.runserver import Command, BaseRunserverCommand
    assert Command is BaseRunserverCommand


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (1, 9),
    reason="requires django.utils.decorators.classproperty introduction",
)
def test_fix_deletion_utils_decorators_classproperty():
    from django.utils.decorators import classproperty

    class MyClass:
        @classproperty
        def myfunc(cls):
            return 43

    assert MyClass.myfunc == 43
    assert MyClass().myfunc == 43


def test_fix_deletion_contrib_admin_ACTION_CHECKBOX_NAME():
    from django.contrib.admin import ACTION_CHECKBOX_NAME, autodiscover
    del autodiscover  # Proper module is targeted
    assert ACTION_CHECKBOX_NAME == "_selected_action"

    import django.contrib.admin
    assert "ACTION_CHECKBOX_NAME" in django.contrib.admin.__all__


def test_fix_deletion_views_debug_ExceptionReporterFilter():
    from django.views.debug import ExceptionReporterFilter
    filter = ExceptionReporterFilter()
    assert filter.get_post_parameters(None) == {}


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (1, 11),
    reason="requires postgres.forms.jsonb module",
)
def test_fix_deletion_contrib_postgres_forms_jsonb_InvalidJSONInput_JSONString():

    # We expect psycopg2 to be installed here

    # These upper level imports NEVER existed!
    with pytest.raises(ImportError):
        from django.contrib.postgres.forms import InvalidJSONInput
    with pytest.raises(ImportError):
        from django.contrib.postgres.forms import JSONString

    from django.contrib.postgres.forms.jsonb import InvalidJSONInput, JSONString

    assert InvalidJSONInput("hello")
    assert JSONString("something")

    try:
        from django.forms.fields import InvalidJSONInput as _InvalidJSONInput, JSONString as _JSONString
    except ImportError:
        pass  # It's OK, these do not exist yet
    else:
        assert _InvalidJSONInput is InvalidJSONInput
        assert _JSONString is JSONString

    # This fixer is UNSAFE since it requires psycopg2
    fixer_id = "fix_deletion_contrib_postgres_forms_jsonb_InvalidJSONInput_JSONString"
    assert django_patching_registry.get_fixer_by_id(fixer_id)
    assert fixer_id in default_settings.DCP_EXCLUDE_FIXER_IDS


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (1, 11),
    reason="requires postgres.fields.jsonb module",
)
def test_fix_deletion_contrib_postgres_fields_jsonb_JsonAdapter():

    from django.contrib.postgres.fields.jsonb import JsonAdapter
    assert JsonAdapter.dumps  # Hard to test here...

    # This fixer is UNSAFE since it requires psycopg2
    fixer_id = "fix_deletion_contrib_postgres_fields_jsonb_JsonAdapter"
    assert django_patching_registry.get_fixer_by_id(fixer_id)
    assert fixer_id in default_settings.DCP_EXCLUDE_FIXER_IDS
