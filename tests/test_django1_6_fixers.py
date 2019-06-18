from __future__ import absolute_import, print_function, unicode_literals

import _test_utilities


def test_fix_deletion_http_request_HttpRequest_raw_post_data():
    from django.core.handlers.wsgi import WSGIRequest
    from django.test.client import FakePayload

    payload = FakePayload("Hello There!")
    request = WSGIRequest(
        {
            "REQUEST_METHOD": "POST",
            "CONTENT_LENGTH": len(payload),
            "wsgi.input": payload,
        }
    )

    assert request.body == request.raw_post_data
    assert request.body == b"Hello There!"
