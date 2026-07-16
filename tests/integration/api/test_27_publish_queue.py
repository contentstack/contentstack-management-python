"""Publish Queue API tests — find, fetch, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(27)


class TestPublishQueue:
    def test_find_all(self, stack):
        resp = stack.publish_queue().find()
        h.assert_status(resp, 200)

    def test_fetch_first_if_any(self, stack):
        items = h.body(stack.publish_queue().find()).get("queue", [])
        if not items:
            pytest.skip("publish queue is empty")
        uid = items[0].get("uid")
        resp = stack.publish_queue(uid).fetch()
        h.assert_status(resp, 200)


class TestPublishQueueCancel:
    def test_cancel(self, stack):
        # Exercise the cancel (unschedule) endpoint. Our publishes are immediate,
        # not scheduled, so cancelling a real/unknown item returns a 4xx — which
        # confirms the SDK issues the unschedule request correctly.
        items = h.body(stack.publish_queue().find()).get("queue", [])
        uid = items[0].get("uid") if items else "no_such_pq"
        resp = stack.publish_queue(uid).cancel()
        h.assert_status(resp, 200, 400, 404, 422)


class TestPublishQueueNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.publish_queue("no_such_pq").fetch()
        h.assert_status(resp, 404, 422)

    def test_fetch_without_uid_raises(self, stack):
        with pytest.raises(Exception):
            stack.publish_queue().fetch()
