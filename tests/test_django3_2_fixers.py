
import pytest

import _test_utilities

from django_compat_patcher import default_settings
from django_compat_patcher.registry import django_patching_registry


def test_fix_deletion_http_response_HttpResponseBase_private_headers():

    from django.template.response import SimpleTemplateResponse

    response = SimpleTemplateResponse(
        'first/test.html',
        {'value': 123},
        headers={'X-Foo': 'foo'},
    )
    assert response.headers['X-Foo'] == 'foo'
    assert response._headers['X-Foo'] == 'foo'
