# Skills — Contentstack Management Python

**This directory is the source of truth** for conventions (workflow, SDK API, style, tests, review, HTTP layer). Read **`AGENTS.md`** at the repo root for the index and quick commands; each skill is a folder with **`SKILL.md`** (YAML frontmatter: `name`, `description`).

## When to use which skill

| Skill folder | Use when |
|--------------|----------|
| **dev-workflow** | Install, **`pytest`** (unit / API / mock), **`__version__`**, pylint, Talisman/Snyk, before PR |
| **contentstack-management** | **`Client`**, **`Stack`**, **`_APIClient`**, domain modules, OAuth, CMA paths and payloads |
| **python-style** | Editing **`contentstack_management/`** or **`setup.py`** / **`requirements.txt`**—layout, style, imports |
| **testing** | Adding or changing tests under **`tests/`**, **`tests/cred.py`**, env for API runs |
| **code-review** | PR checklist, API semver, HTTP regressions, secrets |
| **framework** | Changing **`_APIClient`**, retries, **`requests`** usage, OAuth interceptor wiring |

## How to use these docs

- **Humans / any AI tool:** Start at **`AGENTS.md`**, then open the relevant **`skills/<name>/SKILL.md`**.
- **Cursor users:** **`.cursor/rules/README.md`** only points to **`AGENTS.md`** so guidance stays universal—no duplicate `.mdc` rule sets.
