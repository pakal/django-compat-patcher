
import os, sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ["DJANGO_SETTINGS_MODULE"] = "test_project.settings"

def test_keep_templatetags_future_url():
    pass
