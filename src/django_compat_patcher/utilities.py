from compat_patcher.utilities import PatchingUtilities


class DjangoPatchingUtilities(PatchingUtilities):
    @staticmethod
    def skip_if_app_not_installed(app_name):
        """
        Raises a SkipFixerException if app_name is not enabled in Django settings.
        """
        from django.conf import settings

        if app_name not in settings.INSTALLED_APPS:
            raise SkipFixerException("%s is not enabled in INSTALLED_APPS" % app_name)
