


def test_fix_deletion_utils_text_replace_entity():

    from django.utils import text as text_module

    res = text_module._entity_re.sub(text_module._replace_entity, "HI&gt;")
    assert res == "HI>"


def test_fix_behaviour_core_validators_EmailValidator_whitelist():
    from django.core.validators import EmailValidator

    validator = EmailValidator(whitelist=['localdomain'])
    assert validator.domain_allowlist == ['localdomain']
    assert validator('email@localdomain') is None
    assert validator.domain_allowlist == validator.domain_whitelist

    validator = EmailValidator()
    validator.domain_whitelist = ['mydomain2']
    assert validator.domain_allowlist == validator.domain_whitelist == ['mydomain2']

    validator = EmailValidator(allowlist=['localdomain3'])
    assert validator.domain_allowlist == ['localdomain3']
    assert validator('email@localdomain3') is None
    assert validator.domain_allowlist == validator.domain_whitelist