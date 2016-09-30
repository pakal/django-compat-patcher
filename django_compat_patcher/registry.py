

FIXERS_REGISTRY = {}


def _register_simple_fixer(func):
    FIXERS_REGISTRY[func.__name__] = func
    print("FIXERS_REGISTRY", FIXERS_REGISTRY)

def register_backwards_compatibility_fixer():
    return _register_simple_fixer

