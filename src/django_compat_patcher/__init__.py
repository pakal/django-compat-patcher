from __future__ import absolute_import, print_function, unicode_literals

from compat_patcher_core import generic_patch_software, make_safe_patcher


@make_safe_patcher
def patch(settings=None):
    """Load every dependency, and apply registered fixers according to provided settings (or Django settings as a fallback)."""

    from .registry import django_patching_registry
    from .deprecation import warnings as warnings_proxy

    from .config import DjangoSettingsProvider
    from .utilities import DjangoPatchingUtilities
    from .runner import DjangoPatchingRunner

    django_settings_provider = DjangoSettingsProvider(settings=settings)

    generic_patch_software(
        settings=django_settings_provider,
        patching_registry=django_patching_registry,
        patching_utilities_class=DjangoPatchingUtilities,
        patching_runner_class=DjangoPatchingRunner,
        warnings_proxy=warnings_proxy,
    )
