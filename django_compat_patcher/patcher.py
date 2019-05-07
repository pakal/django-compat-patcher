from __future__ import absolute_import, print_function, unicode_literals

import functools
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
    log = functools.partial(utilities.emit_log, level="DEBUG")
    relevant_fixers = registry.get_relevant_fixers(current_django_version=django_version,
                                                   settings=settings,
                                                   log=log)

    # REVERSED is better for backwards compatibility, for now...
    relevant_fixers.sort(key=lambda x:x["fixer_reference_version"], reverse=True)

    pre_fixers = [f for f in relevant_fixers if not f["fixer_delayed"]]
    post_fixers = [f for f in relevant_fixers if f["fixer_delayed"]]
    assert len(relevant_fixers) == len(pre_fixers) + len(post_fixers)

    def _apply_fixers(fixers):
        for fixer in fixers:
            # print("Applying fixer", fixer)
            if fixer['fixer_id'] not in __APPLIED_FIXERS:
                utilities.emit_log("Django compat fixer '{}-{}' is getting applied".format(
                    fixer["fixer_family"], fixer['fixer_id']), level="INFO"
                )
                try:
                    fixer["fixer_callable"](utilities)
                    __APPLIED_FIXERS.add(fixer['fixer_id'])
                except utilities.SkipFixerException as e:
                    utilities.emit_log("Django compat fixer '{}-{}' was not applied, reason: {}".format(
                        fixer["fixer_family"], fixer['fixer_id'], e), level="WARNING"
                    )
            else:
                utilities.emit_log("Django compat fixer '{}' was already applied".
                                         format(fixer['fixer_id']), level="WARNING")

    _apply_fixers(pre_fixers)
    import django
    django.setup()  # theoretically idempotent (except regarding logging?)
    _apply_fixers(post_fixers)

    return relevant_fixers
