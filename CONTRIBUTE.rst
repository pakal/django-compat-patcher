

**Django-compat-patcher warmly welcomes new fixers, and bugfixes.**

The code must be very DRY, to minimize bugs, and so that future evolutions of this library are as painless as possible.

It must be self-documented, using decorator arguments and docstrings (we do NOT maintain a separate list of what fixes are available).

It must also be as robust as possible - this lib is supposed to workaround breakages, not introduce new ones.


Recommendations:

- in fixers : don't do logging or warnings by yourself, use the injected "utils" object instead
- also use functions from this "utils" object, to patch django code, not direct assignments
- don't do global imports of django submodules or external libraries, import them from inside fixers instead
- respect python/django standards for naming objects, spacings, etc.
- make code py2/py3 compatible by using django.utils.six, and __future__ imports in all python files
