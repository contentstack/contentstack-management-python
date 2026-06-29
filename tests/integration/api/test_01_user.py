"""User API tests — profile fetch and update."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(1)


class TestUser:
    def test_fetch(self, ctx):
        resp = ctx.client.user().fetch()
        h.assert_status(resp, 200)
        user = h.body(resp).get("user", {})
        h.tracked_assert(user.get("uid"), "user uid").truthy()

    def test_update_noop(self, ctx):
        # Send the current first_name back — a harmless update that exercises PUT /user.
        current = h.body(ctx.client.user().fetch()).get("user", {})
        payload = {"user": {"first_name": current.get("first_name", "Test")}}
        resp = ctx.client.user().update(payload)
        h.assert_status(resp, 200, 201)


class TestUserAuthOps:
    """Account auth endpoints exercised safely (bogus tokens / non-real email)."""

    def test_activate_bogus_token(self, ctx):
        resp = ctx.client.user().activate("bogus_activation_token", {"user": {"password": "Test@12345"}})
        h.assert_status(resp, 400, 404, 422)

    def test_reset_password_bogus_token(self, ctx):
        resp = ctx.client.user().reset_password(
            {"user": {"reset_password_token": "bogus", "password": "Test@12345", "password_confirmation": "Test@12345"}}
        )
        h.assert_status(resp, 400, 404, 422)

    def test_forgot_password(self, ctx):
        # Triggers a reset email to a non-real address; APIs typically return 200
        # regardless (to avoid email enumeration) or a 422.
        resp = ctx.client.user().forgot_password({"user": {"email": "noreply+test@example.com"}})
        h.assert_status(resp, 200, 201, 422, 429)
