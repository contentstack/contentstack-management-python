"""Global Field API tests — CRUD, export, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(11)


def _global_field_payload(uid, title=None):
    return {
        "global_field": {
            "title": title or f"GF {uid}",
            "uid": uid,
            "schema": [
                {
                    "display_name": "Single Line",
                    "uid": "single_line",
                    "data_type": "text",
                    "field_metadata": {"description": "", "default_value": ""},
                    "unique": False,
                    "multiple": False,
                    "mandatory": False,
                }
            ],
        }
    }


class TestGlobalFieldCRUD:
    def test_create(self, stack, store):
        uid = h.generate_valid_uid("gf")
        resp = stack.global_fields().create(_global_field_payload(uid))
        h.assert_status(resp, 201)
        store["global_fields"]["main"] = uid
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.global_fields().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store):
        uid = store["global_fields"]["main"]
        resp = stack.global_fields(uid).fetch()
        h.assert_status(resp, 200)
        h.validate_global_field_response(resp, expected_uid=uid)

    def test_update(self, stack, store):
        uid = store["global_fields"]["main"]
        payload = _global_field_payload(uid, title="Updated GF")
        resp = stack.global_fields(uid).update(payload)
        h.assert_status(resp, 200, 201)

    def test_export(self, stack, store):
        uid = store["global_fields"]["main"]
        resp = stack.global_fields(uid).export()
        h.assert_status(resp, 200)


class TestGlobalFieldNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.global_fields("no_such_gf").fetch()
        h.assert_status(resp, 404, 422)


class TestGlobalFieldDelete:
    @pytest.mark.xfail(reason="the test environment returns 500 on global-field delete even via direct "
                              "force=true; tracked as a known environment/API issue", strict=False)
    def test_delete(self, stack):
        uid = h.generate_valid_uid("gf_del")
        stack.global_fields().create(_global_field_payload(uid))
        h.wait(h.SHORT_DELAY)
        resp = stack.global_fields(uid).delete()
        h.assert_status(resp, 200)
