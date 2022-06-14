from __future__ import absolute_import, print_function, unicode_literals

from compat_patcher_core.utilities import WarningsProxy

# Proxy meant to be imported by fixer submodules instead of stdlib "warnings" package
warnings = WarningsProxy()


class RemovedInDjango40Warning(DeprecationWarning):
    pass


class RemovedInDjango31Warning(DeprecationWarning):
    pass


class RemovedInDjango30Warning(DeprecationWarning):
    pass


class RemovedInDjango22Warning(DeprecationWarning):
    pass


class RemovedInDjango21Warning(DeprecationWarning):
    pass


class RemovedInDjango20Warning(DeprecationWarning):
    pass


class RemovedInDjango111Warning(DeprecationWarning):
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


# Beware, think about updating this one!
RemovedInNextVersionWarning = RemovedInDjango22Warning
