
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
