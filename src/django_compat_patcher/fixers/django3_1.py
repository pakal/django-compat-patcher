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