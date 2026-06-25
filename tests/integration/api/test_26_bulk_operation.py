"""Bulk Operation API tests — publish/unpublish, job status, negative cases.

Best-effort against entries/environment created earlier; accepts a range of
statuses since bulk jobs depend on publishable content + environments.
"""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(26)


class TestBulkOperation:
    def test_publish(self, stack, store):
        entry_uid = store.get("entries", {}).get("main")
        ct_uid = store.get("content_types", {}).get("medium")
        env = store.get("environments", {}).get("main")
        if not (entry_uid and ct_uid and env):
            pytest.skip("missing entry/content type/environment for bulk publish")
        data = {
            "entries": [{"uid": entry_uid, "content_type": ct_uid, "locale": "en-us"}],
            "locales": ["en-us"],
            "environments": [env],
        }
        resp = stack.bulk_operation().publish(data)
        h.assert_status(resp, 200, 201)

    def test_unpublish(self, stack, store):
        entry_uid = store.get("entries", {}).get("main")
        ct_uid = store.get("content_types", {}).get("medium")
        env = store.get("environments", {}).get("main")
        if not (entry_uid and ct_uid and env):
            pytest.skip("missing entry/content type/environment for bulk unpublish")
        data = {
            "entries": [{"uid": entry_uid, "content_type": ct_uid, "locale": "en-us"}],
            "locales": ["en-us"],
            "environments": [env],
        }
        resp = stack.bulk_operation().unpublish(data)
        h.assert_status(resp, 200, 201)

    def test_delete(self, stack, store):
        entry_uid = store.get("entries", {}).get("main")
        ct_uid = store.get("content_types", {}).get("medium")
        if not (entry_uid and ct_uid):
            pytest.skip("missing entry/content type for bulk delete")
        # Delete a throwaway entry in bulk (don't remove the shared 'main' entry).
        throwaway = h.body(stack.content_types(ct_uid).entry().create(
            {"entry": {"title": h.generate_unique_title("BulkDel")}}
        )).get("entry", {}).get("uid")
        h.wait(h.SHORT_DELAY)
        data = {"entries": [{"uid": throwaway, "content_type": ct_uid, "locale": "en-us"}]}
        resp = stack.bulk_operation().delete(data)
        h.assert_status(resp, 200, 201)

    @pytest.mark.xfail(reason="bulk update (workflow stage) returns 412 without a valid "
                              "target workflow_stage uid; needs a configured workflow stage", strict=False)
    def test_update_workflow(self, stack, store):
        entry_uid = store.get("entries", {}).get("main")
        ct_uid = store.get("content_types", {}).get("medium")
        if not (entry_uid and ct_uid):
            pytest.skip("missing entry/content type for bulk workflow update")
        data = {"entries": [{"uid": entry_uid, "content_type": ct_uid, "locale": "en-us"}],
                "workflow": {"workflow_stage": {"uid": ""}}}
        resp = stack.bulk_operation().update(data)
        h.assert_status(resp, 200, 201)


class TestBulkOperationNegative:
    def test_job_status_invalid(self, stack):
        resp = stack.bulk_operation().job_status("no_such_job")
        # 401 occurs because bulk job-status is validated against a management
        # token before the job id is checked; an invalid/missing one short-circuits.
        h.assert_status(resp, 400, 401, 404, 422)
