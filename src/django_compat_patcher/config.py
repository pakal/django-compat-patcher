from __future__ import absolute_import, print_function, unicode_literals

import json
from os import getenv

class DjangoSettingsProvider(object):

    _settings = None

    def __init__(self, settings):
        """
        Either directly provided `settings` parameter (if set) or
        Django project settings are used, but no fallback occurs between them.

        Environment variables (in JSON format) have precedence over all DCP settings.
        """
        if settings:
            self._settings = settings
        else:
            from django.conf import settings as django_settings
            self._settings = django_settings

        from . import default_settings as default_settings

        self._fallback_settings = default_settings.__dict__

    def __getitem__(self, item):
        """Might raise KeyError if setting is not existing at all"""

        item = "DCP_" + item.upper()  # Turn to Django naming convention

        value = getenv(item, default=None)
        if value is not None:
            try:
                return json.loads(value)
            except ValueError as exc:
                raise ValueError("Abnormal json value %r for env variable %s (%s)" % (value, item, exc))

        try:
            value = self._settings[item] if isinstance(self._settings, dict) else getattr(self._settings, item)
        except (KeyError, AttributeError) as e:
            # print("EXCEPTION IN get_patcher_setting", name, e)
            value = self._fallback_settings[item]
        return value
