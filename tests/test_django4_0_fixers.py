
import pytest

import _test_utilities


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

