=========================================
Annotated Django Deprecation Timeline
=========================================

This list is meant to help DCP keep track of what fixers have been implemented, which ones 
would be welcome, and which ones will most probably never be added (eg. because they introduce security issues, or deal with too complex details...).

See the different "kinds" available to triage changes, in CONTRIBUTE.rst

.. role:: kind

.. raw:: html

    <style> .kind {color: blue} </style>


2.2
----

See https://docs.djangoproject.com/en/2.2/releases/2.2/#backwards-incompatible-changes-in-2-2



2.1
-----

- contrib.auth.views.login(), logout(), password_change(), password_change_done(), password_reset(), password_reset_done(), password_reset_confirm(), and password_reset_complete() will be removed. :kind:`DELETION`
- The extra_context parameter of contrib.auth.views.logout_then_login() will be removed. :kind:`DELETION`
- django.test.runner.setup_databases() will be removed. :kind:`DELETION`
- django.utils.translation.string_concat() will be removed. :kind:`DELETION`
- django.core.cache.backends.memcached.PyLibMCCache will no longer support passing pylibmc behavior settings as top-level attributes of OPTIONS.
- The host parameter of django.utils.http.is_safe_url() will be removed. :kind:`DELETION`
- Silencing of exceptions raised while rendering the {% include %} template tag will be removed. :kind:`DELETION`
- DatabaseIntrospection.get_indexes() will be removed. :kind:`DELETION`
- The authenticate() method of authentication backends will require a request argument.


2.0
-----

- The weak argument to django.dispatch.signals.Signal.disconnect() will be removed.
- The django.forms.extras package will be removed.
- The assignment_tag helper will be removed.
- The host argument to assertsRedirects will be removed. The compatibility layer which allows absolute URLs to be considered equal to relative ones when the path is identical will also be removed.
- Field.rel will be removed.
- Field.remote_field.to attribute will be removed.
- The on_delete argument for ForeignKey and OneToOneField will be required.
- django.db.models.fields.add_lazy_relation() will be removed.
- When time zone support is enabled, database backends that don't support time zones won't convert aware datetimes to naive values in UTC anymore when such values are passed as parameters to SQL queries executed outside of the ORM, e.g. with cursor.execute().
- The django.contrib.auth.tests.utils.skipIfCustomUser() decorator will be removed.
- The GeoManager and GeoQuerySet classes will be removed.
- The django.contrib.gis.geoip module will be removed.
- The supports_recursion check for template loaders will be removed from:

  - django.template.engine.Engine.find_template()
  - django.template.loader_tags.ExtendsNode.find_template()
  - django.template.loaders.base.Loader.supports_recursion()
  - django.template.loaders.cached.Loader.supports_recursion()
  - The load_template() and load_template_sources() template loader methods will be removed.

