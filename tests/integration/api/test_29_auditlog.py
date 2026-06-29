"""Audit Log API tests — find, fetch, negative cases."""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(29)


class TestAuditLog:
    def test_find_all(self, stack):
        resp = stack.auditlog().find()
        h.assert_status(resp, 200)

    def test_fetch_first_if_any(self, stack):
        logs = h.body(stack.auditlog().find()).get("logs", [])
        if not logs:
            pytest.skip("no audit log items")
        uid = logs[0].get("uid")
        resp = stack.auditlog(uid).fetch()
        h.assert_status(resp, 200)


class TestAuditLogNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.auditlog("no_such_log").fetch()
        h.assert_status(resp, 404, 422)
