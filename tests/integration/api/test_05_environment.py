"""Environment API tests — CRUD, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(5)


class TestEnvironmentCRUD:
    def test_create(self, stack, store):
        name = h.generate_valid_uid("env")
        data = {"environment": {"name": name, "urls": [{"url": "https://example.com", "locale": "en-us"}]}}
        resp = stack.environments().create(data)
        h.assert_status(resp, 201)
        store["environments"]["main"] = name
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.environments().find()
        h.assert_status(resp, 200)
        h.tracked_assert(h.body(resp).get("environments"), "env list").is_type(list)

    def test_fetch(self, stack, store):
        name = store["environments"]["main"]
        resp = stack.environments(name).fetch()
        h.assert_status(resp, 200)
        h.validate_environment_response(resp)

    def test_update(self, stack, store):
        name = store["environments"]["main"]
        data = {"environment": {"name": name, "urls": [{"url": "https://updated.example.com", "locale": "en-us"}]}}
        resp = stack.environments(name).update(data)
        h.assert_status(resp, 200, 201)


class TestEnvironmentNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.environments("does_not_exist_env").fetch()
        h.assert_status(resp, 404, 422)

    def test_fetch_without_name_raises(self, stack):
        with pytest.raises(Exception):
            stack.environments().fetch()


class TestEnvironmentDelete:
    def test_delete(self, stack):
        name = h.generate_valid_uid("env_del")
        stack.environments().create(
            {"environment": {"name": name, "urls": [{"url": "https://d.example.com", "locale": "en-us"}]}}
        )
        h.wait(h.SHORT_DELAY)
        resp = stack.environments(name).delete()
        h.assert_status(resp, 200)
