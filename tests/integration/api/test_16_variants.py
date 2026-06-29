"""Variants API tests — CRUD within a variant group, negative cases.

Requires Personalize + an existing variant group; skips gracefully otherwise.
"""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(16)


@pytest.fixture(scope="class")
def variant_group_uid(store):
    uid = store.get("variant_groups", {}).get("main")
    if not uid:
        pytest.skip("no variant group available (Personalize unavailable)")
    return uid


class TestVariants:
    def test_create(self, stack, store, variant_group_uid):
        uid = h.generate_valid_uid("var")
        # Personalize variants expect an unwrapped object (like variant groups).
        data = {"name": f"Variant {uid}", "uid": uid}
        resp = stack.variant_group(variant_group_uid).variants().create(data)
        h.assert_status(resp, 200, 201)
        # The API assigns its own server-side uid and returns it UNWRAPPED at the
        # top level (not under a "variant" key, and not the uid we sent).
        body = h.body(resp)
        store["variants"]["main"] = body.get("uid") or body.get("variant", {}).get("uid")

    def test_find(self, stack, variant_group_uid):
        resp = stack.variant_group(variant_group_uid).variants().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store, variant_group_uid):
        uid = store.get("variants", {}).get("main")
        if not uid:
            pytest.skip("variant not created")
        resp = stack.variant_group(variant_group_uid).variants(uid).fetch()
        h.assert_status(resp, 200)


class TestVariantsNegative:
    def test_fetch_nonexistent(self, stack, variant_group_uid):
        resp = stack.variant_group(variant_group_uid).variants("no_such_var").fetch()
        # The variants API returns 412 (precondition failed, code 1010) for an
        # unknown variant rather than 404.
        h.assert_status(resp, 404, 412, 422)
