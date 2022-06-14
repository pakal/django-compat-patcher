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
def fix_deletion_conf_urls_url(utils):
    """Preserve django.conf.urls.url() as an alias to django.urls.re_path()"""

    from django.urls import re_path

    def url(regex, view, kwargs=None, name=None):
        warnings.warn(
            'django.conf.urls.url() is deprecated in favor of '
            'django.urls.re_path().',
            RemovedInDjango40Warning,
            stacklevel=2,
        )
        return re_path(regex, view, kwargs, name)

    from django.conf import urls
    utils.inject_callable(urls, "url", url)


@django1_40_bc_fixer()
def fix_deletion_utils_encoding_smart_force_text(utils):
    """Preserve django.utils.encoding.force_text() and smart_text() as aliases for force_str() and smart_str()"""

    from django.utils import encoding as encoding_module

    def smart_text(s, encoding='utf-8', strings_only=False, errors='strict'):
        warnings.warn(
            'smart_text() is deprecated in favor of smart_str().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return encoding_module.smart_str(s, encoding, strings_only, errors)

    def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
        warnings.warn(
            'force_text() is deprecated in favor of force_str().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return encoding_module.force_str(s, encoding, strings_only, errors)

    utils.inject_callable(encoding_module, "smart_text", smart_text)
    utils.inject_callable(encoding_module, "force_text", force_text)


@django1_40_bc_fixer()
def fix_deletion_utils_http_quote_utilities(utils):
    """Preserve aliases of urlib methods (quote, quote_plus, unquote, unquote_plus) in
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


@django1_40_bc_fixer()
def fix_deletion_utils_translation_ugettext_utilities(utils):
    """Preserve ugettext(), ugettext_lazy(), ugettext_noop(), ungettext(), and ungettext_lazy()
    as aliases of gettext methods
    """
    from django.utils import translation

    def ugettext_noop(message):
        """
        A legacy compatibility wrapper for Unicode handling on Python 2.
        Alias of gettext_noop() since Django 2.0.
        """
        warnings.warn(
            'django.utils.translation.ugettext_noop() is deprecated in favor of '
            'django.utils.translation.gettext_noop().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return translation.gettext_noop(message)

    def ugettext(message):
        """
        A legacy compatibility wrapper for Unicode handling on Python 2.
        Alias of gettext() since Django 2.0.
        """
        warnings.warn(
            'django.utils.translation.ugettext() is deprecated in favor of '
            'django.utils.translation.gettext().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return translation.gettext(message)

    def ungettext(singular, plural, number):
        """
        A legacy compatibility wrapper for Unicode handling on Python 2.
        Alias of ngettext() since Django 2.0.
        """
        warnings.warn(
            'django.utils.translation.ungettext() is deprecated in favor of '
            'django.utils.translation.ngettext().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return translation.ngettext(singular, plural, number)

    def ugettext_lazy(message):
        """
        A legacy compatibility wrapper for Unicode handling on Python 2. Has been
        Alias of gettext_lazy since Django 2.0.
        """
        warnings.warn(
            'django.utils.translation.ugettext_lazy() is deprecated in favor of '
            'django.utils.translation.gettext_lazy().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return translation.gettext_lazy(message)

    utils.inject_callable(translation, "ugettext_noop", ugettext_noop)
    utils.inject_callable(translation, "ugettext", ugettext)
    utils.inject_callable(translation, "ungettext", ungettext)
    utils.inject_callable(translation, "ugettext_lazy", ugettext_lazy)
