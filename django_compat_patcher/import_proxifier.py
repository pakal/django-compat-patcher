"""
This module allows to create aliases between packages, so that one
can import a module under a different name (mainly for retrocompatibility purpose).

Note that it is NOT about aliasing local references to modules after import, eg. with "from package import module_name as other_module_name".
Here we really deal with aliasing the "full name" of the module, as it will appear in sys.modules.

There are different ways of implementing "import aliases":

- overridding __import__ (difficult, since this API loads parent modules too)
- using a custom module loader which creates a wrapper class (with setattr,
  getattr etc...), and injects it as a proxy in sys.modules[alias]
- using a custom module loader, which simply copies a reference to the real module
  into sys.modules (and on recent python version, updates its __spec__ to gives hints about this operation).
  *THIS* is the way it is currently implemented, so that imported modules keep being SINGLETONS whatever their
  possible aliases.

Beware about not creating loops with your aliases, as this could trigger infinite recursions.
"""

import os, sys
import importlib, contextlib


# maps ALIASES to REAL MODULES
MODULES_ALIASES_REGISTRY = []


@contextlib.contextmanager
def enrich_import_error(alias_name):
    try:
        yield
    except ImportError as e:
        #print(vars(e), str(e), dir(e), e.args)
        # ImportError exception has different structure between py2k and py3k
        enrich_message = lambda msg: "%s (when loading alias name '%s')" % (msg, alias_name)
        if hasattr(e, "msg"):  # py3k
            e.msg = enrich_message(e.msg)
        else:  # py2k, the "message" attribute is actually ignored by __str__
            e.args = (enrich_message(e.args[0]),)
        raise


def register_module_alias(alias_name, real_name):
    assert not alias_name.startswith("."), alias_name
    assert not real_name.startswith("."), real_name
    assert alias_name != real_name, alias_name  # lots of other import cycles are possible though
    entry = (alias_name, real_name)
    if entry not in MODULES_ALIASES_REGISTRY:
        MODULES_ALIASES_REGISTRY.append(entry)
        return True
    return False


def _get_module_alias_real_name(fullname):
    """
    returns the real name of module (when fullname is an alias name)
    or None.
    """
    for k, v in MODULES_ALIASES_REGISTRY:
        if (k == fullname) or fullname.startswith(k +"."):
            return fullname.replace(k, v)
    return None


try:

    import importlib.machinery, importlib.abc

except ImportError:

    # OLD STYLE : we use PEP 302 find_module/load_module API, available for python2.7+

    is_new_style_proxifier = False


    class AliasingLoader(object):

        def __init__(self, real_name, alias_name):
            self.real_name = real_name
            self.alias_name = alias_name

        def load_module(self, name):
            if name in sys.modules:
                return sys.modules[name]  # shortcut
            # we let the standard machinery handle sys.modules, module attrs etc.
            with enrich_import_error(self.alias_name):
                module = importlib.import_module(self.real_name, package=None)
            sys.modules[name] = module  # cached
            return module


    class ModuleAliasFinder(object):

        @classmethod
        def find_module(self, fullname, *args, **kwargs):

            #print("OldMetaPathFinder FINDMODULE", fullname, args, kwargs)

            real_name = _get_module_alias_real_name(fullname)
            if real_name is None:
                return None  # no aliased module is known
            return AliasingLoader(real_name=real_name, alias_name=fullname)