- The template_dirs argument for template loaders will be removed: go.template.loaders.filesystem.Loader.get_template_sources()
- The django.template.loaders.base.Loader.__call__() method will be removed.
- Support for custom error views with a single positional parameter will be dropped.
- The mime_type attribute of django.utils.feedgenerator.Atom1Feed and django.utils.feedgenerator.RssFeed will be removed in favor of content_type.
- The app_name argument to include() will be removed.
- Support for passing a 3-tuple as the first argument to include() will be removed.
- Support for setting a URL instance namespace without an application namespace will be removed.
- Field._get_val_from_obj() will be removed in favor of Field.value_from_object().
- django.template.loaders.eggs.Loader will be removed.
- The current_app parameter to the contrib.auth views will be removed.
- The callable_obj keyword argument to SimpleTestCase.assertRaisesMessage() will be removed.
- Support for the allow_tags attribute on ModelAdmin methods will be removed.
- The enclosure keyword argument to SyndicationFeed.add_item() will be removed.
- The django.template.loader.LoaderOrigin and django.template.base.StringOrigin aliases for django.template.base.Origin will be removed.
- The makemigrations --exit option will be removed.
- Support for direct assignment to a reverse foreign key or many-to-many relation will be removed.
- The get_srid() and set_srid() methods of django.contrib.gis.geos.GEOSGeometry will be removed.
- The get_x(), set_x(), get_y(), set_y(), get_z(), and set_z() methods of django.contrib.gis.geos.Point will be removed.
- The get_coords() and set_coords() methods of django.contrib.gis.geos.Point will be removed.
- The cascaded_union property of django.contrib.gis.geos.MultiPolygon will be removed.
- django.utils.functional.allow_lazy() will be removed.
- The shell --plain option will be removed.
- The django.core.urlresolvers module will be removed.
- The model CommaSeparatedIntegerField will be removed. A stub field will remain for compatibility with historical migrations.
- Support for the template Context.has_key() method will be removed.
- Support for the django.core.files.storage.Storage.accessed_time(), created_time(), and modified_time() methods will be removed.
- Support for query lookups using the model name when Meta.default_related_name is set will be removed.
- The __search query lookup and the DatabaseOperations.fulltext_search_sql() method will be removed.
- The shim for supporting custom related manager classes without a _apply_rel_filters() method will be removed.
- Using User.is_authenticated() and User.is_anonymous() as methods will no longer be supported.
- The private attribute virtual_fields of Model._meta will be removed.
- The private keyword arguments virtual_only in Field.contribute_to_class() and virtual in Model._meta.add_field() will be removed.
- The javascript_catalog() and json_catalog() views will be removed.
- The django.contrib.gis.utils.precision_wkt() function will be removed.
- In multi-table inheritance, implicit promotion of a OneToOneField to a parent_link will be removed.
- Support for Widget._format_value() will be removed.
- FileField methods get_directory_name() and get_filename() will be removed.
- The mark_for_escaping() function and the classes it uses: EscapeData, EscapeBytes, EscapeText, EscapeString, and EscapeUnicode will be removed.
- The escape filter will change to use django.utils.html.conditional_escape().
- Manager.use_for_related_fields will be removed.
- Model Manager inheritance will follow MRO inheritance rules and the Meta.manager_inheritance_from_future to opt-in to this behavior will be removed.
- Support for old-style middleware using settings.MIDDLEWARE_CLASSES will be removed.


1.11
---------

See https://docs.djangoproject.com/en/2.2/releases/1.11/#backwards-incompatible-changes-in-1-11


1.10
-----

- Support for calling a SQLCompiler directly as an alias for calling its quote_name_unless_alias method will be removed.
- cycle and firstof template tags will be removed from the future template tag library (used during the 1.6/1.7 deprecation period). :kind:`DELETION` [FIXED]
- django.conf.urls.patterns() will be removed. :kind:`DELETION` [FIXED]
- Support for the prefix argument to django.conf.urls.i18n.i18n_patterns() will be removed.
- SimpleTestCase.urls will be removed.
- Using an incorrect count of unpacked values in the for template tag will raise an exception rather than fail silently.
- The ability to reverse URLs using a dotted Python path will be removed. :kind:`BEHAVIOUR` [FIXED]
- The ability to use a dotted Python path for the LOGIN_URL and LOGIN_REDIRECT_URL settings will be removed.
- Support for optparse will be dropped for custom management commands (replaced by argparse).
- The class django.core.management.NoArgsCommand will be removed. Use BaseCommand instead, which takes no arguments by default.
- django.core.context_processors module will be removed.
- django.db.models.sql.aggregates module will be removed.
- django.contrib.gis.db.models.sql.aggregates module will be removed.
- The following methods and properties of django.db.sql.query.Query will be removed:

  - Properties: aggregates and aggregate_select
  - Methods: add_aggregate, set_aggregate_mask, and append_aggregate_mask.

- django.template.resolve_variable will be removed.
- The following private APIs will be removed from django.db.models.options.Options (Model._meta):

  - get_field_by_name()
  - get_all_field_names()
  - get_fields_with_model()
  - get_concrete_fields_with_model()
  - get_m2m_with_model()
  - get_all_related_objects()
  - get_all_related_objects_with_model()
  - get_all_related_many_to_many_objects()
  - get_all_related_m2m_objects_with_model()

