from __future__ import absolute_import, print_function, unicode_literals

import os, sys

import _test_utilities

def test_fix_outsourcing_contrib_comments():

    from django.contrib import comments
    import django.contrib.comments

    import django.contrib.comments.urls
    assert isinstance(django.contrib.comments.urls.urlpatterns, list)

    from django.contrib.comments.views import comments as comments_views
    assert callable(comments_views.post_comment)
