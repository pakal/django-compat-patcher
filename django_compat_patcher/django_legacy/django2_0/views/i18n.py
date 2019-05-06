import importlib
import itertools
import json
import os

from django import http
from django.apps import apps
from django.template import Context, Engine
from django.utils import six
from django.utils._os import upath
from django.utils.translation import (
    check_for_language, get_language, to_locale,
)
from django.utils.translation.trans_real import DjangoTranslation
from django.views.i18n import js_catalog_template, get_formats

from django_compat_patcher.deprecation import *


DEFAULT_PACKAGES = ['django.conf']
LANGUAGE_QUERY_PARAMETER = 'language'


def render_javascript_catalog(catalog=None, plural=None):
    template = Engine().from_string(js_catalog_template)

    def indent(s):
        return s.replace('\n', '\n  ')

    context = Context({
        'catalog_str': indent(json.dumps(
            catalog, sort_keys=True, indent=2)) if catalog else None,
        'formats_str': indent(json.dumps(
            get_formats(), sort_keys=True, indent=2)),
        'plural': plural,
    })

    return http.HttpResponse(template.render(context), 'text/javascript')



def get_javascript_catalog(locale, domain, packages):
    app_configs = apps.get_app_configs()
    allowable_packages = set(app_config.name for app_config in app_configs)
    allowable_packages.update(DEFAULT_PACKAGES)
    packages = [p for p in packages if p in allowable_packages]
    paths = []
    # paths of requested packages
    for package in packages:
        p = importlib.import_module(package)
        path = os.path.join(os.path.dirname(upath(p.__file__)), 'locale')
        paths.append(path)

    trans = DjangoTranslation(locale, domain=domain, localedirs=paths)
    trans_cat = trans._catalog

    plural = None
    if '' in trans_cat:
        for line in trans_cat[''].split('\n'):
            if line.startswith('Plural-Forms:'):
                plural = line.split(':', 1)[1].strip()
    if plural is not None:
        # this should actually be a compiled function of a typical plural-form:
        # Plural-Forms: nplurals=3; plural=n%10==1 && n%100!=11 ? 0 :
        #               n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2;
        plural = [el.strip() for el in plural.split(';') if el.strip().startswith('plural=')][0].split('=', 1)[1]

    pdict = {}
    maxcnts = {}
    catalog = {}
    trans_fallback_cat = trans._fallback._catalog if trans._fallback else {}
    for key, value in itertools.chain(six.iteritems(trans_cat), six.iteritems(trans_fallback_cat)):
        if key == '' or key in catalog:
            continue
        if isinstance(key, six.string_types):
            catalog[key] = value
        elif isinstance(key, tuple):
            msgid = key[0]
            cnt = key[1]
            maxcnts[msgid] = max(cnt, maxcnts.get(msgid, 0))
            pdict.setdefault(msgid, {})[cnt] = value
        else:
            raise TypeError(key)
    for k, v in pdict.items():
        catalog[k] = [v.get(i, '') for i in range(maxcnts[k] + 1)]

    return catalog, plural


def _get_locale(request):
    language = request.GET.get(LANGUAGE_QUERY_PARAMETER)
    if not (language and check_for_language(language)):
        language = get_language()
    return to_locale(language)


def _parse_packages(packages):
    if packages is None:
        packages = list(DEFAULT_PACKAGES)
    elif isinstance(packages, six.string_types):
        packages = packages.split('+')
    return packages


def null_javascript_catalog(request, domain=None, packages=None):
    """
    Returns "identity" versions of the JavaScript i18n functions -- i.e.,
    versions that don't actually do anything.
    """
    return render_javascript_catalog()


def javascript_catalog(request, domain='djangojs', packages=None):
    """
    Returns the selected language catalog as a javascript library.

    Receives the list of packages to check for translations in the
    packages parameter either from an infodict or as a +-delimited
    string from the request. Default is 'django.conf'.

    Additionally you can override the gettext domain for this view,
    but usually you don't want to do that, as JavaScript messages
    go to the djangojs domain. But this might be needed if you
    deliver your JavaScript source from Django templates.
    """
    warnings.warn(
        "The javascript_catalog() view is deprecated in favor of the "
        "JavaScriptCatalog view.", RemovedInDjango20Warning, stacklevel=2
    )
    locale = _get_locale(request)
    packages = _parse_packages(packages)
    catalog, plural = get_javascript_catalog(locale, domain, packages)
    return render_javascript_catalog(catalog, plural)


def json_catalog(request, domain='djangojs', packages=None):
    """
    Return the selected language catalog as a JSON object.

    Receives the same parameters as javascript_catalog(), but returns
    a response with a JSON object of the following format:

        {
            "catalog": {
                # Translations catalog
            },
            "formats": {
                # Language formats for date, time, etc.
            },
            "plural": '...'  # Expression for plural forms, or null.
        }
    """
    warnings.warn(
        "The json_catalog() view is deprecated in favor of the "
        "JSONCatalog view.", RemovedInDjango20Warning, stacklevel=2
    )
    locale = _get_locale(request)
    packages = _parse_packages(packages)
    catalog, plural = get_javascript_catalog(locale, domain, packages)
    data = {
        'catalog': catalog,
        'formats': get_formats(),
        'plural': plural,
    }
    return http.JsonResponse(data)
