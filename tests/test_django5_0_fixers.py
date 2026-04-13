
import _test_utilities


def test_fix_deletion_utils_baseconv():
    import django.utils.baseconv as baseconv
    from django.utils.baseconv import BaseConverter, base36, base62, base64

    # Basic encoding/decoding
    assert base36.encode(1234) == "ya"
    assert base36.decode("ya") == 1234

    assert base62.encode(1234) == "Ju"
    assert base62.decode("Ju") == 1234

    # Negative numbers
    assert base36.encode(-1234) == "-ya"
    assert base36.decode("-ya") == -1234

    # Custom converter
    base20 = BaseConverter("0123456789abcdefghij")
    assert base20.encode(1234) == "31e"
    assert base20.decode("31e") == 1234

    # Module-level access via django.utils
    import django.utils
    assert django.utils.baseconv is baseconv


def test_fix_deletion_utils_datetime_safe():
    import django.utils.datetime_safe as datetime_safe
    from django.utils.datetime_safe import date, datetime, new_date, new_datetime

    # Year < 1000 should format with leading zeros
    d = date(100, 8, 2)
    assert d.strftime("%Y/%m/%d") == "0100/08/02"

    dt = datetime(500, 3, 15, 12, 0, 0)
    assert dt.strftime("%Y-%m-%d") == "0500-03-15"

    # new_date and new_datetime helpers
    import datetime as real_dt
    real_d = real_dt.date(2023, 6, 1)
    safe_d = new_date(real_d)
    assert isinstance(safe_d, date)
    assert safe_d.year == 2023

    real_dt_obj = real_dt.datetime(2023, 6, 1, 10, 30)
    safe_dt = new_datetime(real_dt_obj)
    assert isinstance(safe_dt, datetime)
    assert safe_dt.year == 2023
    assert safe_dt.hour == 10

    # Module-level access via django.utils
    import django.utils
    assert django.utils.datetime_safe is datetime_safe


def test_fix_deletion_utils_timezone_utc():
    import datetime
    from django.utils import timezone

    # utc should be the standard datetime.timezone.utc
    assert timezone.utc is datetime.timezone.utc

    # Should work as a timezone in datetime operations
    aware_dt = datetime.datetime(2023, 1, 1, tzinfo=timezone.utc)
    assert aware_dt.utcoffset() == datetime.timedelta(0)


def test_fix_behaviour_utils_functional_cached_property_name_argument():
    from django.utils.functional import cached_property

    class MyClass:
        @cached_property
        def my_prop(self):
            return 42

    obj = MyClass()
    assert obj.my_prop == 42

    # The name argument should be accepted without raising TypeError
    def my_func(self):
        return 99

    prop = cached_property(my_func, name="my_func")

    class AnotherClass:
        pass

    # __set_name__ sets the name; after patching, passing name= should work
    assert prop is not None


def test_fix_deletion_utils_timezone_make_aware_is_dst():
    import datetime
    from django.utils import timezone

    naive = datetime.datetime(2023, 6, 15, 12, 0)

    # Basic usage without is_dst must still work unchanged
    aware = timezone.make_aware(naive, datetime.timezone.utc)
    assert aware.tzinfo is not None

    # Passing is_dst=False must not raise TypeError (parameter was removed)
    aware2 = timezone.make_aware(naive, datetime.timezone.utc, is_dst=False)
    assert aware == aware2

    # Passing is_dst=None must not raise TypeError
    aware3 = timezone.make_aware(naive, datetime.timezone.utc, is_dst=None)
    assert aware == aware3

    # TruncBase subclass must accept is_dst without TypeError
    from django.db.models.functions import TruncMonth
    trunc = TruncMonth("created", is_dst=None)
    assert trunc is not None

    # TruncMonth without is_dst still works normally
    trunc_no_dst = TruncMonth("created")
    assert trunc_no_dst is not None

    # QuerySet.datetimes also accepts is_dst (verify via signature inspection)
    from django.db.models.query import QuerySet
    import inspect
    sig = inspect.signature(QuerySet.datetimes)
    assert "is_dst" in sig.parameters


def test_fix_deletion_conf_settings_USE_L10N():
    from django.utils import formats
    from django.test.utils import override_settings

    # get_format should work regardless of USE_L10N value
    result = formats.get_format("DATE_FORMAT")
    assert result is not None

    # With USE_L10N=True in settings: localization enabled, function works
    with override_settings(USE_L10N=True):
        result_l10n = formats.get_format("DATE_FORMAT")
        assert result_l10n is not None

    # With USE_L10N=False in settings: function still returns a valid format string
    with override_settings(USE_L10N=False):
        result_no_l10n = formats.get_format("DATE_FORMAT")
        assert result_no_l10n is not None

    # Explicit use_l10n kwarg is still accepted and respected
    result_explicit = formats.get_format("DATE_FORMAT", use_l10n=False)
    assert result_explicit is not None

    result_explicit_true = formats.get_format("DATE_FORMAT", use_l10n=True)
    assert result_explicit_true is not None


