from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_61_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="6.1",
    fixer_applied_from_version="6.1",
)


@django1_61_bc_fixer()
def fix_deletion_contrib_staticfiles_finders_find_all_kwarg(utils):
    """Restore the all= keyword argument of staticfiles.finders.find(), renamed to find_all= and removed in Django 6.1"""
    from django.contrib.staticfiles import finders

    _orig_find = finders.find

    def patched_find(path, all=None, find_all=False):
        if all is not None:
            warnings.warn(
                "The all argument of find() is deprecated in favor of find_all.",
                RemovedInDjango61Warning,
                stacklevel=2,
            )
            find_all = all
        return _orig_find(path, find_all=find_all)

    utils.inject_callable(finders, "find", patched_find)


@django1_61_bc_fixer(fixer_delayed=True)
def fix_behaviour_contrib_auth_RemoteUserMiddleware_aprocess_request_fallback(utils):
    """Restore the aprocess_request() fallback to process_request() for RemoteUserMiddleware subclasses that don't override aprocess_request(), removed in Django 6.1"""
    utils.skip_if_app_not_installed("django.contrib.contenttypes")  # BEFORE IMPORTS!
    from django.contrib.auth.middleware import RemoteUserMiddleware
    from asgiref.sync import sync_to_async

    async def patched_acall(self, request):
        if (
            self.__class__.process_request is not RemoteUserMiddleware.process_request
            and self.__class__.aprocess_request is RemoteUserMiddleware.aprocess_request
        ):
            warnings.warn(
                "Support for subclasses of RemoteUserMiddleware that override "
                "process_request() without overriding aprocess_request() is "
                "deprecated.",
                RemovedInDjango61Warning,
                stacklevel=2,
            )
            await sync_to_async(self.process_request, thread_sensitive=True)(request)
            return await self.get_response(request)
        await self.aprocess_request(request)
        return await self.get_response(request)

    utils.inject_callable(RemoteUserMiddleware, "__acall__", patched_acall)
