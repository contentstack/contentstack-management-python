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


def _environment_names(stack):
    resp = stack.environments().find()
    h.assert_status(resp, 200)
    return [env["name"] for env in h.body(resp).get("environments", [])]


def _create_with_environments(stack, uid, environments):
    data = {"branch": {"uid": uid, "source": "main", "publish_config": {"environments": environments}}}
    return stack.branch().create(data)


def _branch_environments(response):
    return h.body(response).get("branch", {}).get("publish_config", {}).get("environments")


def _delete_created_branch(stack, uid):
    # Same retry as TestBranchDelete: a freshly created branch can briefly be "not valid" (422, code 905).
    for _ in range(4):
        branch = stack.branch(uid)
        branch.add_param("force", "true")
        resp = branch.delete()
        if resp.status_code in (200, 204):
            return
        h.wait(h.LONG_DELAY)
    raise AssertionError(f"branch {uid} was not deleted after retries; status {resp.status_code}")


class TestBranchEnvironmentList:
    """Branch create with publish_config.environments. Each test deletes its branch (stack branch cap)."""

    def test_create_two_names_clones_only_those(self, stack):
        names = _environment_names(stack)
        if len(names) < 2:
            pytest.skip("stack has fewer than two environments")
        wanted = names[:2]
        uid = h.generate_valid_uid("branch_env")
        resp = _create_with_environments(stack, uid, wanted)
        try:
            h.assert_status(resp, 201)
            assert _branch_environments(resp) == wanted
            h.wait(h.LONG_DELAY)
            fetched = stack.branch(uid).fetch()
            h.assert_status(fetched, 200)
            assert _branch_environments(fetched) == wanted
        finally:
            if resp.status_code == 201:
                _delete_created_branch(stack, uid)

    def test_create_empty_list_clones_none(self, stack):
        uid = h.generate_valid_uid("branch_env")
        resp = _create_with_environments(stack, uid, [])
        try:
            h.assert_status(resp, 201)
            assert _branch_environments(resp) == []
            h.wait(h.LONG_DELAY)
            fetched = stack.branch(uid).fetch()
            h.assert_status(fetched, 200)
            assert _branch_environments(fetched) == []
        finally:
            if resp.status_code == 201:
                _delete_created_branch(stack, uid)

    def test_unknown_name_returns_422_and_creates_no_branch(self, stack):
        uid = h.generate_valid_uid("branch_env")
        resp = _create_with_environments(stack, uid, ["no_such_env_for_integration"])
        h.assert_status(resp, 422)
        assert "publish_config.environments" in h.body(resp).get("errors", {})
        h.assert_status(stack.branch(uid).fetch(), 404)

    def test_mix_of_valid_and_unknown_names_returns_422_and_creates_no_branch(self, stack):
        names = _environment_names(stack)
        if not names:
            pytest.skip("stack has no environments")
        uid = h.generate_valid_uid("branch_env")
        resp = _create_with_environments(stack, uid, [names[0], "no_such_env_for_integration"])
        h.assert_status(resp, 422)
        assert "publish_config.environments" in h.body(resp).get("errors", {})
        h.assert_status(stack.branch(uid).fetch(), 404)
