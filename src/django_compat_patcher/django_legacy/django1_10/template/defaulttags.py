import os

from django.conf import settings
from django.template.base import (
    Node, Template, TemplateSyntaxError,
)

from django_compat_patcher.deprecation import *


def include_is_allowed(filepath, allowed_include_roots):
    filepath = os.path.abspath(filepath)
    for root in allowed_include_roots:
        if filepath.startswith(root):
            return True
    return False


class SsiNode(Node):
    def __init__(self, filepath, parsed):
        self.filepath = filepath
        self.parsed = parsed

    def render(self, context):
        filepath = self.filepath.resolve(context)

        if not include_is_allowed(filepath, context.template.engine.allowed_include_roots):
            if settings.DEBUG:
                return "[Didn't have permission to include file]"
            else:
                return ''  # Fail silently for invalid includes.
        try:
            with open(filepath, 'r') as fp:
                output = fp.read()
        except IOError:
            output = ''
        if self.parsed:
            try:
                t = Template(output, name=filepath, engine=context.template.engine)
                return t.render(context)
            except TemplateSyntaxError as e:
                if settings.DEBUG:
                    return "[Included template had syntax error: %s]" % e
                else:
                    return ''  # Fail silently for invalid included templates.
        return output


#@register.tag
def ssi(parser, token):
    """
    Outputs the contents of a given file into the page.

    Like a simple "include" tag, the ``ssi`` tag includes the contents
    of another file -- which must be specified using an absolute path --
    in the current page::

        {% ssi "/home/html/ljworld.com/includes/right_generic.html" %}

    If the optional "parsed" parameter is given, the contents of the included
    file are evaluated as template code, with the current context::

        {% ssi "/home/html/ljworld.com/includes/right_generic.html" parsed %}
    """
    warnings.warn(
        "The {% ssi %} tag is deprecated. Use the {% include %} tag instead.",
        RemovedInDjango110Warning,
    )

    bits = token.split_contents()
    parsed = False
    if len(bits) not in (2, 3):
        raise TemplateSyntaxError("'ssi' tag takes one argument: the path to"
                                  " the file to be included")
    if len(bits) == 3:
        if bits[2] == 'parsed':
            parsed = True
        else:
            raise TemplateSyntaxError("Second (optional) argument to %s tag"
                                      " must be 'parsed'" % bits[0])
    filepath = parser.compile_filter(bits[1])
    return SsiNode(filepath, parsed)

