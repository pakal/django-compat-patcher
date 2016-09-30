

from ..registry import register_backwards_compatibility_fixer


@register_backwards_compatibility_fixer()
def keep_templatetags_future_url(utils):
    from django.template import defaulttags
    from django.templatetags import future
    new_tag = utils.inject_function_alias(defaulttags, "url",
                                          future, "url")
    future.register.tag(new_tag)
