from __future__ import absolute_import, print_function, unicode_literals

import os, sys
import pytest

import _test_utilities


def test_fix_deletion_django_utils_translation_string_concat():
    from django.utils.translation import string_concat
    assert string_concat("a", "b", "c") == "abc"
