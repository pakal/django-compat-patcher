from __future__ import absolute_import, print_function, unicode_literals

import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from django.test import TestCase


import _test_utilities  # initializes django


class MockRequest:
    pass


def test_keep_templatetags_future_url():
    from compat import render_to_string

    rendered = render_to_string('core_tags/test_future_url.html')
    assert rendered.strip() == "/homepage/"

    rendered = render_to_string('core_tags/test_defaulttags_url.html')
    assert rendered.strip() == "/homepage/"


def test_keep_templatetags_future_ssi():
    from compat import render_to_string

    filepath = os.path.abspath(__file__)

    rendered = render_to_string('core_tags/test_future_ssi.html', 
                                dict(filepath=filepath))
    assert "test_keep_templatetags_future_ssi()" in rendered

    rendered = render_to_string('core_tags/test_defaulttags_ssi.html', 
                                dict(filepath=filepath))
    assert "test_keep_templatetags_future_ssi()" in rendered


class FormsExtraTestCase(TestCase):

    def assertFormErrors(self, expected, the_callable, *args, **kwargs):
        from django.forms import ValidationError
        try:
            the_callable(*args, **kwargs)
            self.fail("Testing the 'clean' method on %s failed to raise a ValidationError.")
        except ValidationError as e:
            self.assertEqual(e.messages, expected)

    def test_ipaddress(self):

        from django.forms.fields import IPAddressField

        f = IPAddressField()
        self.assertFormErrors(['This field is required.'], f.clean, '')
        self.assertFormErrors(['This field is required.'], f.clean, None)
        self.assertEqual(f.clean(' 127.0.0.1'), '127.0.0.1')
        self.assertFormErrors(['Enter a valid IPv4 address.'], f.clean, 'foo')
        self.assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '127.0.0.')
        self.assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '1.2.3.4.5')
        self.assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '256.125.1.5')

        f = IPAddressField(required=False)
        self.assertEqual(f.clean(''), '')
        self.assertEqual(f.clean(None), '')
        self.assertEqual(f.clean(' 127.0.0.1'), '127.0.0.1')
        self.assertFormErrors(['Enter a valid IPv4 address.'], f.clean, 'foo')
        self.assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '127.0.0.')
        self.assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '1.2.3.4.5')
        self.assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '256.125.1.5')

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


def test_fix_deletion_utils_datastructures_MergeDict():
    from django.utils.datastructures import MergeDict
    MergeDict()


def test_deletion_utils_datastructures_SortedDict():
    from django.utils.datastructures import SortedDict
    SortedDict()


def test_deletion_utils_importlib():
    from django.utils import importlib


def test_deletion_utils_tzinfo():
    from django.utils import tzinfo


def test_deletion_utils_dictconfig():
    from django.utils import dictconfig


def test_deletion_utils_unittest():
    from django.utils import unittest
