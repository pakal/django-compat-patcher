
import pytest

import _test_utilities
from django_compat_patcher.deprecation import RemovedInDjango40Warning


def test_fix_deletion_conf_urls_url():
    import re
    from django.conf.urls import url as conf_url
    def empty_view(*args, **kwargs):
        return None
    assert conf_url(r'^regex/(?P<pk>[0-9]+)/$', empty_view, name='regex')


def test_fix_deletion_utils_encoding_smart_force_text():
    from django.utils.encoding import smart_text, force_text
    from django.utils.translation import gettext_lazy
    from django.utils.functional import SimpleLazyObject

    s = SimpleLazyObject(lambda: 'x')
    assert type(force_text(s)) is str

    class Test:
        def __str__(self):
            return 'ŠĐĆŽćžšđ'

    lazy_func = gettext_lazy('x')
    assert smart_text(lazy_func) is lazy_func
    assert smart_text(Test()) == '\u0160\u0110\u0106\u017d\u0107\u017e\u0161\u0111'
    assert smart_text(1) == '1'
    assert smart_text('foo') == 'foo'


def test_fix_deletion_utils_http_quote_utilities():
    from django.utils.http import urlquote, urlunquote, urlquote_plus, urlunquote_plus

    assert urlquote('Paris & Orl\xe9ans') == 'Paris%20%26%20Orl%C3%A9ans'
    assert urlquote('Paris & Orl\xe9ans', safe="&") == 'Paris%20&%20Orl%C3%A9ans'

    assert urlunquote('Paris%20%26%20Orl%C3%A9ans') == 'Paris & Orl\xe9ans'
    assert urlunquote('Paris%20&%20Orl%C3%A9ans') == 'Paris & Orl\xe9ans'

    assert urlquote_plus('Paris & Orl\xe9ans') == 'Paris+%26+Orl%C3%A9ans'
    assert urlquote_plus('Paris & Orl\xe9ans', safe="&") == 'Paris+&+Orl%C3%A9ans'

    assert urlunquote_plus('Paris+%26+Orl%C3%A9ans') == 'Paris & Orl\xe9ans'
    assert urlunquote_plus('Paris+&+Orl%C3%A9ans') == 'Paris & Orl\xe9ans'


def test_fix_deletion_utils_translation_ugettext_utilities():
    from django.utils.translation import (ugettext_noop, ugettext, ugettext_lazy,
                                          ungettext, ungettext_lazy, gettext_lazy, ngettext_lazy)

    assert ugettext_noop("weirdstuff") == "weirdstuff"
    assert ugettext("weirdstuff2") == "weirdstuff2"
    assert ungettext("%d weirdstaf", "%d weirdstifs", 0) % 0 == "0 weirdstifs"  # Zero is plural in English
    assert ugettext_lazy("weirdstuff3") == gettext_lazy("weirdstuff3")
    assert ungettext_lazy("%d weirdstaf", "%d weirdstifs", 0) == ngettext_lazy("%d weirdstaf", "%d weirdstifs", 0)


def test_fix_deletion_utils_text_unescape_entities():

    from django.utils import text as text_module

    items = [
        ('', ''),
        ('foo', 'foo'),
        ('&amp;', '&'),
        ('&am;', '&am;'),
        ('&#x26;', '&'),
        ('&#xk;', '&#xk;'),
        ('&#38;', '&'),
        ('foo &amp; bar', 'foo & bar'),
        ('foo & bar', 'foo & bar'),
    ]

    for value, output in items:

        assert text_module.unescape_entities(value) == output

        if _test_utilities.DJANGO_VERSION_TUPLE >= (2, 0):
            from django.utils.functional import lazystr
            assert text_module.unescape_entities(lazystr(value)) == output


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (2, 0),
    reason="requires new is_safe_url() with allowed_hosts parameter",
)
def test_fix_deletion_utils_http_is_safe_url():
    from django.utils.http import is_safe_url
    assert is_safe_url('https://example.com', allowed_hosts={'example.com'}, require_https=True)
    assert not is_safe_url('http://example.com', allowed_hosts={'example.com'}, require_https=True)
    assert not is_safe_url('https://badexample.com', allowed_hosts={'example.com'}, require_https=True)


def test_fix_behaviour_dispatch_dispatcher_Signal_providing_args():
    from django.dispatch import Signal
    instance = Signal(providing_args=['arg1', 'arg2'], use_caching=True)
    assert instance.use_caching


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (3, 1),
    reason="requires InvalidQuery exception based on FieldError and FieldDoesNotExist",
)
def test_fix_deletion_db_models_query_utils_InvalidQuery():
    from django.db.models.query_utils import InvalidQuery, FieldError, FieldDoesNotExist

    assert isinstance(InvalidQuery(), InvalidQuery)

    for exception in (FieldError, FieldDoesNotExist):
        assert isinstance(exception(), InvalidQuery)

    for exception in (FieldError, FieldDoesNotExist, InvalidQuery):
        assert issubclass(exception, InvalidQuery)


def test_fix_deletion_http_request_HttpRequest_is_ajax():
    from django.http import HttpRequest
    request = HttpRequest()
    assert not request.is_ajax()
    request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
    assert request.is_ajax()


