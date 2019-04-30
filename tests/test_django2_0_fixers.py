from __future__ import absolute_import, print_function, unicode_literals

import os, sys
import pytest

import _test_utilities


@pytest.mark.skipif(_test_utilities.DJANGO_VERSION_TUPLE < (1, 10), reason="requires django.urls subpackage")
def test_fix_deletion_django_urls_RegexURLPattern_RegexURLResolver():

    from django.urls import RegexURLPattern
    from django.urls.resolvers import RegexURLPattern as RegexURLPattern2
    assert RegexURLPattern is RegexURLPattern2

    url = RegexURLPattern("^mypage\d", lambda x: x, name="mygoodurl")
    if hasattr(url, "check"):
        assert not url.check()
    assert url.resolve("mypage3")
    assert not url.resolve("mypage")

    from django.urls import RegexURLResolver
    from django.urls.resolvers import RegexURLResolver as RegexURLResolver2
    assert RegexURLResolver is RegexURLResolver2

    from django.conf import settings
    urlconf = settings.ROOT_URLCONF
    resolver = RegexURLResolver(r'^/', urlconf)
    if hasattr(resolver, "check"):
        assert not resolver.check()
    assert resolver.resolve("/homepage/")
    from django.urls import Resolver404
    with pytest.raises(Resolver404):
        resolver.resolve("/homepageXXX/")


@pytest.mark.skipif(_test_utilities.DJANGO_VERSION_TUPLE < (1, 10), reason="requires django.urls subpackage")
def test_fix_deletion_django_core_urlresolvers():

    from django.urls import get_resolver
    from django.core.urlresolvers import get_resolver as get_resolver2
    assert get_resolver is get_resolver2


def test_fix_deletion_django_template_library_assignment_tag():
    from django import template
    register = template.Library()

    @register.assignment_tag
    def mytag():
        return "mycontent"

    assert mytag() == "mycontent"


def test_fix_deletion_django_utils_functional_allow_lazy():
    import six
    from django.utils.encoding import force_text
    from django.utils.functional import allow_lazy, lazy

    def myfunc(arg):
        return arg
    myfunc = allow_lazy(myfunc, six.text_type)

    proxy = myfunc(lazy(force_text, six.text_type)("mystr"))
    assert type(proxy) != str

    value = proxy.__str__()
    assert value == "mystr"


def test_fix_deletion_django_template_context_Context_has_key():
    from django.template.context import Context

    ctx = Context({"a": 65})
    assert ctx.has_key("a")
    assert not ctx.has_key("b")

