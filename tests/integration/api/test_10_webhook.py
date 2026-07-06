"""Webhook API tests — CRUD, executions, export, logs, retry, negatives."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(10)


def _webhook_payload(name):
    return {
        "webhook": {
            "name": name,
            "destinations": [
                {"target_url": "https://example.com/hook", "http_basic_auth": "", "http_basic_password": "", "custom_header": []}
            ],
            "channels": ["assets.create"],
            "retry_policy": "manual",
            "disabled": False,
        }
    }


class TestWebhookCRUD:
    def test_create(self, stack, store):
        name = h.generate_unique_title("Webhook")
        resp = stack.webhooks().create(_webhook_payload(name))
        h.assert_status(resp, 201)
        store["webhooks"]["main"] = h.body(resp).get("webhook", {}).get("uid")
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.webhooks().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store):
        uid = store.get("webhooks", {}).get("main")
        if not uid:
            pytest.skip("webhook not created")
        resp = stack.webhooks(uid).fetch()
        h.assert_status(resp, 200)
        h.validate_webhook_response(resp)

    def test_update(self, stack, store):
        uid = store.get("webhooks", {}).get("main")
        if not uid:
            pytest.skip("webhook not created")
        resp = stack.webhooks(uid).update(_webhook_payload("Updated Webhook"))
        h.assert_status(resp, 200, 201)

    def test_executions(self, stack, store):
        uid = store.get("webhooks", {}).get("main")
        if not uid:
            pytest.skip("webhook not created")
        resp = stack.webhooks(uid).executions()
        h.assert_status(resp, 200)

    def test_export(self, stack, store):
        uid = store.get("webhooks", {}).get("main")
        if not uid:
            pytest.skip("webhook not created")
        resp = stack.webhooks(uid).export()
        h.assert_status(resp, 200)


class TestWebhookExecutionOps:
    def test_logs_for_unknown_execution(self, stack, store):
        # logs() returns 200 with an empty payload for a webhook with no executions.
        uid = store.get("webhooks", {}).get("main")
        if not uid:
            pytest.skip("webhook not created")
        resp = stack.webhooks(uid).logs("no_such_execution")
        h.assert_status(resp, 200, 404)

    def test_retry_unknown_execution(self, stack, store):
        uid = store.get("webhooks", {}).get("main")
        if not uid:
            pytest.skip("webhook not created")
        resp = stack.webhooks(uid).retry("no_such_execution")
        h.assert_status(resp, 400, 404, 422)


class TestWebhookNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.webhooks("no_such_webhook").fetch()
        h.assert_status(resp, 404, 422)


class TestWebhookDelete:
    def test_delete(self, stack, store):
        name = h.generate_unique_title("WebhookDel")
        created = h.body(stack.webhooks().create(_webhook_payload(name)))
        uid = created.get("webhook", {}).get("uid")
        if not uid:
            pytest.skip("webhook not created")
        h.wait(h.SHORT_DELAY)
        resp = stack.webhooks(uid).delete()
        h.assert_status(resp, 200)
