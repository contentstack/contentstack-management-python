# AGENTS.md — AI / automation context

## Project

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

## Common commands

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

## Further guidance

- **Cursor rules:** [`.cursor/rules/README.md`](.cursor/rules/README.md)
- **Skills:** [`skills/README.md`](skills/README.md)

Product docs: [Content Management API](https://www.contentstack.com/docs/developers/apis/content-management-api/).
