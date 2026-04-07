---
name: python-style
description: Package layout under contentstack_management/, setup.py, pylint-friendly style, imports, no secret logging.
---

# Python style and repo layout — Contentstack Management Python

## When to use

- Editing any Python under **`contentstack_management/`**, **`setup.py`**, or **`requirements.txt`**.
- Adding modules or changing how the public package surface is exported.

## Layout

- **`contentstack_management/contentstack.py`** — **`Client`**, **`Region`**, **`user_agents`**, OAuth wiring.
- **`contentstack_management/_api_client.py`** — **`_APIClient`** (HTTP, retries).
- **`contentstack_management/stack/`** — stack-scoped API surface.
- **Domain modules** — **`entries/`**, **`assets/`**, **`webhooks/`**, **`oauth/`**, etc.

## Style

- Match existing modules: naming, docstrings, and patterns already used in the same directory.
- Prefer small, focused changes; keep **`__init__.py`** exports consistent with public API intent (**`README`**, **`contentstack_management.__all__`**).

## Imports

- Use **`requests`** (and **`requests-toolbelt`** where already used) through **`_APIClient`** patterns rather than ad-hoc clients in domain modules unless justified.

## Security

- Do not log **authtokens**, **management tokens**, **passwords**, or **API keys**; preserve existing header handling in **`Client`**.

## References

- **`skills/framework/SKILL.md`**
- **`skills/contentstack-management/SKILL.md`**
- **`skills/testing/SKILL.md`**
