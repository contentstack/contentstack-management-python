---
name: code-review
description: PR review for contentstack-management — public API, Client, _APIClient, OAuth, tests.
---

# Code review — `contentstack-management`

## Checklist

- [ ] **API:** New or changed **`Client`** / **Stack** / resource methods documented; **`contentstack_management/__init__.py`** exports updated if public surface changes.
- [ ] **Version:** **`__version__`** in **`contentstack_management/__init__.py`** aligned with release strategy when user-visible behavior changes.
- [ ] **HTTP:** **`_APIClient`** or OAuth changes covered by unit tests; retries and headers remain consistent.
- [ ] **Tests:** **`pytest tests/unit/`** passes; extend **`tests/api`** or **`tests/mock`** when integration or contract behavior changes.
- [ ] **Secrets:** No tokens in repo; use **`tests/cred.py`** / env for local API runs.

## References

- `.cursor/rules/code-review.mdc`
- `.cursor/rules/dev-workflow.md`
