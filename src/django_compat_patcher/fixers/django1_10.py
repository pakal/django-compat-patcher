from __future__ import absolute_import, print_function, unicode_literals

from functools import partial

from django.core.exceptions import ImproperlyConfigured

from ..deprecation import *
from ..registry import register_django_compatibility_fixer

# for backward-compatibility fixers
django1_10_bc_fixer = partial(
    register_django_compatibility_fixer,
    fixer_reference_version="1.10",
    fixer_applied_from_version="1.10",
)


def _get_url_utils():
    """
    Get URL utilities through versions, despite them being moved and refactored (with new "path()" syntax).
    """
    try:
        from django.urls import (
            get_callable,
            RegexURLPattern,
            URLPattern,
            RegexURLResolver,
            URLResolver,
            NoReverseMatch,
        )
    except ImportError:
        # previously, there was no "RoutePattern vs RegexPattern"
        from django.core.urlresolvers import (
            get_callable,
            RegexURLPattern,
            RegexURLPattern as URLPattern,
            RegexURLResolver,
            RegexURLResolver as URLResolver,
            NoReverseMatch,
        )  # old location
    return (
        get_callable,
        RegexURLPattern,
        URLPattern,
        RegexURLResolver,
        URLResolver,
        NoReverseMatch,
    )


@register_django_compatibility_fixer(
    fixer_reference_version="1.10", fixer_applied_upto_version="1.10"
)
def fix_incoming_urls_submodule(utils):
    """
    Put a forward compatibility import path for django.urls, which replaces django.core.urlresolvers
    """
    from django.core import urlresolvers
    import django
    utils.inject_module("django.urls", urlresolvers)
    utils.inject_attribute(django, "urls", urlresolvers)


@django1_10_bc_fixer()
def fix_deletion_templatetags_future(utils):
    """
    Preserve the "future" templatetags library, with its improved `firstof` and `cycle` tags.
    """
    import django.templatetags
    from ..django_legacy.django1_10.templatetags import future

    utils.inject_module("django.templatetags.future", future)
    utils.inject_attribute(django.templatetags, "future", future)

    from django.template.backends import django as django_templates

    _old_get_installed_libraries = django_templates.get_installed_libraries

    def get_installed_libraries():
        libraries = (
            _old_get_installed_libraries()
        )  # tries real __import__() calls on submodules
        libraries["future"] = "django.templatetags.future"
        # print(">>>>> FINAL libraries", libraries)
        return libraries

    utils.inject_callable(
        django_templates, "get_installed_libraries", get_installed_libraries
    )


@django1_10_bc_fixer()
def fix_deletion_template_defaulttags_ssi(utils):
    """
    Preserve the "ssi" default template tag.
    """
    from django.utils import six
    import django.template.defaulttags
    from ..django_legacy.django1_10.template import defaulttags

    utils.inject_callable(
        django.template.defaulttags,
        "include_is_allowed",
        defaulttags.include_is_allowed,
    )
    utils.inject_class(django.template.defaulttags, "SsiNode", defaulttags.SsiNode)
    utils.inject_callable(django.template.defaulttags, "ssi", defaulttags.ssi)
    django.template.defaulttags.register.tag(defaulttags.ssi)

    from django.template.engine import Engine

    _old_init = Engine.__init__

    def __init__(self, dirs=None, app_dirs=False, allowed_include_roots=None, **kwargs):
        if allowed_include_roots is None:
            allowed_include_roots = []
        if isinstance(allowed_include_roots, six.string_types):
            raise ImproperlyConfigured(
                "allowed_include_roots must be a tuple, not a string."
            )
        self.allowed_include_roots = allowed_include_roots
        _old_init(self, dirs=dirs, app_dirs=app_dirs, **kwargs)

    utils.inject_callable(Engine, "__init__", __init__)


