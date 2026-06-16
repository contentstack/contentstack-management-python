---
name: framework
description: Use for _APIClient, requests usage, retries, timeout, and OAuth interceptor in contentstack-management-python.
---

# Framework / HTTP – Contentstack Management Python

## When to use

- Editing **`contentstack_management/_api_client.py`** or OAuth interceptor/handler wiring.
- Changing retry policy, timeouts, or how **`requests`** is invoked.

## Instructions

### Integration point

- **`_APIClient`** uses **`requests`** in **`_call_request`**, honors **timeout** and **max_retries**, and delegates to **`oauth_interceptor`** when configured.

### When to change

- **Retry or transport behavior** — keep logic centralized in **`_APIClient`** unless a resource truly needs a documented exception.
- **Auth headers** — prefer extending **`Client`** / **`user_agents`** patterns rather than scattering header merges.

### Testing

- **Unit** — mock **`requests`** or **`_APIClient`** at the boundary used by existing tests.
- **API** — full stack via credentials from **`tests/cred.py`**.
