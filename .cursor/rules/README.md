# Cursor Rules — `contentstack-management`

Rules for **contentstack-management-python**: Python **CMA** SDK (`contentstack_management`).

## Rules overview

| Rule | Role |
|------|------|
| [`dev-workflow.md`](dev-workflow.md) | Branch/PR, install, pytest (`unit` / `api` / `mock`), tooling |
| [`python.mdc`](python.mdc) | Python conventions, `contentstack_management/`, `setup.py` |
| [`contentstack-management-python.mdc`](contentstack-management-python.mdc) | **Client**, **Stack**, **`_APIClient`**, CMA modules |
| [`testing.mdc`](testing.mdc) | pytest suites, **`tests/cred.py`**, env |
| [`code-review.mdc`](code-review.mdc) | PR checklist (**always applied**) |

## Rule application

| Context | Typical rules |
|---------|----------------|
| **Every session** | `code-review.mdc` |
| **Most repo files** | `dev-workflow.md` |
| **`contentstack_management/`** | `python.mdc` + `contentstack-management-python.mdc` |
| **`tests/**`** | `testing.mdc` |
| **Packaging / CI** | `python.mdc` |

## Quick reference

| File | `alwaysApply` | Globs (summary) |
|------|---------------|-----------------|
| `dev-workflow.md` | no | `**/*.py`, `setup.py`, `requirements.txt`, `.github/**/*.yml` |
| `python.mdc` | no | `contentstack_management/**/*.py`, `setup.py`, `requirements.txt` |
| `contentstack-management-python.mdc` | no | `contentstack_management/**/*.py` |
| `testing.mdc` | no | `tests/**/*.py` |
| `code-review.mdc` | **yes** | — |

## Skills

- [`skills/README.md`](../../skills/README.md) · [`AGENTS.md`](../../AGENTS.md)
