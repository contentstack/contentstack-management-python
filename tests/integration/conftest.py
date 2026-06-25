"""
pytest configuration for the CMA Python SDK integration suite.

Responsibilities:
  - load .env
  - install the request-capture layer (session-wide)
  - run dynamic stack setup once per session; tear it down at the end
  - expose `ctx`, `stack`, and `store` fixtures to tests
  - collect a per-test record (outcome, captured HTTP calls, tracked assertions)
    and render the custom dashboard HTML report at session finish
"""

import os
import sys
import time
from datetime import datetime

# Make `framework` / `data` importable as top-level packages, and the repo root
# importable for `contentstack_management`, regardless of pytest's rootdir.
_HERE = os.path.dirname(__file__)
_REPO_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
for _p in (_HERE, _REPO_ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pytest
from dotenv import load_dotenv

from framework import capture, report
from framework import setup as setup_mod
from framework.context import reset_store, test_data
from framework.helpers import set_active_tracker
from framework.report import TestRecord

load_dotenv()
load_dotenv(os.path.join(_HERE, ".env"))

# Session-wide accumulators.
_records = []
_session_started = None
_current_assertions = []  # tracker for the test currently running

# Reports are written to the repo root with a per-run timestamp so runs are never
# overwritten. Concrete paths are computed at session finish.
_REPORT_ROOT = _REPO_ROOT


# ---------------------------------------------------------------------------
# Session-scoped setup / teardown
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def ctx():
    """Dynamically created stack context, shared across the whole run."""
    capture.install()
    context = setup_mod.setup()
    capture.clear()  # discard setup traffic so it doesn't bleed into the first test
    yield context
    setup_mod.teardown(context)
    reset_store()
    capture.uninstall()


@pytest.fixture(scope="session")
def stack(ctx):
    """A ready stack accessor bound to the dynamic stack's api_key."""
    return ctx.client.stack(ctx.stack_api_key)


@pytest.fixture(scope="session")
def store():
    """Shared cross-file UID store (content_types, entries, assets, ...)."""
    return test_data


# ---------------------------------------------------------------------------
# Per-test capture wiring
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def _per_test_capture():
    """Clear HTTP capture + assertion tracker before each test."""
    global _current_assertions
    _current_assertions = []
    set_active_tracker(_current_assertions)
    capture.clear()
    yield
    set_active_tracker(None)


@pytest.fixture(autouse=True)
def _reset_client_headers(request):
    """Reset mutable client headers before each test for isolation.

    The SDK shares a single headers dict across all resources on a client, and
    several modules mutate it in place — e.g. Assets.upload() pops 'Content-Type'
    and Assets.update() sets it to 'multipart/form-data'. Without a reset, a JSON
    request that runs after an asset test inherits a broken Content-Type and the
    API returns 400/500. We restore a clean JSON baseline and drop leaked
    per-call headers (branch) so each test starts from a known state.
    """
    context = request.getfixturevalue("ctx")
    headers = context.client.client.headers
    headers["Content-Type"] = "application/json"
    headers.pop("branch", None)
    yield


def _resource_from_nodeid(nodeid: str) -> str:
    """Derive a resource group label from the test file name.
    'tests/integration/api/test_12_content_type.py::...' -> 'content_type'
    """
    filename = nodeid.split("::")[0].rsplit("/", 1)[-1]
    stem = filename.replace("test_", "").replace(".py", "")
    # strip leading order prefix like '12_'
    parts = stem.split("_", 1)
    if parts[0].isdigit() and len(parts) > 1:
        stem = parts[1]
    return stem


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Collect a TestRecord on the 'call' phase (and setup-phase skips/errors)."""
    outcome = yield
    rep = outcome.get_result()

    # Record on call phase; also capture setup-phase skips/failures.
    if rep.when == "call" or (rep.when == "setup" and rep.outcome in ("skipped", "failed")):
        wasxfail = hasattr(rep, "wasxfail")
        if wasxfail and rep.outcome == "passed":
            status = "xpassed"   # a known-broken op unexpectedly passed (maybe fixed!)
        elif wasxfail:
            status = "xfailed"   # known-broken op failed as expected (tracked, not hidden)
        elif rep.outcome == "passed":
            status = "passed"
        elif rep.outcome == "skipped":
            status = "skipped"
        else:
            status = "failed"

        message = ""
        if rep.longrepr is not None and status != "passed":
            message = str(rep.longrepr)

        # First line of the test's docstring, if any, as a human description.
        description = ""
        doc = getattr(getattr(item, "obj", None), "__doc__", None)
        if doc:
            description = doc.strip().split("\n", 1)[0].strip()

        # Class context (the "describe" block), e.g. TestContentTypeCRUD.
        parts = item.nodeid.split("::")
        class_name = parts[1] if len(parts) >= 3 else ""

        _records.append(
            TestRecord(
                nodeid=item.nodeid,
                name=item.name,
                resource=_resource_from_nodeid(item.nodeid),
                outcome=status,
                duration_ms=getattr(rep, "duration", 0) * 1000,
                message=message,
                calls=capture.get_all(),
                assertions=list(_current_assertions),
                description=description,
                group=class_name,
            )
        )


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------
def pytest_sessionstart(session):
    global _session_started
    _session_started = time.time()


def pytest_sessionfinish(session, exitstatus):
    if not _records:
        return
    ended = time.time()
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    html_path = os.path.join(_REPORT_ROOT, f"cma-python-report-{ts}.html")
    curl_path = os.path.join(_REPORT_ROOT, f"api-requests-{ts}.txt")
    report.render(_records, html_path, _session_started or ended, ended)
    report.write_curl_log(_records, curl_path)
    print(f"\nHTML report: {html_path}")
    print(f"cURL log:    {curl_path}")
