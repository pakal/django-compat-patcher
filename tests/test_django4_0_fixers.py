
import pytest

import _test_utilities
from django_compat_patcher.deprecation import RemovedInDjango40Warning


def test_fix_deletion_conf_urls_url(self):
    from django.conf.urls import url as conf_url
    msg = (
        'django.conf.urls.url() is deprecated in favor of '
        'django.urls.re_path().'
    )
    def empty_view(*args, **kwargs)
        return None
    with self.assertRaisesMessage(RemovedInDjango40Warning, msg):
        conf_url(r'^regex/(?P<pk>[0-9]+)/$', empty_view, name='regex')


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

