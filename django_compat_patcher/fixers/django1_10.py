from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from django.core.exceptions import ImproperlyConfigured
from django.utils import six

from ..deprecation import *
from ..registry import register_compatibility_fixer

# for backward-compatibility fixers
django1_10_bc_fixer = partial(register_compatibility_fixer,
                              fixer_reference_version="1.10",
                              fixer_applied_from_django="1.10")


def _get_url_utils():
    """
    Get URL utilities through versions, despite them being moved and refactored (with new "path()" syntax).
    """
    try:
        from django.urls import get_callable, RegexURLPattern, URLPattern, RegexURLResolver, URLResolver, NoReverseMatch
    except ImportError:
        # previously, there was no "RoutePattern vs RegexPattern"
        from django.core.urlresolvers import get_callable, RegexURLPattern, RegexURLPattern as URLPattern, RegexURLResolver, RegexURLResolver as URLResolver, NoReverseMatch   # old location
    return get_callable, RegexURLPattern, URLPattern, RegexURLResolver, URLResolver, NoReverseMatch


@register_compatibility_fixer(fixer_reference_version="1.10", fixer_applied_upto_django="1.10")
def fix_incoming_urls_submodule(utils):
    """
    Put a forward compatibility import path for django.urls, which replaces django.core.urlresolvers
    """
    from django.core import urlresolvers
    utils.inject_module("django.urls", urlresolvers)


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
def fix_behaviour_urls_resolvers_RegexURLPattern(utils):
    """
    Restore support for dotted-string view parameter in RegexURLPattern, instead passing a view object.
    """

    get_callable, RegexURLPattern, URLPattern, RegexURLResolver, URLResolver, NoReverseMatch = _get_url_utils()
    del RegexURLPattern  # we work on the common URLPattern class

    @property
    def callback(self):
        callback = self.__dict__["callback"]  # bypass descriptor
        if isinstance(callback, six.string_types):
            callback_obj = get_callable(callback)
        else:
            callback_obj = callback
        return callback_obj

    @callback.setter
    def callback(self, value):
        self.__dict__["callback"] = value  # bypass descriptor

    # we inject a DATA-DESCRIPTOR, so it'll be accessed in prority
    # over "self.callback" instance attribute
    utils.inject_attribute(URLPattern, "callback", callback)

    def add_prefix(self, prefix):
        """
        Adds the prefix string to a string-based callback.
        """
        callback = self.__dict__["callback"]
        if not prefix or not isinstance(callback, six.string_types):
            return
        self.callback = prefix + '.' + callback
    utils.inject_callable(URLPattern, "add_prefix", add_prefix)

    original_lookup_str = URLPattern.lookup_str
    @property  # not cached...
    def lookup_str(self):
        callback = self.__dict__["callback"]
        if isinstance(callback, six.string_types):
            # no need for warning, already emitted above
            return callback  # already a dotted path to view
        return original_lookup_str.__get__(self, self.__class__)
    utils.inject_attribute(URLPattern, "lookup_str", lookup_str)


@django1_10_bc_fixer()
def fix_behaviour_core_urlresolvers_reverse_with_prefix(utils):
    """
    Preserve the ability to call urlresolver on dotted string view,
    instead of explicit view name.
    """
    from django.utils.functional import cached_property
    get_callable, RegexURLPattern, URLPattern, RegexURLResolver, URLResolver, NoReverseMatch = _get_url_utils()
    del RegexURLResolver  # we patch the common URLResolver class

    original_reverse_with_prefix = URLResolver._reverse_with_prefix

    def _reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs):
        original_lookup = lookup_view
        try:
            if self._is_callback(lookup_view):
                utils.emit_warning(
                    'Reversing by dotted path is deprecated (%s).' % original_lookup,
                    RemovedInDjango110Warning, stacklevel=3
                )
                lookup_view = get_callable(lookup_view)
        except (ImportError, AttributeError) as e:
            raise NoReverseMatch("Error importing '%s': %s." % (lookup_view, e))
        return original_reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs)
    utils.inject_callable(URLResolver, "_reverse_with_prefix", _reverse_with_prefix)



@django1_10_bc_fixer()
def fix_behaviour_conf_urls_url(utils):
    """
    Support passing views to url() as dotted strings instead of view objects.
    """
    get_callable, RegexURLPattern, URLPattern, RegexURLResolver, URLResolver, NoReverseMatch = _get_url_utils()
    del URLPattern  # we stick to the old "regex-only" URL system

    from django.conf import urls

    def url(regex, view, kwargs=None, name=None, prefix=''):
        if isinstance(view, (list, tuple)):
            # For include(...) processing.
            urlconf_module, app_name, namespace = view
            return RegexURLResolver(regex, urlconf_module, kwargs, app_name=app_name, namespace=namespace)
        else:
            if isinstance(view, six.string_types):
                utils.emit_warning(
                    'Support for string view arguments to url() is deprecated and '
                    'will be removed in Django 1.10 (got %s). Pass the callable '
                    'instead.' % view,
                    RemovedInDjango110Warning, stacklevel=2
                )
                if not view:
                    raise ImproperlyConfigured('Empty URL pattern view name not permitted (for pattern %r)' % regex)
                if prefix:
                    view = prefix + '.' + view
            return RegexURLPattern(regex, view, kwargs, name)
    assert callable(urls.url)
    utils.inject_callable(urls, "url", url)


@django1_10_bc_fixer()
def fix_deletion_conf_urls_patterns(utils):
    """
    Preserve the patterns() builder for django urls.
    """
    from django.conf import urls
    get_callable, RegexURLPattern, URLPattern, RegexURLResolver, URLResolver, NoReverseMatch = _get_url_utils()
    del URLPattern  # we stick to the old "regex-only" URL system

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
                t = urls.url(prefix=prefix, *t)
            elif isinstance(t, RegexURLPattern):
                t.add_prefix(prefix)
            pattern_list.append(t)
        return pattern_list
    utils.inject_callable(urls, "patterns", patterns)

    urls.__all__.append(str("patterns"))  # so that star imports work fine


@django1_10_bc_fixer()
def fix_behaviour_template_smartif_OPERATORS_equals(utils):
    """
    Preserve support for a single '=' sign in {% if %} tag.
    """
    from django.template import smartif
    smartif.OPERATORS['='] = smartif.OPERATORS['==']  # operator alias

 

''' REQUIRES PYTHON >= 3.3
@django1_10_bc_fixer()
def fix_deletion_core_context_processors(utils):
    """
    Keep django.core.context_processors middlewares as aliases for
    those of django.template.context_processors.
    """
    from .. import import_proxifier
    import_proxifier.install_module_alias_finder()  # idempotent
    import_proxifier.register_module_alias(module_alias="django.core.context_processors middlewares",
                                           real_module="django.template.context_processors")
'''
