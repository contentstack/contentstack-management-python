"""
Workflow API tests — CRUD, enable/disable, stage transitions, publish rules,
tasks, and negative cases.

Depends on the `medium` content type from the store (creates one if absent).
Publish-rule operations require an ENABLED workflow, an environment, and a role.
"""

import pytest

from data import content_types as ct_data
from framework import helpers as h

pytestmark = pytest.mark.order(21)


@pytest.fixture(scope="class")
def content_type_uid(stack, store):
    uid = store.get("content_types", {}).get("medium")
    if uid:
        return uid
    uid = h.generate_valid_uid("ct_wf")
    stack.content_types().create(ct_data.medium_content_type(uid))
    h.wait(h.SHORT_DELAY)
    store.setdefault("content_types", {})["medium"] = uid
    return uid


@pytest.fixture(scope="class")
def wf_environment(stack):
    """A dedicated environment; returns its uid (publish rules need the env uid)."""
    name = h.generate_valid_uid("env_wf")
    resp = stack.environments().create(
        {"environment": {"name": name, "urls": [{"url": "https://e.example.com", "locale": "en-us"}]}}
    )
    h.wait(h.SHORT_DELAY)
    return h.body(resp).get("environment", {}).get("uid")


@pytest.fixture(scope="class")
def wf_entry(stack, content_type_uid):
    resp = stack.content_types(content_type_uid).entry().create(
        {"entry": {"title": h.generate_unique_title("WFEntry")}}
    )
    h.wait(h.SHORT_DELAY)
    return h.body(resp).get("entry", {}).get("uid")


@pytest.fixture(scope="class")
def wf_stage_uid(stack, store):
    uid = store.get("workflows", {}).get("main")
    if not uid:
        return None
    wf = h.body(stack.workflows(uid).fetch()).get("workflow", {})
    stages = wf.get("workflow_stages", [])
    return stages[0].get("uid") if stages else None


@pytest.fixture(scope="class")
def a_role_uid(stack):
    roles = h.body(stack.roles().find()).get("roles", [])
    return next((r["uid"] for r in roles), None)


def _workflow_payload(name, ct_uid):
    return {
        "workflow": {
            "name": name,
            "content_types": [ct_uid],
            "branches": ["main"],
            "workflow_stages": [
                {"color": "#2196f3", "name": "Draft", "SYS_ACL": {"roles": {"uids": []}, "users": {"uids": ["$all"]}, "others": {}}, "next_available_stages": ["$all"], "entry_lock": "$none"},
                {"color": "#74ba76", "name": "Review", "SYS_ACL": {"roles": {"uids": []}, "users": {"uids": ["$all"]}, "others": {}}, "next_available_stages": ["$all"], "entry_lock": "$none"},
            ],
        }
    }


def _publish_rule_payload(workflow_uid, ct_uid, env_uid, role_uid, stage_uid):
    return {
        "publishing_rule": {
            "workflow": workflow_uid,
            "actions": ["publish"],
            "branches": ["main"],
            "content_types": [ct_uid],
            "locales": ["en-us"],
            "environment": env_uid,
            "approvers": {"users": [], "roles": [role_uid] if role_uid else []},
            "workflow_stage": stage_uid,
            "disable_approver_publishing": False,
        }
    }


class TestWorkflowCRUD:
    def test_create(self, stack, store, content_type_uid):
        resp = stack.workflows().create(_workflow_payload(h.generate_unique_title("Workflow"), content_type_uid))
        h.assert_status(resp, 201)
        store["workflows"]["main"] = h.body(resp).get("workflow", {}).get("uid")
        h.wait(h.SHORT_DELAY)

    def test_find_all(self, stack):
        resp = stack.workflows().find()
        h.assert_status(resp, 200)

    def test_fetch(self, stack, store):
        uid = store.get("workflows", {}).get("main")
        if not uid:
            pytest.skip("workflow not created")
        resp = stack.workflows(uid).fetch()
        h.assert_status(resp, 200)
        h.validate_workflow_response(resp)

    def test_update(self, stack, store, content_type_uid):
        uid = store.get("workflows", {}).get("main")
        if not uid:
            pytest.skip("workflow not created")
        resp = stack.workflows(uid).update(_workflow_payload("Updated Workflow", content_type_uid))
        h.assert_status(resp, 200, 201)

    # Workflows are created DISABLED — enable so stage/publish-rule ops can run.
    def test_enable(self, stack, store):
        uid = store.get("workflows", {}).get("main")
        if not uid:
            pytest.skip("workflow not created")
        resp = stack.workflows(uid).enable()
        h.assert_status(resp, 200, 201)
        h.wait(h.SHORT_DELAY)


