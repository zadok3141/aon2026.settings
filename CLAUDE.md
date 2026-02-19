# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Authoritative Documentation

- `CLAUDE.md` (this file)
- `CHANGELOG.md` (managed by towncrier; do not edit directly)
- `README.md`

## What This Is

A Plone 6.x addon package (`aon2026.settings`) that provides site settings for the OAG (Office of the Auditor-General) New Zealand intranet at `audit.oag.net`. Generated with Cookieplone. Uses the `plone.autoinclude` entry point for automatic ZCML loading.

Deployed within the `aon2026` parent project (buildout-based). Companion packages in that deployment:
- `diazotheme.aon2026` — Diazo theme
- `aon.portlets.reports` — Custom reports portlet

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (package manager)
- Make

## Common Commands

```bash
make install          # Create venv, install deps, generate Zope instance config
make start            # Run Plone on localhost:8080 (admin/admin)
make create-site      # Create a fresh Plone site (DELETE_EXISTING=1 to replace)
make test             # Run pytest
make test-coverage    # Run pytest with coverage report
make format           # Auto-format Python (ruff) and XML/ZCML (zpretty)
make lint             # Lint with ruff, pyroma, check-python-versions, zpretty --check
make check            # format + lint
make i18n             # Regenerate locale files
make clean            # Remove venv, instance config, caches
```

Run a single test file or test:
```bash
.venv/bin/pytest tests/setup/test_setup_install.py
.venv/bin/pytest tests/setup/test_setup_install.py::TestSetupInstall::test_addon_installed
```

## Architecture

### Source layout

All package code lives under `src/aon2026/settings/` (namespace package with `src` layout, built by hatchling).

### Key subsystems (each a sub-package with its own `configure.zcml`)

- `browser/` — Views, templates, static resources, template overrides (via z3c.jbot in `overrides/`)
- `content/` — Content types
- `controlpanels/` — Site control panel schemas and views
- `indexers/` — Catalog index adapters
- `vocabularies/` — Named vocabularies
- `setuphandlers/` — Import/export step handlers
- `upgrades/` — Upgrade steps between profile versions
- `profiles/default/` — GenericSetup XML profile (current version: `1000` in `metadata.xml`)
- `profiles/uninstall/` — Cleanup profile for addon removal
- `locales/` — i18n translations (i18n domain: `aon2026.settings`)

### Configuration

- ZCML files wire everything together; `configure.zcml` is the root
- `dependencies.zcml` declares dependent packages
- `permissions.zcml` defines custom permissions
- `profiles.zcml` registers GenericSetup profiles

### Testing

Uses `pytest` with `pytest-plone`. Three test layers defined in `testing.py`:

- **INTEGRATION_TESTING** — In-memory Plone with the addon profile applied
- **FUNCTIONAL_TESTING** — Same + WSGI server
- **ACCEPTANCE_TESTING** — Same + Robot Framework remote libraries

Fixtures (`integration`, `functional`, `acceptance`) are auto-generated in `tests/conftest.py` via `fixtures_factory`. Tests use these as pytest fixtures.

### Dependency management

- `pyproject.toml` declares runtime and optional (`[test]`, `[release]`) dependencies
- `mx.ini` (mxdev) pins to Plone version constraints and installs the package in editable mode with `[test]` extras
- `instance.yaml` configures the Zope instance via `cookiecutter-zope-instance`

## Style

- Python: ruff (line-length 88, target py310). Imports: single-line, `from`-first, case-insensitive, no sections.
- XML/ZCML: zpretty
- Indentation: 4 spaces for Python; 2 spaces for HTML/XML/ZCML/JSON/YAML/JS/CSS
- Changelog entries go in `news/` as towncrier fragments (not directly in CHANGELOG.md)

## Developing Within the Parent Buildout

When this package is checked out into `aon2026/src/` via mr.developer, buildout requires egg-info metadata. Since this package uses `pyproject.toml` + hatchling (not `setup.py`), generate it manually:

```bash
cd src/aon2026.settings && python -m hatchling build --hooks-only
```

## Adding Features

Use `make add <template_name>` (wraps `plonecli`) to scaffold content types, behaviors, control panels, upgrade steps, etc. via bobtemplates.plone.
