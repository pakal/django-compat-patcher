=========================================
Annotated Django Deprecation Timeline
=========================================

This list is meant to help DCP keep track of what fixers have been implemented, which ones 
would be welcome, and which ones will most probably never be added (eg. because they introduce security issues, or deal with too complex details...).

See the different "kinds" available to triage changes, in CONTRIBUTE.rst

.. role:: kind

.. raw:: html

    <style> .kind {color: blue} </style>



4.0
----

DeleteView now uses FormMixin to handle POST requests. As a consequence, any custom deletion logic in delete() handlers should be moved to form_valid(), or a shared helper method, if required.

Support for cx_Oracle < 7.0 is removed.
To allow serving a Django site on a subpath without changing the value of STATIC_URL, the leading slash is removed from that setting (now 'static/') in the default startproject template.
The AdminSite method for the admin index view is no longer decorated with never_cache when accessed directly, rather than via the recommended AdminSite.urls property, or AdminSite.get_urls() method.
Unsupported operations on a sliced queryset now raise TypeError instead of AssertionError.
The undocumented django.test.runner.reorder_suite() function is renamed to reorder_tests(). It now accepts an iterable of tests rather than a test suite, and returns an iterator of tests.
Calling FileSystemStorage.delete() with an empty name now raises ValueError instead of AssertionError.
Calling EmailMultiAlternatives.attach_alternative() or EmailMessage.attach() with an invalid content or mimetype arguments now raise ValueError instead of AssertionError.
assertHTMLEqual() no longer considers a non-boolean attribute without a value equal to an attribute with the same name and value.
Tests that fail to load, for example due to syntax errors, now always match when using test --tag.
The undocumented django.contrib.admin.utils.lookup_needs_distinct() function is renamed to lookup_spawns_duplicates().
The undocumented HttpRequest.get_raw_uri() method is removed. The HttpRequest.build_absolute_uri() method may be a suitable alternative.
The object argument of undocumented ModelAdmin.log_addition(), log_change(), and log_deletion() methods is renamed to obj.
RssFeed, Atom1Feed, and their subclasses now emit elements with no content as self-closing tags.
NodeList.render() no longer casts the output of render() method for individual nodes to a string. Node.render() should always return a string as documented.
The where_class property of django.db.models.sql.query.Query and the where_class argument to the private get_extra_restriction() method of ForeignObject and ForeignObjectRel are removed. If needed, initialize django.db.models.sql.where.WhereNode instead.
The filter_clause argument of the undocumented Query.add_filter() method is replaced by two positional arguments filter_lhs and filter_rhs.
CsrfViewMiddleware now uses request.META['CSRF_COOKIE_NEEDS_UPDATE'] in place of request.META['CSRF_COOKIE_USED'], request.csrf_cookie_needs_reset, and response.csrf_cookie_set to track whether the CSRF cookie should be sent. This is an undocumented, private API.
The undocumented TRANSLATOR_COMMENT_MARK constant is moved from django.template.base to django.utils.translation.template.
The real_apps argument of the undocumented django.db.migrations.state.ProjectState.__init__() method must now be a set if provided.
RadioSelect and CheckboxSelectMultiple widgets are now rendered in <div> tags so they are announced more concisely by screen readers. If you need the previous behavior, override the widget template with the appropriate template from Django 3.2.
The floatformat template filter no longer depends on the USE_L10N setting and always returns localized output. Use the u suffix to disable localization.
The default value of the USE_L10N setting is changed to True. See the Localization section above for more details.
As part of the move to zoneinfo, django.utils.timezone.utc is changed to alias datetime.timezone.utc.
The minimum supported version of asgiref is increased from 3.3.2 to 3.4.1.

These features have reached the end of their deprecation cycle and are removed in Django 4.0.

See Features deprecated in 3.0 for details on these changes, including how to remove usage of these features.
django.utils.http.urlquote(), urlquote_plus(), urlunquote(), and urlunquote_plus() are removed.  :kind:`DELETION` [FIXED]
django.utils.encoding.force_text() and smart_text() are removed.  :kind:`DELETION` [FIXED]
django.utils.translation.ugettext(), ugettext_lazy(), ugettext_noop(), ungettext(), and ungettext_lazy() are removed.  :kind:`DELETION` [FIXED]
django.views.i18n.set_language() doesn’t set the user language in request.session (key _language).
alias=None is required in the signature of django.db.models.Expression.get_group_by_cols() subclasses.
django.utils.text.unescape_entities() is removed.  :kind:`DELETION` [FIXED]
django.utils.http.is_safe_url() is removed.  :kind:`DELETION` [FIXED]

