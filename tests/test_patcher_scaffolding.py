from __future__ import absolute_import, print_function, unicode_literals

import os, sys, random
import pytest

import _test_utilities

from django_compat_patcher.registry import get_relevant_fixers, get_relevant_fixer_ids, get_fixer_by_id
from django_compat_patcher.utilities import get_patcher_setting
from django_compat_patcher import patch


def test_get_patcher_setting():
    with pytest.raises(ValueError):
        get_patcher_setting("DEBUG")  # only DCP settings allowed
    assert get_patcher_setting("DCP_INCLUDE_FIXER_IDS") == "*"
    assert get_patcher_setting("DCP_INCLUDE_FIXER_IDS",
                               settings=dict(DCP_INCLUDE_FIXER_IDS=["a"])) == ["a"]

    # TODO patch django settings to check that they are used IFF no parameter "settings"


def test_get_relevant_fixer_ids():
    settings = random.choice(({}, None))

    fixer_ids = get_relevant_fixer_ids(current_django_version="1.9", settings=settings)
    assert [expected_fixer_id in fixer_ids for expected_fixer_id in
            ['fix_deletion_templatetags_future_url', 'fix_deletion_core_handlers_wsgi_WSGIRequest_REQUEST']]
    assert len(fixer_ids) > 5

    fixer_ids = get_relevant_fixer_ids(current_django_version="1.10")
    assert [expected_fixer_id in fixer_ids for expected_fixer_id in
            ['fix_deletion_templatetags_future_url', 'fix_deletion_core_handlers_wsgi_WSGIRequest_REQUEST']]
    assert len(fixer_ids) > 5

    fixer_ids = get_relevant_fixer_ids(current_django_version="1.3")
    assert fixer_ids == ['fix_incoming_urls_submodule']

    # TODO update this test when new fixers arrive, and test inclusion/exclusion filters

    settings = dict(DCP_INCLUDE_FIXER_IDS=[],
                    DCP_INCLUDE_FIXER_FAMILIES=[],
                    DCP_EXCLUDE_FIXER_IDS=[],
                    DCP_EXCLUDE_FIXER_FAMILIES=[])
    fixer_ids = get_relevant_fixer_ids(current_django_version="1.9", settings=settings)
    assert len(fixer_ids) == 0

    settings = dict(DCP_INCLUDE_FIXER_IDS=[],
                    DCP_INCLUDE_FIXER_FAMILIES=["django1.9"],
                    DCP_EXCLUDE_FIXER_IDS=[],
                    DCP_EXCLUDE_FIXER_FAMILIES=[])
    fixer_ids = get_relevant_fixer_ids(current_django_version="1.9", settings=settings)
    assert len(fixer_ids) >= 2

    settings = dict(DCP_INCLUDE_FIXER_IDS="*",
                    DCP_INCLUDE_FIXER_FAMILIES=[],
                    DCP_EXCLUDE_FIXER_IDS=[],
                    DCP_EXCLUDE_FIXER_FAMILIES=[])
    fixer_ids = get_relevant_fixer_ids(current_django_version="1.9", settings=settings)
    assert len(fixer_ids) >= 2

    settings = dict(DCP_INCLUDE_FIXER_IDS=[],
                    DCP_INCLUDE_FIXER_FAMILIES="*",
                    DCP_EXCLUDE_FIXER_IDS=[],
                    DCP_EXCLUDE_FIXER_FAMILIES=[])
    fixer_ids = get_relevant_fixer_ids(current_django_version="1.9", settings=settings)
    assert len(fixer_ids) >= 2

    settings = dict(DCP_INCLUDE_FIXER_IDS=['fix_deletion_templatetags_future_url'],
                    DCP_INCLUDE_FIXER_FAMILIES=["django1.9"],
                    DCP_EXCLUDE_FIXER_IDS=[],
                    DCP_EXCLUDE_FIXER_FAMILIES=["django1.6", "django1.7", "django1.8", "django1.9"])
    fixer_ids = get_relevant_fixer_ids(current_django_version="1.9", settings=settings)
    assert fixer_ids == []

    settings = dict(DCP_INCLUDE_FIXER_IDS=['fix_deletion_templatetags_future_url'],
                    DCP_INCLUDE_FIXER_FAMILIES=["django1.9"],
                    DCP_EXCLUDE_FIXER_IDS=['fix_deletion_templatetags_future_url'],
                    DCP_EXCLUDE_FIXER_FAMILIES=[])
    fixer_ids = get_relevant_fixer_ids(current_django_version="1.9", settings=settings)
    assert 'fix_deletion_core_handlers_wsgi_WSGIRequest_REQUEST' in fixer_ids

    settings = dict(DCP_INCLUDE_FIXER_IDS=[],
                    DCP_INCLUDE_FIXER_FAMILIES=["django1.9"],
                    DCP_EXCLUDE_FIXER_IDS=[],
                    DCP_EXCLUDE_FIXER_FAMILIES="*")
    fixer_ids = get_relevant_fixer_ids(current_django_version="1.9", settings=settings)
    assert fixer_ids == []


def test_get_fixer_by_id():
    res = get_fixer_by_id("fix_deletion_templatetags_future_ssi")
    assert isinstance(res, dict)
    assert res["fixer_id"] == "fix_deletion_templatetags_future_ssi"

    with pytest.raises(LookupError):
        get_fixer_by_id("ddssdfsdfsdf")


def test_django_patcher():
    applied_fixer_ids = patch()
    assert len(applied_fixer_ids) > 0  # todo strengthen this tets?
