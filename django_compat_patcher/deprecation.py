from __future__ import absolute_import, print_function, unicode_literals

from django_compat_patcher.utilities import emit_warning

class RemovedInDjango21Warning(PendingDeprecationWarning):
    pass


class RemovedInDjango20Warning(DeprecationWarning):
    pass


class RemovedInDjango110Warning(DeprecationWarning):
    pass


class RemovedInDjango19Warning(DeprecationWarning):
    pass


class RemovedInDjango18Warning(DeprecationWarning):
    pass


class RemovedInDjango17Warning(DeprecationWarning):
    pass


class RemovedInDjango16Warning(DeprecationWarning):
    pass


RemovedInNextVersionWarning = RemovedInDjango21Warning


# replacement for "import warnings", which behaves according to DCP settings
class WarningsProxy():
    def warn(self, *args, **kwargs):
        emit_warning(*args, **kwargs)
warnings = WarningsProxy()
