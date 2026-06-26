"""Branch API tests — CRUD, negative cases.

Branch create/delete are slow on the API; generous waits are used. Stacks cap the
number of branches, so the suite creates at most one and deletes it.
"""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(18)


class TestBranchCRUD:
    def test_create(self, stack, store):
        uid = h.generate_valid_uid("branch")
        resp = stack.branch().create({"branch": {"uid": uid, "source": "main"}})
        h.assert_status(resp, 201)
        store["branches"]["main"] = uid
        h.wait(h.LONG_DELAY)

    def test_find_all(self, stack):
        resp = stack.branch().find()
        h.assert_status(resp, 200)
        h.tracked_assert(h.body(resp).get("branches"), "branches list").is_type(list)

    def test_fetch(self, stack, store):
        uid = store.get("branches", {}).get("main")
        if not uid:
            pytest.skip("branch not created")
        resp = stack.branch(uid).fetch()
        h.assert_status(resp, 200)


class TestBranchNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.branch("no_such_branch").fetch()
        h.assert_status(resp, 404, 422)


class TestBranchDelete:
    def test_delete(self, stack, store):
        uid = store.get("branches", {}).get("main")
        if not uid:
            pytest.skip("branch not created")
        # Branch delete requires force=true (the API otherwise returns a 422
        # confirmation prompt). Branch provisioning is async on the API, so a
        # freshly created branch can briefly be "not valid" for deletion (422,
        # code 905) — retry a few times with a wait until it deletes.
        resp = None
        for attempt in range(4):
            branch = stack.branch(uid)
            branch.add_param("force", "true")
            resp = branch.delete()
            if resp.status_code in (200, 204):
                break
            h.wait(h.LONG_DELAY)
        h.assert_status(resp, 200, 204)
        h.wait(h.SHORT_DELAY)
