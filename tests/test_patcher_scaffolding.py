from __future__ import absolute_import, print_function, unicode_literals

import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import _test_utilities  # initializes django

from django_compat_patcher.registry import get_relevant_fixers, get_relevant_fixer_ids
from django_compat_patcher import patch


def test_get_relevant_fixers():

    fixer_ids = get_relevant_fixer_ids(current_django_version="1.9")
    assert fixer_ids == ['keep_templatetags_future_url', 'keep_request_post_get_mergedict']

    fixer_ids = get_relevant_fixer_ids(current_django_version="1.10")
    assert fixer_ids == ['keep_templatetags_future_url', 'keep_request_post_get_mergedict']

    fixer_ids = get_relevant_fixer_ids(current_django_version="1.8")
    assert fixer_ids == []

    # TODO update this test when new fixers arrive, and test inclusion/exclusion filters


def test_django_patcher():
    
    applied_fixer_ids = patch()
    assert len(applied_fixer_ids) > 0  # todo strengthen this tets?