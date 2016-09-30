
import django

from . import fixers, utils, registry

'''
if not hasattr(django, "setup"):
    def setup_retrocompat():
        pass
    django.setup = setup_retrocompat
'''


def patch():
    for k, v in sorted(registry.FIXERS_REGISTRY.items()):
        #print("Calling fixer", k)
        v(utils)
