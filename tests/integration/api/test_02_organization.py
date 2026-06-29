"""Organization API tests — fetch, roles, stacks, logs, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(2)


class TestOrganization:
    def test_find_all(self, ctx):
        resp = ctx.client.organizations().find()
        h.assert_status(resp, 200)
        h.tracked_assert(h.body(resp).get("organizations"), "orgs list").is_type(list)

    def test_fetch(self, ctx):
        resp = ctx.client.organizations(ctx.organization_uid).fetch()
        h.assert_status(resp, 200)
        org = h.body(resp).get("organization", {})
        h.tracked_assert(org.get("uid"), "org uid").equals(ctx.organization_uid)

    def test_roles(self, ctx):
        resp = ctx.client.organizations(ctx.organization_uid).roles()
        h.assert_status(resp, 200)

    def test_stacks(self, ctx):
        resp = ctx.client.organizations(ctx.organization_uid).stacks()
        h.assert_status(resp, 200)

    def test_logs(self, ctx):
        resp = ctx.client.organizations(ctx.organization_uid).logs()
        h.assert_status(resp, 200)


class TestOrganizationOwnership:
    """Exercised safely with invalid data so no real invite/transfer occurs."""

    def test_add_users_invalid(self, ctx):
        resp = ctx.client.organizations(ctx.organization_uid).add_users({"share": {}})
        h.assert_status(resp, 400, 403, 422)

    def test_transfer_ownership_invalid(self, ctx):
        resp = ctx.client.organizations(ctx.organization_uid).transfer_ownership({"transfer_to": "not-an-email"})
        h.assert_status(resp, 400, 403, 422)


class TestOrganizationNegative:
    def test_fetch_nonexistent(self, ctx):
        resp = ctx.client.organizations("org_does_not_exist").fetch()
        h.assert_status(resp, 404, 422, 403)