def test_fix_behaviour_utils_crypto_get_random_string_length():
    from django.utils.crypto import get_random_string
    assert len(get_random_string()) == 12  # Default length
    assert get_random_string(allowed_chars="f") ==  "f" * 12


def test_fix_deletion_contrib_postgres_forms_jsonb():
    from django.contrib.postgres import forms
    assert forms.JSONField()

    assert forms.jsonb  # Module was prelinked here
    import django.contrib.postgres.forms.jsonb as json
    del json


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (2, 0),
    reason="requires initial implementation of django.contrib.postgres.fields.jsonb",
)
def test_fix_deletion_contrib_postgres_fields_jsonb():
    from django.contrib.postgres.fields.jsonb import KeyTextTransform, KeyTransform
    assert KeyTransform('foo', 'bar')
    assert KeyTextTransform('foo', 'bar')


def test_fix_deletion_template_defaulttags_ifequal_ifnotequal():
    from compat import render_to_string

    rendered = render_to_string("core_tags/test_defaulttags_ifequal_ifnotequal.html")
    assert rendered.strip() == "ifequalgood\nifnotequalgood"


def test_fix_deletion_forms_models_ModelMultipleChoiceField_error_messages_list_entry():
    from django.forms.models import ModelMultipleChoiceField
    from test_project.models import SimpleModel

    field = ModelMultipleChoiceField(
        queryset=SimpleModel.objects.all(),
        error_messages={'list': 'NOT A LIST OF VALUES'},
    )
    assert field.error_messages['list'] == 'NOT A LIST OF VALUES'
    if _test_utilities.DJANGO_VERSION_TUPLE >= (3, 1):
        assert field.error_messages['invalid_list'] == 'NOT A LIST OF VALUES'  # Properly transferred


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (2, 0),
    reason="requires new middleware system with get_response attribute",
)
def test_fix_behaviour_middleware_get_response_parameter_nullability():
    from django.contrib.admindocs.middleware import XViewMiddleware
    from django.contrib.auth.middleware import (
        AuthenticationMiddleware, RemoteUserMiddleware,
    )
    from django.contrib.flatpages.middleware import FlatpageFallbackMiddleware
    from django.contrib.messages.middleware import MessageMiddleware
    from django.contrib.redirects.middleware import RedirectFallbackMiddleware
    from django.contrib.sessions.middleware import SessionMiddleware
    from django.contrib.sites.middleware import CurrentSiteMiddleware
    from django.middleware.cache import (
        CacheMiddleware, FetchFromCacheMiddleware, UpdateCacheMiddleware,
    )
    from django.middleware.clickjacking import XFrameOptionsMiddleware
    from django.middleware.common import (
        BrokenLinkEmailsMiddleware, CommonMiddleware,
    )
    from django.middleware.csrf import CsrfViewMiddleware
    from django.middleware.gzip import GZipMiddleware
    from django.middleware.http import ConditionalGetMiddleware
    from django.middleware.locale import LocaleMiddleware
    from django.middleware.security import SecurityMiddleware

    middlewares = [
        AuthenticationMiddleware,
        BrokenLinkEmailsMiddleware,
        CacheMiddleware,
        CommonMiddleware,
        ConditionalGetMiddleware,
        CsrfViewMiddleware,
        CurrentSiteMiddleware,
        FetchFromCacheMiddleware,
        FlatpageFallbackMiddleware,
        GZipMiddleware,
        LocaleMiddleware,
        MessageMiddleware,
        RedirectFallbackMiddleware,
        RemoteUserMiddleware,
        SecurityMiddleware,
        SessionMiddleware,
        UpdateCacheMiddleware,
        XFrameOptionsMiddleware,
        XViewMiddleware,
    ]

    for middleware in middlewares:

        obj1 = middleware()
        # Fallback on dummy callable when Django>=4.0
        assert obj1.get_response is None or callable(obj1.get_response)

        obj2 = middleware(None)
        assert obj2.get_response is None or callable(obj2.get_response)

        dummy_get_response = lambda *args, **kwargs: 777
        obj3 = middleware(dummy_get_response)
        assert obj3.get_response is dummy_get_response


# Standalone test, unrelated to fixers
@pytest.mark.django_db
def test_NullBooleanField_still_operational():
    """NullBooleanField model field is removed in django 4.0, but still usable if checks are silenced"""
    from test_project.models import SimpleModel

    record = SimpleModel()
    record.save()
    assert record.is_deleted is None

    record.is_deleted = True
    record.save()
    assert record.is_deleted

    assert SimpleModel.objects.first() == record


# Standalone test, unrelated to fixers
@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (3, 2),
    reason="requires common JSONField implementation (sqlite-compatible)",
)
@pytest.mark.django_db
def test_postgres_JSONField_still_operational():
    """The django.contrib.postgres.fields.JSONField model field is removed in django 4.0, but still usable if checks are silenced"""
    from test_project.models import SimpleModel

    # This works with sqlite because postgres->JSONField actually a generic field now
    record = SimpleModel(misc_postgres_json=dict(a="33"))
    record.save()

    record = SimpleModel.objects.first()
    assert record.misc_postgres_json == dict(a="33")
