from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_41_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="4.1",
    fixer_applied_from_version="4.1",
)


@django1_41_bc_fixer()
def fix_deletion_utils_text_replace_entity(utils):
    """Preserve undocumented _replace_entity() and _entity_re in django.utils.text module"""
    import html.entities
    from django.utils.regex_helper import _lazy_re_compile
    from django.utils import text

    def _replace_entity(match):
        text = match[1]
        if text[0] == '#':
            text = text[1:]
            try:
                if text[0] in 'xX':
                    c = int(text[1:], 16)
                else:
                    c = int(text)
                return chr(c)
            except ValueError:
                return match[0]
        else:
            try:
                return chr(html.entities.name2codepoint[text])
            except KeyError:
                return match[0]

    _entity_re = _lazy_re_compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")

    utils.inject_callable(text, "_replace_entity", _replace_entity)
    utils.inject_attribute(text, "_entity_re", _entity_re)


@django1_41_bc_fixer()
def fix_behaviour_core_validators_EmailValidator_whitelist(utils):
    """Preserve whitelist parameter of EmailValidator, superseded by allowlist"""
    from django.core.validators import EmailValidator
    original_EmailValidator_init = EmailValidator.__init__

    @property
    def domain_whitelist(self):
        utils.emit_warning(
            'The domain_whitelist attribute is deprecated in favor of '
            'domain_allowlist.',
            RemovedInDjango41Warning,
            stacklevel=2,
        )
        return self.domain_allowlist

    @domain_whitelist.setter
    def domain_whitelist(self, allowlist):
        utils.emit_warning(
            'The domain_whitelist attribute is deprecated in favor of '
            'domain_allowlist.',
            RemovedInDjango41Warning,
            stacklevel=2,
        )
        self.domain_allowlist = allowlist

    def __init__EmailValidator__(self, message=None, code=None, allowlist=None, *, whitelist=None):
        if whitelist is not None:
            allowlist = whitelist
            warnings.warn(
                'The whitelist argument is deprecated in favor of allowlist.',
                RemovedInDjango41Warning,
                stacklevel=2,
            )
        original_EmailValidator_init(self, message=message, code=code, allowlist=allowlist)

    utils.inject_attribute(EmailValidator, "domain_whitelist", domain_whitelist)
    utils.inject_callable(EmailValidator, "__init__", __init__EmailValidator__)


@django1_41_bc_fixer()
def fix_behaviour_views_static_was_modified_since(utils):
    """Preserve (but ignore) the 'size' parameter of was_modified_since()"""

    import django.views.static
    original_was_modified_since = django.views.static.was_modified_since

    def _was_modified_since(header=None, mtime=0, size=0):
        del size  # About nobody uses HTTP_IF_MODIFIED_SINCE with "length" subparameter
        return original_was_modified_since(header=header, mtime=mtime)

    utils.inject_callable(django.views.static, "was_modified_since", _was_modified_since)
