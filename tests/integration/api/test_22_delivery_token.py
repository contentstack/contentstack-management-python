"""Delivery Token API tests — CRUD, negative cases.

Depends on an environment; consumes the one from the store, else creates one.
"""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(22)


@pytest.fixture(scope="class")
def environment_name(stack, store):
    name = store.get("environments", {}).get("main")
    if name:
        return name
    name = h.generate_valid_uid("env_dt")
    stack.environments().create(
        {"environment": {"name": name, "urls": [{"url": "https://e.example.com", "locale": "en-us"}]}}
    )
    h.wait(h.SHORT_DELAY)
    store.setdefault("environments", {})["main"] = name
    return name


def _token_payload(name, env):
    # Branches-enabled orgs require a branch (or branch_alias) scope entry.
    return {
        "token": {
            "name": name,
            "description": "integration test delivery token",
            "scope": [
                {"module": "environment", "environments": [env], "acl": {"read": True}},
                {"module": "branch", "branches": ["main"], "acl": {"read": True}},
            ],
        }
    }


class TestDeliveryTokenCRUD:
    def test_create(self, stack, store, environment_name):
        name = h.generate_unique_title("DT")
        resp = stack.delivery_token().create(_token_payload(name, environment_name))
        h.assert_status(resp, 201)
        store["delivery_tokens"]["main"] = h.body(resp).get("token", {}).get("uid")
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.delivery_token().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store):
        uid = store.get("delivery_tokens", {}).get("main")
        if not uid:
            pytest.skip("delivery token not created")
        resp = stack.delivery_token(uid).fetch()
        h.assert_status(resp, 200)

    def test_update(self, stack, store, environment_name):
        uid = store.get("delivery_tokens", {}).get("main")
        if not uid:
            pytest.skip("delivery token not created")
        resp = stack.delivery_token(uid).update(_token_payload("Updated DT", environment_name))
        h.assert_status(resp, 200, 201)


class TestDeliveryTokenNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.delivery_token("no_such_dt").fetch()
        h.assert_status(resp, 404, 422)


class TestDeliveryTokenDelete:
    def test_delete(self, stack, store):
        uid = store.get("delivery_tokens", {}).get("main")
        if not uid:
            pytest.skip("delivery token not created")
        resp = stack.delivery_token(uid).delete()
        h.assert_status(resp, 200)
