from __future__ import absolute_import, print_function, unicode_literals

from django.utils import six

FIXERS_REGISTRY = []


def _normalize_version(version):
    if version is None:
        return version
    if isinstance(version, six.string_types):
        version = tuple(int(x) for x in version.split("."))
    assert len(version) <= 4, version
    assert (1, 3) <= version, version
    assert all(isinstance(x, six.integer_types) for x in version), version
    return version


def _extract_doc(func):
    doc = func.__doc__
    assert doc, "Fixer %r must provide a help string" % func
    return doc


def register_compatibility_fixer(fixer_applied_from_django=None,
                                   fixer_applied_upto_django=None,
                                   feature_supported_from_django=None,
                                   feature_supported_upto_django=None):
    """
    Registers a fixer, which will be executed only if current django version
    is >= `apply_from_django` and <= `apply_upto_django` (let them None to have no limit).

    `feature_supported_from_django` and `feature_supported_upto_django` can be used to limit
    range of django versions for which the related unit-test is expected to work (i.e versions
    for which is feature is available, either as a monkey-paching or as standard django code).

    Version identifiers must be strings, eg. "1.9.1".
    """
    def _register_simple_fixer(func):
        new_fixer = dict(fixer_applied_from_django=_normalize_version(fixer_applied_from_django),
                         fixer_applied_upto_django=_normalize_version(fixer_applied_upto_django),
                         feature_supported_from_django=_normalize_version(feature_supported_from_django),
                         feature_supported_upto_django=_normalize_version(feature_supported_upto_django),
                         fixer_callable=func,
                         fixer_explanation=_extract_doc(func))
        FIXERS_REGISTRY.append(new_fixer)
        #print("FIXERS_REGISTRY", FIXERS_REGISTRY)
    return _register_simple_fixer

