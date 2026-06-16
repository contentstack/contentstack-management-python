# Contentstack Management Python – Agent guide

**Universal entry point** for contributors and AI agents. Detailed conventions live in **`skills/*/SKILL.md`**.

## What this repo is

| Field | Detail |
|--------|--------|
| **Name:** | **`contentstack-management`** (PyPI) — [contentstack/contentstack-management-python](https://github.com/contentstack/contentstack-management-python) |
| **Purpose:** | Python client for the **Content Management API (CMA)**: organizations, stacks, content types, entries, assets, webhooks, workflows, OAuth, and related resources. Uses **`requests`** via **`_APIClient`**. |

## Tech stack (at a glance)

| Area | Details |
|------|---------|
| Language | Python ≥ 3.9 (`setup.py` `python_requires`) |
| Build | `setuptools` / `setup.py`; package `contentstack_management` |
| HTTP | `requests`, `requests-toolbelt`, `urllib3` |
| Tests | `pytest` — `tests/unit`, `tests/api`, `tests/mock` |
| Lint / coverage | `pylint`, `coverage` (see `requirements.txt`) |
| Secrets / hooks | Talisman, Snyk (see `README.md` development setup) |

## Source layout

| Path | Role |
|------|------|
| `contentstack_management/contentstack.py` | **`Client`**, **`Region`**, endpoint construction, **`user_agents`**, optional **OAuth** wiring |
| `contentstack_management/_api_client.py` | **`_APIClient`** — HTTP calls, retries, optional **OAuth** interceptor |
| `contentstack_management/stack/stack.py` | **Stack**-scoped CMA operations |
| `contentstack_management/*/` | Domain modules (entries, assets, webhooks, taxonomies, …) |
| `contentstack_management/__init__.py` | Public exports |
| `tests/cred.py` | **`get_credentials()`** — **dotenv** + env vars for API/mock tests |

## Commands (quick reference)

| Command Type | Command |
|---|---|
| Install | `pip install -e ".[dev]"` |
| Test (unit) | `pytest tests/unit/ -v` |
| Test (API, live) | `pytest tests/api/ -v` (needs `.env` — see `tests/cred.py`) |
| Test (mock) | `pytest tests/mock/ -v` |
| Coverage | `coverage run -m pytest tests/unit/` |
| Lint | `pylint contentstack_management/` |

## Environment variables (API / integration tests)

Loaded via **`tests/cred.py`** (`load_dotenv()`). Examples include **`HOST`**, **`APIKEY`**, **`AUTHTOKEN`**, **`MANAGEMENT_TOKEN`**, **`ORG_UID`**, and resource UIDs (**`CONTENT_TYPE_UID`**, **`ENTRY_UID`**, …). See that file for the full list.

Do not commit secrets.

## Where the documentation lives: skills

| Skill | Path | What it covers |
|-------|------|----------------|
| **Development workflow** | [`skills/dev-workflow/SKILL.md`](skills/dev-workflow/SKILL.md) | Install, pytest suites, packaging version, pylint, hooks, PR baseline |
| **Contentstack Management (SDK)** | [`skills/contentstack-management/SKILL.md`](skills/contentstack-management/SKILL.md) | **`Client`**, **`Stack`**, **`_APIClient`**, CMA resources, OAuth, CMA docs |
| **Python style & repo layout** | [`skills/python-style/SKILL.md`](skills/python-style/SKILL.md) | Package layout, naming, imports via **`_APIClient`**, secrets in logs |
| **Testing** | [`skills/testing/SKILL.md`](skills/testing/SKILL.md) | pytest unit / API / mock, **`tests/cred.py`**, env hygiene |
| **Code review** | [`skills/code-review/SKILL.md`](skills/code-review/SKILL.md) | PR checklist—public API, HTTP/auth, tests, security |
| **Framework / HTTP** | [`skills/framework/SKILL.md`](skills/framework/SKILL.md) | **`requests`**, retries, OAuth interceptor, where to change transport |

An index with “when to use” hints is in [`skills/README.md`](skills/README.md).

## Using Cursor (optional)

If you use **Cursor**, [`.cursor/rules/README.md`](.cursor/rules/README.md) only points to **`AGENTS.md`**—same docs as everyone else.

Product docs: [Content Management API](https://www.contentstack.com/docs/developers/apis/content-management-api/).
