# Contentstack Management Python — Agent guide

**Universal entry point** for anyone automating or assisting work in this repo—AI agents (Cursor, Copilot, CLI tools), reviewers, and contributors. Conventions and detailed guidance live in **`skills/*/SKILL.md`**, not in editor-specific config, so the same instructions apply whether or not you use Cursor.

## What this repo is

| | |
|---|---|
| **Name** | **`contentstack-management`** (PyPI) — **Contentstack Management Python SDK** |
| **Purpose** | Python client for the **Content Management API (CMA)**: organizations, stacks, content types, entries, assets, webhooks, workflows, OAuth, and related resources. Uses **`requests`** via **`_APIClient`**. |
| **Repository** | [contentstack/contentstack-management-python](https://github.com/contentstack/contentstack-management-python.git) |

## Tech stack

| Area | Details |
|------|---------|
| **Language** | **Python** ≥ 3.9 (`setup.py` `python_requires`) |
| **HTTP** | **`requests`**, **`requests-toolbelt`**, **`urllib3`** |
| **Tests** | **pytest** — **`tests/unit`**, **`tests/api`**, **`tests/mock`** |
| **Lint** | **pylint** (see `requirements.txt`) |
| **Secrets / hooks** | **Talisman**, **Snyk** (see **README.md** development setup) |

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

```bash
pip install -e ".[dev]"
# or: pip install -r requirements.txt && pip install pytest pytest-cov

pytest tests/unit/ -v
pytest tests/api/ -v      # live CMA — needs .env (see tests/cred.py)
pytest tests/mock/ -v
pytest tests/ -v
coverage run -m pytest tests/unit/
```

## Environment variables (API / integration tests)

Loaded via **`tests/cred.py`** (`load_dotenv()`). Examples include **`HOST`**, **`APIKEY`**, **`AUTHTOKEN`**, **`MANAGEMENT_TOKEN`**, **`ORG_UID`**, and resource UIDs (**`CONTENT_TYPE_UID`**, **`ENTRY_UID`**, …). See that file for the full list.

Do not commit secrets.

## Where the real documentation lives: skills

Read these **`SKILL.md` files** for full conventions—**this is the source of truth** for implementation and review:

| Skill | Path | What it covers |
|-------|------|----------------|
| **Development workflow** | [`skills/dev-workflow/SKILL.md`](skills/dev-workflow/SKILL.md) | Install, pytest suites, packaging version, pylint, hooks, PR baseline |
| **Contentstack Management (SDK)** | [`skills/contentstack-management/SKILL.md`](skills/contentstack-management/SKILL.md) | **`Client`**, **`Stack`**, **`_APIClient`**, CMA resources, OAuth, CMA docs |
| **Python style & repo layout** | [`skills/python-style/SKILL.md`](skills/python-style/SKILL.md) | Package layout, naming, imports via **`_APIClient`**, secrets in logs |
| **Testing** | [`skills/testing/SKILL.md`](skills/testing/SKILL.md) | pytest unit / API / mock, **`tests/cred.py`**, env hygiene |
| **Code review** | [`skills/code-review/SKILL.md`](skills/code-review/SKILL.md) | PR checklist—public API, HTTP/auth, tests, security |
| **Framework / HTTP** | [`skills/framework/SKILL.md`](skills/framework/SKILL.md) | **`requests`**, retries, OAuth interceptor, where to change transport |

An index with short “when to use” hints is in [`skills/README.md`](skills/README.md).

## Using Cursor

If you use **Cursor**, [`.cursor/rules/README.md`](.cursor/rules/README.md) only points to **`AGENTS.md`**—same source of truth as everyone else; no separate `.mdc` rule files.

Product docs: [Content Management API](https://www.contentstack.com/docs/developers/apis/content-management-api/).
