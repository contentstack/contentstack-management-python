---
name: framework
description: HTTP layer — requests-based _APIClient, retries, OAuth interceptor for the Management SDK.
---

# Framework skill — `requests` + `_APIClient`

## Integration point

- **`contentstack_management/_api_client.py`** — **`_APIClient`** uses **`requests`** in **`_call_request`**, honors **timeout** and **max_retries**, and delegates to **`oauth_interceptor`** when configured.

## When to change

- **Retry or transport behavior** — keep logic centralized in **`_APIClient`** unless a resource truly needs a documented exception.
- **Auth headers** — prefer extending **`Client`** / **`user_agents`** patterns rather than scattering header merges.

## Testing

- **Unit** — mock **`requests`** or **`_APIClient`** at the boundary used by existing tests.
- **API** — full stack via credentials from **`tests/cred.py`**.

## Rule shortcut

- `.cursor/rules/contentstack-management-python.mdc`