- The error_message argument of django.forms.RegexField will be removed.
- The unordered_list filter will no longer support old style lists.
- Support for string view arguments to url() will be removed. :kind:`BEHAVIOUR` [FIXED]
- The backward compatible shim to rename django.forms.Form._has_changed() to has_changed() will be removed.
- The removetags template filter will be removed.
- The remove_tags() and strip_entities() functions in django.utils.html will be removed.
- The is_admin_site argument to django.contrib.auth.views.password_reset() will be removed.
- django.db.models.field.subclassing.SubfieldBase will be removed.
- django.utils.checksums will be removed; its functionality is included in django-localflavor 1.1+.
- The original_content_type_id attribute on django.contrib.admin.helpers.InlineAdminForm will be removed.
- The backwards compatibility shim to allow FormMixin.get_form() to be defined with no default value for its form_class argument will be removed.
- The following settings will be removed:

  - ALLOWED_INCLUDE_ROOTS
  - TEMPLATE_CONTEXT_PROCESSORS
  - TEMPLATE_DEBUG
  - TEMPLATE_DIRS
  - TEMPLATE_LOADERS
  - TEMPLATE_STRING_IF_INVALID

- The backwards compatibility alias django.template.loader.BaseLoader will be removed.
- Django template objects returned by get_template() and select_template() won't accept a Context in their render() method anymore.
- Template response APIs will enforce the use of dict and backend-dependent template objects instead of Context and Template respectively.
- The current_app parameter for the following function and classes will be removed:

  - django.shortcuts.render()
  - django.template.Context()
  - django.template.RequestContext()
  - django.template.response.TemplateResponse()

- The dictionary and context_instance parameters for the following functions will be removed:

  - django.shortcuts.render()
  - django.shortcuts.render_to_response()
  - jango.template.loader.render_to_string()

- The dirs parameter for the following functions will be removed:

  - django.template.loader.get_template()
  - django.template.loader.select_template()
  - django.shortcuts.render()
  - django.shortcuts.render_to_response()

- Session verification will be enabled regardless of whether or not 'django.contrib.auth.middleware.SessionAuthenticationMiddleware' is in MIDDLEWARE_CLASSES.
- Private attribute django.db.models.Field.related will be removed.
- The --list option of the migrate management command will be removed.
- The ssi template tag will be removed. :kind:`DELETION` [FIXED]
- Support for the = comparison operator in the if template tag will be removed. :kind:`BEHAVIOUR` [FIXED]
- The backwards compatibility shims to allow Storage.get_available_name() and Storage.save() to be defined without a max_length argument will be removed.
- Support for the legacy %(<foo>)s syntax in ModelFormMixin.success_url will be removed.
- GeoQuerySet aggregate methods collect(), extent(), extent3d(), make_line(), and unionagg() will be removed.
- Ability to specify ContentType.name when creating a content type instance will be removed.
- Support for the old signature of allow_migrate will be removed. It changed from allow_migrate(self, db, model) to allow_migrate(self, db, app_label, model_name=None, \**hints).
- Support for the syntax of {% cycle %} that uses comma-separated arguments will be removed.
- The warning that Signer issues when given an invalid separator will become an exception.

1.9
-----

- django.utils.dictconfig will be removed. :kind:`DELETION` [FIXED]
- django.utils.importlib will be removed. :kind:`DELETION` [FIXED]
- django.utils.tzinfo will be removed. :kind:`DELETION` [FIXED]
- django.utils.unittest will be removed. :kind:`DELETION` [FIXED]
- The syncdb command will be removed. :kind:`DELETION` [WONTFIX]
- django.db.models.signals.pre_syncdb and django.db.models.signals.post_syncdb will be removed. :kind:`DELETION` [WONTFIX]
- allow_syncdb on database routers will no longer automatically become allow_migrate. :kind:`BEHAVIOUR` [WONTFIX]
- Automatic syncing of apps without migrations will be removed. Migrations will become compulsory for all apps unless you pass the --run-syncdb option to migrate. :kind:`BEHAVIOUR` [WONTFIX]
- The SQL management commands for apps without migrations, sql, sqlall, sqlclear, sqldropindexes, and sqlindexes, will be removed. :kind:`DELETION` [WONTFIX]
- Support for automatic loading of initial_data fixtures and initial SQL data will be removed. :kind:`BEHAVIOUR` [WONTFIX]
- All models will need to be defined inside an installed application or declare an explicit app_label. Furthermore, it won't be possible to import them before their application is loaded. In particular, it won't be possible to import models inside the root package of their application. :kind:`BEHAVIOUR` [WONTFIX]
- The model and form IPAddressField will be removed. A stub field will remain for compatibility with historical migrations. :kind:`DELETION` [FIXED, but for forms only]
- AppCommand.handle_app() will no longer be supported. :kind:`DELETION` [FIXED]
- RequestSite and get_current_site() will no longer be importable from django.contrib.sites.models. :kind:`DELETION` [FIXED]
- FastCGI support via the runfcgi management command will be removed. Please deploy your project using WSGI.
- django.utils.datastructures.SortedDict will be removed. Use collections.OrderedDict from the Python standard library instead. :kind:`DELETION` [FIXED]
- ModelAdmin.declared_fieldsets will be removed.
- Instances of util.py in the Django codebase have been renamed to utils.py in an effort to unify all util and utils references. The modules that provided backwards compatibility will be removed:

  - django.contrib.admin.util
  - django.contrib.gis.db.backends.util
  - django.db.backends.util
  - django.forms.util

