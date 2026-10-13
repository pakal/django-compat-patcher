
import pytest
import _test_utilities


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (5, 2),
    reason="staticfiles.finders.find()'s find_all keyword argument was only added in Django 5.2",
)
def test_fix_deletion_contrib_staticfiles_finders_find_all_kwarg():
    from django.contrib.staticfiles import finders

    # django.contrib.admin ships static files discoverable via AppDirectoriesFinder
    result_all = finders.find("admin/css/base.css", all=True)
    result_find_all = finders.find("admin/css/base.css", find_all=True)
    assert result_all == result_find_all
    assert result_all  # non-empty list, the file must be found

    # Default behaviour (no kwarg at all) is untouched
    assert finders.find("admin/css/base.css") == result_find_all[0]


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (6, 0),
    reason="RemoteUserMiddleware.aprocess_request() was only added in Django 6.0",
)
def test_fix_behaviour_contrib_auth_RemoteUserMiddleware_aprocess_request_fallback():
    from asgiref.sync import async_to_sync
    from django.contrib.auth.middleware import RemoteUserMiddleware

    calls = []

    class LegacyMiddleware(RemoteUserMiddleware):
        def process_request(self, request):
            calls.append(("sync", request))

    async def get_response(request):
        return "response"

    legacy = LegacyMiddleware(get_response)
    dummy_request = object()

    # __acall__() is the real ASGI entry point used by Django; it must fall
    # back to process_request() via a sync-to-async bridge instead of
    # invoking the (unoverridden) default aprocess_request().
    result = async_to_sync(legacy.__acall__)(dummy_request)

    assert calls == [("sync", dummy_request)]
    assert result == "response"

    # Subclasses that already define aprocess_request() are left untouched
    class ModernMiddleware(RemoteUserMiddleware):
        def process_request(self, request):
            raise AssertionError("sync process_request() should not be called")

        async def aprocess_request(self, request):
            calls.append(("async", request))

    modern = ModernMiddleware(get_response)
    async_to_sync(modern.__acall__)(dummy_request)

    assert calls[-1] == ("async", dummy_request)
