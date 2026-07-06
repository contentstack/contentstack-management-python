"""Metadata API tests — find, create against an entry, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(28)


def _create_extension(stack):
    """Create a field extension; metadata requires a valid extension_uid."""
    resp = stack.extension().create({
        "extension": {
            "tags": ["meta"], "data_type": "text", "title": h.generate_unique_title("MetaExt"),
            "src": "https://example.com/ext", "multiple": False, "config": "{}", "type": "field",
        }
    })
    return h.body(resp).get("extension", {}).get("uid")


@pytest.fixture(scope="class")
def environment_name(stack, store):
    name = store.get("environments", {}).get("main")
    if name:
        return name
    name = h.generate_valid_uid("env_meta")
    stack.environments().create(
        {"environment": {"name": name, "urls": [{"url": "https://e.example.com", "locale": "en-us"}]}}
    )
    h.wait(h.SHORT_DELAY)
    store.setdefault("environments", {})["main"] = name
    return name


def _metadata_payload(entry_uid, ct_uid, extension_uid):
    return {"metadata": {"entity_uid": entry_uid, "type": "entry", "extension_uid": extension_uid,
                         "_content_type_uid": ct_uid, "presets": [{"uid": h.short_id(), "name": "preset", "options": {}}]}}


class TestMetadata:
    def test_find_all(self, stack):
        resp = stack.metadata().find()
        h.assert_status(resp, 200)

    def test_create(self, stack, store):
        entry_uid = store.get("entries", {}).get("main")
        ct_uid = store.get("content_types", {}).get("medium")
        if not (entry_uid and ct_uid):
            pytest.skip("no entry available for metadata")
        extension_uid = _create_extension(stack)
        h.tracked_assert(extension_uid, "extension created for metadata").truthy()
        h.wait(h.SHORT_DELAY)
        data = {
            "metadata": {
                "entity_uid": entry_uid,
                "type": "entry",
                "extension_uid": extension_uid,
                "_content_type_uid": ct_uid,
                "presets": [{"uid": h.short_id(), "name": "preset", "options": {}}],
            }
        }
        resp = stack.metadata().create(data)
        h.assert_status(resp, 201)
        uid = h.body(resp).get("metadata", {}).get("uid")
        h.tracked_assert(uid, "metadata uid").truthy()
        store["metadata"] = {"main": uid, "entry": entry_uid, "ct": ct_uid, "ext": extension_uid}

    def test_fetch(self, stack, store):
        uid = store.get("metadata", {}).get("main")
        if not uid:
            pytest.skip("metadata not created")
        resp = stack.metadata(uid).fetch()
        h.assert_status(resp, 200)

    def test_update(self, stack, store):
        meta = store.get("metadata", {})
        if not meta.get("main"):
            pytest.skip("metadata not created")
        resp = stack.metadata(meta["main"]).update(
            _metadata_payload(meta["entry"], meta["ct"], meta["ext"])
        )
        h.assert_status(resp, 200, 201)

    def test_publish(self, stack, store, environment_name):
        meta = store.get("metadata", {})
        if not meta.get("main"):
            pytest.skip("metadata not created")
        resp = stack.metadata(meta["main"]).publish(
            {"metadata": {"environments": [environment_name], "locales": ["en-us"]}}
        )
        h.assert_status(resp, 200, 201)
        h.wait(h.SHORT_DELAY)

    def test_unpublish(self, stack, store, environment_name):
        meta = store.get("metadata", {})
        if not meta.get("main"):
            pytest.skip("metadata not created")
        resp = stack.metadata(meta["main"]).unpublish(
            {"metadata": {"environments": [environment_name], "locales": ["en-us"]}}
        )
        h.assert_status(resp, 200, 201)


class TestMetadataDelete:
    def test_delete(self, stack, store):
        meta = store.get("metadata", {})
        if not meta.get("main"):
            pytest.skip("metadata not created")
        resp = stack.metadata(meta["main"]).delete()
        h.assert_status(resp, 200)


class TestMetadataNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.metadata("no_such_metadata").fetch()
        h.assert_status(resp, 404, 422)

    def test_fetch_without_uid_raises(self, stack):
        with pytest.raises(Exception):
            stack.metadata().fetch()
