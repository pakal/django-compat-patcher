
import pytest


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
