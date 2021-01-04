from __future__ import absolute_import, print_function, unicode_literals

import os
import pytest
from django.contrib.auth.models import Permission

import _test_utilities


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (1, 10),
    reason="requires django.urls subpackage",
)
def test_fix_deletion_urls_RegexURLPattern_RegexURLResolver():

    from django.urls import RegexURLPattern
    from django.urls.resolvers import RegexURLPattern as RegexURLPattern2

    assert RegexURLPattern is RegexURLPattern2

    url = RegexURLPattern("^mypage\d", lambda x: x, name="mygoodurl")
    if hasattr(url, "check"):
        assert not url.check()
    assert url.resolve("mypage3")
    assert not url.resolve("mypage")

    from django.urls import RegexURLResolver
    from django.urls.resolvers import RegexURLResolver as RegexURLResolver2

    assert RegexURLResolver is RegexURLResolver2

    from django.conf import settings

    urlconf = settings.ROOT_URLCONF
    resolver = RegexURLResolver(r"^/", urlconf)
    if hasattr(resolver, "check"):
        assert not resolver.check()
    assert resolver.resolve("/homepage/")
    from django.urls import Resolver404

    with pytest.raises(Resolver404):
        resolver.resolve("/homepageXXX/")


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (1, 10),
    reason="requires django.urls subpackage",
)
def test_fix_deletion_core_urlresolvers():

    from django.urls import get_resolver
    from django.core.urlresolvers import get_resolver as get_resolver2

    assert get_resolver is get_resolver2


def test_fix_deletion_template_library_assignment_tag():
    from django import template

    register = template.Library()

    @register.assignment_tag
    def mytag():
        return "mycontent"

    assert mytag() == "mycontent"


def test_fix_deletion_utils_functional_allow_lazy():
    import six
    from django.utils.encoding import force_text
    from django.utils.functional import allow_lazy, lazy

    def myfunc(arg):
        return arg

    myfunc = allow_lazy(myfunc, six.text_type)

    proxy = myfunc(lazy(force_text, six.text_type)("mystr"))
    assert type(proxy) != str

    value = proxy.__str__()
    assert value == "mystr"


def test_fix_deletion_template_context_Context_has_key():
    from django.template.context import Context

    ctx = Context({"a": 65})
    assert ctx.has_key("a")
    assert not ctx.has_key("b")


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (1, 9), reason="Requires json_catalog() view"
)
def test_fix_deletion_views_i18n_javascript_and_json_catalog():
    from django.views.i18n import (
        javascript_catalog,
        json_catalog,
        render_javascript_catalog,
        null_javascript_catalog,
    )
    from django.http import HttpResponse
    from django.test.client import RequestFactory

    request = RequestFactory().get("/homepage/")

    response = javascript_catalog(request)
    assert isinstance(response, HttpResponse)

    response = json_catalog(request)
    assert isinstance(response, HttpResponse)

    response = null_javascript_catalog(request)
    assert isinstance(response, HttpResponse)

    response = render_javascript_catalog({"chateau": "castle"})
    assert isinstance(response, HttpResponse)


@pytest.mark.skipif(
    _test_utilities.DJANGO_VERSION_TUPLE < (2, 0),
    reason="Requires field.remote_field attribute",
)
def test_fix_behaviour_db_models_fields_related_ForeignKey_OneToOneField():

    from django.contrib.auth import get_user_model
    from django.db.models import ForeignKey, OneToOneField, CASCADE, PROTECT

    User = get_user_model()

    fk = ForeignKey(User)
    assert fk.remote_field.on_delete == CASCADE
    del fk

    fk = ForeignKey(User, on_delete=PROTECT)
    assert fk.remote_field.on_delete == PROTECT
    del fk

    fk = OneToOneField(User)
    assert fk.remote_field.on_delete == CASCADE
    del fk

    fk = OneToOneField(User, on_delete=PROTECT)
    assert fk.remote_field.on_delete == PROTECT
    del fk


def test_fix_behaviour_conf_urls_include_3tuples():
    from django.conf.urls import include

    try:
        from django.urls import include as include2

        assert include is include2
    except ImportError:  # normal for old Django versions
        if _test_utilities.DJANGO_VERSION_TUPLE >= (2, 0):
            raise

    from django.contrib import admin

    assert len(admin.site.urls) == 3
    include(admin.site.urls)  # is OK as a 3-tuple

    from django.core.exceptions import ImproperlyConfigured

    with pytest.raises(ImproperlyConfigured):
        include(admin.site.urls, namespace="mynamespace")


def test_fix_behaviour_contrib_auth_user_is_anonymous_is_authenticated_callability():
    from django.contrib.auth.models import AnonymousUser
    from django.contrib.auth import get_user_model
    from django.conf import settings

    property_usage_enabled = (_test_utilities.DJANGO_VERSION_TUPLE >= (1, 10))

    # In Django>=2.0, importing ANonymousUser triggers import of ContentTypes, so in minimal-settings mode its gives a
    # "RuntimeError: Model class django.contrib.contenttypes.models.ContentType doesn't declare an explicit app_label
    # and isn't in an application in INSTALLED_APPS."
    patching_is_impossible = (_test_utilities.DJANGO_VERSION_TUPLE >= (2, 0) and "django.contrib.contenttypes" not in settings.INSTALLED_APPS)

    user = AnonymousUser()

    if not patching_is_impossible:
        assert user.is_anonymous()
        assert user.is_anonymous() == 1 == True
        assert not user.is_authenticated()
        assert user.is_authenticated() == 0 == False

    if property_usage_enabled:
        assert user.is_anonymous
        assert user.is_anonymous == 1 == True
        assert not user.is_authenticated
        assert user.is_authenticated == 0 == False

    User = get_user_model()
    user = User(username="john")

    if not patching_is_impossible:
        assert not user.is_anonymous()
        assert user.is_anonymous() == 0 == False
        assert user.is_authenticated()
        assert user.is_authenticated() == 1 == True

    if property_usage_enabled:
        assert not user.is_anonymous
        assert user.is_anonymous == 0 == False
        assert user.is_authenticated
        assert user.is_authenticated == 1 == True


@pytest.mark.django_db
def test_fix_behaviour_db_models_fields_related_descriptors_ReverseManyToOneDescriptor_setter(db):
    from django.contrib.auth.models import User, Group
    from django.contrib.contenttypes.models import ContentType
    from test_project.models import SimpleModel, SimpleModelChild

    # MANY2MANY CASE

    group1 = Group.objects.create(name="group1")
    group2 = Group.objects.create(name="group2")
    user = User.objects.create_user(username="username")

    assert not group1.user_set.count()
    assert not group2.user_set.count()

    user.groups = [group1, group2]

    assert group1.user_set.get() == user
    assert group2.user_set.get() == user

    # MANY2ONE CASE

    model = SimpleModel.objects.create(name="parent")
    assert model.simplemodelchild_set.count() == 0

    from test_project.models import SimpleModelChild
    model_child = SimpleModelChild.objects.create(name="child")

    model.simplemodelchild_set = [model_child]

    assert model.simplemodelchild_set.get() == model_child