@django1_10_bc_fixer()
def fix_behaviour_urls_resolvers_RegexURLPattern(utils):
    """
    Restore support for dotted-string view parameter in RegexURLPattern, instead passing a view object.
    """
    from django.utils import six

    get_callable, RegexURLPattern, URLPattern, RegexURLResolver, URLResolver, NoReverseMatch = (
        _get_url_utils()
    )
    del RegexURLPattern  # we work on the common URLPattern class

    @property
    def callback(self):
        callback = self.__dict__["callback"]  # bypass descriptor
        if isinstance(callback, six.string_types):
            callback_obj = get_callable(callback)
        else:
            callback_obj = callback
        return callback_obj

    @callback.setter
    def callback(self, value):
        self.__dict__["callback"] = value  # bypass descriptor

    # we inject a DATA-DESCRIPTOR, so it'll be accessed in prority
    # over "self.callback" instance attribute
    utils.inject_attribute(URLPattern, "callback", callback)

    def add_prefix(self, prefix):
        """
        Adds the prefix string to a string-based callback.
        """
        callback = self.__dict__["callback"]
        if not prefix or not isinstance(callback, six.string_types):
            return
        self.callback = prefix + "." + callback

    utils.inject_callable(URLPattern, "add_prefix", add_prefix)

    original_lookup_str = URLPattern.lookup_str

    @property  # not cached...
    def lookup_str(self):
        callback = self.__dict__["callback"]
        if isinstance(callback, six.string_types):
            # no need for warning, already emitted above
            return callback  # already a dotted path to view
        return original_lookup_str.__get__(self, self.__class__)

    utils.inject_attribute(URLPattern, "lookup_str", lookup_str)


@django1_10_bc_fixer()
def fix_behaviour_core_urlresolvers_reverse_with_prefix(utils):
    """
    Preserve the ability to call urlresolver on dotted string view,
    instead of explicit view name.
    """

    get_callable, RegexURLPattern, URLPattern, RegexURLResolver, URLResolver, NoReverseMatch = (
        _get_url_utils()
    )
    del RegexURLResolver  # we patch the common URLResolver class

    original_reverse_with_prefix = URLResolver._reverse_with_prefix

    def _reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs):
        original_lookup = lookup_view
        try:
            if self._is_callback(lookup_view):
                utils.emit_warning(
                    "Reversing by dotted path is deprecated (%s)." % original_lookup,
                    RemovedInDjango110Warning,
                    stacklevel=3,
                )
                lookup_view = get_callable(lookup_view)
        except (ImportError, AttributeError) as e:
            raise NoReverseMatch("Error importing '%s': %s." % (lookup_view, e))
        return original_reverse_with_prefix(self, lookup_view, _prefix, *args, **kwargs)

    utils.inject_callable(URLResolver, "_reverse_with_prefix", _reverse_with_prefix)


@django1_10_bc_fixer()
def fix_behaviour_conf_urls_url(utils):
    """
    Support passing views to url() as dotted strings instead of view objects.
    """
    from django.utils import six

    get_callable, RegexURLPattern, URLPattern, RegexURLResolver, URLResolver, NoReverseMatch = (
        _get_url_utils()
    )
    del URLPattern  # we stick to the old "regex-only" URL system

    from django.conf import urls

    def url(regex, view, kwargs=None, name=None, prefix=""):
        if isinstance(view, (list, tuple)):
            # For include(...) processing.
            urlconf_module, app_name, namespace = view
            return RegexURLResolver(
                regex, urlconf_module, kwargs, app_name=app_name, namespace=namespace
            )
        else:
            if isinstance(view, six.string_types):
                utils.emit_warning(
                    "Support for string view arguments to url() is deprecated and "
                    "will be removed in Django 1.10 (got %s). Pass the callable "
                    "instead." % view,
                    RemovedInDjango110Warning,
                    stacklevel=2,
                )
                if not view:
                    raise ImproperlyConfigured(
                        "Empty URL pattern view name not permitted (for pattern %r)"
                        % regex
                    )
                if prefix:
                    view = prefix + "." + view
            return RegexURLPattern(regex, view, kwargs, name)

    assert callable(urls.url)
    utils.inject_callable(urls, "url", url)


