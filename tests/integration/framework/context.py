"""
Shared test context and cross-file data store for the integration suite.

`TestContext` holds the dynamically created stack credentials and auth state for a
single test run. `test_data` is a shared store used to pass created-resource UIDs
between test files (e.g. a content type created in test_12 is referenced by the
entry tests in test_14).

These are exposed to tests through session-scoped fixtures in conftest.py
(`ctx`, `stack`, `store`) rather than imported directly, keeping the global mutable
state contained to the framework layer.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class TestContext:
    """Holds auth + dynamically created stack state for one test run."""

    # SDK client
    client: Any = None
    stack: Any = None

    # Authentication
    authtoken: Optional[str] = None
    user_uid: Optional[str] = None

    # Stack (dynamically created)
    stack_api_key: Optional[str] = None
    stack_uid: Optional[str] = None
    stack_name: Optional[str] = None

    # Management token (dynamically created)
    management_token: Optional[str] = None
    management_token_uid: Optional[str] = None

    # Organization (from env)
    organization_uid: Optional[str] = None

    # Personalize project (dynamically created, optional)
    personalize_project_uid: Optional[str] = None
    personalize_project_name: Optional[str] = None

    # Lifecycle flags
    is_logged_in: bool = False
    is_dynamic_stack_created: bool = False
    is_personalize_created: bool = False


def _empty_store() -> dict:
    """Fresh cross-file UID store. One bucket per resource family."""
    return {
        "content_types": {},
        "entries": {},
        "assets": {},
        "folders": {},
        "global_fields": {},
        "taxonomies": {},
        "terms": {},
        "extensions": {},
        "environments": {},
        "locales": {},
        "workflows": {},
        "webhooks": {},
        "labels": {},
        "roles": {},
        "delivery_tokens": {},
        "management_tokens": {},
        "releases": {},
        "branches": {},
        "aliases": {},
        "variant_groups": {},
        "variants": {},
    }


# Shared, mutable across the whole run. Reset via `reset_store()` in session teardown.
test_data: dict = _empty_store()


def reset_store() -> None:
    """Clear all cross-file UID buckets (called in session teardown)."""
    global test_data
    test_data.clear()
    test_data.update(_empty_store())
