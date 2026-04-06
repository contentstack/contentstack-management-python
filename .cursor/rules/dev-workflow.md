---
description: "Branches, install, and test layout for contentstack-management-python"
globs:
  - "**/*.py"
  - "setup.py"
  - "requirements.txt"
  - ".github/**/*.yml"
alwaysApply: false
---

# Development workflow — `contentstack-management`

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

## Links

- [`AGENTS.md`](../../AGENTS.md) · [`skills/contentstack-management-python/SKILL.md`](../../skills/contentstack-management-python/SKILL.md)
