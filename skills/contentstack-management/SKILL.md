---
name: contentstack-management
description: Use for Client, Stack, _APIClient, domain resources, OAuth, and CMA API alignment.
---

# Contentstack Management SDK – Contentstack Management Python

## When to use

- Implementing or changing **`Client`**, **Stack**, or resource modules (entries, assets, webhooks, …).
- Updating **`README.md`** or public exports for user-visible behavior.
- Assessing semver impact of constructor, method, or export changes.

## Instructions

### Main entry (consumer API)

- **`contentstack_management.Client`** in **`contentstack.py`**: builds CMA **endpoint** from **region** / **host** / **scheme**, merges **headers** (**authtoken**, **management_token**, **early_access**), constructs **`_APIClient`**, optional **`oauth_config`** with **`OAuthHandler`**.

### Structure

- **`Stack`** — **`contentstack_management/stack/stack.py`**: stack-scoped resources (content types, entries, assets, branches, webhooks, …).
- **Org / user** — **`organizations/`**, **`users/`**, **`user_session/`** as applicable.
- **Resources** — packages under **`contentstack_management/`** following existing patterns.
- **OAuth** — **`oauth/oauth_handler.py`**, **`oauth/oauth_interceptor.py`**; keep aligned with **`_APIClient`** request path.

### HTTP layer

- **`_APIClient._call_request`** — central place for method, URL, JSON, files; respect **timeout** and **max_retries**.

### Extending

- Add methods on the appropriate resource class; align path and payload shapes with **CMA** docs.
- Prefer routing HTTP through **`_APIClient`** for consistent retries and OAuth handling.

### Docs and versioning

- Exported **`Client`**, **`Region`**, and stack helpers should match **README** and **`contentstack_management.__init__.py`**.
- Document migration for intentional breaking changes.
