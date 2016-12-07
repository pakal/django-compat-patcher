from __future__ import absolute_import, print_function, unicode_literals

import functools
import logging
import types
import warnings
from functools import wraps, partial

import sys
from django.utils import six



def get_patcher_setting(name, settings=None):
    """
    Fetches the value of the DCP setting.

    If it's not found, a default value is returned for the setting.

    If provided, the 'settings' arguments is a dict which *completely*
    replaces django settings (no fallback occurs).

    :param name: The name of the setting
    :param settings: Possible replacement for the project's settings
    :return: The value of the setting "name"
    """
    from django.conf import settings as django_settings
    from . import default_settings

    if settings is None:
        settings = django_settings

    if not name.startswith("DCP"):
        raise ValueError("Only 'DCP_XXX' setting names are allowed in get_patcher_setting()")

    try:
        if isinstance(settings, dict):
            setting = settings[name]
        else:
            setting = getattr(settings, name)  # Will break if unknown setting
    except (AttributeError, KeyError) as e:
        #print("EXCEPTION IN get_patcher_setting", name, e)
        setting = getattr(default_settings, name)

    # Micromanaging, because a validation Schema is overkill for now
    if name in ("DCP_PATCH_INJECTED_OBJECTS", "DCP_ENABLE_LOGGING", "DCP_ENABLE_WARNINGS"):
        assert isinstance(setting, bool), setting
    else:
        assert (setting == "*" or (isinstance(setting, list) and
                                   all(isinstance(f, six.string_types) for f in setting))), setting
    return setting


def apply_runtime_settings(settings=None):
    """
    If provided, 'settings' ENTIRELY replaces django settings
    during this setup.
    """
    global DO_EMIT_WARNINGS
    do_emit_warnings = get_patcher_setting("DCP_ENABLE_WARNINGS", settings=settings)
    assert do_emit_warnings in (True, False)
    DO_EMIT_WARNINGS = do_emit_warnings  # runtime switch on/off



# use this logger, from inside fixers!
logger = logging.getLogger("django.compat.patcher")


# global on/off switch, lazily initialized, and to be modified by patch() if wanted
DO_EMIT_WARNINGS = None

def emit_warning(message, category=None, stacklevel=1):
    category = category or DeprecationWarning
    assert issubclass(category, DeprecationWarning), category  # only those are used atm

    global DO_EMIT_WARNINGS
    if DO_EMIT_WARNINGS is None:
        DO_EMIT_WARNINGS = get_patcher_setting("DCP_ENABLE_WARNINGS")
    assert DO_EMIT_WARNINGS is not None

    print ("DO_EMIT_WARNINGS is ", DO_EMIT_WARNINGS)

    if DO_EMIT_WARNINGS:
        warnings.warn(message, category, stacklevel + 1)


def get_django_version():
    import django
    return django.get_version()


def _patch_injected_object(object_to_patch):
    # we expect a "custom" object here...
    assert object_to_patch not in (True, False, None)
    if get_patcher_setting('DCP_PATCH_INJECTED_OBJECTS'):
        #print("PATCHING injected object", object_to_patch)
        try:
            setattr(object_to_patch, "__dcp_injected__", True)
        except AttributeError:
            pass # properties and such special objects can't be modified


def _is_simple_callable(obj):
    return isinstance(obj, (types.FunctionType, types.BuiltinFunctionType, functools.partial))


def inject_attribute(target_object, target_attrname, attribute):
    """
    :param target_object: The object to patch
    :param target_attrname: The name given to the new attribute in the object to patch
    :param attribute: The attribute to inject: must not be a callable
    """
    # TODO logging and warnings
    assert attribute is not None
    assert not _is_simple_callable(attribute), attribute
    assert not isinstance(attribute, six.class_types), attribute

    _patch_injected_object(attribute)
    setattr(target_object, target_attrname, attribute)


def inject_callable(target_object, target_callable_name, patch_callable):
    """
    :param target_object: The object to patch
    :param target_callable_name: The name given to the new callable in the object to patch
    :param patch_callable: The callable to inject: must be a callable, but not a class
    """
    # TODO logging and warnings
    assert _is_simple_callable(patch_callable), patch_callable

    from django.conf import settings as django_settings3
    #assert not django_settings3.DCP_PATCH_INJECTED_OBJECT

    _patch_injected_object(patch_callable)
    setattr(target_object, target_callable_name, patch_callable)


