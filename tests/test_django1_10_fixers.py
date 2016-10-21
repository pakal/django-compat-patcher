from __future__ import absolute_import, print_function, unicode_literals

import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_fix_deletion_templatetags_future():
    from django.templatetags.future import cycle, firstof
    assert False


def test_fix_deletion_template_defaulttags_ssi():
    # already tested in "test_fix_deletion_templatetags_future_ssi()"
    pass
    ''' TODO TEST THIS
    @ignore_warnings(category=RemovedInDjango110Warning)
    @setup({'firstof11': '{% load firstof from future %}{% firstof a b %}'})
    def test_firstof11(self):
        output = self.engine.render_to_string('firstof11', {'a': '<', 'b': '>'})
        self.assertEqual(output, '&lt;')
    DjangoTemplates.fromstring
   '''