class TestWorkflowStagesAndTasks:
    def test_fetch_tasks(self, stack):
        resp = stack.workflows().fetch_tasks()
        h.assert_status(resp, 200)

    def test_set_workflow_stage(self, stack, store, content_type_uid, wf_entry, wf_stage_uid):
        if not (wf_entry and wf_stage_uid):
            pytest.skip("workflow stage / entry not available")
        data = {"workflow": {"workflow_stage": {"comment": "moving", "uid": wf_stage_uid, "notify": False}}}
        resp = stack.workflows().set_workflow_stage(content_type_uid, wf_entry, data)
        h.assert_status(resp, 200, 201)

    def test_fetch_publish_rules(self, stack):
        resp = stack.workflows().fetch_publish_rules()
        h.assert_status(resp, 200)

    def test_fetch_publish_rule_content_type(self, stack, content_type_uid):
        resp = stack.workflows().fetch_publish_rule_content_type(content_type_uid)
        h.assert_status(resp, 200)


class TestWorkflowPublishRules:
    def test_create_publish_rule(self, stack, store, content_type_uid, wf_environment, a_role_uid, wf_stage_uid):
        wf_uid = store.get("workflows", {}).get("main")
        if not (wf_uid and wf_stage_uid and wf_environment):
            pytest.skip("workflow prerequisites missing")
        resp = stack.workflows().create_publish_rule(
            _publish_rule_payload(wf_uid, content_type_uid, wf_environment, a_role_uid, wf_stage_uid)
        )
        h.assert_status(resp, 200, 201)
        store["workflows"]["rule"] = h.body(resp).get("publishing_rule", {}).get("uid")
        h.wait(h.SHORT_DELAY)

    def test_fetch_publish_rule(self, stack, store):
        rule_uid = store.get("workflows", {}).get("rule")
        if not rule_uid:
            pytest.skip("publish rule not created")
        resp = stack.workflows().fetch_publish_rule(rule_uid)
        h.assert_status(resp, 200)

    def test_update_publish_rule(self, stack, store, content_type_uid, wf_environment, a_role_uid, wf_stage_uid):
        rule_uid = store.get("workflows", {}).get("rule")
        wf_uid = store.get("workflows", {}).get("main")
        if not rule_uid:
            pytest.skip("publish rule not created")
        resp = stack.workflows(rule_uid).update_publish_rule(
            rule_uid, _publish_rule_payload(wf_uid, content_type_uid, wf_environment, a_role_uid, wf_stage_uid)
        )
        h.assert_status(resp, 200, 201)

    def test_delete_publish_rule(self, stack, store):
        rule_uid = store.get("workflows", {}).get("rule")
        if not rule_uid:
            pytest.skip("publish rule not created")
        resp = stack.workflows().delete_publish_rule(rule_uid)
        h.assert_status(resp, 200)

    @pytest.mark.xfail(reason="publish_request_approval returns 401 — the test account "
                              "lacks publish-approval permission on a fresh stack", strict=False)
    def test_publish_request_approval(self, stack, content_type_uid, wf_entry):
        if not wf_entry:
            pytest.skip("entry not available")
        resp = stack.workflows().publish_request_approval(content_type_uid, wf_entry)
        h.assert_status(resp, 200, 201)


class TestWorkflowDisable:
    def test_disable(self, stack, store):
        uid = store.get("workflows", {}).get("main")
        if not uid:
            pytest.skip("workflow not created")
        resp = stack.workflows(uid).disable()
        h.assert_status(resp, 200, 201)


class TestWorkflowNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.workflows("no_such_workflow").fetch()
        h.assert_status(resp, 404, 422)


class TestWorkflowDelete:
    def test_delete(self, stack, store):
        uid = store.get("workflows", {}).get("main")
        if not uid:
            pytest.skip("workflow not created")
        resp = stack.workflows(uid).delete()
        h.assert_status(resp, 200)
