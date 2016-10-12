from __future__ import absolute_import, print_function, unicode_literals

import os, sys
import pytest


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import _test_utilities  # initializes django

from django_compat_patcher.registry import get_relevant_fixers, get_relevant_fixer_ids, get_fixer_by_id
from django_compat_patcher.utilities import get_patcher_setting
from django_compat_patcher import patch


def test_get_patcher_setting():
    with pytest.raises(AttributeError): 
        get_patcher_setting("DEBUG")  # only DCP settings allowed
    assert get_patcher_setting("DCP_INCLUDE_FIXER_IDS") is None
    assert get_patcher_setting("DCP_INCLUDE_FIXER_IDS",settings=dict(DCP_INCLUDE_FIXER_IDS=345)) == 345
    
    # TODO patch django settings to check that they are used IFF no parameter "settings"


def test_get_relevant_fixer_ids():

    fixer_ids = get_relevant_fixer_ids(current_django_version="1.9")
    assert fixer_ids == ['keep_templatetags_future_url', 'keep_request_post_get_mergedict']

    fixer_ids = get_relevant_fixer_ids(current_django_version="1.10")
    assert fixer_ids == ['keep_templatetags_future_url', 'keep_request_post_get_mergedict']

    fixer_ids = get_relevant_fixer_ids(current_django_version="1.8")
    assert fixer_ids == []

    # TODO update this test when new fixers arrive, and test inclusion/exclusion filters


def test_get_fixer_by_id():

    res = get_fixer_by_id("keep_templatetags_future_url")
    assert isinstance(res, dict)
    assert res["fixer_id"] == "keep_templatetags_future_url"
    
    with pytest.raises(LookupError):
        get_fixer_by_id("ddssdfsdfsdf")
    
    


def test_django_patcher():
    
    applied_fixer_ids = patch()
    assert len(applied_fixer_ids) > 0  # todo strengthen this tets?