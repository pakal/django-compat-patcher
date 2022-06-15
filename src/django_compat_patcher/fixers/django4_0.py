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
    urls.__all__.append("url")


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

    def ungettext_lazy(singular, plural, number=None):
        """
        A legacy compatibility wrapper for Unicode handling on Python 2.
        An alias of ungettext_lazy() since Django 2.0.
        """
        warnings.warn(
            'django.utils.translation.ungettext_lazy() is deprecated in favor of '
            'django.utils.translation.ngettext_lazy().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return translation.ngettext_lazy(singular, plural, number)

    utils.inject_callable(translation, "ugettext_noop", ugettext_noop)
    utils.inject_callable(translation, "ugettext", ugettext)
    utils.inject_callable(translation, "ungettext", ungettext)
    utils.inject_callable(translation, "ugettext_lazy", ugettext_lazy)
    utils.inject_callable(translation, "ungettext_lazy", ungettext_lazy)


@django1_40_bc_fixer()
def fix_deletion_utils_text_unescape_entities(utils):
    """Preserve django.utils.text.unescape_entities() as an alias of html.unescape()"""
    from django.utils.functional import keep_lazy_text
    from django.utils import text as text_module

    @keep_lazy_text
    def unescape_entities(text):
        warnings.warn(
            'django.utils.text.unescape_entities() is deprecated in favor of '
            'html.unescape().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return text_module._entity_re.sub(text_module._replace_entity, str(text))

    utils.inject_callable(text_module, "unescape_entities", unescape_entities)


@django1_40_bc_fixer()
def fix_deletion_utils_http_is_safe_url(utils):
    """Preserve django.utils.http.is_safe_url() as an alias to url_has_allowed_host_and_scheme()"""
    from django.utils import http

    def is_safe_url(url, allowed_hosts, require_https=False):
        warnings.warn(
            'django.utils.http.is_safe_url() is deprecated in favor of '
            'url_has_allowed_host_and_scheme().',
            RemovedInDjango40Warning, stacklevel=2,
        )
        return http.url_has_allowed_host_and_scheme(url, allowed_hosts, require_https)

    utils.inject_callable(http, "is_safe_url", is_safe_url)


@django1_40_bc_fixer()
def fix_behaviour_dispatch_dispatcher_Signal_providing_args(utils):
    """Keep accepting the `providing_args` init argument of Signal instances."""

    from django.dispatch.dispatcher import Signal

    original_signal_init = Signal.__init__

    def __patched_Signal__init__(self, providing_args=None, use_caching=False):
        if providing_args is not None:
            warnings.warn(
                'The providing_args argument is deprecated. As it is purely '
                'documentational, it has no replacement. If you rely on this '
                'argument as documentation, you can move the text to a code '
                'comment or docstring.',
                RemovedInDjango40Warning, stacklevel=2,
            )
        original_signal_init(self, use_caching=use_caching)

    utils.inject_callable(Signal, "__init__", __patched_Signal__init__)


@django1_40_bc_fixer()
def fix_deletion_db_models_query_utils_InvalidQuery(utils):
    """Preserve the django.db.models.query_utils.InvalidQuery exception class"""
    from django.core.exceptions import FieldDoesNotExist, FieldError
    from django.db.models import query_utils

    class InvalidQueryType(type):
        @property
        def _subclasses(self):
            return (FieldDoesNotExist, FieldError)

        def __warn(self):
            warnings.warn(
                'The InvalidQuery exception class is deprecated. Use '
                'FieldDoesNotExist or FieldError instead.',
                category=RemovedInDjango40Warning,
                stacklevel=4,
            )

        def __instancecheck__(self, instance):
            self.__warn()
            return isinstance(instance, self._subclasses) or super().__instancecheck__(instance)

        def __subclasscheck__(self, subclass):
            self.__warn()
            return issubclass(subclass, self._subclasses) or super().__subclasscheck__(subclass)

    class InvalidQuery(Exception, metaclass=InvalidQueryType):
        pass

    utils.inject_class(query_utils, "FieldDoesNotExist", FieldDoesNotExist)  # Import was removed
    utils.inject_class(query_utils, "InvalidQuery", InvalidQuery)


@django1_40_bc_fixer()
def fix_deletion_http_request_HttpRequest_is_ajax(utils):
    """Preserve the HttpRequest.is_ajax() method"""
    from django.http.request import HttpRequest

    def is_ajax(self):
        warnings.warn(
            'request.is_ajax() is deprecated. See Django 3.1 release notes '
            'for more details about this deprecation.',
            RemovedInDjango40Warning,
            stacklevel=2,
        )
        return self.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    utils.inject_callable(HttpRequest, "is_ajax", is_ajax)


@django1_40_bc_fixer()
def fix_behaviour_utils_crypto_get_random_string_length(utils):
    """Allow get_random_string() call without length argument (defaults to length=12)"""
    from django.utils import crypto
    original_get_random_string = crypto.get_random_string

    NOT_PROVIDED = object()
    def get_random_string(length=NOT_PROVIDED, *args, **kwargs):
        length = length if length is not NOT_PROVIDED else 12
        return original_get_random_string(length, *args, **kwargs)

    utils.inject_callable(crypto, "get_random_string", get_random_string)


@django1_40_bc_fixer()
def fix_deletion_contrib_postgres_forms_jsonb(utils):
    """
    Preserve django.contrib.postgres.forms.JSONField and its jsonb source module
    """
    import django.utils
    from django_compat_patcher.django_legacy.django4_0 import contrib__postgres__forms__jsonb
    import django.contrib.postgres.forms

    utils.inject_module("django.contrib.postgres.forms.jsonb", contrib__postgres__forms__jsonb)
    utils.inject_attribute(django.contrib.postgres.forms, "jsonb", contrib__postgres__forms__jsonb)

    # We restore the "from .jsonb import *" in postgres.forms module
    utils.inject_class(django.contrib.postgres.forms, "JSONField",
                           contrib__postgres__forms__jsonb.JSONField)


@django1_40_bc_fixer()
def fix_deletion_contrib_postgres_fields_jsonb(utils):
    """Preserve django.contrib.postgres.fields.jsonb.KeyTransform/KeyTextTransform as aliases
    to django.db.models.fields.json objects"""
    from django.db.models.fields.json import (
        KeyTextTransform as BuiltinKeyTextTransform,
        KeyTransform as BuiltinKeyTransform,
    )

    class KeyTransform(BuiltinKeyTransform):
        def __init__(self, *args, **kwargs):
            warnings.warn(
                'django.contrib.postgres.fields.jsonb.KeyTransform is deprecated '
                'in favor of django.db.models.fields.json.KeyTransform.',
                RemovedInDjango40Warning, stacklevel=2,
            )
            super().__init__(*args, **kwargs)

    class KeyTextTransform(BuiltinKeyTextTransform):
        def __init__(self, *args, **kwargs):
            warnings.warn(
                'django.contrib.postgres.fields.jsonb.KeyTextTransform is '
                'deprecated in favor of '
                'django.db.models.fields.json.KeyTextTransform.',
                RemovedInDjango40Warning, stacklevel=2,
            )
            super().__init__(*args, **kwargs)

    from django.contrib.postgres.fields import jsonb
    utils.inject_class(jsonb, "KeyTransform", KeyTransform)
    utils.inject_class(jsonb, "KeyTextTransform", KeyTextTransform)


@django1_40_bc_fixer()
def fix_deletion_template_defaulttags_ifequal_ifnotequal(utils):
    """Preserve {% ifequal %} and {% ifnotequal %} builtin template tags"""

    from django.template import TemplateSyntaxError
    from django.template import NodeList, Node
    from django.template.defaulttags import register

    class IfEqualNode(Node):
        # RemovedInDjango40Warning.
        child_nodelists = ('nodelist_true', 'nodelist_false')

        def __init__(self, var1, var2, nodelist_true, nodelist_false, negate):
            self.var1, self.var2 = var1, var2
            self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
            self.negate = negate

        def __repr__(self):
            return '<%s>' % self.__class__.__name__

        def render(self, context):
            val1 = self.var1.resolve(context, ignore_failures=True)
            val2 = self.var2.resolve(context, ignore_failures=True)
            if (self.negate and val1 != val2) or (not self.negate and val1 == val2):
                return self.nodelist_true.render(context)
            return self.nodelist_false.render(context)

    def do_ifequal(parser, token, negate):
        # RemovedInDjango40Warning.
        bits = list(token.split_contents())
        if len(bits) != 3:
            raise TemplateSyntaxError("%r takes two arguments" % bits[0])
        end_tag = 'end' + bits[0]
        nodelist_true = parser.parse(('else', end_tag))
        token = parser.next_token()
        if token.contents == 'else':
            nodelist_false = parser.parse((end_tag,))
            parser.delete_first_token()
        else:
            nodelist_false = NodeList()
        val1 = parser.compile_filter(bits[1])
        val2 = parser.compile_filter(bits[2])
        return IfEqualNode(val1, val2, nodelist_true, nodelist_false, negate)

    @register.tag
    def ifequal(parser, token):
        """
        Output the contents of the block if the two arguments equal each other.

        Examples::

            {% ifequal user.id comment.user_id %}
                ...
            {% endifequal %}

            {% ifnotequal user.id comment.user_id %}
                ...
            {% else %}
                ...
            {% endifnotequal %}
        """
        warnings.warn(
            'The {% ifequal %} template tag is deprecated in favor of {% if %}.',
            RemovedInDjango40Warning,
        )
        return do_ifequal(parser, token, False)

    @register.tag
    def ifnotequal(parser, token):
        """
        Output the contents of the block if the two arguments are not equal.
        See ifequal.
        """
        warnings.warn(
            'The {% ifnotequal %} template tag is deprecated in favor of '
            '{% if %}.',
            RemovedInDjango40Warning,
        )
        return do_ifequal(parser, token, True)

    from django.template import defaulttags
    utils.inject_class(defaulttags, "IfEqualNode", IfEqualNode)
    utils.inject_callable(defaulttags, "do_ifequal", do_ifequal)
    utils.inject_callable(defaulttags, "ifequal", ifequal)
    utils.inject_callable(defaulttags, "ifnotequal", ifnotequal)


@django1_40_bc_fixer()
def fix_deletion_forms_models_ModelMultipleChoiceField_error_messages_list_entry(utils):
    """Preserve "list" error message for ModelMultipleChoiceField, replaced by "invalid_list"
    """

    from django.forms.models import ModelMultipleChoiceField
    original_ModelMultipleChoiceField_init = ModelMultipleChoiceField.__init__

    def __patched_ModelMultipleChoiceField__init__(self, *args, **kwargs):
        original_ModelMultipleChoiceField_init(self, *args, **kwargs)
        if self.error_messages.get('list') is not None:
            warnings.warn(
                "The 'list' error message key is deprecated in favor of "
                "'invalid_list'.",
                RemovedInDjango40Warning, stacklevel=2,
            )
            self.error_messages['invalid_list'] = self.error_messages['list']

    utils.inject_callable(ModelMultipleChoiceField, "__init__", __patched_ModelMultipleChoiceField__init__)


@django1_40_bc_fixer(fixer_delayed=True)
def fix_behaviour_middleware_get_response_parameter_nullability(utils):
    """Keep `get_response` argument optional and nullable in middleware classes"""

    # We patch subclasses to make the get_response parameters optional, and we give it
    # a non-None value so that MiddlewareMixin doesn't raise a ValueError('get_response must be provided.')

    def fake_get_response(*args, **kwargs):
        raise NotImplementedError("You must provide a get_response callback to your middleware")

    def _patch_middleware_class_init(cls):
        original_cls_init = cls.__init__

        def __patched_init__(self, get_response=None, *args, **kwargs):
            if get_response is None:
                get_response = fake_get_response

            original_cls_init(self, get_response, *args, **kwargs)

        utils.inject_callable(cls, "__init__", __patched_init__)

    from django.utils.deprecation import MiddlewareMixin
    from django.contrib.sessions.middleware import SessionMiddleware
    from django.middleware.cache import UpdateCacheMiddleware, FetchFromCacheMiddleware, CacheMiddleware
    from django.middleware.security import SecurityMiddleware

    from django.conf import settings

    middleware_classes = [MiddlewareMixin, #RedirectFallbackMiddleware,
                    SessionMiddleware, UpdateCacheMiddleware, FetchFromCacheMiddleware,
                    CacheMiddleware, SecurityMiddleware]

    if "django.contrib.redirects" in settings.INSTALLED_APPS:
        from django.contrib.redirects.middleware import RedirectFallbackMiddleware
        middleware_classes.append(RedirectFallbackMiddleware)

    for middleware_classe in middleware_classes:
        _patch_middleware_class_init(middleware_classe)


