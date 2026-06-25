"""Role API tests — CRUD, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(20)


def _role_payload(name):
    return {
        "role": {
            "name": name,
            "description": "integration test role",
            "rules": [{"module": "environment", "environments": [], "acl": {"read": True}}],
        }
    }


class TestRoleCRUD:
    def test_create(self, stack, store):
        name = h.generate_unique_title("Role")
        resp = stack.roles().create(_role_payload(name))
        h.assert_status(resp, 201)
        store["roles"]["main"] = h.body(resp).get("role", {}).get("uid")
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.roles().find()
        h.assert_status(resp, 200)
        h.tracked_assert(h.body(resp).get("roles"), "roles list").is_type(list)

    def test_fetch(self, stack, store):
        uid = store.get("roles", {}).get("main")
        if not uid:
            pytest.skip("role not created")
        resp = stack.roles(uid).fetch()
        h.assert_status(resp, 200)
        h.validate_role_response(resp)

    def test_update(self, stack, store):
        uid = store.get("roles", {}).get("main")
        if not uid:
            pytest.skip("role not created")
        resp = stack.roles(uid).update(_role_payload("Updated Role"))
        h.assert_status(resp, 200, 201)


class TestRoleNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.roles("no_such_role").fetch()
        h.assert_status(resp, 404, 422)


class TestRoleDelete:
    def test_delete(self, stack):
        created = h.body(stack.roles().create(_role_payload(h.generate_unique_title("RoleDel"))))
        uid = created.get("role", {}).get("uid")
        if not uid:
            pytest.skip("role not created")
        h.wait(h.SHORT_DELAY)
        resp = stack.roles(uid).delete()
        h.assert_status(resp, 200)
