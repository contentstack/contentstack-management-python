"""Management Token API tests — find, fetch, create, update, delete, negative cases.

The setup already created one management token; this exercises the SDK surface
with its own throwaway token.
"""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(23)

# Branches-enabled orgs require a branch (or branch_alias) scope entry.
_SCOPE = [
    {"module": "content_type", "acl": {"read": True, "write": True}},
    {"module": "branch", "branches": ["main"], "acl": {"read": True}},
]


def _payload(name):
    return {"token": {"name": name, "description": "integration test", "scope": _SCOPE}}


class TestManagementTokenCRUD:
    def test_create(self, stack, store):
        name = h.generate_unique_title("MT")
        resp = stack.management_token().create(_payload(name))
        h.assert_status(resp, 201)
        store["management_tokens"]["main"] = h.body(resp).get("token", {}).get("uid")
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.management_token().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store):
        uid = store.get("management_tokens", {}).get("main")
        if not uid:
            pytest.skip("management token not created")
        resp = stack.management_token(uid).fetch()
        h.assert_status(resp, 200)

    def test_update(self, stack, store):
        uid = store.get("management_tokens", {}).get("main")
        if not uid:
            pytest.skip("management token not created")
        resp = stack.management_token(uid).update(_payload("Updated MT"))
        h.assert_status(resp, 200, 201)


class TestManagementTokenNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.management_token("no_such_mt").fetch()
        h.assert_status(resp, 404, 422)

    def test_fetch_without_uid_raises(self, stack):
        with pytest.raises(Exception):
            stack.management_token().fetch()


class TestManagementTokenDelete:
    def test_delete(self, stack, store):
        uid = store.get("management_tokens", {}).get("main")
        if not uid:
            pytest.skip("management token not created")
        resp = stack.management_token(uid).delete()
        h.assert_status(resp, 200)
