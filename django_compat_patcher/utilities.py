from __future__ import absolute_import, print_function, unicode_literals

import functools
import logging
import types
import warnings
from functools import wraps, partial

import sys
from django.utils import six

# use this logger, from inside fixers!
PATCH_NAME_SUFFIX = "__DJANGO_COMPAT_PATCHER"
logger = logging.getLogger("django.compat.patcher")


def emit_warning(message, category=None, stacklevel=1):
    # TODO put default category here ?
    warnings.warn(message, category, stacklevel + 1)


def get_django_version():
    import django
    return django.get_version()


def _patch_object__name__(object_to_patch, target_name):
    # Prevent external libraries that use __name__ from failing
    assert object_to_patch.__name__ == target_name
    if not get_patcher_setting('DCP_MONKEY_PATCH_NAME'):
        return
    if not six.PY3:
        return  # changing __name__ on python2 might break pickling
    if not object_to_patch.__name__.endswith(PATCH_NAME_SUFFIX):
        new_name = "{}{}".format(object_to_patch.__name__, PATCH_NAME_SUFFIX)
        object_to_patch.__name__ = new_name


def get_patcher_setting(name, settings_override=None):
    """
    Fetches the value of the setting with its name, either from the settings argument,
    falling back to the project's settings
    :param name: The name of the setting
    :param settings_override: An override for the project's settings
    :return: The value of the setting "name"
    """
    from django.conf import settings as django_settings
    from . import default_settings
    from django.conf import LazySettings

    if settings_override is None or settings_override == {}:
        settings = django_settings
    else:
        settings = settings_override

    assert name.startswith("DCP")

    try:
        if isinstance(settings, LazySettings):
            setting = getattr(settings, name)  # will break if unknown setting
        else:
            setting = settings.get(name)
    except AttributeError:
        setting = getattr(default_settings, name)

    # Micromanaging, because a validation Schema is overkill now
    if name == "DCP_MONKEY_PATCH_NAME":
        assert isinstance(setting, bool)
    else:
        assert (setting == "*" or (isinstance(setting, list) and
                                   all(isinstance(f, six.string_types) for f in setting))), setting
    return setting


def inject_attribute(target_object, target_attrname, attribute):
    """
    :param target_object: The object to patch
    :param target_attrname: The name given to the new attribute in the object to patch
    :param attribute: The attribute to inject : must not be a class, or a callable (that is not a class)
    """
    # TODO logging and warnings
    assert attribute is not None
    assert not isinstance(attribute, (types.FunctionType, types.BuiltinFunctionType, functools.partial, six.class_types)), attribute
    setattr(target_object, target_attrname, attribute)


def inject_callable(target_object, target_callable_name, patch_callable):
    """
    :param target_object: The object to patch
    :param target_callable_name: The name given to the new callable in the object to patch
    :param patch_callable: The callable to inject : must me a callable, but not a class
    """
    # TODO logging and warnings
    assert isinstance(patch_callable, (types.FunctionType, types.BuiltinFunctionType, functools.partial)), patch_callable

    _patch_object__name__(patch_callable, target_callable_name)
    setattr(target_object, target_callable_name, patch_callable)


def inject_module(target_module_name, target_module):
    """
    :param target_module_name:  The name of the new module
    :param target_module: The new module
    """
    # TODO logging and warnings
    target_module_name = str(target_module_name)  # Python2 compatibility
    assert isinstance(target_module, types.ModuleType), target_module
    assert sys.modules.get(target_module_name) is None

    sys.modules[target_module_name] = target_module


def inject_class(target_object, target_klassname, klass):
    """
    :param target_object: The object to patch
    :param target_klassname: The name given to the new class in the object to patch
    :param klass: The class to inject : must be a class
    """
    # TODO logging and warnings
    assert isinstance(klass, six.class_types), klass

    _patch_object__name__(klass, target_klassname)
    setattr(target_object, target_klassname, klass)


def inject_function_alias(source_object, source_attrname,
                          target_object, target_attrname):
    """
    Create and inject an alias for the source function,
    by handling logging/warnings

    Returns the created alias.
    """

    old_function = getattr(source_object, source_attrname)

    @wraps(old_function)
    def wrapper(*args, **kwds):
        # TODO HERE WARNINGS AND LOGGINGS WITH CONTEXT INFO
        return old_function(*args, **kwds)

    # TODO LOGGING HERE

    setattr(target_object, target_attrname, wrapper)

    return wrapper


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