See Features deprecated in 3.1 for details on these changes, including how to remove usage of these features.
The PASSWORD_RESET_TIMEOUT_DAYS setting is removed.
The isnull lookup no longer allows using non-boolean values as the right-hand side.
The django.db.models.query_utils.InvalidQuery exception class is removed.  :kind:`DELETION` [FIXED]
The django-admin.py entry point is removed.
The HttpRequest.is_ajax() method is removed.  :kind:`DELETION` [FIXED]
Support for the pre-Django 3.1 encoding format of cookies values used by django.contrib.messages.storage.cookie.CookieStorage is removed.
Support for the pre-Django 3.1 password reset tokens in the admin site (that use the SHA-1 hashing algorithm) is removed.
Support for the pre-Django 3.1 encoding format of sessions is removed.
Support for the pre-Django 3.1 django.core.signing.Signer signatures (encoded with the SHA-1 algorithm) is removed.
Support for the pre-Django 3.1 django.core.signing.dumps() signatures (encoded with the SHA-1 algorithm) in django.core.signing.loads() is removed.
Support for the pre-Django 3.1 user sessions (that use the SHA-1 algorithm) is removed.
The get_response argument for django.utils.deprecation.MiddlewareMixin.__init__() is required and doesn’t accept None.  :kind:`BEHAVIOUR` [FIXED]
The providing_args argument for django.dispatch.Signal is removed.  :kind:`BEHAVIOUR` [FIXED]
The length argument for django.utils.crypto.get_random_string() is required.  :kind:`BEHAVIOUR` [FIXED]
The list message for ModelMultipleChoiceField is removed.  :kind:`DELETION` [FIXED]
Support for passing raw column aliases to QuerySet.order_by() is removed.
The NullBooleanField model field is removed, except for support in historical migrations.   :kind:`DELETION` [WORKAROUND]
django.conf.urls.url() is removed.  :kind:`DELETION` [FIXED]
The django.contrib.postgres.fields.JSONField model field is removed, except for support in historical migrations.  :kind:`DELETION` [WORKAROUND]
django.contrib.postgres.fields.jsonb.KeyTransform and django.contrib.postgres.fields.jsonb.KeyTextTransform are removed.  :kind:`DELETION` [FIXED]
django.contrib.postgres.forms.JSONField is removed.  :kind:`DELETION` [FIXED]
The {% ifequal %} and {% ifnotequal %} template tags are removed.  :kind:`DELETION` [FIXED]
The DEFAULT_HASHING_ALGORITHM transitional setting is removed.


3.2
----

**Miscellaneous**

Django now supports non-pytz time zones, such as Python 3.9+’s zoneinfo module and its backport.

The undocumented SpatiaLiteOperations.proj4_version() method is renamed to proj_version().

slugify() now removes leading and trailing dashes and underscores.

The intcomma and intword template filters no longer depend on the USE_L10N setting.

Support for argon2-cffi < 19.1.0 is removed.

The cache keys no longer includes the language when internationalization is disabled (USE_I18N = False) and localization is enabled (USE_L10N = True). After upgrading to Django 3.2 in such configurations, the first request to any previously cached value will be a cache miss.

ForeignKey.validate() now uses _base_manager rather than _default_manager to check that related instances exist.

When an application defines an AppConfig subclass in an apps.py submodule, Django now uses this configuration automatically, even if it isn’t enabled with default_app_config. Set default = False in the AppConfig subclass if you need to prevent this behavior. See What’s new in Django 3.2 for more details.

Instantiating an abstract model now raises TypeError.

Keyword arguments to setup_databases() are now keyword-only.

The undocumented django.utils.http.limited_parse_qsl() function is removed. Please use urllib.parse.parse_qsl() instead.

django.test.utils.TestContextDecorator now uses addCleanup() so that cleanups registered in the setUp() method are called before TestContextDecorator.disable().

