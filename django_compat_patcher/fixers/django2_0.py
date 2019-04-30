from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_compatibility_fixer

# for backward-compatibility fixers
django1_20_bc_fixer = partial(register_compatibility_fixer,
                              fixer_reference_version="2.0",
                              fixer_applied_from_django="2.0")


@django1_20_bc_fixer()
def fix_deletion_django_urls_RegexURLPattern_RegexURLResolver(utils):
    """
    Preserve RegexURLPattern and RegexURLResolver in django.urls, which disappeared due to DEP 0201.
    """
    import django.urls.resolvers
    from django.urls.resolvers import RegexPattern, URLPattern, URLResolver

    class RegexURLPattern(URLPattern):
        def __init__(self, pattern, *args, **kwargs):
            URLPattern.__init__(self, RegexPattern(pattern), *args, **kwargs)

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