from __future__ import absolute_import, print_function, unicode_literals

import os, sys
import pytest

import _test_utilities


@pytest.mark.skipif(_test_utilities.DJANGO_VERSION_TUPLE < (2, 10), reason="requires django.urls subpackage")
def test_fix_deletion_django_urls_RegexURLPattern_RegexURLResolver():

    from django.urls import RegexURLPattern
    from django.urls.resolvers import RegexURLPattern as RegexURLPattern2
    assert RegexURLPattern is RegexURLPattern2

    url = RegexURLPattern("^mypage\d", lambda x: x, name="mygoodurl")
    assert not url.check()
    assert url.resolve("mypage3")
    assert not url.resolve("mypage")

    from django.urls import RegexURLResolver
    from django.urls.resolvers import RegexURLResolver as RegexURLResolver2
    assert RegexURLResolver is RegexURLResolver2

    from django.conf import settings
    urlconf = settings.ROOT_URLCONF
    resolver = RegexURLResolver(r'^/', urlconf)
    assert resolver.check()  # like "Your URL pattern '^homepage/$' uses include with a route ending with a '$'"
    assert resolver.resolve("/homepage/")
    from django.urls import Resolver404
    with pytest.raises(Resolver404):
        resolver.resolve("/homepageXXX/")


@pytest.mark.skipif(_test_utilities.DJANGO_VERSION_TUPLE < (2, 10), reason="requires django.urls subpackage")
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