@django1_10_bc_fixer()
def fix_deletion_conf_urls_patterns(utils):
    """
    Preserve the patterns() builder for django urls.
    """
    from django.conf import urls

    get_callable, RegexURLPattern, URLPattern, RegexURLResolver, URLResolver, NoReverseMatch = (
        _get_url_utils()
    )
    del URLPattern  # we stick to the old "regex-only" URL system

    def patterns(prefix, *args):
        utils.emit_warning(
            "django.conf.urls.patterns() is deprecated and will be removed in "
            "Django 1.10. Update your urlpatterns to be a list of "
            "django.conf.urls.url() instances instead.",
            RemovedInDjango110Warning,
            stacklevel=2,
        )
        pattern_list = []
        for t in args:
            if isinstance(t, (list, tuple)):
                t = urls.url(prefix=prefix, *t)
            elif isinstance(t, RegexURLPattern):
                t.add_prefix(prefix)
            pattern_list.append(t)
        return pattern_list

    utils.inject_callable(urls, "patterns", patterns)

    urls.__all__.append(str("patterns"))  # so that star imports work fine


@django1_10_bc_fixer()
def fix_behaviour_template_smartif_OPERATORS_equals(utils):
    """
    Preserve support for a single '=' sign in {% if %} tag.
    """
    from django.template import smartif

    smartif.OPERATORS["="] = smartif.OPERATORS["=="]  # operator alias


''' REQUIRES PYTHON >= 3.3
@django1_10_bc_fixer()
def fix_deletion_core_context_processors(utils):
    """
    Keep django.core.context_processors middlewares as aliases for
    those of django.template.context_processors.
    """
    from .. import import_proxifier
    import_proxifier.install_module_alias_finder()  # idempotent
    import_proxifier.register_module_alias(module_alias="django.core.context_processors middlewares",
                                           real_module="django.template.context_processors")
'''


