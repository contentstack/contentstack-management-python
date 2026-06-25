"""Stack API tests — fetch, settings, users, share/unshare."""

import os

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(3)


class TestStack:
    def test_fetch(self, ctx):
        resp = ctx.client.stack(ctx.stack_api_key).fetch()
        h.assert_status(resp, 200)
        stack = h.body(resp).get("stack", {})
        h.tracked_assert(stack.get("api_key"), "api_key").equals(ctx.stack_api_key)

    def test_settings(self, ctx):
        resp = ctx.client.stack(ctx.stack_api_key).settings()
        h.assert_status(resp, 200)

    def test_create_settings(self, ctx):
        data = {
            "stack_settings": {
                "stack_variables": {"enforce_unique_urls": "true"},
            }
        }
        resp = ctx.client.stack(ctx.stack_api_key).create_settings(data)
        h.assert_status(resp, 200, 201)

    def test_users(self, ctx):
        resp = ctx.client.stack(ctx.stack_api_key).users()
        h.assert_status(resp, 200)

    def test_update(self, ctx):
        data = {"stack": {"description": "updated by integration suite"}}
        resp = ctx.client.stack(ctx.stack_api_key).update(data)
        h.assert_status(resp, 200, 201)

    def test_reset_settings(self, ctx):
        resp = ctx.client.stack(ctx.stack_api_key).reset_settings({"stack_settings": {}})
        h.assert_status(resp, 200, 201)


class TestStackOwnership:
    """Ownership/role operations exercised safely (no real transfer occurs)."""

    def test_update_user_role(self, ctx):
        # Map the current user to a role; on a fresh single-user stack this may
        # be accepted (200) or rejected (422) — both confirm the SDK call works.
        roles = h.body(ctx.client.stack(ctx.stack_api_key).roles().find()).get("roles", [])
        role_uid = next((r["uid"] for r in roles), None)
        if not (role_uid and ctx.user_uid):
            pytest.skip("no role/user available")
        resp = ctx.client.stack(ctx.stack_api_key).update_user_role({"users": {ctx.user_uid: [role_uid]}})
        # 404 when the user isn't a separately-added stack member (owner self-assign).
        h.assert_status(resp, 200, 201, 404, 422)

    def test_transfer_ownership_invalid(self, ctx):
        # Transferring to an invalid address must fail — exercises the endpoint
        # without actually handing the stack to anyone.
        resp = ctx.client.stack(ctx.stack_api_key).transfer_ownership({"transfer_to": "not-an-email"})
        h.assert_status(resp, 400, 422)

    def test_accept_ownership_bogus_token(self, ctx):
        # Accepting with a bogus token must fail.
        resp = ctx.client.stack(ctx.stack_api_key).accept_ownership(ctx.user_uid or "uid", "bogus_token")
        h.assert_status(resp, 400, 404, 422)


class TestStackSharing:
    def test_share(self, ctx):
        member = os.getenv("MEMBER_EMAIL")
        if not member:
            pytest.skip("MEMBER_EMAIL not set")
        # Sharing requires a valid role mapping per email — an empty roles object
        # is rejected with 422 "roles is not valid".
        roles = h.body(ctx.client.stack(ctx.stack_api_key).roles().find()).get("roles", [])
        role_uid = next((r["uid"] for r in roles if r.get("name") != "Admin"),
                        roles[0]["uid"] if roles else None)
        if not role_uid:
            pytest.skip("no role available to share with")
        data = {"emails": [member], "roles": {member: [role_uid]}}
        resp = ctx.client.stack(ctx.stack_api_key).share(data)
        h.assert_status(resp, 200, 201)

    def test_unshare(self, ctx):
        member = os.getenv("MEMBER_EMAIL")
        if not member:
            pytest.skip("MEMBER_EMAIL not set")
        resp = ctx.client.stack(ctx.stack_api_key).unshare({"email": member})
        h.assert_status(resp, 200, 201)
