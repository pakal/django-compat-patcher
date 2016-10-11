
import django

from . import fixers, utils, registry

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
        fixer["fixer_callable"](utils)
