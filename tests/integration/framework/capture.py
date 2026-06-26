"""
Request/response capture for the integration suite.

The SDK issues HTTP calls through `requests.request(...)` inside
`contentstack_management._api_client._APIClient._call_request`. We monkeypatch
`requests.request` once per session so every SDK call is recorded with enough detail
to drive the HTML report and a copy-ready cURL command — without changing SDK code.

This mirrors the JS suite's axios request-capture plugin.
"""

import json
import os
import time
from typing import Any, Optional

import requests

# Ring buffer of captured calls. Cleared per-test by conftest so each test's report
# entry only shows its own traffic.
_captured: list = []
_MAX_BUFFER = 200

# Saved reference to the original requests.request so we can call through + restore.
_original_request = None

# Headers whose values should be masked in the report / cURL output.
_SENSITIVE_HEADERS = {"authtoken", "authorization"}

# Cap on response/request body length stored for the report (bytes/chars).
_MAX_BODY = 4000


def _mask(key: str, value: str) -> str:
    if key.lower() in _SENSITIVE_HEADERS and isinstance(value, str):
        if len(value) > 15:
            return value[:10] + "..." + value[-5:]
        return "***"
    return value


def _truncate(text: str) -> str:
    if text is None:
        return None
    if len(text) > _MAX_BODY:
        return text[:_MAX_BODY] + "\n... (truncated)"
    return text


def _stringify(data: Any) -> Optional[str]:
    if data is None:
        return None
    if isinstance(data, (bytes, bytearray)):
        return f"<binary {len(data)} bytes>"
    if isinstance(data, str):
        return data
    try:
        return json.dumps(data)
    except (TypeError, ValueError):
        return str(data)


def _generate_curl(method: str, url: str, headers: dict, data: Any) -> str:
    parts = [f"curl -X {method.upper()} '{url}'"]
    for key, value in (headers or {}).items():
        if value is None:
            continue
        parts.append(f"  -H '{key}: {_mask(key, str(value))}'")
    body = _stringify(data)
    if body and not body.startswith("<binary"):
        safe = body.replace("'", "'\\''")
        parts.append(f"  -d '{safe}'")
    return " \\\n".join(parts)


def _detect_sdk_method(method: str, url: str) -> str:
    """Best-effort human label for the SDK method exercised, from method + path."""
    try:
        path = url.split("://", 1)[-1]
        path = "/" + path.split("/", 1)[1] if "/" in path else path
    except (IndexError, AttributeError):
        path = url
    # Strip /v3 prefix for readability.
    if "/v3/" in path:
        path = path.split("/v3", 1)[1]
    m = method.upper()
    table = [
        (r"/user-session", "POST", "client.login()"),
        (r"/user-session", "DELETE", "client.logout()"),
        (r"/user", "GET", "client.user().fetch()"),
        (r"/stacks", "POST", "client.stack().create()"),
        (r"/stacks", "GET", "client.stack().fetch()"),
        (r"/content_types", "POST", "stack.content_types().create()"),
        (r"/content_types", "GET", "stack.content_types().find()"),
        (r"/entries", "POST", "content_type.entry().create()"),
        (r"/entries", "GET", "content_type.entry().find()"),
        (r"/assets", "POST", "stack.assets().upload()"),
        (r"/assets", "GET", "stack.assets().find()"),
        (r"/global_fields", "POST", "stack.global_fields().create()"),
        (r"/global_fields", "GET", "stack.global_fields().find()"),
        (r"/environments", "POST", "stack.environments().create()"),
        (r"/locales", "POST", "stack.locale().create()"),
        (r"/webhooks", "POST", "stack.webhooks().create()"),
        (r"/workflows", "POST", "stack.workflows().create()"),
        (r"/taxonomies", "POST", "stack.taxonomy().create()"),
        (r"/releases", "POST", "stack.releases().create()"),
    ]
    import re

    for pat, meth, label in table:
        if meth == m and re.search(pat + r"(/|$|\?)", path):
            return label
    return f"{m} {path}"


# Transient network errors get a couple of automatic retries so a single dev11
# blip (e.g. a read timeout) doesn't red the whole suite.
_TRANSIENT_RETRIES = 2
_RETRY_BACKOFF_SECONDS = 3


def _request_with_retry(method, url, kwargs):
    """Call the real requests.request, retrying transient network failures."""
    import requests.exceptions as rex

    transient = (rex.ConnectionError, rex.ConnectTimeout, rex.ReadTimeout, rex.Timeout)
    last_exc = None
    for attempt in range(_TRANSIENT_RETRIES + 1):
        try:
            return _original_request(method, url, **kwargs)
        except transient as exc:
            last_exc = exc
            if attempt < _TRANSIENT_RETRIES:
                time.sleep(_RETRY_BACKOFF_SECONDS)
            # Re-open any file handles (consumed by the failed multipart attempt).
            files = kwargs.get("files")
            if files:
                for key, val in list(files.items()):
                    name = getattr(val[1] if isinstance(val, (tuple, list)) else val, "name", None)
                    if name and os.path.exists(name):
                        kwargs["files"][key] = (val[0], open(name, "rb"), val[2]) if isinstance(val, (tuple, list)) else open(name, "rb")
    raise last_exc


def _patched_request(method, url, **kwargs):
    """Drop-in for requests.request that records the call, then delegates."""
    start = time.time()
    req_headers = kwargs.get("headers") or {}
    req_data = kwargs.get("data")
    req_files = kwargs.get("files")
    record = {
        "timestamp": start,
        "method": str(method).upper(),
        "url": url,
        "request_headers": {k: _mask(k, str(v)) for k, v in req_headers.items()},
        "request_body": _truncate(_stringify(req_data)),
        "has_files": bool(req_files),
        "status": None,
        "status_text": None,
        "response_headers": {},
        "response_body": None,
        "duration_ms": None,
        "curl": _generate_curl(str(method), url, req_headers, req_data),
        "sdk_method": _detect_sdk_method(str(method), url),
        "error": None,
    }
    try:
        response = _request_with_retry(method, url, kwargs)
        record["status"] = response.status_code
        record["status_text"] = response.reason
        record["response_headers"] = dict(response.headers)
        try:
            body = json.dumps(response.json(), indent=2)
        except ValueError:
            body = response.text
        record["response_body"] = _truncate(body)
        return response
    except Exception as exc:  # network error, timeout, etc.
        record["error"] = str(exc)
        raise
    finally:
        record["duration_ms"] = round((time.time() - start) * 1000, 1)
        _captured.append(record)
        if len(_captured) > _MAX_BUFFER:
            _captured.pop(0)


def install() -> None:
    """Monkeypatch requests.request. Idempotent."""
    global _original_request
    if _original_request is None:
        _original_request = requests.request
        requests.request = _patched_request


def uninstall() -> None:
    """Restore the original requests.request."""
    global _original_request
    if _original_request is not None:
        requests.request = _original_request
        _original_request = None


def clear() -> None:
    """Clear the capture buffer (called before each test)."""
    _captured.clear()


def get_all() -> list:
    """All captured calls currently in the buffer."""
    return list(_captured)


def get_last() -> Optional[dict]:
    """Most recent captured call, or None."""
    return _captured[-1] if _captured else None
