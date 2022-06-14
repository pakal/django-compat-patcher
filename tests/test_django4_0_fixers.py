
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
    from django.utils.functional import lazystr
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
        assert text_module.unescape_entities(lazystr(value)) == output


def test_fix_deletion_utils_http_is_safe_url():
    from django.utils.http import is_safe_url
    assert is_safe_url('https://example.com', allowed_hosts={'example.com'}, require_https=True)
    assert not is_safe_url('http://example.com', allowed_hosts={'example.com'}, require_https=True)
    assert not is_safe_url('https://badexample.com', allowed_hosts={'example.com'}, require_https=True)


def test_fix_behaviour_dispatch_dispatcher_Signal_providing_args():
    from django.dispatch import Signal
    instance = Signal(providing_args=['arg1', 'arg2'], use_caching=True)
    assert instance.use_caching


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
