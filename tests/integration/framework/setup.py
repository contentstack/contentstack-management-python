"""
Dynamic stack lifecycle for the integration suite.

Drives the full setup/teardown:
  1. validate environment
  2. build SDK client + login (email/password, optional MFA)
  3. create a fresh test stack
  4. create a management token for it
  5. (teardown) delete stack + logout, gated by DELETE_DYNAMIC_RESOURCES

All calls go through the SDK so the request-capture layer records them. Uses the
SDK exactly as a customer would — exercising the real artifact under test.

Env vars (see .env.example):
  Required: EMAIL, PASSWORD, HOST, ORGANIZATION
  Optional: MFA_SECRET, DELETE_DYNAMIC_RESOURCES (default 'true')
"""

import os

import contentstack_management

from .context import TestContext
from .helpers import short_id, wait

# Generous timeout for live integration calls (SDK default is only 2s).
# Generous read timeout for live calls; transient timeouts are also retried in
# the capture layer so a single dev11 blip doesn't fail the run.
_CLIENT_TIMEOUT = 120

# Management-token scope: core content modules + branch read (branches-enabled orgs).
_MGMT_TOKEN_SCOPE = [
    {"module": "content_type", "acl": {"read": True, "write": True}},
    {"module": "entry", "acl": {"read": True, "write": True}},
    {"module": "asset", "acl": {"read": True, "write": True}},
    {"module": "environment", "acl": {"read": True, "write": True}},
    {"module": "locale", "acl": {"read": True, "write": True}},
    {"module": "branch", "branches": ["main"], "acl": {"read": True}},
    {"module": "branch_alias", "branch_aliases": [], "acl": {"read": True}},
]

REQUIRED_ENV = ["EMAIL", "PASSWORD", "HOST", "ORGANIZATION"]


def validate_environment() -> None:
    missing = [k for k in REQUIRED_ENV if not os.getenv(k)]
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"See tests/integration/.env.example."
        )


def should_delete_resources() -> bool:
    return os.getenv("DELETE_DYNAMIC_RESOURCES", "true").lower() != "false"


