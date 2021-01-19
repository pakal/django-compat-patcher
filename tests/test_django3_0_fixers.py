import sys
from io import BytesIO

import six
import pytest


skip_on_python2 = pytest.mark.skipif(sys.version_info < (3,), reason="This Django3 fixer requires python3 or higher")


def test_fix_deletion_utils_six():
    import django.utils.six
    from django.utils import six as six2
    assert django.utils.six.string_types
    assert six2.string_types

    from django.utils.encoding import six as six3
    assert isinstance(six3.PY2, bool)
    assert six3 is six2

    # Old versions of compat-patcher-core crashed due to wrong module names set by six._importer
    from django.utils.six.moves.urllib.parse import urlencode
    assert urlencode(dict(name="h\xc3llo")) == "name=h%C3%83llo" if six.PY3 else "name=h%C3llo"


def test_fix_deletion_utils_upath_npath_abspathu():
    from os.path import abspath
    from django.utils._os import abspathu, upath, npath

    assert abspathu(".") == abspath(".")
    assert upath("/something/file.txt") == "/something/file.txt"  # No-op
    assert npath("/something2/file.txt") == "/something2/file.txt"  # No-op


@skip_on_python2
def test_fix_deletion_utils_decorators_ContextDecorator():
    from django.utils.decorators import ContextDecorator
    from contextlib import ContextDecorator as ContextDecoratorOriginal
    assert isinstance(ContextDecorator, type)
    assert ContextDecorator is ContextDecoratorOriginal


def test_fix_deletion_utils_decorators_available_attrs():
    from django.utils.decorators import available_attrs
    from functools import WRAPPER_ASSIGNMENTS

    def func():
        pass

    assert available_attrs(func) == WRAPPER_ASSIGNMENTS


@skip_on_python2
def test_fix_deletion_utils_lru_cache_lru_cache():
    from django.utils.lru_cache import lru_cache as django_lru_cache_function
    from functools import lru_cache
    assert callable(django_lru_cache_function)
    assert django_lru_cache_function is lru_cache


@skip_on_python2
def test_fix_deletion_utils_safestring_SafeBytes():
    from django.utils.safestring import SafeBytes
    assert SafeBytes("abc", "ascii") == bytes("abc", "ascii")


@skip_on_python2
def test_fix_deletion_test_utils_str_prefix():
    from django.test.utils import str_prefix
    assert str_prefix("%(_)shello") == "hello"


def test_fix_deletion_test_utils_patch_logger():
    import logging
    from django.test.utils import patch_logger
    with patch_logger("django", "info") as calls:
        logging.getLogger("django").info("Patch-logger context manager seems to work %s", "fine")
    assert len(calls) == 1
    assert calls == ["Patch-logger context manager seems to work fine"]


@skip_on_python2
def test_fix_deletion_utils_encoding_python_2_unicode_compatible():
    from django.utils.encoding import python_2_unicode_compatible

    @python_2_unicode_compatible
    class MyClass:
        def __str__(self):
            return "<Some MyClass object>"

    obj = MyClass()
    assert isinstance(obj, MyClass)


def test_fix_deletion_utils_functional_curry():

    from django.utils.functional import curry

    def func(value1, value2, value3, value4):
        return value1 + value2 + value3 + value4

    func2 = curry(func, "hello", value3="general")
    assert func2("there", value4="kenobi") == "hellotheregeneralkenobi"


def test_fix_deletion_shortcuts_render_to_response():
    from django.shortcuts import render_to_response
    res = render_to_response("example_template.html", context=dict(message="ThiIsATest"),
                             content_type="dummycontenttype", status=201)
    assert res['Content-Type'] == "dummycontenttype"
    assert res.status_code == 201
    assert six.b("ThiIsATest") in res.content


def test_fix_deletion_http_request_HttpRequest_xreadlines():
    from django.http.request import HttpRequest

    request = HttpRequest()
    request._stream = BytesIO(b"hello\nthere\n")

    result = [line for line in request.xreadlines()]
    assert result == [b'hello\n', b'there\n']


def test_fix_deletion_utils_http_cookie_date():
    from django.utils.http import cookie_date
    assert cookie_date(1611067745) == 'Tue, 19-Jan-2021 14:49:05 GMT'


def test_fix_deletion_contrib_staticfiles_templatetags_and_admin_static():
    from django.template import Template, Context

    tpl = Template("{% load admin_static %}Here is: {% static \"sample_file.png\" %}")
    data = tpl.render(Context())
    assert data == "Here is: /static/sample_file.png"

    tpl = Template("{% load staticfiles %}Here is: {% static \"myotherfile.jpg\" %}")
    data = tpl.render(Context())
    assert data == "Here is: /static/myotherfile.jpg"


@pytest.mark.django_db
def test_fix_behaviour_db_models_query_QuerySet_earliest_latest():
    from test_project.models import SimpleModel

    SimpleModel.objects.create(name="Max", age=10, is_active=True)
    SimpleModel.objects.create(name="Sandy", age=26, is_active=True)

    assert SimpleModel.objects.earliest("age").name == "Max"
    assert SimpleModel.objects.latest("age").name == "Sandy"

    assert SimpleModel.objects.earliest(field_name="age").name == "Max"
    assert SimpleModel.objects.latest(field_name="age").name == "Sandy"
