from __future__ import absolute_import, print_function, unicode_literals

import _test_utilities
import pytest

import django_compat_patcher
from django_compat_patcher import default_settings
from django_compat_patcher.registry import django_patching_registry


def test_fix_incoming_urls_submodule():
    from django.urls import (
        get_callable,
        RegexURLPattern,
        RegexURLResolver,
        NoReverseMatch,
    )

    assert get_callable


def test_fix_deletion_templatetags_future():
    from compat import render_to_string
    from django.templatetags.future import cycle, firstof

    rendered = render_to_string("core_tags/test_future_cycle_and_firstof.html")
    assert rendered.strip() == "row1\nA"


def test_fix_deletion_template_defaulttags_ssi():
    # already tested in "test_fix_deletion_templatetags_future_ssi()"
    from django.template.defaulttags import ssi

    assert callable(ssi)


def test_fix_behaviour_urls_resolvers_RegexURLPattern():

    from django.core.urlresolvers import RegexURLPattern

    has_lookup_str = hasattr(RegexURLPattern, "lookup_str")

    def dummy_view(request):
        return 72627

    pattern = RegexURLPattern("homepage/", dummy_view)
    assert pattern.callback is dummy_view
    pattern.add_prefix("muyprefix")
    assert pattern.callback is dummy_view
    if has_lookup_str:
        assert pattern.lookup_str.endswith(".dummy_view")  # complex on py3k

    pattern = RegexURLPattern("homepage/", "test_project.views.my_view")
    assert pattern.callback.__name__ == "my_view"
    if has_lookup_str:
        assert pattern.lookup_str == "test_project.views.my_view"
    pattern.add_prefix("myprefix")
    try:
        pattern.callback  # bad prefix now
    except ImportError:
        pass  # might or not raise, depending on django version (caching or not)
    if has_lookup_str:
        # our own "lookup_str" property bypasses the original, CACHED, one
        assert pattern.lookup_str == "myprefix.test_project.views.my_view"

    pattern = RegexURLPattern("homepage/", "my_view")
    with pytest.raises(ImportError):
        myvar = pattern.callback  # missing prefix
    if has_lookup_str:
        assert pattern.lookup_str == "my_view"  # missing prefix but works
    pattern.add_prefix("test_project.views")
    assert pattern.callback.__name__ == "my_view"
    if has_lookup_str:
        assert pattern.lookup_str == "test_project.views.my_view"


def test_fix_behaviour_core_urlresolvers_reverse_with_prefix():
    try:
        from django.core.urlresolvers import reverse
    except ImportError:
        from django.urls import reverse

    view = reverse("homepage")  # by view name
    assert view == "/homepage/"

    view = reverse("test_project.views.my_view")  # by dotted path
    assert view == "/my_view/"


def test_fix_behaviour_conf_urls_url():
    from django.conf.urls import url

    url(r"^admin2/", "test_project.views.my_view", name="test_admin_abc"),


def test_fix_deletion_conf_urls_patterns():
    import django.conf.urls
    from django.conf.urls import patterns, url

    patterns(
        "admin",
        (r"^admin1/", "test_project.views.my_view"),
        url(r"^admin2/", "test_project.views.my_view", name="test_admin_other"),
    )
    assert "patterns" in django.conf.urls.__all__


def test_fix_behaviour_template_smartif_OPERATORS_equals():
    from compat import render_to_string

    rendered = render_to_string("core_tags/test_smartif_operators.html", dict(a=3))
    assert rendered.strip() == "hello\nbye"


def test_fix_behaviour_core_management_parser_optparse():
    from django.core import management
    from six import StringIO
    from django.test.utils import captured_stderr, captured_stdout

    with captured_stdout() as stdout, captured_stderr():
        # Check that new, argparse-based commands, still work as intended!
        management.execute_from_command_line(['django-admin', 'diffsettings'])
    stdout_value = stdout.getvalue()
    print(stdout_value)
    assert "ALLOWED_HOSTS" in stdout_value

    # Check that optparse-based command works
    out = StringIO()
    management.call_command('optparse_cmd', stdout=out)
    assert out.getvalue() == "All right, let's dance Rock'n'Roll.\n"

    # Simulate command line execution
    with captured_stdout() as stdout, captured_stderr():
        # We skip checks since test project is not complete
        needs_skip_checks = (_test_utilities.DJANGO_VERSION_TUPLE >= (1, 10))
        cmd_line = ['django-admin', 'optparse_cmd'] + (["--skip-checks"] if needs_skip_checks else [])
        management.execute_from_command_line(cmd_line)
    stdout_value = stdout.getvalue()
    print(stdout_value)
    assert stdout_value == "All right, let's dance Rock'n'Roll.\n"

    # This fixer is UNSAFE!
    fixer_id = "fix_behaviour_core_management_parser_optparse"
    assert django_patching_registry.get_fixer_by_id(fixer_id)
    assert fixer_id in default_settings.DCP_EXCLUDE_FIXER_IDS
