
import pytest
import _test_utilities


@pytest.mark.django_db
def test_fix_behaviour_db_models_Model_save_positional_args():
    from test_project.models import SimpleModel

    obj = SimpleModel(name="positional", age=1)
    # All positional: force_insert, force_update, using, update_fields
    obj.save(False, False, None, None)
    assert obj.pk is not None

    obj.name = "updated"
    obj.save(False, True, None, None)  # force_update positional
    obj.refresh_from_db()
    assert obj.name == "updated"

    # Keyword args remain unaffected
    obj2 = SimpleModel(name="kwargs", age=2)
    obj2.save(force_insert=True)
    assert obj2.pk is not None

    # alters_data marker (used by Django templates to forbid unsafe calls) must be preserved
    assert SimpleModel.save.alters_data is True
    assert SimpleModel.asave.alters_data is True


@pytest.mark.django_db
def test_fix_behaviour_db_models_Model_asave_positional_args():
    from asgiref.sync import async_to_sync
    from test_project.models import SimpleModel

    obj = SimpleModel(name="async-positional", age=3)
    async_to_sync(obj.asave)(False, False, None, None)
    assert obj.pk is not None

    # Keyword args remain unaffected
    obj2 = SimpleModel(name="async-kwargs", age=4)
    async_to_sync(obj2.asave)(force_insert=True)
    assert obj2.pk is not None


def test_fix_deletion_db_models_constraints_CheckConstraint_check_kwarg():
    from django.db.models import CheckConstraint, Q

    constraint = CheckConstraint(check=Q(age__gte=0), name="age_gte_0")
    assert constraint.condition == Q(age__gte=0)

    # New-style condition= keyword is unaffected
    constraint2 = CheckConstraint(condition=Q(age__gte=0), name="age_gte_0_v2")
    assert constraint2.condition == Q(age__gte=0)


def test_fix_deletion_utils_html_format_html_without_args():
    from django.utils.html import format_html
    from django.utils.safestring import SafeString

    result = format_html("<b>safe text</b>")
    assert isinstance(result, SafeString)
    assert result == "<b>safe text</b>"

    # Normal usage (with args/kwargs) still works and still escapes
    result2 = format_html("<b>{}</b>", "<script>")
    assert result2 == "<b>&lt;script&gt;</b>"


def test_fix_behaviour_contrib_admin_ChangeList_get_filters_lookup_allowed_request_arg():
    from django.contrib.admin.exceptions import DisallowedModelAdminLookup
    from django.contrib.admin.options import ModelAdmin
    from django.contrib.admin.sites import AdminSite
    from django.contrib.admin.views.main import ChangeList
    from test_project.models import SimpleModel

    # Old-style override, predating the "request" parameter added in Django 5.0
    class OldStyleAdmin(ModelAdmin):
        def lookup_allowed(self, lookup, value):
            return lookup == "name"

    def _make_changelist(model_admin, filter_params):
        changelist = ChangeList.__new__(ChangeList)
        changelist.model_admin = model_admin
        changelist.model = SimpleModel
        changelist.lookup_opts = SimpleModel._meta
        changelist.list_filter = []
        changelist.date_hierarchy = None
        changelist.filter_params = filter_params
        return changelist

    old_style_admin = OldStyleAdmin(SimpleModel, AdminSite())

    # Must not raise TypeError even though lookup_allowed() doesn't accept a request arg
    changelist = _make_changelist(old_style_admin, {"name": ["x"]})
    filter_specs, has_filters, remaining_params, may_have_duplicates, has_active_filters = (
        changelist.get_filters(request=None)
    )
    assert remaining_params == {"name": ["x"]}

    # A lookup not allowed by the (old-style) override still raises as expected
    changelist2 = _make_changelist(old_style_admin, {"age": ["1"]})
    with pytest.raises(DisallowedModelAdminLookup):
        changelist2.get_filters(request=None)

    # New-style overrides (accepting request) are unaffected
    class NewStyleAdmin(ModelAdmin):
        def lookup_allowed(self, lookup, value, request):
            return request is not None

    new_style_admin = NewStyleAdmin(SimpleModel, AdminSite())
    changelist3 = _make_changelist(new_style_admin, {"name": ["x"]})
    changelist3.get_filters(request="a-real-request")
    with pytest.raises(DisallowedModelAdminLookup):
        changelist3.get_filters(request=None)


def test_fix_behaviour_forms_URLField_default_scheme():
    from django import forms

    field = forms.URLField(required=False)
    assert field.clean("example.com") == "http://example.com"

    field_https = forms.URLField(required=False, assume_scheme="https")
    assert field_https.clean("example.com") == "https://example.com"


def test_fix_deletion_db_models_enums_ChoicesMeta():
    from django.db.models import enums

    assert enums.ChoicesMeta is enums.ChoicesType
