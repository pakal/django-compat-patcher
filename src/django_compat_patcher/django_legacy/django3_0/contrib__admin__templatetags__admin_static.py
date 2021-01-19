
from django.template import Library
from django.templatetags.static import static as _static
from django_compat_patcher.deprecation import RemovedInDjango30Warning, warnings

register = Library()


@register.simple_tag
def static(path):
    warnings.warn(
        '{% load admin_static %} is deprecated in favor of {% load static %}.',
        RemovedInDjango30Warning,
    )
    return _static(path)
