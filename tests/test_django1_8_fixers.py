from __future__ import absolute_import, print_function, unicode_literals

import os

import pytest

import _test_utilities


def test_fix_outsourcing_contrib_comments():

    if os.environ.get(
        "IGNORE_CONTRIB_COMMENTS"
    ):  # case where external dependency "django_comments" isn't loaded

        with pytest.raises(ImportError) as exc:
            from django.contrib import comments
        assert (
            "No module named 'django_comments' (when loading alias name 'django.contrib.comments')"
            in str(exc)
        )

    else:

        from django.contrib import comments
        import django.contrib.comments

        import django.contrib.comments.urls

        assert isinstance(django.contrib.comments.urls.urlpatterns, list)

        from django.contrib.comments.views import comments as comments_views

        assert callable(comments_views.post_comment)
