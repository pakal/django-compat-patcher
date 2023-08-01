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
    """Preserve _replace_entity() and _entity_re in django.utils.text module"""
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

