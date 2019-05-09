from __future__ import absolute_import, print_function, unicode_literals

import os, sys
import pytest

import _test_utilities


class MockRequest:
    pass


def test_fix_deletion_templatetags_future_url():
    from compat import render_to_string

    rendered = render_to_string('core_tags/test_future_url.html')
    assert rendered.strip() == "/homepage/"

    rendered = render_to_string('core_tags/test_defaulttags_url.html')
    assert rendered.strip() == "/homepage/"


def test_fix_deletion_templatetags_future_ssi():
    from compat import render_to_string

    filepath = os.path.abspath(__file__)

    rendered = render_to_string('core_tags/test_future_ssi.html',
                                dict(filepath=filepath))
    assert "test_keep_templatetags_future_ssi()" in rendered

    rendered = render_to_string('core_tags/test_defaulttags_ssi.html',
                                dict(filepath=filepath))
    assert "test_keep_templatetags_future_ssi()" in rendered


def test_fix_deletion_forms_fields_IPAddressField():
    from django.forms import ValidationError
    from django.forms.fields import IPAddressField

    def assertEqual(a, b):
        assert a == b

    def assertFormErrors(expected, the_callable, *args, **kwargs):
        try:
            the_callable(*args, **kwargs)
            raise ValueError("Testing the 'clean' method on %s failed to raise a ValidationError.")
        except ValidationError as e:
            assert e.messages == expected

    f = IPAddressField()
    assertFormErrors(['This field is required.'], f.clean, '')
    assertFormErrors(['This field is required.'], f.clean, None)
    assertEqual(f.clean(' 127.0.0.1'), '127.0.0.1')
    assertFormErrors(['Enter a valid IPv4 address.'], f.clean, 'foo')
    assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '127.0.0.')
    assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '1.2.3.4.5')
    assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '256.125.1.5')

    f = IPAddressField(required=False)
    assertEqual(f.clean(''), '')
    assertEqual(f.clean(None), '')
    assertEqual(f.clean(' 127.0.0.1'), '127.0.0.1')
    assertFormErrors(['Enter a valid IPv4 address.'], f.clean, 'foo')
    assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '127.0.0.')
    assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '1.2.3.4.5')
    assertFormErrors(['Enter a valid IPv4 address.'], f.clean, '256.125.1.5')

    from django.db.models.fields import IPAddressField as ModelIPAddressField
    res = ModelIPAddressField().formfield()
    assert isinstance(res, IPAddressField)


def test_fix_deletion_core_handlers_wsgi_WSGIRequest_REQUEST():
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


def test_fix_deletion_contrib_admin_ModelAdmin_get_formsets():
    from django.contrib.admin import ModelAdmin
    from test_project.models import SimpleModel
    from django.contrib.admin import AdminSite

    assert hasattr(ModelAdmin, 'get_formsets')

    ma = ModelAdmin(SimpleModel, AdminSite())

    assert ma.get_fieldsets(request=MockRequest()) == [(None, {'fields': ['name', 'age', 'is_active']})]


def test_fix_deletion_utils_datastructures_MergeDict():
    from django.utils.datastructures import MergeDict
    MergeDict()


def test_fix_deletion_utils_datastructures_SortedDict():
    from django.utils.datastructures import SortedDict
    SortedDict()


def test_fix_deletion_utils_importlib():
    import django.utils.importlib
    from django.utils import importlib
    csv_module = importlib.import_module("csv")
    import csv
    assert csv_module is csv


def test_fix_deletion_utils_tzinfo():
    import django.utils.tzinfo
    from django.utils import tzinfo
    assert tzinfo.FixedOffset(35)


def test_fix_deletion_utils_dictconfig():
    import django.utils.dictconfig
    from django.utils import dictconfig
    assert dictconfig.valid_ident("myident")


def test_fix_deletion_utils_functional_memoize():
    import django.utils.functional
    from django.utils.functional import memoize
    cache = {}
    def myfun(myarg):
        return myarg
    myfun = memoize(myfun, cache, num_args=1)
    myfun(3)
    myfun(4)
    assert cache == {(3,): 3, (4,): 4}


def test_fix_deletion_utils_unittest():
    import django.utils.unittest
    from django.utils import unittest
    assert callable(unittest.TestCase)


def test_fix_deletion_core_management_base_AppCommand_handle_app():
    from django.core.management.base import AppCommand

    class DummyAppconfig(object):
        label = "my dummy app"
        models_module = "fake_models_module"

    appconfig = DummyAppconfig()

    class DummyAppCommand(AppCommand):
        def handle_app(self, models_module, **options):
            return 33

    res = DummyAppCommand().handle_app_config(appconfig, other_arg=12)
    assert res == 33


def test_fix_deletion_contrib_sites_models_RequestSite():
    from django.contrib.sites.models import RequestSite
    from django.contrib.sites.requests import RequestSite as RealRequestSite
    assert callable(RequestSite)
    assert issubclass(RequestSite, RealRequestSite)


def test_fix_deletion_contrib_sites_models_get_current_site():
    from django.core.exceptions import ImproperlyConfigured
    class request:
        SITE_ID = 1
    from django.contrib.sites.models import get_current_site
    with pytest.raises(ImproperlyConfigured):  # DCP tests have no DB access for now
        assert get_current_site(request)
