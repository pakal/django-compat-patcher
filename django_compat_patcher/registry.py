from __future__ import absolute_import, print_function, unicode_literals

import collections
from django.utils import six

from . import default_settings

FIXERS_REGISTRY = collections.OrderedDict()


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


def register_compatibility_fixer(fixer_family,
                                   fixer_applied_from_django=None,
                                   fixer_applied_upto_django=None,
                                   feature_supported_from_django=None,
                                   feature_supported_upto_django=None):
    """
    Registers a fixer, which will be executed only if current django version
    is >= `apply_from_django` and <= `apply_upto_django` (let them None to have no limit).

    `feature_supported_from_django` and `feature_supported_upto_django` can be used to limit
    range of django versions for which related unit-tests are expected to work (i.e versions
    for which the feature is available, either as a monkey-paching or as standard django code).

    Version identifiers must be strings, eg. "1.9.1".
    """

    assert fixer_family and fixer_family.startswith("django"), fixer_family

    def _register_simple_fixer(func):
        fixer_id = func.__name__  # untouched ATM, not fully qualified
        new_fixer = dict(fixer_callable=func,
                         fixer_explanation=_extract_doc(func),
                         fixer_id=fixer_id,
                         fixer_family=fixer_family,
                         fixer_applied_from_django=_normalize_version(fixer_applied_from_django),
                         fixer_applied_upto_django=_normalize_version(fixer_applied_upto_django),
                         feature_supported_from_django=_normalize_version(feature_supported_from_django),
                         feature_supported_upto_django=_normalize_version(feature_supported_upto_django),)

        assert fixer_id not in FIXERS_REGISTRY, "duplicate fixer id %s detected" % fixer_id
        FIXERS_REGISTRY[fixer_id] = new_fixer
        #print("FIXERS_REGISTRY", FIXERS_REGISTRY)
    return _register_simple_fixer


def get_fixer_by_id(fixer_id):
    return FIXERS_REGISTRY[fixer_id]


def get_relevant_fixers(current_django_version,
                        # included_families=None,
                        # included_fixer_ids=None,
                        # excluded_families=None,
                        # excluded_fixer_ids=None
                        # TODO define these filters, and fetch them from django settings
                        settings=None,
                        log=None):
    """
    Selects the fixers to be applied on the target django version, based on the
    metadata of fixers, but also inclusion/exclusion lists provided as arguments.

    For inclusion filters, a None value means "include all", for exclusion filters
    it means "don't exclude any".
    """

    current_django_version = _normalize_version(current_django_version)

    relevant_fixers = []
    settings = settings or default_settings
    settings = settings if isinstance(settings, dict) else settings.__dict__ 
    log = log or (lambda x: x)

    for fixer_id, fixer in FIXERS_REGISTRY.items():
        assert fixer_id == fixer["fixer_id"], fixer

        if (fixer["fixer_applied_from_django"] and
            current_django_version < fixer["fixer_applied_from_django"]):
            log("Skipping fixer %s, useful only in subsequent django versions" % fixer_id)
            continue

        if (fixer["fixer_applied_upto_django"] and
            current_django_version > fixer["fixer_applied_upto_django"]):
            assert False, "Please update tests to account for first 'fixer_applied_upto_django' usage"
            log("Skipping fixer %s, useful only in previous django versions" % fixer_id)
            continue

        # TODO - inclusion and exclusion filtering (and its logging)

        relevant_fixers.append(fixer)

    return relevant_fixers


def _extract_fixer_ids(fixers):
    return [f["fixer_id"] for f in fixers]


def get_relevant_fixer_ids(*args, **kwargs):
    fixers = get_relevant_fixers(*args, **kwargs)
    return _extract_fixer_ids(fixers)
