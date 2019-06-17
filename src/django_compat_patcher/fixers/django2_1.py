from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_21_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="2.1",
    fixer_applied_from_version="2.1",
)


@django1_21_bc_fixer()
def fix_deletion_utils_translation_string_concat(utils):
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
            "django.utils.translate.string_concat() is deprecated in "
            "favor of django.utils.text.format_lazy().",
            RemovedInDjango21Warning,
            stacklevel=2,
        )
        return "".join(str(s) for s in strings)

    string_concat = lazy(_string_concat, str)
    utils.inject_callable(django.utils.translation, "string_concat", string_concat)


@django1_21_bc_fixer()
def fix_behaviour_widget_render_forced_renderer(utils):
    """
    Restore the behaviour where the "renderer" parameter of Widget.render() may not be supported by subclasses.
    """
    from django.forms.boundfield import BoundField

    original_as_widget = BoundField.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):

        widget = widget or self.field.widget

        from django.utils.inspect import func_supports_parameter, func_accepts_kwargs

        if not (
            func_supports_parameter(widget.render, "renderer")
            or func_accepts_kwargs(widget.render)
        ):
            original_widget_render = widget.render

            utils.emit_warning(
                "Add the `renderer` argument to the render() method of %s. "
                "It will be mandatory in Django 2.1." % widget.__class__,
                RemovedInDjango21Warning,
                stacklevel=2,
            )

            def instance_render(name, value, attrs=None, renderer=None):
                del renderer  # restore non-mandatory support for this parameter
                return original_widget_render(name=name, value=value, attrs=attrs)

            utils.inject_callable(
                widget, "render", instance_render
            )  # beware, function stored in INSTANCE

        return original_as_widget(
            self, widget=widget, attrs=attrs, only_initial=only_initial
        )

    utils.inject_callable(BoundField, "as_widget", as_widget)