@django1_10_bc_fixer()
def fix_behaviour_core_management_parser_optparse(utils):
    """[UNSAFE] Preserve the support for old optparse instead of argparse parser, in management commands.

    Beware, Bash shell autocompletion might fail if some management commands use Optparse!
    """
    import sys
    from django.core.management import base, BaseCommand

    utils.inject_attribute(BaseCommand, "option_list", ())
    utils.inject_attribute(BaseCommand, "args", '')

    # ---

    @property
    def use_argparse(self):
        return not bool(self.option_list)
    utils.inject_attribute(BaseCommand, "use_argparse", use_argparse)

    def usage(self, subcommand):  # Predecessor of self.print_help()
        """
        Return a brief description of how to use this command, by
        default from the attribute ``self.help``.
        """
        usage = '%%prog %s [options] %s' % (subcommand, self.args)
        if self.help:
            return '%s\n\n%s' % (usage, self.help)
        else:
            return usage
    utils.inject_callable(BaseCommand, "usage", usage)

    # ---

    original_create_parser = BaseCommand.create_parser

    def create_parser(self, prog_name, subcommand, **kwargs):
        if not self.use_argparse:
            from optparse import OptionParser

            def store_as_int(option, opt_str, value, parser):
                setattr(parser.values, option.dest, int(value))

            # Backwards compatibility: use deprecated optparse module
            warnings.warn("OptionParser usage for Django management commands "
                          "is deprecated, use ArgumentParser instead",
                          RemovedInDjango110Warning)
            parser = OptionParser(prog=prog_name,
                                usage=self.usage(subcommand),
                                version=self.get_version())
            parser.add_option('-v', '--verbosity', action='callback', dest='verbosity', default=1,
                type='choice', choices=['0', '1', '2', '3'], callback=store_as_int,
                help='Verbosity level; 0=minimal output, 1=normal output, 2=verbose output, 3=very verbose output')
            parser.add_option('--settings',
                help=(
                    'The Python path to a settings module, e.g. '
                    '"myproject.settings.main". If this isn\'t provided, the '
                    'DJANGO_SETTINGS_MODULE environment variable will be used.'
                ),
            )
            parser.add_option('--pythonpath',
                help='A directory to add to the Python path, e.g. "/home/djangoprojects/myproject".'),
            parser.add_option('--traceback', action='store_true',
                help='Raise on CommandError exceptions')
            parser.add_option('--no-color', action='store_true', dest='no_color', default=False,
                help="Don't colorize the command output.")
            parser.add_option('--force-color', action='store_true',  # ADDED to old code
                help='FORWARD-COMPATIBILITY OPTION FOR OLD OPTPARSE PARSER')
            parser.add_option('--skip-checks', action='store_true',  # ADDED to old code
                help='FORWARD-COMPATIBILITY OPTION FOR OLD OPTPARSE PARSER')
            for opt in self.option_list:
                parser.add_option(opt)
        else:
            parser = original_create_parser(self, prog_name, subcommand)
            if self.args:
                # Keep compatibility and always accept positional arguments, like optparse when args is set
                parser.add_argument('args', nargs='*')
        return parser
    utils.inject_callable(BaseCommand, "create_parser", create_parser)

    # ---

    original_run_from_argv = BaseCommand.run_from_argv

    def run_from_argv(self, argv):
        """
        Set up any environment changes requested (e.g., Python path
        and Django settings), then run this command. If the
        command raises a ``CommandError``, intercept it and print it sensibly
        to stderr. If the ``--traceback`` option is present or the raised
        ``Exception`` is not ``CommandError``, raise it.
        """

        if self.use_argparse:
            original_run_from_argv(self, argv)
            return

        # Fallback for OPTPARSE #
        self._called_from_command_line = True
        parser = self.create_parser(argv[0], argv[1])
        options, args = parser.parse_args(argv[2:])
        cmd_options = vars(options)

        # Copy of the remainder of the original run_from_argv() method
        base.handle_default_options(options)
        try:
            self.execute(*args, **cmd_options)
        except Exception as e:
            if options.traceback or not isinstance(e, base.CommandError):
                raise

            # SystemCheckError takes care of its own formatting.
            if isinstance(e, base.SystemCheckError):
                self.stderr.write(str(e), lambda x: x)
            else:
                self.stderr.write('%s: %s' % (e.__class__.__name__, e))
            sys.exit(1)
        finally:
            base.connections.close_all()
    utils.inject_callable(BaseCommand, "run_from_argv", run_from_argv)

    # ---

    from django.core import management
    original_call_command = management.call_command

    def call_command(name, *args, **options):
        try:
            return original_call_command(name, *args, **options)
        except AttributeError as exc:
            # We expect something like "AttributeError: 'OptionParser' object has no attribute '_actions'"

            if "OptionParser" not in str(exc):
                raise  # It's an unrelated exception

            # FALLBACK TO OPTPARSE PARSER, by reproducing call_command() code

            # Load the command object.
            try:
                app_name = management.get_commands()[name]
            except KeyError:
                raise management.CommandError("Unknown command: %r" % name)

            if isinstance(app_name, BaseCommand):
                # If the command is already loaded, use it directly.
                command = app_name
            else:
                command = management.load_command_class(app_name, name)

            # Simulate argument parsing to get the option defaults (see #10080 for details).
            parser = command.create_parser('', name)
            # Legacy optparse method
            defaults, _ = parser.parse_args(args=[])
            defaults = dict(defaults.__dict__, **options)
            if 'skip_checks' not in options:
                defaults['skip_checks'] = True

            return command.execute(*args, **defaults)
    utils.inject_callable(management, "call_command", call_command)
