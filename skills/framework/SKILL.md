---
name: framework
description: requests-based _APIClient, retries, timeout, OAuth interceptor—central HTTP for the Management SDK.
---

# Framework / HTTP — Contentstack Management Python

## When to use

- Editing **`contentstack_management/_api_client.py`** or OAuth interceptor/handler wiring.
- Changing retry policy, timeouts, or how **`requests`** is invoked.

## Integration point

- **`_APIClient`** uses **`requests`** in **`_call_request`**, honors **timeout** and **max_retries**, and delegates to **`oauth_interceptor`** when configured.

## When to change

- **Retry or transport behavior** — keep logic centralized in **`_APIClient`** unless a resource truly needs a documented exception.
- **Auth headers** — prefer extending **`Client`** / **`user_agents`** patterns rather than scattering header merges.

## Testing

- **Unit** — mock **`requests`** or **`_APIClient`** at the boundary used by existing tests.
- **API** — full stack via credentials from **`tests/cred.py`**.

## References

- **`skills/contentstack-management/SKILL.md`**
- **`skills/dev-workflow/SKILL.md`**
- **`skills/testing/SKILL.md`**
