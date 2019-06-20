from __future__ import absolute_import, print_function, unicode_literals

class DjangoSettingsProvider(object):

    _settings = None

    def __init__(self, settings):

        if settings:
            self._settings = settings
        else:
            from django.conf import settings as django_settings

            self._settings = django_settings.__dict__

        from . import default_settings as default_settings

        self._fallback_settings = default_settings.__dict__

    def __getitem__(self, item):
        # Might raise KeyError if setting not existing at all

        item = "DCP_" + item.upper()  # Turn to Django naming convention

        try:
            value = self._settings[item]
        except KeyError as e:
            # print("EXCEPTION IN get_patcher_setting", name, e)
            value = self._fallback_settings[item]
        return value
