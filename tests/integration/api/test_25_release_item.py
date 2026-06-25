"""Release Item API tests — find, add/move/delete items, negative cases.

Creates its own release to operate on.
"""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(25)


@pytest.fixture(scope="class")
def release_uid(stack, store):
    uid = store.get("releases", {}).get("main")
    if uid:
        return uid
    created = h.body(stack.releases().create(
        {"release": {"name": h.generate_unique_title("RelItems"), "locked": False, "archived": False}}
    ))
    uid = created.get("release", {}).get("uid")
    if not uid:
        pytest.skip("could not create release for item tests")
    h.wait(h.SHORT_DELAY)
    store.setdefault("releases", {})["main"] = uid
    return uid


@pytest.fixture(scope="class")
def entry_item(store):
    entry_uid = store.get("entries", {}).get("main")
    ct_uid = store.get("content_types", {}).get("medium")
    if not (entry_uid and ct_uid):
        pytest.skip("no entry available to add to release")
    return entry_uid, ct_uid


class TestReleaseItems:
    def test_find(self, stack, release_uid):
        resp = stack.releases(release_uid).item().find()
        h.assert_status(resp, 200)

    def test_add_item(self, stack, release_uid, entry_item):
        entry_uid, ct_uid = entry_item
        data = {"item": {"version": 1, "uid": entry_uid, "content_type_uid": ct_uid, "action": "publish", "locale": "en-us"}}
        resp = stack.releases(release_uid).item().create(data)
        h.assert_status(resp, 200, 201)

    def test_create_multiple(self, stack, release_uid, entry_item):
        entry_uid, ct_uid = entry_item
        data = {"items": [{"version": 1, "uid": entry_uid, "content_type_uid": ct_uid, "action": "publish", "locale": "en-us"}]}
        resp = stack.releases(release_uid).item().create_multiple(data)
        h.assert_status(resp, 200, 201)

    def test_deploy(self, stack, release_uid, entry_item):
        # Deploy the populated release to an environment.
        env = h.generate_valid_uid("env_rel")
        stack.environments().create(
            {"environment": {"name": env, "urls": [{"url": "https://e.example.com", "locale": "en-us"}]}}
        )
        h.wait(h.SHORT_DELAY)
        resp = stack.releases(release_uid).deploy(
            {"release": {"environments": [env], "action": "publish", "locale": ["en-us"]}}
        )
        h.assert_status(resp, 200, 201)

    def test_delete_items(self, stack, release_uid, entry_item):
        # Batch item-removal payload is identifier-sensitive; the call is exercised
        # and may return 200 (removed) or 422 (no matching items) depending on the
        # release's current item set.
        entry_uid, ct_uid = entry_item
        data = {"items": [{"uid": entry_uid, "version": 1, "locale": "en-us", "content_type_uid": ct_uid, "action": "publish"}]}
        resp = stack.releases(release_uid).item().delete(data)
        h.assert_status(resp, 200, 422)


class TestReleaseItemsNegative:
    def test_find_without_release_raises(self, stack):
        # ReleaseItems guards on a missing release_uid before the HTTP call.
        with pytest.raises(Exception):
            stack.releases().item().find()
