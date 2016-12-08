
from functools import wraps

from django.utils import six

from django_compat_patcher.deprecation import *

def memoize(func, cache, num_args):
    """
    Wrap a function so that results for any argument tuple are stored in
    'cache'. Note that the args to the function must be usable as dictionary
    keys.

    Only the first num_args are considered when creating the key.
    """
    warnings.warn("memoize wrapper is deprecated and will be removed in "
                  "Django 1.9. Use django.utils.lru_cache instead.",
                  RemovedInDjango19Warning, stacklevel=2)

    @wraps(func)
    def wrapper(*args):
        mem_args = args[:num_args]
        if mem_args in cache:
            return cache[mem_args]
        result = func(*args)
        cache[mem_args] = result
        return result
    return wrapper
