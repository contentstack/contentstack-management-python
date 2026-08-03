"""Taxonomy API tests — CRUD, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(7)


class TestTaxonomyCRUD:
    def test_create(self, stack, store):
        uid = h.generate_valid_uid("tax")
        data = {"taxonomy": {"uid": uid, "name": f"Taxonomy {uid}", "description": "test"}}
        resp = stack.taxonomy().create(data)
        h.assert_status(resp, 201)
        store["taxonomies"]["main"] = uid
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.taxonomy().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store):
        uid = store["taxonomies"]["main"]
        resp = stack.taxonomy(uid).fetch()
        h.assert_status(resp, 200)
        h.validate_taxonomy_response(resp)

    def test_update(self, stack, store):
        uid = store["taxonomies"]["main"]
        data = {"taxonomy": {"name": f"Updated {uid}"}}
        resp = stack.taxonomy(uid).update(data)
        h.assert_status(resp, 200, 201)


class TestTaxonomyNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.taxonomy("does_not_exist_tax").fetch()
        h.assert_status(resp, 404, 422)


class TestTaxonomyLocalize:
    def test_localize(self, stack, store):
        """Localize a taxonomy into a non-master locale."""
        uid = store["taxonomies"]["main"]
        locale = store["locales"].get("custom", "fr-fr")
        data = {"taxonomy": {"name": f"Taxonomy {locale}"}}
        resp = stack.taxonomy(uid).localize(data, locale)
        h.assert_status(resp, 200, 201)
        h.wait(h.SHORT_DELAY)

    def test_unlocalize(self, stack, store):
        """Remove the non-master locale variant."""
        uid = store["taxonomies"]["main"]
        locale = store["locales"].get("custom", "fr-fr")
        stack.client.headers.pop("Content-Type", None)
        resp = stack.taxonomy(uid).unlocalize(locale)
        h.assert_status(resp, 200, 204)


class TestTaxonomyPublish:
    def test_publish(self, stack, store):
        """Publish a taxonomy (requires taxonomy_publish feature flag on the stack)."""
        uid = store["taxonomies"]["main"]
        env = store["environments"].get("main")
        locale = store["locales"].get("custom", "fr-fr")
        if not env:
            pytest.skip("No environment in store — skipping publish test")
        data = {"locales": [locale], "environments": [env], "items": [{"uid": uid}]}
        resp = stack.taxonomy().publish(data)
        if resp.status_code == 403:
            pytest.skip("taxonomy_publish feature not enabled on this stack")
        h.assert_status(resp, 200, 201, 202)
        h.wait(h.SHORT_DELAY)

    def test_unpublish(self, stack, store):
        """Unpublish a taxonomy (requires taxonomy_publish feature flag on the stack)."""
        uid = store["taxonomies"]["main"]
        env = store["environments"].get("main")
        locale = store["locales"].get("custom", "fr-fr")
        if not env:
            pytest.skip("No environment in store — skipping unpublish test")
        data = {"locales": [locale], "environments": [env], "items": [{"uid": uid}]}
        resp = stack.taxonomy().unpublish(data)
        if resp.status_code == 403:
            pytest.skip("taxonomy_publish feature not enabled on this stack")
        h.assert_status(resp, 200, 201, 202)


class TestTaxonomyDelete:
    def test_delete(self, stack):
        uid = h.generate_valid_uid("tax_del")
        stack.taxonomy().create({"taxonomy": {"uid": uid, "name": f"Del {uid}"}})
        h.wait(h.SHORT_DELAY)
        # The CMA API rejects a body-less DELETE that carries Content-Type:
        # application/json (the Python SDK merges it by default; the JS SDK/axios
        # omits it). Drop it before the call so the delete succeeds (204).
        stack.client.headers.pop("Content-Type", None)
        resp = stack.taxonomy(uid).delete()
        h.assert_status(resp, 200, 204)
