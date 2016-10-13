from __future__ import absolute_import, print_function, unicode_literals

from . import fixers, utilities, deprecation, registry

__APPLIED_FIXERS = set()

def patch(settings=None):
    """Patches the Django package with relevant fixers.
    
    A settings dict/objects can be provided, to REPLACE lookups in Django settings.
    
    Returns a list of ids of fixers applied.
    """
    
    print("Fixers are:", registry.FIXERS_REGISTRY)
    django_version = utilities.get_django_version()
    selected_fixers = registry.get_relevant_fixers(current_django_version=django_version, settings=settings)
    for fixer in selected_fixers:
        #print("Applying fixer", fixer)
        # TODO - create custom injected "utils" object with context information, logging, warnings, etc.
        if fixer['fixer_id'] not in __APPLIED_FIXERS:
            fixer["fixer_callable"](utilities)
            __APPLIED_FIXERS.add(fixer['fixer_id'])
        else:
            utilities.logger.warning("Fixer '{}' was already applied".format(fixer['fixer_id']))
    return selected_fixers