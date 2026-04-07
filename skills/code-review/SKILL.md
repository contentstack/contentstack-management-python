---
name: code-review
description: PR checklist—public API, Client/Stack, _APIClient/OAuth, tests, secrets; align with README and exports.
---

# Code review — Contentstack Management Python

## When to use

- Reviewing a PR, self-review before submit, or automated review prompts.

## Instructions

Work through the checklist below. Optionally tag findings: **Blocker**, **Major**, **Minor**.

### Public API

- [ ] **Exported** **`Client`**, **`Region`**, stack and resource helpers match **README** and **`contentstack_management.__all__`** / **`__init__.py`**.
- [ ] **Docstrings** on **`Client`** and changed public methods when behavior or parameters change.

### Compatibility

- [ ] Avoid breaking **`Client`** constructor or stack method chains without a semver strategy; document migration for breaking changes.

### HTTP / auth

- [ ] Changes to **`_APIClient`** or **OAuth** paths: verify retries, headers, and interceptor behavior with unit tests; no regressions for **authtoken** / **management_token** headers.

### Testing

- [ ] **Unit** coverage for new logic; **API** updates when live CMA request/response behavior changes; **mock** when contract-style tests are appropriate.
- [ ] **`pytest tests/unit/`** passes.

### Security

- [ ] No hardcoded tokens; no logging secrets in new code.

### Severity (optional)

| Level | Examples |
|-------|----------|
| **Blocker** | Breaking public API without approval; security issue; no tests for new logic where tests are practical |
| **Major** | Inconsistent HTTP/auth behavior; README examples that do not match code |
| **Minor** | Style; minor docs |

## References

- **`skills/testing/SKILL.md`**
- **`skills/contentstack-management/SKILL.md`**
- **`skills/dev-workflow/SKILL.md`**