else:

    # NEW STYLE : we use modern import hooks (PEP 451 etc.)

    is_new_style_proxifier = True


    class AliasingLoader(importlib.abc.Loader):

        target_spec_backup = None

        def __init__(self, real_name, alias_name):
            self.real_name = real_name
            self.alias_name = alias_name

        def create_module(self, spec):
            # we do the real loading of aliased module here
            with enrich_import_error(self.alias_name):
                module = importlib.import_module(self.real_name, package=None)
            assert module.__name__ == self.real_name, module.__name__
            self.target_spec_backup = module.__spec__
            return module

        def exec_module(self, module):
            # __name__ is, on some python versions, overridden by init_module_attrs(_force_name=True)
            assert module.__name__ in (self.alias_name, self.real_name), module.__name__
            module.__name__ = self.real_name
            assert module.__spec__.origin == "alias", module.__spec__  # well overridden
            assert module.__spec__.loader_state["aliased_spec"] is None
            assert self.target_spec_backup, self.target_spec_backup
            module.__spec__.loader_state["aliased_spec"] = self.target_spec_backup
            pass  # nothing else to do, module already loaded


    class ModuleAliasFinder(importlib.abc.MetaPathFinder):
        """
        Note : due to new call of _init_module_attrs(spec...) on aliased
        module, its __spec__ attribute will be changed by this new import...
        """

        @classmethod
        def find_spec(cls, fullname, *args, **kwargs):

            #print("MetaPathFinder FINDSPEC", fullname, args, kwargs)

            real_name = _get_module_alias_real_name(fullname)
            if real_name is None:
                return None  # no aliased module is known

            # TODO emit warnings/logging

            alias_loader = AliasingLoader(real_name=real_name, alias_name=fullname)

            spec = importlib.machinery.ModuleSpec(name=fullname,
                                           loader=alias_loader,
                                           origin="alias",
                                           loader_state={"aliased_name": fullname,
                                                         "aliased_spec": None},
                                           is_package=True)  # in doubt, assume...

            return spec



def install_import_proxifier():
    """
    Add a meta path hook before all others, so that new module loadings
    may be redirected to aliased module.

    Idempotent function.
    """
    if ModuleAliasFinder not in sys.meta_path:
        sys.meta_path.insert(0, ModuleAliasFinder)
    assert ModuleAliasFinder in sys.meta_path, sys.meta_path



if __name__ == "__main__":

    import logging.handlers

    install_import_proxifier()
    install_import_proxifier()  # idempotent

    register_module_alias("json.tool_alias", "json.tool")
    register_module_alias("mylogging", "logging")
    register_module_alias("mylogging", "logging")
    register_module_alias("infinite_recursion", "infinite_recursion2")
    register_module_alias("infinite_recursion2", "infinite_recursion")
    register_module_alias("unexisting_alias", "unexisting_module")

    fullname = "logging.handlers"
    print ("ALREADY THERE:", fullname, fullname in sys.modules)

    import json.tool_alias
    assert sys.modules["json.tool_alias"]
    assert json.tool_alias

    fullname = "json.comments"
    print ("ALREADY THERE:", fullname, fullname in sys.modules)

    fullname = "json.tool"
    print ("ALREADY THERE:", fullname, fullname in sys.modules)

    import json.tool
    if is_new_style_proxifier:
        print ("JSON TOOL SPEC loader_state:", json.tool.__spec__.loader_state)

    assert json.tool_alias is json.tool, (json.tool_alias,  json.tool)
    assert json.tool.__name__ == "json.tool", json.tool.__name__
    if is_new_style_proxifier:
        assert json.tool.__spec__.origin == "alias", json.tool.__spec__.origin
        assert json.tool.__spec__.name == "json.tool_alias"
        assert json.tool.__spec__.loader_state["aliased_spec"].name == "json.tool"

    from mylogging import config
    assert config.dictConfig
    assert "logging.config" in sys.modules

    from mylogging.handlers import RotatingFileHandler
    from logging.handlers import RotatingFileHandler as RotatingFileHandlerOriginal
    print("mylogging led to RotatingFileHandler", RotatingFileHandler)
    assert RotatingFileHandler is RotatingFileHandlerOriginal

    try:
        import infinite_recursion
    except RuntimeError:
        pass
    else:
        raise RuntimeError("Import should have led to infinite recursion")

    try:
        import unexisting_alias
    except ImportError as e:
        assert "unexisting_alias" in str(e), (str(e), vars(e))
        assert "unexisting_module" in str(e), str(e)
    else:
        raise RuntimeError("import error noy raised")

    try:
        import unexisting_module
    except ImportError as e:
        assert "unexisting_alias" not in str(e), str(e)
        assert "unexisting_module" in str(e), str(e)
    else:
        raise RuntimeError("import error noy raised")

    print("\n*** Tests were successful ***")