- ModelAdmin.get_formsets will be removed. :kind:`DELETION` [FIXED]
- The backward compatibility shim introduced to rename the BaseMemcachedCache._get_memcache_timeout() method to get_backend_timeout() will be removed.
- The --natural and -n options for dumpdata will be removed.
- The use_natural_keys argument for serializers.serialize() will be removed.
- Private API django.forms.forms.get_declared_fields() will be removed.
- The ability to use a SplitDateTimeWidget with DateTimeField will be removed.
- The WSGIRequest.REQUEST property will be removed. :kind:`DELETION` [FIXED]
- The class django.utils.datastructures.MergeDict will be removed. :kind:`DELETION` [FIXED]
- The zh-cn and zh-tw language codes will be removed and have been replaced by the zh-hans and zh-hant language code respectively.
- The internal django.utils.functional.memoize will be removed. :kind:`DELETION` [FIXED]
- django.core.cache.get_cache will be removed. Add suitable entries to CACHES and use django.core.cache.caches instead.
- django.db.models.loading will be removed.
- Passing callable arguments to querysets will no longer be possible.
- BaseCommand.requires_model_validation will be removed in favor of requires_system_checks. Admin validators will be replaced by admin checks.
- The ModelAdmin.validator_class and default_validator_class attributes will be removed.
- ModelAdmin.validate() will be removed.
- django.db.backends.DatabaseValidation.validate_field will be removed in favor of the check_field method.
- The validate management command will be removed.
- django.utils.module_loading.import_by_path will be removed in favor of django.utils.module_loading.import_string.
- ssi and url template tags will be removed from the future template tag library (used during the 1.3/1.4 deprecation period). :kind:`DELETION` [FIXED]
- django.utils.text.javascript_quote will be removed.
- Database test settings as independent entries in the database settings, prefixed by \TEST_, will no longer be supported.
- The cache_choices option to ModelChoiceField and ModelMultipleChoiceField will be removed.
- The default value of the RedirectView.permanent attribute will change from True to False.
- django.contrib.sitemaps.FlatPageSitemap will be removed in favor of django.contrib.flatpages.sitemaps.FlatPageSitemap.
- Private API django.test.utils.TestTemplateLoader will be removed.
- The django.contrib.contenttypes.generic module will be removed.
- Private APIs django.db.models.sql.where.WhereNode.make_atom() and django.db.models.sql.where.Constraint will be removed.

1.8
-----

- django.contrib.comments will be removed. :kind:`OUTSOURCING` [FIXED]
- The following transaction management APIs will be removed:

  - TransactionMiddleware,
  - the decorators and context managers autocommit, commit_on_success, and commit_manually, defined in django.db.transaction,
  - the functions commit_unless_managed and rollback_unless_managed, also defined in django.db.transaction,
  - the TRANSACTIONS_MANAGED setting.

