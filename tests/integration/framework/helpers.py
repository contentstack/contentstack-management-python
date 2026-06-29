"""
Test helper utilities for the integration suite.

Provides:
- unique test-data generators (uids, titles, emails, dates)
- timing utilities (wait, retry with backoff)
- response-shape validators (one per resource family)
- error-response assertions tuned to the Python SDK (which returns a
  requests.Response on HTTP errors rather than raising)
- tracked_assert: records expected/actual into the active test's report tracker

Python equivalent of the JS suite's testHelpers.js.
"""

import random
import re
import string
import time
from typing import Any, Iterable

# ---------------------------------------------------------------------------
# Configurable delays (seconds) — reused across dependent operations to reduce
# flakiness against a live API.
# ---------------------------------------------------------------------------
SHORT_DELAY = 2
API_DELAY = 5
LONG_DELAY = 10


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------
def short_id(length: int = 5) -> str:
    """Short lowercase alphanumeric suffix, e.g. 'a1b2c'."""
    alphabet = string.ascii_lowercase + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def generate_valid_uid(prefix: str = "test") -> str:
    """Contentstack-valid uid: lowercase, underscore-separated."""
    return f"{prefix}_{short_id()}".lower()


def generate_unique_title(base: str = "Test") -> str:
    return f"{base} {short_id()}"


def generate_random_email() -> str:
    return f"test_{short_id(8)}@example.com"


def generate_future_date(days_from_now: int = 7) -> str:
    from datetime import datetime, timedelta, timezone

    return (datetime.now(timezone.utc) + timedelta(days=days_from_now)).isoformat()


def generate_past_date(days_ago: int = 7) -> str:
    from datetime import datetime, timedelta, timezone

    return (datetime.now(timezone.utc) - timedelta(days=days_ago)).isoformat()


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------
def wait(seconds: float) -> None:
    time.sleep(seconds)


def retry(fn, attempts: int = 3, delay: float = 1.0):
    """Retry `fn` with linear backoff. Re-raises the last error on exhaustion."""
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - retry is intentionally broad
            last_error = exc
            if attempt < attempts:
                time.sleep(delay * attempt)
    raise last_error


# ---------------------------------------------------------------------------
# JSON body helper
# ---------------------------------------------------------------------------
def body(response) -> dict:
    """Parse a requests.Response JSON body, returning {} on non-JSON."""
    try:
        return response.json()
    except ValueError:
        return {}


def wait_for_scan(stack, asset_uid, expected, timeout=40, interval=3):
    """Poll an asset's _asset_scan_status (AM 2.0) until it reaches `expected`.

    Requires the include_asset_scan_status=true query param to surface the field.
    Returns the last observed status (the caller asserts == expected).
    """
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        asset = stack.assets(asset_uid)
        asset.add_param("include_asset_scan_status", "true")
        last = body(asset.fetch()).get("asset", {}).get("_asset_scan_status")
        if last == expected:
            return last
        time.sleep(interval)
    return last


# ---------------------------------------------------------------------------
# Status / error assertions (Python SDK does NOT raise on HTTP errors)
# ---------------------------------------------------------------------------
def assert_status(response, *expected_codes: int):
    """Assert response.status_code is one of expected_codes (helpful message)."""
    assert response.status_code in expected_codes, (
        f"Expected status in {expected_codes}, got {response.status_code}. "
        f"Body: {body(response)}"
    )


def assert_success(response):
    """Assert a 2xx success status."""
    assert 200 <= response.status_code < 300, (
        f"Expected 2xx success, got {response.status_code}. Body: {body(response)}"
    )


def validate_error_body(response):
    """Assert the error body carries the standard Contentstack error shape."""
    data = body(response)
    assert "error_message" in data or "error_code" in data, (
        f"Expected error body with error_message/error_code, got: {data}"
    )
    return data


# ---------------------------------------------------------------------------
# Response-shape validators
# ---------------------------------------------------------------------------
def _require_keys(obj: dict, keys: Iterable[str], label: str):
    for key in keys:
        assert key in obj, f"{label}: expected key '{key}' in response, got keys {list(obj)}"


def validate_content_type_response(response, expected_uid: str = None):
    data = body(response).get("content_type", body(response))
    _require_keys(data, ["uid", "title", "schema"], "content_type")
    assert isinstance(data["schema"], list)
    assert re.match(r"^[a-z][a-z0-9_]*$", data["uid"]), f"bad uid format: {data['uid']}"
    if expected_uid:
        assert data["uid"] == expected_uid
    return data


