from __future__ import absolute_import, print_function, unicode_literals

import functools
import logging
import types
import warnings as stdlib_warnings  # do NOT use elseware than in emit_warning()
from functools import wraps, partial

import sys
from django.utils import six


class SkipFixerException(Exception):
    """
    Exception to signal a fixer which is not 
    applicable in that project context.
    """
    pass


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
    if name == "DCP_LOGGING_LEVEL":
        assert setting is None or hasattr(logging, setting), repr(setting)
    elif name in ("DCP_PATCH_INJECTED_OBJECTS", "DCP_ENABLE_WARNINGS"):
        assert isinstance(setting, bool), repr(setting)
    else:
        assert (setting == "*" or
                (isinstance(setting, list) and all(isinstance(f, six.string_types) for f in setting))), setting
    return setting


def apply_runtime_settings(settings):
    """
    Change at runtime the logging/warnings settings.
    """
    global DCP_ENABLE_WARNINGS, DCP_LOGGING_LEVEL, _initial_setup_done

    settings = settings or {}

    if not _initial_setup_done:
        DCP_ENABLE_WARNINGS = get_patcher_setting("DCP_ENABLE_WARNINGS")
        DCP_LOGGING_LEVEL = get_patcher_setting("DCP_LOGGING_LEVEL")
        _initial_setup_done = True

    if "DCP_ENABLE_WARNINGS" in settings:
        dcp_enable_warnings = settings["DCP_ENABLE_WARNINGS"]
        assert dcp_enable_warnings in (True, False), dcp_enable_warnings
        DCP_ENABLE_WARNINGS = dcp_enable_warnings  # runtime switch on/off

    if "DCP_LOGGING_LEVEL" in settings:
        dcp_logging_level = settings["DCP_LOGGING_LEVEL"]
        assert dcp_logging_level is None or hasattr(logging, dcp_logging_level), dcp_logging_level
        DCP_LOGGING_LEVEL = dcp_logging_level


# for lazy setup of the some settings
_initial_setup_done = False

# global on/off switch for (deprecation) warnings, to be modified by patch() if wanted
DCP_ENABLE_WARNINGS = False

# global logging level string, or None if no logging
DCP_LOGGING_LEVEL = None


def emit_log(message, level="INFO"):
    if DCP_LOGGING_LEVEL is None:
        return
    if getattr(logging, level) < getattr(logging, DCP_LOGGING_LEVEL):
        return
    full_message = "[DCP_%s] %s" % (level, message)
    print(full_message, file=sys.stderr)


def emit_warning(message, category=None, stacklevel=1):
    category = category or DeprecationWarning
    assert issubclass(category, DeprecationWarning), category  # only those are used atm
    if DCP_ENABLE_WARNINGS:
        stdlib_warnings.warn(message, category, stacklevel + 1)


def get_django_version():
    import django
    return django.get_version()


def skip_if_app_not_installed(app_name):
    """
    Raises a SkipFixerException if app_name is not enabled in Django settings.
    """
    from django.conf import settings
    if app_name not in settings.INSTALLED_APPS:
        raise SkipFixerException("%s is not enabled in INSTALLED_APPS" % app_name)


def _patch_injected_object(object_to_patch):
    # we expect a "custom" object here...
    assert object_to_patch not in (True, False, None)
    if get_patcher_setting('DCP_PATCH_INJECTED_OBJECTS'):
        #print("PATCHING injected object", object_to_patch)
        try:
            setattr(object_to_patch, "__dcp_injected__", True)
        except AttributeError:
            pass # '@properties' and such special objects can't be modified


def _is_simple_callable(obj):
    return isinstance(obj, (types.FunctionType, types.BuiltinFunctionType, functools.partial))


def inject_attribute(target_object, target_attrname, attribute):
    """
    :param target_object: The object to patch
    :param target_attrname: The name given to the new attribute in the object to patch
    :param attribute: The attribute to inject: must not be a callable
    """
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
    assert _is_simple_callable(patch_callable), patch_callable

    _patch_injected_object(patch_callable)
    setattr(target_object, target_callable_name, patch_callable)


def inject_module(target_module_name, target_module):
    """
    :param target_module_name: The name of the new module in sys.modules
    :param target_module: The new module
    """
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
    source_callable = getattr(source_object, source_attrname)
    assert _is_simple_callable(source_callable), source_callable

    @wraps(source_callable)
    def wrapper(*args, **kwds):
        # we dunno if it's a backwards or forwards compatibility shim...
        emit_warning('%s.%s, which is an alias for %s.%s, was called. One of these is deprecated.' %
                     (target_object, source_attrname, source_object, source_attrname),
                     DeprecationWarning)
        return source_callable(*args, **kwds)

    _patch_injected_object(wrapper)
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
