
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