- The cycle and firstof template tags will auto-escape their arguments. In 1.6 and 1.7, this behavior is provided by the version of these tags in the future template tag library.
- The SEND_BROKEN_LINK_EMAILS setting will be removed. Add the django.middleware.common.BrokenLinkEmailsMiddleware middleware to your MIDDLEWARE_CLASSES setting instead.
- django.middleware.doc.XViewMiddleware will be removed. Use django.contrib.admindocs.middleware.XViewMiddleware instead.
- Model._meta.module_name was renamed to model_name.
- Remove the backward compatible shims introduced to rename get_query_set and similar queryset methods. This affects the following classes: BaseModelAdmin, ChangeList, BaseCommentNode, GenericForeignKey, Manager, SingleRelatedObjectDescriptor and ReverseSingleRelatedObjectDescriptor.
- Remove the backward compatible shims introduced to rename the attributes ChangeList.root_query_set and ChangeList.query_set.
- django.views.defaults.shortcut will be removed, as part of the goal of removing all django.contrib references from the core Django codebase. Instead use django.contrib.contenttypes.views.shortcut. django.conf.urls.shortcut will also be removed.
- Support for the Python Imaging Library (PIL) module will be removed, as it no longer appears to be actively maintained & does not work on Python 3. You are advised to install Pillow, which should be used instead.
- The following private APIs will be removed:

  - django.db.backend
  - django.db.close_connection()
  - django.db.backends.creation.BaseDatabaseCreation.set_autocommit()
  - django.db.transaction.is_managed()
  - django.db.transaction.managed()
  - django.forms.widgets.RadioInput will be removed in favor of django.forms.widgets.RadioChoiceInput.

- The module django.test.simple and the class django.test.simple.DjangoTestSuiteRunner will be removed. Instead use django.test.runner.DiscoverRunner.
- The module django.test._doctest will be removed. Instead use the doctest module from the Python standard library.
- The CACHE_MIDDLEWARE_ANONYMOUS_ONLY setting will be removed.
- Usage of the hard-coded Hold down 'Control', or 'Command' on a Mac, to select more than one string to override or append to user-provided help_text in forms for ManyToMany model fields will not be performed by Django anymore either at the model or forms layer.
- The Model._meta.get_(add|change|delete)_permission methods will be removed.
- The session key django_language will no longer be read for backwards compatibility.
- Geographic Sitemaps will be removed (django.contrib.gis.sitemaps.views.index and django.contrib.gis.sitemaps.views.sitemap).
- django.utils.html.fix_ampersands, the fix_ampersands template filter and django.utils.html.clean_html will be removed following an accelerated deprecation.

1.7
-----

- The module django.utils.simplejson will be removed. The standard library provides json which should be used instead.
- The function django.utils.itercompat.product will be removed. The Python builtin version should be used instead.
- Auto-correction of INSTALLED_APPS and TEMPLATE_DIRS settings when they are specified as a plain string instead of a tuple will be removed and raise an exception.
- The mimetype argument to the __init__ methods of HttpResponse, SimpleTemplateResponse, and TemplateResponse, will be removed. content_type should be used instead. This also applies to the render_to_response() shortcut and the sitemap views, index() and sitemap().
- When HttpResponse is instantiated with an iterator, or when content is set to an iterator, that iterator will be immediately consumed.
- The AUTH_PROFILE_MODULE setting, and the get_profile() method on the User model, will be removed.
- The cleanup management command will be removed. It's replaced by clearsessions.
- The daily_cleanup.py script will be removed.
- The depth keyword argument will be removed from select_related().
- The undocumented get_warnings_state()/restore_warnings_state() functions from django.test.utils and the save_warnings_state()/ restore_warnings_state() django.test.*TestCase methods are deprecated. Use the warnings.catch_warnings context manager available starting with Python 2.6 instead.
- The undocumented check_for_test_cookie method in AuthenticationForm will be removed following an accelerated deprecation. Users subclassing this form should remove calls to this method, and instead ensure that their auth related views are CSRF protected, which ensures that cookies are enabled.
- The version of django.contrib.auth.views.password_reset_confirm() that supports base36 encoded user IDs (django.contrib.auth.views.password_reset_confirm_uidb36) will be removed. If your site has been running Django 1.6 for more than PASSWORD_RESET_TIMEOUT_DAYS, this change will ha  e no effect. If not, then any password reset links generated before you upgrade to Django 1.7 won't work after the upgrade.
- The django.utils.encoding.StrAndUnicode mix-in will be removed. Define a __str__ method and apply the python_2_unicode_compatible() decorator instead.

    
1.6
###

- The attribute HttpRequest.raw_post_data was renamed to HttpRequest.body in 1.4. The backward compatibility will be removed, HttpRequest.raw_post_data will no longer work. :kind:`DELETION` [FIXED]
    
