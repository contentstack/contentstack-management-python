"""Locale API tests — CRUD, fallback, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(4)

# A non-master locale code to create/manipulate.
_CODE = "fr-fr"


class TestLocaleCRUD:
    def test_create(self, stack, store):
        data = {"locale": {"name": "French", "code": _CODE}}
        resp = stack.locale().create(data)
        h.assert_status(resp, 201)
        store["locales"]["custom"] = _CODE
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.locale().find()
        h.assert_status(resp, 200)
        h.tracked_assert(h.body(resp).get("locales"), "locales list").is_type(list)

    def test_fetch(self, stack):
        resp = stack.locale(_CODE).fetch()
        h.assert_status(resp, 200)
        h.validate_locale_response(resp)

    def test_update(self, stack):
        data = {"locale": {"name": "French (FR)"}}
        resp = stack.locale(_CODE).update(data)
        h.assert_status(resp, 200, 201)

    def test_set_fallback(self, stack):
        data = {"locale": {"name": "German", "code": "de-de", "fallback_locale": "en-us"}}
        resp = stack.locale().set_fallback(data)
        h.assert_status(resp, 200, 201)

    def test_update_fallback(self, stack):
        # Ensure de-de exists, then update its fallback configuration.
        stack.locale().create({"locale": {"name": "German", "code": "de-de"}})
        h.wait(h.SHORT_DELAY)
        data = {"locale": {"name": "German", "code": "de-de", "fallback_locale": "en-us"}}
        resp = stack.locale("de-de").update_fallback(data)
        h.assert_status(resp, 200, 201)


class TestLocaleNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.locale("zz-zz").fetch()
        h.assert_status(resp, 404, 422)

    def test_fetch_without_code_raises(self, stack):
        # Locale guards on a missing locale_code before the HTTP call.
        with pytest.raises(Exception):
            stack.locale().fetch()


class TestLocaleDelete:
    def test_delete(self, stack):
        resp = stack.locale("de-de").delete()
        h.assert_status(resp, 200)
