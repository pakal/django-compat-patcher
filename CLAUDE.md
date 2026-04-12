# Django Compat Patcher — Claude Configuration

## Project Overview

`django-compat-patcher` (DCP) is a runtime monkey-patcher that applies compatibility shims ("fixers") to Django, allowing projects to mix apps targeting different Django versions. It patches deprecated or removed Django APIs so they keep working without changing application code.

- **Source layout**: `src/django_compat_patcher/`
- **Tests**: `tests/`
- **Python**: 3.7–>3.13 | **Django**: 1.8–>5.2
- **Build**: setuptools via `pyproject.toml`
- **Core dependency**: `compat-patcher-core`

## Key Architecture

| Path | Purpose |
|---|---|
| `src/django_compat_patcher/__init__.py` | Entry point — `patch()` function |
| `src/django_compat_patcher/registry.py` | Fixer registration (`@register_django_compatibility_fixer`) |
| `src/django_compat_patcher/fixers/` | Version-specific fixers (`django1_8.py` … `django5_1.py`) |
| `src/django_compat_patcher/config.py` | Settings loading (`DCP_*` vars, env overrides) |
| `src/django_compat_patcher/django_legacy/` | Backported Django code for compatibility shims |
| `tests/conftest.py` | Meta-test: ensures every registered fixer has a test |
| `tests/_test_utilities.py` | Bootstraps DCP patches for the test environment |
| `tests/test_project/minimal_settings.py` | Minimal Django settings used by tests |

## Running Tests

```bash
# Run all tests for the current Django version:
pytest

# Via tox (full matrix — Python × Django combinations):
tox

# Single tox environment:
tox -e py312-django5_1
```

Pytest config lives in `pytest.ini` (project root).

### Behaviour-check scripts (run inside tox or manually)
```bash
cd tests
python check_behaviour_with_minimal_settings.py
python check_behaviour_with_environment_variables.py
```

## Adding or Modifying Fixers

1. Add the fixer function to the appropriate `src/django_compat_patcher/fixers/djangoX_Y.py`.
2. Decorate with `@register_django_compatibility_fixer(fixer_family=..., feature_supported_from=..., feature_removed_from=...)`.
   Deduplicate these decorators using partials like `django1_10_bc_fixer`.
3. Add a corresponding test in `tests/test_djangoX_Y.py` — `conftest.py` enforces 1-to-1 coverage.
4. Unsafe fixers (e.g., postgres utilities) must be added to `DCP_EXCLUDE_FIXER_IDS` defaults in `default_settings.py`.

## README Generation

The README is auto-generated from a template:
```bash
python generate_readme.py   # Reads README.in, injects fixer list, writes README.rst
```

Do **not** edit `README.rst` directly — edit `README.in` instead.

## Settings & Configuration

DCP settings are loaded from Django settings (`DCP_*` keys), with JSON-encoded environment variables taking precedence. Key settings:

- `DCP_INCLUDE_FIXER_IDS` / `DCP_EXCLUDE_FIXER_IDS` — fixer allow/deny lists
- `DCP_INCLUDE_FIXER_FAMILIES` / `DCP_EXCLUDE_FIXER_FAMILIES` — family allow/deny lists
- `DCP_LOGGING_LEVEL` — default `"INFO"`
- `DCP_ENABLE_WARNINGS` — default `True`

## CI

AppVeyor (`.appveyor.yml`) runs the tox matrix on Windows. No linter configuration is present; keep code style consistent with existing files.