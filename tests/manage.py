#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

import _test_utilities  # bootstraps django-compat-patcher

if __name__ == "__main__":


    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