def test_fix_deletion_forms_BaseForm_html_output():
    from django import forms

    class ContactForm(forms.Form):
        name = forms.CharField()
        email = forms.EmailField()

    form = ContactForm(data={"name": "Alice", "email": "alice@example.com"})
    assert form.is_valid()

    # Method must exist and be callable
    assert callable(getattr(form, "_html_output", None))

    # Calling _html_output must produce HTML without raising
    html = form._html_output(
        normal_row=(
            '<tr%(html_class_attr)s><th>%(label)s</th>'
            '<td>%(errors)s%(field)s%(help_text)s</td></tr>'
        ),
        error_row='<tr><td colspan="2">%s</td></tr>',
        row_ender="</td></tr>",
        help_text_html=' <span class="helptext">%s</span>',
        errors_on_separate_row=False,
    )
    assert "<tr" in html
    assert "<input" in html

    # Hidden fields are appended to the last row
    class FormWithHidden(forms.Form):
        visible = forms.CharField()
        token = forms.CharField(widget=forms.HiddenInput())

    hform = FormWithHidden(data={"visible": "x", "token": "secret"})
    h_html = hform._html_output(
        normal_row='<p>%(label)s %(field)s%(help_text)s</p>',
        error_row="<p>%s</p>",
        row_ender="</p>",
        help_text_html=" %s",
        errors_on_separate_row=False,
    )
    assert 'type="hidden"' in h_html

    # Invalid form: errors are rendered
    invalid_form = ContactForm(data={"name": "", "email": "not-an-email"})
    assert not invalid_form.is_valid()
    err_html = invalid_form._html_output(
        normal_row='<p>%(label)s %(errors)s %(field)s%(help_text)s</p>',
        error_row="<p>%s</p>",
        row_ender="</p>",
        help_text_html=" %s",
        errors_on_separate_row=True,
    )
    assert "errorlist" in err_html or "This field" in err_html


def test_fix_behaviour_db_models_query_QuerySet_iterator_prefetch_without_chunk_size(db):
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
    qs = user_model._default_manager.all().prefetch_related("groups")
    rows = list(qs.iterator())
    assert isinstance(rows, list)


def test_fix_behaviour_contrib_auth_backends_RemoteUserBackend_configure_user_created_argument(db):
    from django.contrib.auth.backends import RemoteUserBackend

    class LegacyConfigureUserBackend(RemoteUserBackend):
        def configure_user(self, request, user):
            user.first_name = "legacy"
            user.save(update_fields=["first_name"])
            return user

    backend = LegacyConfigureUserBackend()
    user = backend.authenticate(request=None, remote_user="legacy-remote-user")
    assert user is not None
    assert user.first_name == "legacy"


def test_fix_behaviour_test_SimpleTestCase_assertFormError_response_and_form_name_arguments():
    from types import SimpleNamespace
    from django import forms
    from django.test import SimpleTestCase

    class DemoForm(forms.Form):
        name = forms.IntegerField(required=True)

    form = DemoForm(data={})
    assert not form.is_valid()

    response = SimpleNamespace(context={"demo_form": form})
    test_case = SimpleTestCase()
    expected_error = [form.fields["name"].error_messages["required"]]
    test_case.assertFormError(response, "demo_form", "name", expected_error)


def test_fix_behaviour_db_models_expressions_OrderBy_nulls_false():
    from django.db.models import F

    asc_order = F("id").asc(nulls_first=False)
    desc_order = F("id").desc(nulls_last=False)
    assert asc_order.nulls_first is None
    assert desc_order.nulls_last is None


def test_fix_behaviour_test_SimpleTestCase_assertFormSetError_response_and_formset_name_arguments():
    from types import SimpleNamespace
    from django import forms
    from django.forms import formset_factory
    from django.test import SimpleTestCase

    class DemoForm(forms.Form):
        name = forms.IntegerField(required=True)

    demo_formset_class = formset_factory(DemoForm, extra=1)

    invalid_formset = demo_formset_class(
        data={
            "form-TOTAL_FORMS": "1",
            "form-INITIAL_FORMS": "0",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            "form-0-name": "not-a-number",
        }
    )
    assert not invalid_formset.is_valid()

    response = SimpleNamespace(context={"demo_formset": invalid_formset})
    test_case = SimpleTestCase()
    expected_error = [invalid_formset.forms[0].fields["name"].error_messages["invalid"]]
    test_case.assertFormSetError(response, "demo_formset", 0, "name", expected_error)

    valid_formset = demo_formset_class(
        data={
            "form-TOTAL_FORMS": "1",
            "form-INITIAL_FORMS": "0",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            "form-0-name": "1",
        }
    )
    assert valid_formset.is_valid()

    valid_response = SimpleNamespace(context={"demo_formset": valid_formset})
    test_case.assertFormSetError(valid_response, "demo_formset", 0, "name", None)
    if hasattr(test_case, "assertFormsetError"):
        test_case.assertFormsetError(valid_response, "demo_formset", 0, "name", None)