def _expiry_iso(days: int = 30) -> str:
    from datetime import datetime, timedelta, timezone

    return (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()


def setup() -> TestContext:
    """Login, create a fresh stack + management token. Returns a populated context."""
    validate_environment()
    ctx = TestContext()
    ctx.organization_uid = os.getenv("ORGANIZATION")
    host = os.getenv("HOST", "api.contentstack.io")

    print("\n" + "=" * 60)
    print("CMA Python SDK Integration Suite — Dynamic Setup")
    print("=" * 60)
    print(f"Host:          {host}")
    print(f"Organization:  {ctx.organization_uid}")
    print(f"Delete after:  {should_delete_resources()}")
    print("=" * 60)

    # 1. Client + login. The primary EMAIL account is logged in with plain
    #    email/password (matching the JS suite). MFA_SECRET in .env belongs to the
    #    dedicated 2FA account (TFA_EMAIL) used only by 2FA-specific tests — it must
    #    NOT be applied to the primary login. Since the SDK auto-reads MFA_SECRET from
    #    the environment, we suppress it for the primary attempt and only fall back to
    #    MFA if the account genuinely requires 2FA.
    ctx.client = contentstack_management.Client(host=host, timeout=_CLIENT_TIMEOUT)
    login_resp = _login_primary(ctx.client)
    if login_resp.status_code != 200:
        raise RuntimeError(
            f"Login failed ({login_resp.status_code}): {login_resp.text}"
        )
    user = login_resp.json().get("user", {})
    ctx.authtoken = user.get("authtoken")
    ctx.user_uid = user.get("uid")
    ctx.is_logged_in = True
    print(f"Logged in as: {os.getenv('EMAIL')}")

    # 2. Create a fresh stack.
    #    NOTE: Stack.create() has an SDK bug — its `if organization_uid is not None
    #    and '':` guard is always falsy, so it never sets the organization_uid
    #    header, and the API rejects the create (422, error_code 110). We set the
    #    header on the client here as a setup-side workaround (the JS suite likewise
    #    bypasses the SDK for stack creation). This does not modify SDK source.
    ctx.client.client.headers["organization_uid"] = ctx.organization_uid
    stack_name = f"SDK_Py_Test_{short_id()}"
    create_resp = ctx.client.stack().create(
        ctx.organization_uid,
        {
            "stack": {
                "name": stack_name,
                "description": "Automated Python SDK integration test stack",
                "master_locale": "en-us",
            }
        },
    )
    if create_resp.status_code not in (200, 201):
        raise RuntimeError(
            f"Stack creation failed ({create_resp.status_code}): {create_resp.text}"
        )
    stack = create_resp.json().get("stack", {})
    ctx.stack_api_key = stack.get("api_key")
    ctx.stack_uid = stack.get("uid")
    ctx.stack_name = stack.get("name", stack_name)
    ctx.is_dynamic_stack_created = True
    # Bind a stack accessor for the tests.
    ctx.stack = ctx.client.stack(ctx.stack_api_key)
    print(f"Created stack: {ctx.stack_name} ({ctx.stack_api_key})")

    # Wait for provisioning (branches-enabled orgs set up the main branch).
    wait(5)

    # 3. Create a management token (non-fatal; retry once after a wait).
    _create_management_token(ctx)

    # 4. Create a Personalize project linked to the stack (non-fatal) so variant
    #    tests can run instead of skipping. Mirrors the JS suite.
    _create_personalize_project(ctx)

    print("=" * 60)
    print("Setup complete — running tests")
    print("=" * 60 + "\n")
    return ctx


def _create_personalize_project(ctx: TestContext) -> None:
    personalize_host = os.getenv("PERSONALIZE_HOST")
    if not personalize_host:
        print("PERSONALIZE_HOST not set — skipping personalize project (variant tests will skip).")
        return
    import requests

    name = f"SDK_Py_Proj_{short_id()}"
    try:
        resp = requests.post(
            f"https://{personalize_host}/projects",
            json={
                "name": name,
                "description": "Auto-generated test project",
                "connectedStackApiKey": ctx.stack_api_key,
            },
            headers={
                "authtoken": ctx.authtoken,
                "organization_uid": ctx.organization_uid,
                "Content-Type": "application/json",
            },
            timeout=_CLIENT_TIMEOUT,
        )
        if resp.status_code in (200, 201):
            data = resp.json()
            ctx.personalize_project_uid = data.get("uid") or data.get("project_uid") or data.get("_id")
            ctx.personalize_project_name = data.get("name", name)
            ctx.is_personalize_created = True
            print(f"Created personalize project: {ctx.personalize_project_name}")
        else:
            print(f"Personalize project not created ({resp.status_code}) — variant tests will skip.")
    except Exception as exc:  # noqa: BLE001
        print(f"Personalize project creation error: {exc} — variant tests will skip.")


def _login_primary(client):
    """Login the primary (normal) account with EMAIL / PASSWORD.

    This is a plain, non-2FA login. MFA_SECRET in .env belongs to the OAuth/TFA
    account (TFA_EMAIL) and must NOT be applied here, so it is suppressed from the
    SDK's automatic env pickup. If EMAIL turns out to require 2FA, we surface a
    clear, actionable error rather than silently borrowing the wrong account's secret.
    """
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    saved = os.environ.pop("MFA_SECRET", None)  # keep OAuth secret out of normal login
    try:
        resp = client.login(email, password)
    finally:
        if saved is not None:
            os.environ["MFA_SECRET"] = saved

    if resp.status_code != 200:
        try:
            err = resp.json()
        except ValueError:
            err = {"error_message": resp.text}
        if err.get("error_code") in (104, 294):
            raise RuntimeError(
                f"Login failed ({resp.status_code}): {err.get('error_message')}\n"
                f"The EMAIL account '{email}' requires Two-Factor Authentication. "
                f"For normal-login tests, EMAIL/PASSWORD must be a NON-2FA account "
                f"(MFA_SECRET is reserved for the OAuth/TFA_EMAIL suite)."
            )
    return resp


def _create_management_token(ctx: TestContext) -> None:
    token_name = f"SDK_Py_Token_{short_id()}"
    payload = {
        "token": {
            "name": token_name,
            "description": "Auto-generated test token",
            "scope": _MGMT_TOKEN_SCOPE,
            "expires_on": _expiry_iso(30),
        }
    }
    for attempt in (1, 2):
        try:
            resp = ctx.stack.management_token().create(payload)
            if resp.status_code in (200, 201):
                token = resp.json().get("token", {})
                ctx.management_token = token.get("token")
                ctx.management_token_uid = token.get("uid")
                print(f"Created management token: {token_name}")
                return
            print(f"Management token attempt {attempt} failed "
                  f"({resp.status_code}): {resp.text[:200]}")
        except Exception as exc:  # noqa: BLE001
            print(f"Management token attempt {attempt} error: {exc}")
        if attempt == 1:
            wait(5)
    print("Management token not created (non-fatal).")


def teardown(ctx: TestContext) -> None:
    """Delete the stack + logout, gated by DELETE_DYNAMIC_RESOURCES."""
    print("\n" + "=" * 60)
    print("CMA Python SDK Integration Suite — Cleanup")
    print("=" * 60)

    if ctx is None:
        return

    if should_delete_resources():
        if ctx.is_personalize_created and ctx.personalize_project_uid:
            _delete_personalize_project(ctx)
        if ctx.is_dynamic_stack_created and ctx.stack_api_key:
            try:
                resp = ctx.client.stack(ctx.stack_api_key).delete()
                print(f"Deleted stack {ctx.stack_name}: {resp.status_code}")
            except Exception as exc:  # noqa: BLE001
                print(f"Stack deletion warning: {exc}")
        _logout(ctx)
    else:
        print("DELETE_DYNAMIC_RESOURCES=false — preserving resources for debugging:")
        print(f"  Stack:        {ctx.stack_name}")
        print(f"  API Key:      {ctx.stack_api_key}")
        if ctx.management_token:
            print(f"  Mgmt Token:   {ctx.management_token}")
        print("  Remember to delete these manually when done.")
        _logout(ctx)

    print("=" * 60 + "\n")


def _delete_personalize_project(ctx: TestContext) -> None:
    personalize_host = os.getenv("PERSONALIZE_HOST")
    if not personalize_host:
        return
    import requests

    try:
        resp = requests.delete(
            f"https://{personalize_host}/projects/{ctx.personalize_project_uid}",
            headers={"authtoken": ctx.authtoken, "organization_uid": ctx.organization_uid},
            timeout=_CLIENT_TIMEOUT,
        )
        print(f"Deleted personalize project {ctx.personalize_project_name}: {resp.status_code}")
    except Exception as exc:  # noqa: BLE001
        print(f"Personalize deletion warning: {exc}")


def _logout(ctx: TestContext) -> None:
    if not ctx.is_logged_in:
        return
    try:
        ctx.client.logout()
        ctx.is_logged_in = False
        print("Logged out.")
    except Exception as exc:  # noqa: BLE001
        print(f"Logout warning: {exc}")
