


def test_fix_deletion_utils_text_replace_entity():

    from django.utils import text as text_module

    res = text_module._entity_re.sub(text_module._replace_entity, "HI&gt;")
    assert res == "HI>"
