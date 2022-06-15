from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_30_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="3.0",
    fixer_applied_from_version="3.0",
)


@django1_30_bc_fixer()
def fix_deletion_utils_six(utils):
    """Preserve the vendored copy of "six" compatibility utility, in django.utils,
    as well as the `six` import in django.utils.encoding"""
    import six
    utils.inject_import_alias(alias_name="django.utils.six", real_name="six")

    from django.utils import encoding
    if not hasattr(encoding, "six"):
        utils.inject_attribute(encoding, "six", six)


@django1_30_bc_fixer()
def fix_deletion_utils_upath_npath_abspathu(utils):
    """Preserve python2 path normalization functions."""

    from os.path import abspath as abspathu  # For backwards-compatibility in Django 2.0

    def upath(path):
        """Always return a unicode path (did something for Python 2)."""
        return path

    def npath(path):
        """
        Always return a native path, that is unicode on Python 3 and bytestring on
        Python 2. Noop for Python 3.
        """
        return path

    from django.utils import _os
    utils.inject_callable(_os, "abspathu", abspathu)
    utils.inject_callable(_os, "upath", upath)
    utils.inject_callable(_os, "npath", npath)


@django1_30_bc_fixer()
def fix_deletion_utils_decorators_ContextDecorator(utils):
    """Preserve django.utils.decorators.ContextDecorator, alias of contextlib.ContextDecorator."""
    from contextlib import ContextDecorator
    from django.utils import decorators
    utils.inject_class(decorators, "ContextDecorator", ContextDecorator)


@django1_30_bc_fixer()
def fix_deletion_utils_decorators_available_attrs(utils):
    """Preserve django.utils.decorators.available_attrs, which just returns functools.WRAPPER_ASSIGNMENTS."""

    def available_attrs(fn):  # For backwards compatibility in Django 2.0.
        """
        Return the list of functools-wrappable attributes on a callable.
        This was required as a workaround for https://bugs.python.org/issue3445
        under Python 2.
        """
        from functools import WRAPPER_ASSIGNMENTS
        return WRAPPER_ASSIGNMENTS

    from django.utils import decorators
    utils.inject_callable(decorators, "available_attrs", available_attrs)


@django1_30_bc_fixer()
def fix_deletion_utils_lru_cache_lru_cache(utils):
    """Preserve django.utils.lru_cache.lru_cache(), alias of functools.lru_cache(), and its containing module."""
    from ..django_legacy.django3_0 import lru_cache as django_lru_cache_module
    import django.utils

    utils.inject_module("django.utils.lru_cache", django_lru_cache_module)
    utils.inject_attribute(django.utils, "lru_cache", django_lru_cache_module)


@django1_30_bc_fixer()
def fix_deletion_utils_safestring_SafeBytes(utils):
    """Preserve django.utils.safestring.SafeBytes class."""
    from django.utils.safestring import SafeData, SafeText
    from django.utils import safestring

    class SafeBytes(bytes, SafeData):
        """
        A bytes subclass that has been specifically marked as "safe" (requires no
        further escaping) for HTML output purposes.

        Kept in Django 2.0 for usage by apps supporting Python 2. Shouldn't be used
        in Django anymore.
        """
        def __add__(self, rhs):
            """
            Concatenating a safe byte string with another safe byte string or safe
            string is safe. Otherwise, the result is no longer safe.
            """
            t = super(SafeBytes, self).__add__(rhs)
            if isinstance(rhs, SafeText):
                return SafeText(t)
            elif isinstance(rhs, SafeBytes):
                return SafeBytes(t)
            return t

    utils.inject_class(safestring, "SafeBytes", SafeBytes)


@django1_30_bc_fixer()
def fix_deletion_test_utils_str_prefix(utils):
    """Preserve django.test.utils.str_prefix class."""
    from django.test import utils as test_utils
    def str_prefix(s):
        return s % {'_': ''}
    utils.inject_callable(test_utils, "str_prefix", str_prefix)


@django1_30_bc_fixer()
def fix_deletion_test_utils_patch_logger(utils):
    """Preserve django.test.utils.patch_logger() context manager."""
    from contextlib import contextmanager
    import logging
    from django.test import utils as test_utils

    @contextmanager
    def patch_logger(logger_name, log_level, log_kwargs=False):
        """
        Context manager that takes a named logger and the logging level
        and provides a simple mock-like list of messages received.

        Use unittest.assertLogs() if you only need Python 3 support. This
        private API will be removed after Python 2 EOL in 2020 (#27753).
        """
        calls = []

        def replacement(msg, *args, **kwargs):
            call = msg % args
            calls.append((call, kwargs) if log_kwargs else call)
        logger = logging.getLogger(logger_name)
        orig = getattr(logger, log_level)
        setattr(logger, log_level, replacement)
        try:
            yield calls
        finally:
            setattr(logger, log_level, orig)
    utils.inject_callable(test_utils, "patch_logger", patch_logger)


@django1_30_bc_fixer()
def fix_deletion_utils_encoding_python_2_unicode_compatible(utils):
    """Preserve django.utils.encoding.python_2_unicode_compatible() class decorator."""
    import six
    from django.utils import encoding
    utils.inject_callable(encoding, "python_2_unicode_compatible", six.python_2_unicode_compatible)


