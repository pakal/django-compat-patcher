from __future__ import absolute_import, print_function, unicode_literals

import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_fix_deletion_templatetags_future():
    from django.templatetags.future import cycle, firstof


def test_fix_deletion_template_defaulttags_ssi():
    from django.template.defaulttags import ssi