def validate_entry_response(response, content_type_uid: str = None):
    data = body(response).get("entry", body(response))
    _require_keys(data, ["uid", "title", "locale"], "entry")
    assert re.match(r"^blt[a-f0-9]+$", data["uid"]), f"bad entry uid: {data['uid']}"
    return data


def validate_asset_response(response):
    data = body(response).get("asset", body(response))
    _require_keys(data, ["uid", "filename", "url", "content_type"], "asset")
    assert re.match(r"^(blt|am)[a-f0-9]+$", data["uid"]), f"bad asset uid: {data['uid']}"
    return data


def validate_global_field_response(response, expected_uid: str = None):
    data = body(response).get("global_field", body(response))
    _require_keys(data, ["uid", "title", "schema"], "global_field")
    assert isinstance(data["schema"], list)
    if expected_uid:
        assert data["uid"] == expected_uid
    return data


def validate_locale_response(response):
    data = body(response).get("locale", body(response))
    _require_keys(data, ["code", "name"], "locale")
    return data


def validate_environment_response(response):
    data = body(response).get("environment", body(response))
    _require_keys(data, ["uid", "name"], "environment")
    return data


def validate_workflow_response(response):
    data = body(response).get("workflow", body(response))
    _require_keys(data, ["uid", "name", "workflow_stages"], "workflow")
    assert isinstance(data["workflow_stages"], list) and data["workflow_stages"]
    return data


def validate_webhook_response(response):
    data = body(response).get("webhook", body(response))
    _require_keys(data, ["uid", "name", "destinations", "channels"], "webhook")
    return data


def validate_role_response(response):
    data = body(response).get("role", body(response))
    # Permission rules are returned as 'rules' on create but 'SYS_ACL' on fetch,
    # so only uid + name are guaranteed across both shapes.
    _require_keys(data, ["uid", "name"], "role")
    return data


def validate_release_response(response):
    data = body(response).get("release", body(response))
    _require_keys(data, ["uid", "name"], "release")
    return data


def validate_token_response(response):
    data = body(response).get("token", body(response))
    _require_keys(data, ["uid", "name", "token"], "token")
    return data


def validate_branch_response(response):
    data = body(response).get("branch", body(response))
    _require_keys(data, ["uid", "source"], "branch")
    return data


def validate_taxonomy_response(response):
    data = body(response).get("taxonomy", body(response))
    _require_keys(data, ["uid", "name"], "taxonomy")
    return data


def validate_term_response(response):
    data = body(response).get("term", body(response))
    _require_keys(data, ["uid", "name"], "term")
    return data


# ---------------------------------------------------------------------------
# tracked_assert — records expected/actual to the active test's report tracker.
# The tracker is set by conftest before each test; if absent, this degrades to a
# plain assert so helpers remain usable outside a pytest run.
# ---------------------------------------------------------------------------
_active_tracker = None


def set_active_tracker(tracker) -> None:
    global _active_tracker
    _active_tracker = tracker


def _record(description: str, expected: Any, actual: Any, passed: bool):
    if _active_tracker is not None:
        _active_tracker.append(
            {
                "description": description,
                "expected": _fmt(expected),
                "actual": _fmt(actual),
                "passed": passed,
            }
        )


def _fmt(value: Any) -> str:
    text = repr(value)
    return text if len(text) <= 200 else text[:200] + "..."


def tracked_assert(actual: Any, description: str = ""):
    """Chainable tracked assertion, e.g.
    tracked_assert(resp.status_code, 'status').equals(201)
    """

    class _Chain:
        def equals(self, expected):
            passed = actual == expected
            _record(description or "equals", expected, actual, passed)
            assert passed, f"{description}: expected {expected!r}, got {actual!r}"
            return self

        def is_in(self, options):
            passed = actual in options
            _record(description or "is_in", options, actual, passed)
            assert passed, f"{description}: expected one of {options!r}, got {actual!r}"
            return self

        def is_type(self, typ):
            passed = isinstance(actual, typ)
            _record(description or "is_type", typ.__name__, type(actual).__name__, passed)
            assert passed, f"{description}: expected {typ.__name__}, got {type(actual).__name__}"
            return self

        def truthy(self):
            passed = bool(actual)
            _record(description or "truthy", "truthy", actual, passed)
            assert passed, f"{description}: expected truthy, got {actual!r}"
            return self

        def matches(self, pattern):
            passed = bool(re.match(pattern, str(actual)))
            _record(description or "matches", pattern, actual, passed)
            assert passed, f"{description}: {actual!r} does not match {pattern}"
            return self

    return _Chain()