@django1_30_bc_fixer()
def fix_deletion_utils_functional_curry(utils):
    """Preserve django.utils.functional.curry()function."""

    from django.utils import functional
    # You can't trivially replace this with `functools.partial` because this binds
    # to classes and returns bound instances, whereas functools.partial (on
    # CPython) is a type and its instances don't bind. --> see `functools.partialmethod` now!
    def curry(_curried_func, *args, **kwargs):
        def _curried(*moreargs, **morekwargs):
            allkwargs = dict(**kwargs)
            allkwargs.update(morekwargs)
            return _curried_func(*(args + moreargs), **allkwargs)
        return _curried

    utils.inject_callable(functional, "curry", curry)


@django1_30_bc_fixer()
def fix_deletion_shortcuts_render_to_response(utils):
    """Preserve django.shortcuts.render_to_response(), superseded by render()."""
    from django import shortcuts

    def render_to_response(template_name, context=None, content_type=None, status=None, using=None):
        """
        Return a HttpResponse whose content is filled with the result of calling
        django.template.loader.render_to_string() with the passed arguments.
        """
        warnings.warn(
            'render_to_response() is deprecated in favor of render(). It has the '
            'same signature except that it also requires a request.',
            RemovedInDjango30Warning, stacklevel=2,
        )
        from django.template import loader
        from django.http import HttpResponse
        content = loader.render_to_string(template_name, context, using=using)
        return HttpResponse(content, content_type, status)

    utils.inject_callable(shortcuts, "render_to_response", render_to_response)


@django1_30_bc_fixer()
def fix_deletion_http_request_HttpRequest_xreadlines(utils):
    """Preserve HttpRequest.xreadlines(), replaced by iteration on request object."""
    from django.http import HttpRequest
    def xreadlines(self):
        warnings.warn(
            'HttpRequest.xreadlines() is deprecated in favor of iterating the '
            'request.', RemovedInDjango30Warning, stacklevel=2,
        )
        for line in self:
            yield line
    utils.inject_callable(HttpRequest, "xreadlines", xreadlines)


@django1_30_bc_fixer()
def fix_deletion_utils_http_cookie_date(utils):
    """Preserve django.utils.http.cookie_date(), superseded by http_date()."""
    from django.utils import http

    def cookie_date(epoch_seconds=None):
        """
        Format the time to ensure compatibility with Netscape's cookie standard.

        `epoch_seconds` is a floating point number expressed in seconds since the
        epoch, in UTC - such as that outputted by time.time(). If set to None, it
        defaults to the current time.

        Output a string in the format 'Wdy, DD-Mon-YYYY HH:MM:SS GMT'.
        """
        from email.utils import formatdate
        warnings.warn(
            'cookie_date() is deprecated in favor of http_date(), which follows '
            'the format of the latest RFC.',
            RemovedInDjango30Warning, stacklevel=2,
        )
        rfcdate = formatdate(epoch_seconds)
        return '%s-%s-%s GMT' % (rfcdate[:7], rfcdate[8:11], rfcdate[12:25])

    utils.inject_callable(http, "cookie_date", cookie_date)


@django1_30_bc_fixer()
def fix_deletion_contrib_staticfiles_templatetags_and_admin_static(utils):
    """Preserve staticfiles and admin_static template tag libraries."""

    utils.inject_import_alias(
        "django.contrib.admin.templatetags.admin_static",
        real_name="django_compat_patcher.django_legacy.django3_0.contrib__admin__templatetags__admin_static")
    utils.inject_import_alias(
        "django.contrib.staticfiles.templatetags",
        real_name="django_compat_patcher.django_legacy.django3_0.contrib__staticfiles__templatetags__staticfiles")

    from django.template.backends import django as django_templates

    _old_get_installed_libraries = django_templates.get_installed_libraries

    # Original uses pkgutil.walk_packages() so it won't see our injected template
    def get_installed_libraries(*args, **kwargs):
        libraries = _old_get_installed_libraries(*args, **kwargs)
        libraries.update({
            "admin_static": "django.contrib.admin.templatetags.admin_static",
            "staticfiles": "django.contrib.staticfiles.templatetags.staticfiles",
        })
        return libraries

    utils.inject_callable(django_templates, "get_installed_libraries", get_installed_libraries)


@django1_30_bc_fixer()
def fix_behaviour_db_models_query_QuerySet_earliest_latest(utils):
    """Preserve the field_name keyword argument to QuerySet.earliest() and latest()"""

    from django.db.models.query import QuerySet

    _original_earliest = QuerySet._earliest

    def _earliest(self, *fields, **kwargs):
        """
        Return the earliest object according to fields (if given) or by the
        model's Meta.get_latest_by.
        """

        field_name = kwargs.pop("field_name", None)

        if fields and field_name is not None:
            raise ValueError('Cannot use both positional arguments and the field_name keyword argument.')

        if field_name is not None:
            warnings.warn(
                'The field_name keyword argument to earliest() and latest() '
                'is deprecated in favor of passing positional arguments.',
                RemovedInDjango30Warning,
            )
            fields = (field_name,)

        return _original_earliest(self, *fields, **kwargs)

    def earliest(self, *fields, **kwargs):
        return self._earliest(*fields, **kwargs)

    def latest(self, *fields, **kwargs):
        return self.reverse()._earliest(*fields, **kwargs)

    utils.inject_callable(QuerySet, "_earliest", _earliest)  # Used by all
    utils.inject_callable(QuerySet, "earliest", earliest)
    utils.inject_callable(QuerySet, "latest", latest)
