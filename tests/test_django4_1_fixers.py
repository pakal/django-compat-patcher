


def test_fix_deletion_utils_text_replace_entity():

    from django.utils import text as text_module

    res = text_module._entity_re.sub(text_module._replace_entity, "HI&gt;")
    assert res == "HI>"


def test_fix_behaviour_core_validators_EmailValidator_whitelist():
    from django.core.validators import EmailValidator

    has_allowlist = hasattr(EmailValidator, "domain_allowlist")

    validator = EmailValidator(whitelist=['localdomain'])
    assert validator('email@localdomain') is None
    if has_allowlist:
        assert validator.domain_allowlist == ['localdomain']
        assert validator.domain_allowlist == validator.domain_whitelist

    validator = EmailValidator()
    validator.domain_whitelist = ['mydomain2']
    if has_allowlist:
        assert validator.domain_allowlist == validator.domain_whitelist == ['mydomain2']

    if has_allowlist:
        validator = EmailValidator(allowlist=['localdomain3'])
        assert validator('email@localdomain3') is None
        assert validator.domain_allowlist == ['localdomain3']
        assert validator.domain_allowlist == validator.domain_whitelist


def test_fix_behaviour_views_static_was_modified_since():
    import time
    from django.views.static import was_modified_since
    assert was_modified_since("Wed, 21 Oct 2015 07:28:00 GMT", time.time(), 8262726)
    assert not was_modified_since("Wed, 21 Oct 2015 07:28:00 GMT", 100, size=2356)