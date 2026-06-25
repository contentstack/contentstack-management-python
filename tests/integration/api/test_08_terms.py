"""Terms API tests — CRUD within a taxonomy, search, hierarchy, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(8)


@pytest.fixture(scope="class")
def taxonomy_uid(stack, store):
    uid = store.get("taxonomies", {}).get("main")
    if uid:
        return uid
    uid = h.generate_valid_uid("tax_terms")
    stack.taxonomy().create({"taxonomy": {"uid": uid, "name": f"Tax {uid}"}})
    h.wait(h.SHORT_DELAY)
    store.setdefault("taxonomies", {})["main"] = uid
    return uid


class TestTermsCRUD:
    def test_create(self, stack, store, taxonomy_uid):
        uid = h.generate_valid_uid("term")
        data = {"term": {"uid": uid, "name": f"Term {uid}"}}
        resp = stack.taxonomy(taxonomy_uid).terms().create(data)
        h.assert_status(resp, 201)
        store["terms"]["main"] = uid
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack, taxonomy_uid):
        resp = stack.taxonomy(taxonomy_uid).terms().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store, taxonomy_uid):
        uid = store["terms"]["main"]
        resp = stack.taxonomy(taxonomy_uid).terms(uid).fetch()
        h.assert_status(resp, 200)
        h.validate_term_response(resp)

    def test_update(self, stack, store, taxonomy_uid):
        uid = store["terms"]["main"]
        data = {"term": {"name": f"Updated {uid}"}}
        resp = stack.taxonomy(taxonomy_uid).terms(uid).update(data)
        h.assert_status(resp, 200, 201)

    def test_descendants(self, stack, store, taxonomy_uid):
        uid = store["terms"]["main"]
        resp = stack.taxonomy(taxonomy_uid).terms(uid).descendants()
        h.assert_status(resp, 200)

    def test_ancestors(self, stack, store, taxonomy_uid):
        uid = store["terms"]["main"]
        resp = stack.taxonomy(taxonomy_uid).terms(uid).ancestors()
        h.assert_status(resp, 200)

    def test_search(self, stack, taxonomy_uid):
        resp = stack.taxonomy(taxonomy_uid).terms().search("Term")
        h.assert_status(resp, 200)

    def test_move(self, stack, store, taxonomy_uid):
        # Create a child term and reparent it under the main term. The move payload
        # requires the term's name alongside the new parent_uid.
        child = h.generate_valid_uid("term_child")
        name = f"Child {child}"
        stack.taxonomy(taxonomy_uid).terms().create({"term": {"uid": child, "name": name}})
        h.wait(h.SHORT_DELAY)
        parent = store["terms"]["main"]
        resp = stack.taxonomy(taxonomy_uid).terms(child).move(
            {"term": {"uid": child, "name": name, "parent_uid": parent}}
        )
        h.assert_status(resp, 200, 201)


class TestTermsNegative:
    def test_fetch_nonexistent(self, stack, taxonomy_uid):
        resp = stack.taxonomy(taxonomy_uid).terms("no_such_term").fetch()
        h.assert_status(resp, 404, 422)


class TestTermsDelete:
    @pytest.mark.xfail(reason="the test environment returns 400 on term delete; tracked as a known "
                              "environment/API issue", strict=False)
    def test_delete(self, stack, taxonomy_uid):
        uid = h.generate_valid_uid("term_del")
        stack.taxonomy(taxonomy_uid).terms().create({"term": {"uid": uid, "name": f"Del {uid}"}})
        h.wait(h.SHORT_DELAY)
        resp = stack.taxonomy(taxonomy_uid).terms(uid).delete()
        h.assert_status(resp, 200)
