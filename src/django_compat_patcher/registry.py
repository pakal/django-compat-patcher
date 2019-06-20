from __future__ import absolute_import, print_function, unicode_literals

from compat_patcher_core.registry import PatchingRegistry


class DjangoPatchingRegistry(PatchingRegistry):
    pass  # Add hre custom behaviours for the Django registry

    def register_compatibility_fixer(self, *args, **kwargs):
        """Helper override to easily handle the "fixer_delayed" tag of Django-specific fixers."""
        fixer_delayed = kwargs.pop("fixer_delayed", None)
        if fixer_delayed:
            kwargs.setdefault("fixer_tags", []).append("fixer_delayed")
        return super(DjangoPatchingRegistry, self).register_compatibility_fixer(
            *args, **kwargs
        )


def get_current_django_version():
    import django

    return django.get_version()


def populate_django_fixers_registry(registry):
    import django_compat_patcher.fixers


# Must be instantiated HERE so that fixer submodules can access it at import time
django_patching_registry = DjangoPatchingRegistry(
    family_prefix="django",
    populate_callable=populate_django_fixers_registry,
    current_software_version=get_current_django_version,
)

register_django_compatibility_fixer = (
    django_patching_registry.register_compatibility_fixer
)  # Shortcut
