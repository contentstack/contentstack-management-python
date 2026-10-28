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


def _create_branch(stack, uid, environments=None):
    branch = {"uid": uid, "source": "main"}
    if environments is not None:
        branch["publish_config"] = {"environments": environments}
    return stack.branch().create({"branch": branch})


def _branch(response):
    return h.body(response).get("branch", {})


def _branch_environments(response):
    return (_branch(response).get("publish_config") or {}).get("environments")


def _fetch_when_ready(stack, uid):
    # Branch provisioning is async: poll until the fetch succeeds
    resp = None
    for _ in range(10):
        resp = stack.branch(uid).fetch()
        if resp.status_code == 200:
            return resp
        h.wait(h.SHORT_DELAY)
    return resp


def _delete_created_branch(stack, uid):
    # Same retry as TestBranchDelete: a freshly created branch can briefly be "not valid" (422, code 905).
    resp = None
    for _ in range(4):
        branch = stack.branch(uid)
        branch.add_param("force", "true")
        resp = branch.delete()
        if resp.status_code in (200, 204):
            return
        h.wait(h.LONG_DELAY)
    raise AssertionError(f"branch {uid} was not deleted after retries; status {resp.status_code}")


def _not_found(response):
    return response.status_code, h.body(response).get("error_code")


@pytest.fixture(scope="class")
def env_names(stack):
    """Three environments of this class, so a list of two is a strict subset; deleted after."""
    names = [h.generate_valid_uid("bev") for _ in range(3)]
    for name in names:
        data = {"environment": {"name": name, "urls": [{"url": "https://example.com", "locale": "en-us"}]}}
        h.assert_status(stack.environments().create(data), 201)
    yield names
    for name in names:
        stack.environments(name).delete()


@pytest.fixture(scope="class")
def nonexistent(stack):
    """The response for a branch that does not exist (dev11: 422, error_code 905)."""
    resp = stack.branch(h.generate_valid_uid("nob")).fetch()
    assert resp.status_code != 200
    return _not_found(resp)


class TestBranchEnvironmentList:
    """Branch create with publish_config.environments. Each test deletes its branch (stack branch cap)."""

    def test_create_two_names_clones_only_those(self, stack, env_names):
        wanted = env_names[:2]
        uid = h.generate_valid_uid("bev")
        resp = _create_branch(stack, uid, wanted)
        try:
            h.assert_status(resp, 201)
            assert sorted(_branch_environments(resp)) == sorted(wanted)
            fetched = _fetch_when_ready(stack, uid)
            h.assert_status(fetched, 200)
            assert sorted(_branch_environments(fetched)) == sorted(wanted)
            assert env_names[2] not in _branch_environments(fetched)
        finally:
            if resp.status_code == 201:
                _delete_created_branch(stack, uid)

    def test_create_one_name_reads_back_that_one(self, stack, env_names):
        uid = h.generate_valid_uid("bev")
        resp = _create_branch(stack, uid, env_names[:1])
        try:
            h.assert_status(resp, 201)
            fetched = _fetch_when_ready(stack, uid)
            h.assert_status(fetched, 200)
            assert _branch_environments(fetched) == env_names[:1]
        finally:
            if resp.status_code == 201:
                _delete_created_branch(stack, uid)

    def test_create_empty_list_clones_none(self, stack, env_names):
        uid = h.generate_valid_uid("bev")
        resp = _create_branch(stack, uid, [])
        try:
            h.assert_status(resp, 201)
            assert _branch_environments(resp) == []
            fetched = _fetch_when_ready(stack, uid)
            h.assert_status(fetched, 200)
            assert "publish_config" in _branch(fetched)
            assert _branch_environments(fetched) == []
        finally:
            if resp.status_code == 201:
                _delete_created_branch(stack, uid)

    def test_create_without_list_reads_back_no_publish_config(self, stack, env_names):
        uid = h.generate_valid_uid("bev")
        resp = _create_branch(stack, uid)
        try:
            h.assert_status(resp, 201)
            fetched = _fetch_when_ready(stack, uid)
            h.assert_status(fetched, 200)
            assert "publish_config" not in _branch(fetched)
        finally:
            if resp.status_code == 201:
                _delete_created_branch(stack, uid)

    @pytest.mark.parametrize("case", ["unknown", "other_case", "mix"])
    def test_rejected_names_return_422_and_create_no_branch(self, stack, env_names, nonexistent, case):
        environments = {
            "unknown": [h.generate_valid_uid("nos")],
            "other_case": [env_names[0].upper()],
            "mix": [env_names[0], h.generate_valid_uid("nos")],
        }[case]
        uid = h.generate_valid_uid("bev")
        resp = _create_branch(stack, uid, environments)
        fetched = stack.branch(uid).fetch()
        if fetched.status_code == 200:
            _delete_created_branch(stack, uid)
        h.assert_status(resp, 422)
        assert h.body(resp).get("error_message")
        assert "publish_config.environments" in h.body(resp).get("errors", {})
        assert _not_found(fetched) == nonexistent, "a rejected create must leave no branch behind"
