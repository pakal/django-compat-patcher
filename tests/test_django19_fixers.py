from __future__ import absolute_import, print_function, unicode_literals

import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import _test_utilities  # initializes django

class MockRequest:
    pass

def test_keep_templatetags_future_url():
    from compat import render_to_string

    rendered = render_to_string('core_tags/test_future_url.html')
    assert rendered.strip() == "/homepage/"

    rendered = render_to_string('core_tags/test_defaulttags_url.html')
    assert rendered.strip() == "/homepage/"


def test_keep_request_post_get_mergedict():
    from django.test.client import RequestFactory
    factory = RequestFactory()

    request = factory.get('/homepage/?abcd=66')
    assert "abc" not in request.REQUEST

    request = factory.get('/homepage/?abc')
    assert request.REQUEST["abc"] == ""

    request = factory.get('/homepage/?abc=6%26')
    assert request.REQUEST["abc"] == "6&"

    request = factory.post('/homepage/?abc=66', data=dict(abc="aju"))
    assert request.REQUEST["abc"] == "aju"  # POST takes precedence over GET

def test_keep_modeladmin_get_formsets():
    from django.contrib.admin import ModelAdmin
    from test_project.models import SimpleModel
    from django.contrib.admin import AdminSite

    assert hasattr(ModelAdmin, 'get_formsets')

    ma = ModelAdmin(SimpleModel, AdminSite())

    assert ma.get_fieldsets(request=MockRequest()) == [(None, {'fields': ['name', 'age', 'is_active']})]


def test_keep_utils_importlib():
    from django.utils import importlib


def test_keep_utils_tzinfo():
    from django.utils import tzinfo


def test_keep_utils_dictconfig():
    from django.utils import dictconfig


def test_keep_utils_unittest():
    from django.utils import unittest
