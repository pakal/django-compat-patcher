from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_compatibility_fixer

# for backward-compatibility fixers
django1_21_bc_fixer = partial(register_compatibility_fixer,
                              fixer_reference_version="2.1",
                              fixer_applied_from_django="2.1")


@django1_21_bc_fixer()
def fix_deletion_django_utils_translation_string_concat(utils):
    """
    Preserve django.utils.translation.string_concat(), superseded by django.utils.text.format_lazy().
    """
    import django.utils.translation
    from django.utils.functional import lazy

    def _string_concat(*strings):
        """
        Lazy variant of string concatenation, needed for translations that are
        constructed from multiple parts.
        """
        utils.emit_warning(
            'django.utils.translate.string_concat() is deprecated in '
            'favor of django.utils.text.format_lazy().',
            RemovedInDjango21Warning, stacklevel=2)
        return ''.join(str(s) for s in strings)

    string_concat = lazy(_string_concat, str)
    utils.inject_callable(django.utils.translation, "string_concat", string_concat)
