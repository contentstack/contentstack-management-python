"""Extension API tests — create (custom field), upload (HTML widget), CRUD, negatives."""

import os

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(9)

_EXT_HTML = os.path.join(os.path.dirname(__file__), "..", "data", "assets", "extension.html")


def _custom_field_payload(title):
    return {
        "extension": {
            "tags": ["tag1"],
            "data_type": "text",
            "title": title,
            "src": "https://example.com/widget",
            "multiple": False,
            "config": "{}",
            "type": "field",
        }
    }


class TestExtensionCRUD:
    def test_create(self, stack, store):
        title = h.generate_unique_title("Ext")
        resp = stack.extension().create(_custom_field_payload(title))
        h.assert_status(resp, 201)
        uid = h.body(resp).get("extension", {}).get("uid")
        store["extensions"]["main"] = uid

    def test_find_all(self, stack):
        resp = stack.extension().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store):
        uid = store.get("extensions", {}).get("main")
        if not uid:
            pytest.skip("extension was not created")
        resp = stack.extension(uid).fetch()
        h.assert_status(resp, 200)

    def test_update(self, stack, store):
        uid = store.get("extensions", {}).get("main")
        if not uid:
            pytest.skip("extension was not created")
        resp = stack.extension(uid).update(_custom_field_payload("Updated Ext"))
        h.assert_status(resp, 200, 201)

    def test_upload(self, stack):
        # Upload an HTML widget extension (multipart upload).
        resp = stack.extension().upload({
            "file_name": _EXT_HTML,
            "data_type": "text",
            "title": h.generate_unique_title("UploadExt"),
            "multiple": False,
            "tags": {},
            "type": "field",
        })
        h.assert_status(resp, 200, 201)


class TestExtensionNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.extension("no_such_ext").fetch()
        h.assert_status(resp, 404, 422)

    def test_fetch_without_uid_raises(self, stack):
        with pytest.raises(Exception):
            stack.extension().fetch()


class TestExtensionDelete:
    def test_delete(self, stack, store):
        uid = store.get("extensions", {}).get("main")
        if not uid:
            pytest.skip("extension was not created")
        resp = stack.extension(uid).delete()
        h.assert_status(resp, 200)
