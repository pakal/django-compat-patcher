from __future__ import absolute_import, print_function, unicode_literals


def patch(settings=None):
    """Load every dependency, and apply registered fixers according to provided settings (or Django settings as a fallback)."""

    from .config import DjangoConfigProvider
    from .utilities import DjangoPatchingUtilities
    from .registry import DjangoFixersRegistry
    from .runner import DjangoPatchingRunner

    config_provider = DjangoConfigProvider(settings=settings)

    patching_utilities = DjangoPatchingUtilities(config_provider=config_provider)

    from . import deprecation  # Immediately finish setting up this module
    deprecation.warnings.set_patching_utilities(patching_utilities)

    from . import fixers  # Force-load every fixer submodule
    from .registry import django_fixers_registry

    django_patching_runner = DjangoPatchingRunner(config_provider=config_provider,
                                                  patching_utilities=patching_utilities,
                                                  fixers_registry=django_fixers_registry,)
    django_patching_runner.patch_software()