def inject_module(target_module_name, target_module):
    """
    :param target_module_name: The name of the new module in sys.modules
    :param target_module: The new module
    """
    # TODO logging and warnings
    target_module_name = str(target_module_name)  # Python2 compatibility
    assert isinstance(target_module, types.ModuleType), target_module
    assert sys.modules.get(target_module_name) is None

    _patch_injected_object(target_module)

    sys.modules[target_module_name] = target_module


def inject_class(target_object, target_klassname, klass):
    """
    :param target_object: The object to patch
    :param target_klassname: The name given to the new class in the object to patch
    :param klass: The class to inject : must be a class
    """
    # TODO logging and warnings
    assert isinstance(klass, six.class_types), klass

    _patch_injected_object(klass)
    setattr(target_object, target_klassname, klass)


def inject_callable_alias(source_object, source_attrname,
                          target_object, target_attrname):
    """
    Create and inject an alias for the source callable (not a class),
    by handling logging/warnings

    Returns the created alias.
    """

    old_function = getattr(source_object, source_attrname)
    assert _is_simple_callable(old_function), old_function

    @wraps(old_function)
    def wrapper(*args, **kwds):
        # TODO HERE WARNINGS AND LOGGINGS WITH CONTEXT INFO
        return old_function(*args, **kwds)

    _patch_injected_object(wrapper)
    # TODO LOGGING HERE

    setattr(target_object, target_attrname, wrapper)

    return wrapper


def register_import_alias(alias_name, real_name):
    from . import import_proxifier
    import_proxifier.install_import_proxifier()  # idempotent activation
    import_proxifier.register_module_alias(alias_name=alias_name,
                                           real_name=real_name)


def _tuplify_version(version):
    """
    Coerces the version string (if not None), to a version tuple.
    Ex. "1.7.0" becomes (1, 7, 0).
    """
    if version is None:
        return version
    if isinstance(version, six.string_types):
        version = tuple(int(x) for x in version.split("."))
    assert len(version) <= 4, version
    assert (1, 3) <= version, version
    assert all(isinstance(x, six.integer_types) for x in version), version
    return version


def _detuplify_version(input_tuple):
    """
    Coerces the version tuple (if not None), to a version string.
    Ex. (1, 7, 0) becomes "1.7.0".
    """
    if input_tuple is None:
        return ""
    assert isinstance(input_tuple, tuple)
    string = ".".join(str(number) for number in input_tuple)
    return string


'''
BORROWED FROM DJANGO DEPRECATION MODULE

class RenameMethodsBase(type):
    """
    Handles the deprecation paths when renaming a method.

    It does the following:
        1) Define the new method if missing and complain about it.
        2) Define the old method if missing.
        3) Complain whenever an old method is called.

    See #15363 for more details.
    """

    renamed_methods = ()

    def __new__(cls, name, bases, attrs):
        new_class = super(RenameMethodsBase, cls).__new__(cls, name, bases, attrs)

        for base in inspect.getmro(new_class):
            class_name = base.__name__
            for renamed_method in cls.renamed_methods:
                old_method_name = renamed_method[0]
                old_method = base.__dict__.get(old_method_name)
                new_method_name = renamed_method[1]
                new_method = base.__dict__.get(new_method_name)
                deprecation_warning = renamed_method[2]
                wrapper = warn_about_renamed_method(class_name, *renamed_method)

                # Define the new method if missing and complain about it
                if not new_method and old_method:
                    warnings.warn(
                        "`%s.%s` method should be renamed `%s`." %
                        (class_name, old_method_name, new_method_name),
                        deprecation_warning, 2)
                    setattr(base, new_method_name, old_method)
                    setattr(base, old_method_name, wrapper(old_method))

                # Define the old method as a wrapped call to the new method.
                if not old_method and new_method:
                    setattr(base, old_method_name, wrapper(new_method))

        return new_class

'''