SessionMiddleware now raises a SessionInterrupted exception instead of SuspiciousOperation when a session is destroyed in a concurrent request.

The django.db.models.Field equality operator now correctly distinguishes inherited field instances across models. Additionally, the ordering of such fields is now defined.

The undocumented django.core.files.locks.lock() function now returns False if the file cannot be locked, instead of raising BlockingIOError.

The password reset mechanism now invalidates tokens when the user email is changed.

makemessages command no longer processes invalid locales specified using makemessages --locale option, when they contain hyphens ('-').

The django.contrib.auth.forms.ReadOnlyPasswordHashField form field is now disabled by default. Therefore UserChangeForm.clean_password() is no longer required to return the initial value.

The cache.get_many(), get_or_set(), has_key(), incr(), decr(), incr_version(), and decr_version() cache operations now correctly handle None stored in the cache, in the same way as any other value, instead of behaving as though the key didn’t exist.

Due to a python-memcached limitation, the previous behavior is kept for the deprecated MemcachedCache backend.

The minimum supported version of SQLite is increased from 3.8.3 to 3.9.0.

CookieStorage now stores messages in the RFC 6265 compliant format. Support for cookies that use the old format remains until Django 4.1.

The minimum supported version of asgiref is increased from 3.2.10 to 3.3.2.


3.1
----

**Miscellaneous**
The cache keys used by cache and generated by make_template_fragment_key() are different from the keys generated by older versions of Django. After upgrading to Django 3.1, the first request to any previously cached template fragment will be a cache miss.
The logic behind the decision to return a redirection fallback or a 204 HTTP response from the set_language() view is now based on the Accept HTTP header instead of the X-Requested-With HTTP header presence.
The compatibility imports of django.core.exceptions.EmptyResultSet in django.db.models.query, django.db.models.sql, and django.db.models.sql.datastructures are removed.  :kind:`DELETION` [FIXED]
The compatibility import of django.core.exceptions.FieldDoesNotExist in django.db.models.fields is removed.  :kind:`DELETION` [FIXED]
The compatibility imports of django.forms.utils.pretty_name() and django.forms.boundfield.BoundField in django.forms.forms are removed.  :kind:`DELETION` [FIXED]
The compatibility imports of Context, ContextPopException, and RequestContext in django.template.base are removed.  :kind:`DELETION` [FIXED]
The compatibility import of django.contrib.admin.helpers.ACTION_CHECKBOX_NAME in django.contrib.admin is removed.  :kind:`DELETION` [FIXED]
The STATIC_URL and MEDIA_URL settings set to relative paths are now prefixed by the server-provided value of SCRIPT_NAME (or / if not set). This change should not affect settings set to valid URLs or absolute paths.
ConditionalGetMiddleware no longer adds the ETag header to responses with an empty content.
django.utils.decorators.classproperty() decorator is made public and moved to django.utils.functional.classproperty().  :kind:`DELETION` [FIXED]
floatformat template filter now outputs (positive) 0 for negative numbers which round to zero.
Meta.ordering and Meta.unique_together options on models in django.contrib modules that were formerly tuples are now lists.
The admin calendar widget now handles two-digit years according to the Open Group Specification, i.e. values between 69 and 99 are mapped to the previous century, and values between 0 and 68 are mapped to the current century.
Date-only formats are removed from the default list for DATETIME_INPUT_FORMATS.
The FileInput widget no longer renders with the required HTML attribute when initial data exists.
The undocumented django.views.debug.ExceptionReporterFilter class is removed. As per the Custom error reports documentation, classes to be used with DEFAULT_EXCEPTION_REPORTER_FILTER need to inherit from django.views.debug.SafeExceptionReporterFilter.  :kind:`DELETION` [FIXED]
The cache timeout set by cache_page() decorator now takes precedence over the max-age directive from the Cache-Control header.
Providing a non-local remote field in the ForeignKey.to_field argument now raises FieldError.
SECURE_REFERRER_POLICY now defaults to 'same-origin'. See the What’s New Security section above for more details.
check management command now runs the database system checks only for database aliases specified using check --database option.
migrate management command now runs the database system checks only for a database to migrate.
The admin CSS classes row1 and row2 are removed in favor of :nth-child(odd) and :nth-child(even) pseudo-classes.
The make_password() function now requires its argument to be a string or bytes. Other types should be explicitly cast to one of these.  :kind:`BEHAVIOUR` [WONTFIX]
The undocumented version parameter to the AsKML function is removed.
JSON and YAML serializers, used by dumpdata, now dump all data with Unicode by default. If you need the previous behavior, pass ensure_ascii=True to JSON serializer, or allow_unicode=False to YAML serializer.
The auto-reloader no longer monitors changes in built-in Django translation files.
The minimum supported version of mysqlclient is increased from 1.3.13 to 1.4.0.
The undocumented django.contrib.postgres.forms.InvalidJSONInput and django.contrib.postgres.forms.JSONString are moved to django.forms.fields.  :kind:`DELETION` [FIXED]
The undocumented django.contrib.postgres.fields.jsonb.JsonAdapter class is removed.
The {% localize off %} tag and unlocalize filter no longer respect DECIMAL_SEPARATOR setting.
The minimum supported version of asgiref is increased from 3.2 to 3.2.10.
The Media class now renders <script> tags without the type attribute to follow WHATWG recommendations.
ModelChoiceIterator, used by ModelChoiceField and ModelMultipleChoiceField, now yields 2-tuple choices containing ModelChoiceIteratorValue instances as the first value element in each choice. In most cases this proxies transparently, but if you need the field value itself, use the ModelChoiceIteratorValue.value attribute instead.


