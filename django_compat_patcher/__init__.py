from __future__ import absolute_import, print_function, unicode_literals

from . import fixers, utilities, registry

'''
if not hasattr(django, "setup"):
    def setup_retrocompat():
        pass
    django.setup = setup_retrocompat
'''


def patch():
    print("Fixers are:", registry.FIXERS_REGISTRY)
    django_version = utilities.get_django_version()
    for fixer in registry.get_relevant_fixers(current_django_version=django_version):
        #print("Applying fixer", fixer)
        # TODO - create custom injected "utils" object with context information, logging, warnings, etc.
        fixer["fixer_callable"](utilities)
