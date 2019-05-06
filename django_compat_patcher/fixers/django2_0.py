from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_compatibility_fixer

# for backward-compatibility fixers
django1_20_bc_fixer = partial(register_compatibility_fixer,
                              fixer_reference_version="2.0",
                              fixer_applied_from_django="2.0")


# This change should not be patched, since security issues could ensue:
# "Using User.is_authenticated() and User.is_anonymous() as methods rather than properties is no longer supported."


@django1_20_bc_fixer()
def fix_deletion_django_urls_RegexURLPattern_RegexURLResolver(utils):
    """
    Preserve RegexURLPattern and RegexURLResolver in django.urls, which disappeared due to DEP 0201.
    """
    import django.urls.resolvers
    from django.urls.resolvers import RegexPattern, URLPattern, URLResolver

    class RegexURLPattern(URLPattern):
        def __init__(self, pattern, *args, **kwargs):
            # we force is_endpoint else Warnings about "$" ends in regexes...
            URLPattern.__init__(self, RegexPattern(pattern, is_endpoint=True), *args, **kwargs)

    utils.inject_class(django.urls.resolvers, "RegexURLPattern", RegexURLPattern)
    utils.inject_class(django.urls, "RegexURLPattern", RegexURLPattern)

    class RegexURLResolver(URLResolver):
        def __init__(self, pattern, *args, **kwargs):
            URLResolver.__init__(self, RegexPattern(pattern), *args, **kwargs)
    utils.inject_class(django.urls.resolvers, "RegexURLResolver", RegexURLResolver)
    utils.inject_class(django.urls, "RegexURLResolver", RegexURLResolver)


@django1_20_bc_fixer()
def fix_deletion_django_core_urlresolvers(utils):
    """
    Preserve django.core.urlresolvers module, now replaced by django.urls.
    """
    from django import urls
    utils.inject_module("django.core.urlresolvers", urls)


@django1_20_bc_fixer()
def fix_deletion_django_template_library_assignment_tag(utils):
    """
    Preserve the assignment_tag() helper, superseded by simple_tag().
    """
    import django.template.library

    def assignment_tag(self, func=None, takes_context=None, name=None):
        utils.emit_warning(
            "assignment_tag() is deprecated. Use simple_tag() instead",
            RemovedInDjango20Warning,
            stacklevel=2,
        )
        return self.simple_tag(func, takes_context, name)
    utils.inject_callable(django.template.library.Library, "assignment_tag", assignment_tag)


@django1_20_bc_fixer()
def fix_deletion_django_utils_functional_allow_lazy(utils):
    """
    Preserve the allow_lazy() utility, superseded by keep_lazy().
    """
    import django.utils.functional
    def allow_lazy(func, *resultclasses):
        from django.utils.functional import keep_lazy
        utils.emit_warning(
            "django.utils.functional.allow_lazy() is deprecated in favor of "
            "django.utils.functional.keep_lazy()",
            RemovedInDjango20Warning, 2)
        return keep_lazy(*resultclasses)(func)
    utils.inject_callable(django.utils.functional, "allow_lazy", allow_lazy)


@django1_20_bc_fixer()
def fix_deletion_django_template_context_Context_has_key(utils):
    """
    Preserve the Context.has_key() utility, replaced by "in" operator use.
    """
    import django.template.context
    def has_key(self, key):
        utils.emit_warning(
            "%s.has_key() is deprecated in favor of the 'in' operator." % self.__class__.__name__,
            RemovedInDjango20Warning
        )
        return key in self
    utils.inject_callable(django.template.context.Context, "has_key", has_key)


@django1_20_bc_fixer()
def fix_deletion_django_views_i18n_javascript_and_json_catalog(utils):
    """
    Preserve the javascript_catalog() and json_catalog() i18n views, superseded by class-based views.
    """

    from django_compat_patcher.django_legacy.django2_0.views.i18n import \
        javascript_catalog, json_catalog, render_javascript_catalog, null_javascript_catalog

    import django.views.i18n
    utils.inject_callable(django.views.i18n, "javascript_catalog", javascript_catalog)
    utils.inject_callable(django.views.i18n, "json_catalog", json_catalog)
    utils.inject_callable(django.views.i18n, "render_javascript_catalog", render_javascript_catalog)
    utils.inject_callable(django.views.i18n, "null_javascript_catalog", null_javascript_catalog)
