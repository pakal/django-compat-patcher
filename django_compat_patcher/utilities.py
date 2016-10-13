from __future__ import absolute_import, print_function, unicode_literals

import logging
import warnings
from functools import wraps, partial

from django.utils import six


# use this logger, from inside fixers!
logger = logging.getLogger("django.compat.patcher")


def emit_warning(message, category=None, stacklevel=1):
    # TODO put default category here ?
    warnings.warn(message, category, stacklevel+1)


def get_django_version():
    import django
    return django.get_version()


def get_patcher_setting(name, settings=None):
    from django.conf import settings as django_settings
    from . import default_settings
    settings = settings if settings is not None else django_settings
    settings = settings if isinstance(settings, dict) else settings.__dict__
    default = getattr(default_settings, name)  # will break if unknown setting
    setting = settings.get(name, default)
    assert (setting == "*" or (isinstance(setting, list) and 
                              all(isinstance(f, six.string_types) for f in setting))), setting
    return setting


def inject_attribute(target_object, target_attrname, callable):
    # TODO logging and warnings
    setattr(target_object, target_attrname, callable)


def inject_method(target_object, target_attrname, callable):
    # TODO logging and warnings, as well as func.__name__ setup
    setattr(target_object, target_attrname, callable)


def inject_class(target_object, target_attrname, klass):
    # TODO logging and warnings, as well as func.__name__ setup
    setattr(target_object, target_attrname, klass)


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
        #TODO HERE WARNINGS AND LOGGINGS WITH CONTEXT INFO
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
