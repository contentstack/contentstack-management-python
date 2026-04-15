---
name: dev-workflow
description: Install, pytest unit/API/mock, versioning, pylint, hooks—standard workflow for this SDK repo.
---

# Development workflow — Contentstack Management Python

## When to use

- Setting up locally, opening a PR, or matching CI expectations.
- Answering “how do we run tests?” or “what runs in CI?”

## Before a PR

1. **Install** — `pip install -e ".[dev]"` or install **`requirements.txt`** plus **pytest** / **pytest-cov** as needed.
2. **`pytest tests/unit/`** — required baseline (matches CI **`coverage run -m pytest tests/unit/`**).
3. **API tests** — `pytest tests/api/` when your change affects live CMA behavior; configure **`.env`** per **`tests/cred.py`**. Never commit tokens.
4. **Mock tests** — `pytest tests/mock/` when extending mocked HTTP or fixtures.

## Packaging

- Bump **`contentstack_management/__init__.py`** **`__version__`** and align **`setup.py`** versioning if release-facing.

## Tooling

- **pylint** is listed in **`requirements.txt`**; follow existing style in touched files.
- **Husky / Talisman / Snyk** — see **README.md** for local hook setup.

## Pull requests

- Build passes: **`pytest tests/unit/`** at minimum; run **API** / **mock** when your change touches those layers.
- Follow **`skills/code-review/SKILL.md`** before merge.
- Prefer backward-compatible public API; call out breaking changes and semver.

## References

- **`AGENTS.md`**
- **`skills/contentstack-management/SKILL.md`**
- **`skills/testing/SKILL.md`**
