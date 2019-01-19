from __future__ import absolute_import, print_function, unicode_literals

import collections

from django.utils import six

from django_compat_patcher.utilities import _tuplify_version
from . import utilities

FIXERS_REGISTRY = collections.OrderedDict()


def _extract_doc(func):
    """Extract and check the docstring of a callable"""
    doc = func.__doc__
    assert doc, "Fixer %r must provide a help string" % func
    return doc


def register_compatibility_fixer(fixer_reference_version,
                                 fixer_applied_from_django=None,  # INCLUDING this version
                                 fixer_applied_upto_django=None,  # EXCLUDING this version
                                 fixer_delayed=False,
                                 feature_supported_from_django=None,
                                 feature_supported_upto_django=None,
                                 ):
    """
    Registers a fixer, which will be executed only if current django version
    is >= `fixer_applied_from_django` and < `fixer_applied_upto_django` (let them None to have no limit).

    `fixer_reference_version` is mainly here for documentation purposes.

    `feature_supported_from_django` and `feature_supported_upto_django` will be used to limit
    range of django versions for which related unit-tests are expected to work (i.e versions
    for which the feature is available, either as a monkey-paching or as standard django code).

    Version identifiers must be strings, eg. "1.9.1".

    If `fixer_delayed`is True, the fixer is only applied after django.setup() has been called
    (eg. so that ORM models are available for introspection and patching).
    """

    assert isinstance(fixer_reference_version, six.string_types)  # eg. "1.9"
    assert fixer_delayed in (True, False), fixer_delayed

    fixer_family = "django" + fixer_reference_version  # eg. django1.9

    def _register_simple_fixer(func):
        fixer_id = func.__name__  # untouched ATM, not fully qualified
        new_fixer = dict(fixer_callable=func,
                         fixer_explanation=_extract_doc(func),
                         fixer_id=fixer_id,
                         fixer_reference_version=_tuplify_version(fixer_reference_version),
                         fixer_family=fixer_family,
                         fixer_applied_from_django=_tuplify_version(fixer_applied_from_django),
                         fixer_applied_upto_django=_tuplify_version(fixer_applied_upto_django),
                         fixer_delayed=fixer_delayed,
                         feature_supported_from_django=_tuplify_version(feature_supported_from_django),
                         feature_supported_upto_django=_tuplify_version(feature_supported_upto_django), )

        assert fixer_id not in FIXERS_REGISTRY, "duplicate fixer id %s detected" % fixer_id
        FIXERS_REGISTRY[fixer_id] = new_fixer
        # print("FIXERS_REGISTRY", FIXERS_REGISTRY)

    return _register_simple_fixer


def get_fixer_by_id(fixer_id):
    return FIXERS_REGISTRY[fixer_id]


def get_relevant_fixers(current_django_version,
                        settings=None,
                        log=None):
    """
    Selects the fixers to be applied on the target django version, based on the
    metadata of fixers, but also inclusion/exclusion lists provided as arguments.

    For inclusion/exclusion filters, a special "*" value means "all fixers", 
    else a list of strings is expected.
    """

    current_django_version = _tuplify_version(current_django_version)

    relevant_fixers = []

    log = log or (lambda x: x)

    ALL = "*"  # special value for patcher settings
    include_fixer_ids = utilities.get_patcher_setting("DCP_INCLUDE_FIXER_IDS", settings=settings)
    include_fixer_families = utilities.get_patcher_setting("DCP_INCLUDE_FIXER_FAMILIES", settings=settings)
    exclude_fixer_ids = utilities.get_patcher_setting("DCP_EXCLUDE_FIXER_IDS", settings=settings)
    exclude_fixer_families = utilities.get_patcher_setting("DCP_EXCLUDE_FIXER_FAMILIES", settings=settings)

    for fixer_id, fixer in FIXERS_REGISTRY.items():
        assert fixer_id == fixer["fixer_id"], fixer

        if (fixer["fixer_applied_from_django"] and
                    current_django_version < fixer["fixer_applied_from_django"]):  # SMALLER STRICTLY
            log("Skipping fixer %s, useful only in subsequent django versions" % fixer_id)
            continue

        if (fixer["fixer_applied_upto_django"] and
                    current_django_version >= fixer["fixer_applied_upto_django"]):  # GREATER OR EQUAL
            log("Skipping fixer %s, useful only in previous django versions" % fixer_id)
            continue

        included = False
        if include_fixer_ids == ALL or (fixer_id in include_fixer_ids):
            included = True
        if include_fixer_families == ALL or (fixer["fixer_family"] in include_fixer_families):
            included = True

        if not included:
            log("Skipping fixer having neither id (%s) nor family (%s) included by patcher settings" % (fixer_id, fixer["fixer_family"]))
            continue

        if exclude_fixer_ids == ALL or (fixer_id in exclude_fixer_ids):
            log("Skipping fixer %s, excluded by patcher settings" % fixer_id)
            continue

        if exclude_fixer_families == ALL or (fixer["fixer_family"] in exclude_fixer_families):
            log("Skipping fixer %s, having family %s excluded by patcher settings" % (fixer_id, fixer["fixer_family"]))
            continue

        # cheers, this fixer has passed all filters!
        relevant_fixers.append(fixer)

    return relevant_fixers


def _extract_fixer_ids(fixers):
    return [f["fixer_id"] for f in fixers]


def get_relevant_fixer_ids(*args, **kwargs):
    fixers = get_relevant_fixers(*args, **kwargs)
    return _extract_fixer_ids(fixers)


def get_all_fixers():
    return list(FIXERS_REGISTRY.values())
