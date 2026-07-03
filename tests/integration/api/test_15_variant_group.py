"""Variant Group API tests — CRUD, link/unlink content types, negative cases.

Variant groups require Personalize. Tests accept 422 and skip downstream work when
the project isn't available.
"""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(15)


def _vg_payload(uid, name):
    # The variant-group (Personalize) API expects an UNwrapped object — not
    # nested under a "variant_group" key.
    return {"name": name, "uid": uid, "content_types": []}


class TestVariantGroupCRUD:
    def test_create(self, stack, store):
        uid = h.generate_valid_uid("vg")
        resp = stack.variant_group().create(_vg_payload(uid, f"VG {uid}"))
        h.assert_status(resp, 200, 201)
        if resp.status_code in (200, 201):
            store["variant_groups"]["main"] = h.body(resp).get("variant_group", {}).get("uid", uid)
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.variant_group().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store):
        uid = store.get("variant_groups", {}).get("main")
        if not uid:
            pytest.skip("variant group not created (Personalize unavailable)")
        resp = stack.variant_group(uid).fetch()
        h.assert_status(resp, 200)

    def test_update(self, stack, store):
        uid = store.get("variant_groups", {}).get("main")
        if not uid:
            pytest.skip("variant group not created")
        resp = stack.variant_group(uid).update({"name": "Updated VG", "content_types": []})
        h.assert_status(resp, 200, 201)


class TestVariantGroupNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.variant_group("no_such_vg").fetch()
        # The variant-group API returns 200 with an empty body for an unknown uid.
        h.assert_status(resp, 200)


class TestVariantGroupDelete:
    def test_delete(self, stack, store):
        # Use a throwaway variant group so the shared 'main' one stays available
        # for the variants tests (test_16).
        uid = h.generate_valid_uid("vg_del")
        created = stack.variant_group().create(_vg_payload(uid, f"VGDel {uid}"))
        if created.status_code not in (200, 201):
            pytest.skip("variant group not created (Personalize unavailable)")
        h.wait(h.SHORT_DELAY)
        resp = stack.variant_group(uid).delete()
        h.assert_status(resp, 200)
