from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_40_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="4.0",
    fixer_applied_from_version="4.0",
)

@django1_40_bc_fixer()
def fix_deletion_utils_http_quote_utilities(utils):
    """Preserve aliases of urrlib methods (quote, quote_plus, unquote, unquote_plus) in
     django.utils.http
    """
    from django.utils.functional import keep_lazy_text
    from urllib.parse import quote, quote_plus, unquote, unquote_plus

    @keep_lazy_text
    def urlquote(url, safe='/'):
        """
        A legacy compatibility wrapper to Python's urllib.parse.quote() function.
        (was used for unicode handling on Python 2)
        """
        warnings.warn(
            'django.utils.http.urlquote() is deprecated in favor of '
            'urllib.parse.quote().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return quote(url, safe)


    @keep_lazy_text
    def urlquote_plus(url, safe=''):
        """
        A legacy compatibility wrapper to Python's urllib.parse.quote_plus()
        function. (was used for unicode handling on Python 2)
        """
        warnings.warn(
            'django.utils.http.urlquote_plus() is deprecated in favor of '
            'urllib.parse.quote_plus(),',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return quote_plus(url, safe)


    @keep_lazy_text
    def urlunquote(quoted_url):
        """
        A legacy compatibility wrapper to Python's urllib.parse.unquote() function.
        (was used for unicode handling on Python 2)
        """
        warnings.warn(
            'django.utils.http.urlunquote() is deprecated in favor of '
            'urllib.parse.unquote().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return unquote(quoted_url)


    @keep_lazy_text
    def urlunquote_plus(quoted_url):
        """
        A legacy compatibility wrapper to Python's urllib.parse.unquote_plus()
        function. (was used for unicode handling on Python 2)
        """
        warnings.warn(
            'django.utils.http.urlunquote_plus() is deprecated in favor of '
            'urllib.parse.unquote_plus().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return unquote_plus(quoted_url)

    from django.utils import http
    utils.inject_callable(http, "urlquote", urlquote)
    utils.inject_callable(http, "urlquote_plus", urlquote_plus)
    utils.inject_callable(http, "urlunquote", urlunquote)
    utils.inject_callable(http, "urlunquote_plus", urlunquote_plus)
