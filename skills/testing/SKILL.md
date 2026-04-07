---
name: testing
description: pytest—unit, API, mock; tests/cred.py and .env; no committed secrets.
---

# Testing — Contentstack Management Python

## When to use

- Adding or changing tests under **`tests/`**.
- Debugging API vs mock failures; improving **`tests/cred.py`** usage.

## Runner and tooling

| Suite | Path | Notes |
|-------|------|--------|
| **Unit** | `tests/unit/**` | Fast, isolated; primary CI target |
| **API** | `tests/api/**` | Live CMA — **`.env`** via **`tests/cred.py`** |
| **Mock** | `tests/mock/**` | Mocked HTTP / contracts |

### Commands

| Goal | Command |
|------|---------|
| Unit (CI-style) | `pytest tests/unit/ -v` or `coverage run -m pytest tests/unit/` |
| API (live CMA) | `pytest tests/api/ -v` |
| Mock | `pytest tests/mock/ -v` |
| Full tree | `pytest tests/ -v` |

## Environment (`tests/cred.py`)

- **`get_credentials()`** loads **dotenv** and returns host, tokens, and resource UIDs.
- Common vars: **`HOST`**, **`APIKEY`**, **`AUTHTOKEN`**, **`MANAGEMENT_TOKEN`**, **`ORG_UID`**, plus resource UIDs as tests require.
- Use a **`.env`** at repo root for local API runs; never commit secrets.

## Hygiene

- No committed secrets; use placeholders or env-only values for CI.
- Avoid leaving **`pytest.skip`** or focused-only tests enabled in paths meant for full suite runs unless intentional.

## References

- **`skills/dev-workflow/SKILL.md`**
- **`skills/code-review/SKILL.md`**
