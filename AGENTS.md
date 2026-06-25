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
| Tests | `pytest` — `tests/integration` (live e2e / sanity, dynamic stack), `tests/unit`, `tests/mock`, `tests/api` (legacy, superseded by `tests/integration`) |
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
| `tests/integration/` | **Live e2e / sanity suite** (pytest). Self-contained: creates a fresh stack per run, exercises every SDK method (positive/negative/edge), tears it down. Own `framework/` + `data/`; config in `tests/integration/.env`. |
| `tests/cred.py` | **`get_credentials()`** — **dotenv** + env vars for the legacy `tests/api` / `tests/mock` suites |

## Commands (quick reference)

| Command Type | Command |
|---|---|
| Install | `pip install -e ".[dev]"` |
| **Sanity / e2e (live)** | `pytest tests/integration` — dynamically creates a stack, runs the full suite, tears it down. Needs `tests/integration/.env` (`EMAIL`, `PASSWORD`, `HOST`, `ORGANIZATION`). Writes a timestamped HTML report + cURL log to the repo root. |
| Sanity, keep stack | `DELETE_DYNAMIC_RESOURCES=false pytest tests/integration` (preserve the created stack for debugging) |
| Sanity, one resource | `pytest tests/integration/api/test_12_content_type.py` |
| Test (unit) | `pytest tests/unit/ -v` |
| Test (mock) | `pytest tests/mock/ -v` |
| Test (legacy API, live) | `pytest tests/api/ -v` (needs `.env` — see `tests/cred.py`) |
| Coverage (CI) | `coverage run -m pytest tests/unit/` |
| Lint | `pylint contentstack_management/` |

> **CI note:** `.github/workflows/unit-test.yml` runs **only `tests/unit/`** (no credentials). The `tests/integration` sanity suite is run manually (or via a credential-gated job) because it provisions real stacks.

## Environment variables

**Sanity / e2e suite** (`tests/integration`) — configured via **`tests/integration/.env`** (gitignored). No pre-existing stack/UIDs needed; the suite creates everything at runtime.

| Var | Required | Purpose |
|-----|----------|---------|
| `EMAIL`, `PASSWORD` | ✅ | Login for the run (a **non-2FA** account) |
| `HOST` | ✅ | API host (e.g. `api.contentstack.io`) |
| `ORGANIZATION` | ✅ | Org the dynamic test stack is created in |
| `MFA_SECRET` | — | TOTP secret (for the OAuth/2FA account, not the primary login) |
| `DELETE_DYNAMIC_RESOURCES` | — | `false` keeps the created stack for debugging (default deletes) |
| `CLIENT_ID`, `APP_ID`, `REDIRECT_URI` | — | OAuth tests |
| `PERSONALIZE_HOST` | — | Personalize project for variant tests |

**Legacy `tests/api` / `tests/mock`** — loaded via **`tests/cred.py`** (`load_dotenv()`): `HOST`, `APIKEY`, `AUTHTOKEN`, `MANAGEMENT_TOKEN`, `ORG_UID`, and resource UIDs. See that file for the full list.

Do not commit secrets. `tests/integration/.env`, `docs/`, and the repo-root `cma-python-report-*.html` / `api-requests-*.txt` are gitignored.

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
