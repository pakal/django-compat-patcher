from __future__ import absolute_import, print_function, unicode_literals

from . import fixers, utilities, deprecation, registry

__APPLIED_FIXERS = set()


def patch(settings=None):
    """Patches the Django package with relevant fixers.
    
    A settings dict/objects can be provided, to REPLACE lookups in Django settings.
    
    Returns a list of ids of fixers applied.
    """

    utilities.apply_runtime_settings(settings)  # called even if settings are empty

    # print("Fixers are:", registry.FIXERS_REGISTRY)
    django_version = utilities.get_django_version()
    relevant_fixers = registry.get_relevant_fixers(current_django_version=django_version, settings=settings)

    # REVERSED is better for backwards compatibility, for now...
    relevant_fixers.sort(key=lambda x:x["fixer_reference_version"], reverse=True)

    pre_fixers = [f for f in relevant_fixers if not f["fixer_delayed"]]
    post_fixers = [f for f in relevant_fixers if f["fixer_delayed"]]
    assert len(relevant_fixers) == len(pre_fixers) + len(post_fixers)

    def _apply_fixers(fixers):
        for fixer in fixers:
            # print("Applying fixer", fixer)
            # TODO - create custom injected "utils" object with context information, logging, warnings, etc.
            if fixer['fixer_id'] not in __APPLIED_FIXERS:
                utilities.logger.info("Django compat fixer '{}-{}' is getting applied".format(
                    fixer["fixer_family"], fixer['fixer_id'])
                )
                fixer["fixer_callable"](utilities)
                __APPLIED_FIXERS.add(fixer['fixer_id'])
            else:
                utilities.logger.warning("Django compat fixer '{}' was already applied".format(fixer['fixer_id']))

    _apply_fixers(pre_fixers)
    import django
    django.setup()  # idempotent
    _apply_fixers(post_fixers)

    return relevant_fixers
