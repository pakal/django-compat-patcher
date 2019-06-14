from __future__ import absolute_import, print_function, unicode_literals

from compat_patcher import generic_patch_software


def patch(settings=None):
    """Load every dependency, and apply registered fixers according to provided settings (or Django settings as a fallback)."""

    from .registry import django_patching_registry
    from .deprecation import warnings as warnings_proxy

    from .config import DjangoConfigProvider
    from .utilities import DjangoPatchingUtilities
    from .runner import DjangoPatchingRunner

    django_config_provider = DjangoConfigProvider(settings=settings)

    generic_patch_software(
        config_provider=django_config_provider,
        patching_registry=django_patching_registry,
        patching_utilities_class=DjangoPatchingUtilities,
        patching_runner_class=DjangoPatchingRunner,
        warnings_proxy=warnings_proxy,
    )
