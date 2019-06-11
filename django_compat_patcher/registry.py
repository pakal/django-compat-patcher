from compat_patcher.registry import FixersRegistry



class DjangoFixersRegistry(FixersRegistry):
    pass  # Add hre custom behaviours for the Django registry

    def register_compatibility_fixer(self, *args, **kwargs):
        """Helper override to easily handle the "fixer_delayed" tag of Django-specific fixers."""
        fixer_delayed = kwargs.pop("fixer_delayed", None)
        if fixer_delayed:
            kwargs.setdefault("fixer_tags", []).append("fixer_delayed")
        return super(DjangoFixersRegistry, self).register_compatibility_fixer(*args, **kwargs)


# Must be instantiated HERE so that fixer submodules can access it at import time
django_fixers_registry = DjangoFixersRegistry(family_prefix="django_")


register_django_compatibility_fixer = django_fixers_registry.register_compatibility_fixer