3.0
----

- Model.save() when providing a default for the primary key
- New default value for the FILE_UPLOAD_PERMISSIONS setting
- New default values for security settings

Removed private Python 2 compatibility APIs:  :kind:`DELETION` [ALL FIXED]

- django.test.utils.str_prefix() - Strings don’t have ‘u’ prefixes in Python 3.
- django.test.utils.patch_logger() - Use unittest.TestCase.assertLogs() instead.
- django.utils.lru_cache.lru_cache() - Alias of functools.lru_cache().
- django.utils.decorators.available_attrs() - This function returns functools.WRAPPER_ASSIGNMENTS.
- django.utils.decorators.ContextDecorator - Alias of contextlib.ContextDecorator.
- django.utils._os.abspathu() - Alias of os.path.abspath().
- django.utils._os.upath() and npath() - These functions do nothing on Python 3.
- django.utils.six - Remove usage of this vendored library or switch to six.
- django.utils.encoding.python_2_unicode_compatible() - Alias of six.python_2_unicode_compatible().
- django.utils.functional.curry() - Use functools.partial() or functools.partialmethod. See 5b1c389603a353625ae1603.
- django.utils.safestring.SafeBytes - Unused since Django 2.0.

Miscellaneous:

- ContentType.__str__() now includes the model’s app_label to disambiguate models with the same name in different apps.
- Because accessing the language in the session rather than in the cookie is deprecated, LocaleMiddleware no longer looks for the user’s language in the session and django.contrib.auth.logout() no longer preserves the session’s language after logout.
- django.utils.html.escape() now uses html.escape() to escape HTML. This converts ' to &#x27; instead of the previous equivalent decimal code &#39;.
- The django-admin test -k option now works as the unittest -k option rather than as a shortcut for --keepdb.
- Support for pywatchman < 1.2.0 is removed.
- urlencode() now encodes iterable values as they are when doseq=False, rather than iterating them, bringing it into line with the standard library urllib.parse.urlencode() function.
- intword template filter now translates 1.0 as a singular phrase and all other numeric values as plural. This may be incorrect for some languages.
- Assigning a value to a model’s ForeignKey or OneToOneField '_id' attribute now unsets the corresponding field. Accessing the field afterwards will result in a query.
- patch_vary_headers() now handles an asterisk '*' according to RFC 7231#section-7.1.4, i.e. if a list of header field names contains an asterisk, then the Vary header will consist of a single asterisk '*'.
- On MySQL 8.0.16+, PositiveIntegerField and PositiveSmallIntegerField now include a check constraint to prevent negative values in the database.
- alias=None is added to the signature of Expression.get_group_by_cols().
- RegexPattern, used by re_path(), no longer returns keyword arguments with None values to be passed to the view for the optional named groups that are missing.

