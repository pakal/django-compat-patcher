
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

import _test_utilities  # initializes django


def test_keep_templatetags_future_url():
    from compat import render_to_string

    rendered = render_to_string('core_tags/test_future_url.html')
    assert rendered.strip() == "/homepage/"

    rendered = render_to_string('core_tags/test_defaulttags_url.html')
    assert rendered.strip() == "/homepage/"


def test_keep_request_post_get_mergedict():
    from django.test.client import RequestFactory
    factory = RequestFactory()

    request = factory.get('/homepage/?abcd=66')
    assert "abc" not in request.REQUEST

    request = factory.get('/homepage/?abc')
    assert request.REQUEST["abc"] == ""

    request = factory.get('/homepage/?abc=6%26')
    assert request.REQUEST["abc"] == "6&"

    request = factory.post('/homepage/?abc=66', data=dict(abc="aju"))
    assert request.REQUEST["abc"] == "aju"  # POST takes precedence over GET
