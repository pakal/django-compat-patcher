from __future__ import absolute_import, print_function, unicode_literals

from . import fixers, utilities, deprecation, registry

def patch():
    """Returns a list of ids of fixers applied"""
    
    print("Fixers are:", registry.FIXERS_REGISTRY)
    django_version = utilities.get_django_version()
    selected_fixers = registry.get_relevant_fixers(current_django_version=django_version)
    for fixer in selected_fixers:
        #print("Applying fixer", fixer)
        # TODO - create custom injected "utils" object with context information, logging, warnings, etc.
        fixer["fixer_callable"](utilities)
    return selected_fixers