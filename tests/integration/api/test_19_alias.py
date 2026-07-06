"""Branch Alias API tests — assign, find, fetch, delete, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(19)


class TestAliasCRUD:
    def test_assign(self, stack, store):
        alias_uid = h.generate_valid_uid("alias")
        resp = stack.alias(alias_uid).assign({"branch_alias": {"target_branch": "main"}})
        h.assert_status(resp, 200, 201)
        store["aliases"]["main"] = alias_uid
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.alias().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store):
        uid = store.get("aliases", {}).get("main")
        if not uid:
            pytest.skip("alias not created")
        resp = stack.alias(uid).fetch()
        h.assert_status(resp, 200)


class TestAliasNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.alias("no_such_alias").fetch()
        h.assert_status(resp, 404, 422)


class TestAliasDelete:
    def test_delete(self, stack, store):
        uid = store.get("aliases", {}).get("main")
        if not uid:
            pytest.skip("alias not created")
        # Branch-alias delete requires force=true (otherwise a 422 confirmation prompt).
        alias = stack.alias(uid)
        alias.add_param("force", "true")
        resp = alias.delete()
        h.assert_status(resp, 200)
