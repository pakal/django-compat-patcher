from __future__ import absolute_import, print_function, unicode_literals

from . import fixers, utilities, deprecation, registry
from .patcher import patch


'''
if not hasattr(django, "setup"):
    def setup_retrocompat():
        pass
    django.setup = setup_retrocompat
'''