Features removed in 3.0:

- The django.db.backends.postgresql_psycopg2 module is removed.
- django.shortcuts.render_to_response() is removed.  :kind:`DELETION` [FIXED]
- The DEFAULT_CONTENT_TYPE setting is removed.  [WONTFIX?]
- HttpRequest.xreadlines() is removed.  :kind:`DELETION` [FIXED]
- Support for the context argument of Field.from_db_value() and Expression.convert_value() is removed.
- The field_name keyword argument of QuerySet.earliest() and latest() is removed.
- The ForceRHR GIS function is removed.
- django.utils.http.cookie_date() is removed.   :kind:`DELETION` [FIXED]
- The staticfiles and admin_static template tag libraries are removed.    :kind:`DELETION` [FIXED]
- django.contrib.staticfiles.templatetags.staticfiles.static() is removed.    :kind:`DELETION` [FIXED]


2.2
----

- Admin actions are no longer collected from base ModelAdmin classes
- TransactionTestCase serialized data loading
- sqlparse is required dependency
- cached_property aliases
- Permissions for proxy models
- Merging of form Media assets

- To improve readability, the UUIDField form field now displays values with dashes, e.g. 550e8400-e29b-41d4-a716-446655440000 instead of 550e8400e29b41d4a716446655440000.
- On SQLite, PositiveIntegerField and PositiveSmallIntegerField now include a check constraint to prevent negative values in the database. If you have existing invalid data and run a migration that recreates a table, you’ll see CHECK constraint failed.
- For consistency with WSGI servers, the test client now sets the Content-Length header to a string rather than an integer.
- The return value of django.utils.text.slugify() is no longer marked as HTML safe.
- The default truncation character used by the urlizetrunc, truncatechars, truncatechars_html, truncatewords, and truncatewords_html template filters is now the real ellipsis character (…) instead of 3 dots. You may have to adapt some test output comparisons.
- Support for bytestring paths in the template filesystem loader is removed.
- django.utils.http.urlsafe_base64_encode() now returns a string instead of a bytestring, and django.utils.http.urlsafe_base64_decode() may no longer be passed a bytestring.
- Support for cx_Oracle < 6.0 is removed.
- The minimum supported version of mysqlclient is increased from 1.3.7 to 1.3.13.
- The minimum supported version of SQLite is increased from 3.7.15 to 3.8.3.
- In an attempt to provide more semantic query data, NullBooleanSelect now renders <option> values of unknown, true, and false instead of 1, 2, and 3. For backwards compatibility, the old values are still accepted as data.
- Group.name max_length is increased from 80 to 150 characters.
- Tests that violate deferrable database constraints now error when run on SQLite 3.20+, just like on other backends that support such constraints.
- To catch usage mistakes, the test Client and django.utils.http.urlencode() now raise TypeError if None is passed as a value to encode because None can’t be encoded in GET and POST data. Either pass an empty string or omit the value.
- The ping_google management command now defaults to https instead of http for the sitemap’s URL. If your site uses http, use the new ping_google --sitemap-uses-http option. If you use the ping_google() function, set the new sitemap_uses_https argument to False.
- runserver no longer supports pyinotify (replaced by Watchman).
- The Avg, StdDev, and Variance aggregate functions now return a Decimal instead of a float when the input is Decimal.
- Tests will fail on SQLite if apps without migrations have relations to apps with migrations. This has been a documented restriction since migrations were added in Django 1.7, but it fails more reliably now. You’ll see tests failing with errors like no such table: <app_label>_<model>. This was observed with several third-party apps that had models in tests without migrations. You must add migrations for such models.
- Providing an integer in the key argument of the cache.delete() or cache.get() now raises ValueError.


2.1
-----

- contrib.auth.views.login(), logout(), password_change(), password_change_done(), password_reset(), password_reset_done(), password_reset_confirm(), and password_reset_complete() will be removed. :kind:`DELETION`
- The extra_context parameter of contrib.auth.views.logout_then_login() will be removed. :kind:`DELETION`
- django.test.runner.setup_databases() will be removed. :kind:`DELETION`
- django.utils.translation.string_concat() will be removed. :kind:`DELETION` [FIXED]
- django.core.cache.backends.memcached.PyLibMCCache will no longer support passing pylibmc behavior settings as top-level attributes of OPTIONS.
- The host parameter of django.utils.http.is_safe_url() will be removed. :kind:`DELETION`
- Silencing of exceptions raised while rendering the {% include %} template tag will be removed. :kind:`DELETION`
- DatabaseIntrospection.get_indexes() will be removed. :kind:`DELETION`
- The authenticate() method of authentication backends will require a request argument.

