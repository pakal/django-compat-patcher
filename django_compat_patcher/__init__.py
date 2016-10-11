from __future__ import absolute_import, print_function, unicode_literals

import django

from . import fixers, utilities, registry

'''
if not hasattr(django, "setup"):
    def setup_retrocompat():
        pass
    django.setup = setup_retrocompat
'''


def patch():
    print("Fixers are:", registry.FIXERS_REGISTRY)
    for fixer in sorted(registry.FIXERS_REGISTRY):
        #print("Applying fixer", fixer)
        # TODO - create custom injected "utils" object with context information, logging, warnings, etc.
        fixer["fixer_callable"](utilities)
