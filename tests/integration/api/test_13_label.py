"""Label API tests — CRUD, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(13)


class TestLabelCRUD:
    def test_create(self, stack, store):
        name = h.generate_unique_title("Label")
        resp = stack.label().create({"label": {"name": name, "content_types": []}})
        h.assert_status(resp, 201)
        store["labels"]["main"] = h.body(resp).get("label", {}).get("uid")
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.label().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store):
        uid = store.get("labels", {}).get("main")
        if not uid:
            pytest.skip("label not created")
        resp = stack.label(uid).fetch()
        h.assert_status(resp, 200)

    def test_update(self, stack, store):
        uid = store.get("labels", {}).get("main")
        if not uid:
            pytest.skip("label not created")
        resp = stack.label(uid).update({"label": {"name": "Updated Label", "content_types": []}})
        h.assert_status(resp, 200, 201)


class TestLabelNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.label("no_such_label").fetch()
        h.assert_status(resp, 404, 422)


class TestLabelDelete:
    def test_delete(self, stack):
        created = h.body(stack.label().create({"label": {"name": h.generate_unique_title("LabelDel"), "content_types": []}}))
        uid = created.get("label", {}).get("uid")
        if not uid:
            pytest.skip("label not created")
        h.wait(h.SHORT_DELAY)
        resp = stack.label(uid).delete()
        h.assert_status(resp, 200)