MISSING ENTRY IN OFFICIAL DOCS:

- The "renderer" parameter of Widget.render() must now be supported by subclasses.  :kind:`BEHAVIOUR` [FIXED]


2.0
-----

- The weak argument to django.dispatch.signals.Signal.disconnect() will be removed.
- The django.forms.extras package will be removed.
- The assignment_tag helper will be removed.  :kind:`DELETION` [FIXED]
- The host argument to assertsRedirects will be removed. The compatibility layer which allows absolute URLs to be considered equal to relative ones when the path is identical will also be removed.
- Field.rel will be removed.
- Field.remote_field.to attribute will be removed.
- The on_delete argument for ForeignKey and OneToOneField will be required.  :kind:`BEHAVIOUR` [FIXED]
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
- Support for passing a 3-tuple as the first argument to include() will be removed.  :kind:`BEHAVIOUR` [FIXED]
- Support for setting a URL instance namespace without an application namespace will be removed.
- Field._get_val_from_obj() will be removed in favor of Field.value_from_object().
- django.template.loaders.eggs.Loader will be removed.
- The current_app parameter to the contrib.auth views will be removed.
- The callable_obj keyword argument to SimpleTestCase.assertRaisesMessage() will be removed.
- Support for the allow_tags attribute on ModelAdmin methods will be removed.
- The enclosure keyword argument to SyndicationFeed.add_item() will be removed.
- The django.template.loader.LoaderOrigin and django.template.base.StringOrigin aliases for django.template.base.Origin will be removed.
- The makemigrations --exit option will be removed.
- Support for direct assignment to a reverse foreign key or many-to-many relation will be removed.  :kind:`BEHAVIOUR` [FIXED]
- The get_srid() and set_srid() methods of django.contrib.gis.geos.GEOSGeometry will be removed.
- The get_x(), set_x(), get_y(), set_y(), get_z(), and set_z() methods of django.contrib.gis.geos.Point will be removed.
- The get_coords() and set_coords() methods of django.contrib.gis.geos.Point will be removed.
- The cascaded_union property of django.contrib.gis.geos.MultiPolygon will be removed.
- django.utils.functional.allow_lazy() will be removed.  :kind:`DELETION` [FIXED]
- The shell --plain option will be removed.
- The django.core.urlresolvers module will be removed.  :kind:`DELETION` [FIXED]
- The model CommaSeparatedIntegerField will be removed. A stub field will remain for compatibility with historical migrations.
- Support for the template Context.has_key() method will be removed.  :kind:`DELETION` [FIXED]
- Support for the django.core.files.storage.Storage.accessed_time(), created_time(), and modified_time() methods will be removed.
- Support for query lookups using the model name when Meta.default_related_name is set will be removed.
- The __search query lookup and the DatabaseOperations.fulltext_search_sql() method will be removed.
- The shim for supporting custom related manager classes without a _apply_rel_filters() method will be removed.
- Using User.is_authenticated() and User.is_anonymous() as methods will no longer be supported.  :kind:`BEHAVIOUR` [FIXED]
- The private attribute virtual_fields of Model._meta will be removed.
- The private keyword arguments virtual_only in Field.contribute_to_class() and virtual in Model._meta.add_field() will be removed.
- The javascript_catalog() and json_catalog() views will be removed.  :kind:`DELETION` [FIXED]
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

- The signature of private API Widget.build_attrs() changed from extra_attrs=None, **kwargs to base_attrs, extra_attrs=None. :kind:`BEHAVIOUR` [FIXED]


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
- Support for optparse will be dropped for custom management commands (replaced by argparse).  :kind:`BEHAVIOUR` [FIXED]
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
- django.core.cache.get_cache will be removed. Add suitable entries to CACHES and use django.core.cache.caches instead.  :kind:`DELETION` [FIXED]
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
    
