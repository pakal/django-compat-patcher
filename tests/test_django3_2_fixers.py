import django
import pytest

import _test_utilities

from django_compat_patcher import default_settings
from django_compat_patcher.registry import django_patching_registry


def test_fix_deletion_http_response_HttpResponseBase_private_headers():

    from django.template.response import SimpleTemplateResponse

    response = SimpleTemplateResponse(
        'first/test.html',
        {'value': 123},
        # headers={'X-Foo': 'foo'} =>  parameter NOT always available!
    )
    response['X-Foo'] = 'foo'
    if _test_utilities.DJANGO_VERSION_TUPLE >= (3, 2):
        assert response.headers['X-Foo'] == 'foo'
    assert response._headers['x-foo'] == ('X-Foo', 'foo')
