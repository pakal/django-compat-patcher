
import pytest

import _test_utilities
from django_compat_patcher.deprecation import RemovedInDjango40Warning


def test_fix_deletion_conf_urls_url():
    import re
    from django.conf.urls import url as conf_url
    msg = re.escape(
        'django.conf.urls.url() is deprecated in favor of '
        'django.urls.re_path().'
    )
    def empty_view(*args, **kwargs):
        return None
    with pytest.raises(RemovedInDjango40Warning, match=msg):
        conf_url(r'^regex/(?P<pk>[0-9]+)/$', empty_view, name='regex')


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

