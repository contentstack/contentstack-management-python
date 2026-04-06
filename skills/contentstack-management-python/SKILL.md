---
name: contentstack-management-python
description: contentstack-management — Python CMA client, Client, Stack, _APIClient, OAuth.
---

# Contentstack Management Python SDK skill

## Entry

- **`contentstack_management.Client`** — **`contentstack_management/contentstack.py`**: builds CMA **endpoint** from **region** / **host**, sets **headers** (**authtoken**, **management_token**), creates **`_APIClient`**, optional **OAuth**.

## Structure

- **`Stack`** — **`contentstack_management/stack/stack.py`**: stack-scoped resources (content types, entries, assets, …).
- **Resources** — packages under **`contentstack_management/`** (e.g. **`entries/`**, **`assets/`**, **`webhooks/`**).
- **OAuth** — **`oauth/oauth_handler.py`**, **`oauth/oauth_interceptor.py`**.

## Extending

- Add methods on the appropriate resource class; align path and payload shapes with **CMA** docs.
- Prefer routing HTTP through **`_APIClient`** for consistent retries and OAuth handling.

## Docs

- [Content Management API](https://www.contentstack.com/docs/developers/apis/content-management-api/)

## Rule shortcut

- `.cursor/rules/contentstack-management-python.mdc`
