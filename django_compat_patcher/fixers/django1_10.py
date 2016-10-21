from __future__ import absolute_import, print_function, unicode_literals

import warnings
from functools import partial

from django.utils import six

from ..deprecation import *
from ..registry import register_compatibility_fixer

# for backward-compatibility fixers
django1_10_bc_fixer = partial(register_compatibility_fixer,
                              fixer_reference_version="1.10",
                              fixer_applied_from_django="1.10")


@django1_10_bc_fixer()
def fix_deletion_templatetags_future(utils):
    """
    Preserve the "future" templatetags library, with its improved `firstof` and `cycle` tags.
    """
    import django.templatetags
    from ..django_legacy.django1_10.templatetags import future
    utils.inject_module("django.templatetags.future", future)
    utils.inject_attribute(django.templatetags, "future", future)

    from django.template.backends import django as django_templates
    _old_get_installed_libraries = django_templates.get_installed_libraries

    def get_installed_libraries():
        libraries = _old_get_installed_libraries()  # tries real __import__() calls on submodules
        libraries["future"] = "django.templatetags.future"
        # print(">>>>> FINAL libraries", libraries)
        return libraries

    utils.inject_callable(django_templates, "get_installed_libraries", get_installed_libraries)


@django1_10_bc_fixer()
def fix_deletion_template_defaulttags_ssi(utils):
    """
    Preserve the "ssi" default template tag.
    """
    import django.template.defaulttags
    from ..django_legacy.django1_10.template import defaulttags

    utils.inject_callable(django.template.defaulttags, "include_is_allowed", defaulttags.include_is_allowed)
    utils.inject_class(django.template.defaulttags, "SsiNode", defaulttags.SsiNode)
    utils.inject_callable(django.template.defaulttags, "ssi", defaulttags.ssi)
    django.template.defaulttags.register.tag(defaulttags.ssi)

    from django.template.engine import Engine
    _old_init = Engine.__init__

    def __init__(self, dirs=None, app_dirs=False, allowed_include_roots=None, **kwargs):
        if allowed_include_roots is None:
            allowed_include_roots = []
        if isinstance(allowed_include_roots, six.string_types):
            raise ImproperlyConfigured(
                "allowed_include_roots must be a tuple, not a string.")
        self.allowed_include_roots = allowed_include_roots
        _old_init(self, dirs=dirs, app_dirs=app_dirs, **kwargs)

    utils.inject_callable(Engine, "__init__", __init__)


@django1_10_bc_fixer()
def fix_deletion_conf_urls_patterns(utils):
    """
    Preserve the patterns() builder for django urls.
    """
    from django.core.urlresolvers import RegexURLPattern
    from django.conf.urls import url
    from django.conf import urls

    def add_prefix(self, prefix):
        """
        Adds the prefix string to a string-based callback.
        """
        if not prefix or not hasattr(self, '_callback_str'):
            return
        self._callback_str = prefix + '.' + self._callback_str
    utils.inject_callable(RegexURLPattern, "add_prefix", add_prefix)

    def patterns(prefix, *args):
        utils.emit_warning(
            'django.conf.urls.patterns() is deprecated and will be removed in '
            'Django 1.10. Update your urlpatterns to be a list of '
            'django.conf.urls.url() instances instead.',
            RemovedInDjango110Warning, stacklevel=2
        )
        pattern_list = []
        for t in args:
            if isinstance(t, (list, tuple)):
                t = url(prefix=prefix, *t)
            elif isinstance(t, RegexURLPattern):
                t.add_prefix(prefix)
            pattern_list.append(t)
        return pattern_list
    utils.inject_callable(urls, "patterns", patterns)
