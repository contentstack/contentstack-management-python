"""Release API tests — CRUD, clone, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(24)


def _release_payload(name):
    return {"release": {"name": name, "description": "integration test release", "locked": False, "archived": False}}


class TestReleaseCRUD:
    def test_create(self, stack, store):
        name = h.generate_unique_title("Release")
        resp = stack.releases().create(_release_payload(name))
        h.assert_status(resp, 201)
        store["releases"]["main"] = h.body(resp).get("release", {}).get("uid")
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.releases().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store):
        uid = store.get("releases", {}).get("main")
        if not uid:
            pytest.skip("release not created")
        resp = stack.releases(uid).fetch()
        h.assert_status(resp, 200)
        h.validate_release_response(resp)

    def test_update(self, stack, store):
        uid = store.get("releases", {}).get("main")
        if not uid:
            pytest.skip("release not created")
        resp = stack.releases(uid).update({"release": {"name": "Updated Release", "description": "updated"}})
        h.assert_status(resp, 200, 201)

    def test_clone(self, stack, store):
        uid = store.get("releases", {}).get("main")
        if not uid:
            pytest.skip("release not created")
        resp = stack.releases(uid).clone({"release": {"name": h.generate_unique_title("Clone")}})
        h.assert_status(resp, 200, 201)


class TestReleaseNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.releases("no_such_release").fetch()
        h.assert_status(resp, 404, 422)


class TestReleaseDelete:
    def test_delete(self, stack):
        created = h.body(stack.releases().create(_release_payload(h.generate_unique_title("RelDel"))))
        uid = created.get("release", {}).get("uid")
        if not uid:
            pytest.skip("release not created")
        h.wait(h.SHORT_DELAY)
        resp = stack.releases(uid).delete()
        h.assert_status(resp, 200)
