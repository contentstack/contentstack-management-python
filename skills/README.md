# Skills – Contentstack Management Python

Source of truth for detailed guidance. Read **[`AGENTS.md`](../AGENTS.md)** first, then open the skill that matches your task.

## When to use which skill

| Skill folder | Use when |
|--------------|----------|
| **dev-workflow** | Install, **`pytest`** (unit / API / mock), **`__version__`**, pylint, Talisman/Snyk, before PR |
| **contentstack-management** | **`Client`**, **`Stack`**, **`_APIClient`**, domain modules, OAuth, CMA paths and payloads |
| **python-style** | Editing **`contentstack_management/`** or **`setup.py`** / **`requirements.txt`**—layout, style, imports |
| **testing** | Adding or changing tests under **`tests/`**, **`tests/cred.py`**, env for API runs |
| **code-review** | PR checklist, API semver, HTTP regressions, secrets |
| **framework** | Changing **`_APIClient`**, retries, **`requests`** usage, OAuth interceptor wiring |

Each folder contains `SKILL.md` with YAML frontmatter (`name`, `description`).
