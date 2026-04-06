---
name: testing
description: pytest unit, api, and mock suites for contentstack-management-python.
---

# Testing — `contentstack-management`

## Commands

| Goal | Command |
|------|---------|
| Unit (CI-style) | `pytest tests/unit/ -v` or `coverage run -m pytest tests/unit/` |
| API (live CMA) | `pytest tests/api/ -v` |
| Mock | `pytest tests/mock/ -v` |
| Full tree | `pytest tests/ -v` |

## Environment

See **`tests/cred.py`** — **`get_credentials()`** after **`load_dotenv()`**.

- Common vars: **`HOST`**, **`APIKEY`**, **`AUTHTOKEN`**, **`MANAGEMENT_TOKEN`**, **`ORG_UID`**, plus resource UIDs as tests require.
- Use a **`.env`** at repo root for local API runs; never commit secrets.

## References

- `.cursor/rules/testing.mdc`
