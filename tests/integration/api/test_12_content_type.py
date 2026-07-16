"""
Content Type API tests — full CRUD plus complex-schema round-trip validation.

Creates the full family of schemas ported from the JS sanity suite (simple, medium,
complex with modular blocks/groups/JSON RTE, author, article with references,
singleton) and verifies the SDK round-trips every field type. Created UIDs are
stashed in `store["content_types"]` for the entry tests (test_14).

Reference ordering matters: `author` is created before `article`, which references it.
"""

import pytest

from data import content_types as ct_data
from framework import helpers as h

pytestmark = pytest.mark.order(12)


class TestContentTypeCRUD:
    def test_create_simple(self, stack, store):
        resp = stack.content_types().create(ct_data.simple_content_type())
        h.assert_status(resp, 201)
        data = h.validate_content_type_response(resp, expected_uid="simple_test")
        h.tracked_assert(data["uid"], "created uid").equals("simple_test")
        store["content_types"]["simple"] = "simple_test"

    def test_fetch(self, stack, store):
        resp = stack.content_types("simple_test").fetch()
        h.assert_status(resp, 200)
        h.validate_content_type_response(resp, expected_uid="simple_test")

    def test_find_all(self, stack):
        resp = stack.content_types().find()
        h.assert_status(resp, 200)
        h.tracked_assert(h.body(resp).get("content_types"), "content_types list").is_type(list)

    def test_find_with_pagination(self, stack):
        query = stack.content_types()
        query.add_param("limit", 1)
        query.add_param("skip", 0)
        resp = query.find()
        h.assert_status(resp, 200)
        h.tracked_assert(len(h.body(resp).get("content_types", [])) <= 1, "limit respected").equals(True)

    def test_update(self, stack):
        current = h.body(stack.content_types("simple_test").fetch())["content_type"]
        current["title"] = h.generate_unique_title("Updated Simple")
        resp = stack.content_types("simple_test").update({"content_type": current})
        h.assert_status(resp, 200)
        h.tracked_assert(h.body(resp)["content_type"]["title"], "updated title").equals(current["title"])

    def test_references(self, stack):
        resp = stack.content_types("simple_test").references()
        h.assert_status(resp, 200)

    def test_export(self, stack):
        resp = stack.content_types("simple_test").export()
        h.assert_status(resp, 200)


class TestComplexSchemas:
    """Create every field type and confirm the SDK round-trips the full schema."""

    def test_create_medium(self, stack, store):
        resp = stack.content_types().create(ct_data.medium_content_type())
        h.assert_status(resp, 201)
        ct = h.validate_content_type_response(resp, expected_uid="medium_complexity")
        types = {f["data_type"] for f in ct["schema"]}
        # isodate, file, link, number, boolean, text all present
        for expected in ("text", "number", "boolean", "isodate", "file", "link"):
            h.tracked_assert(expected in types, f"medium has {expected} field").equals(True)
        store["content_types"]["medium"] = "medium_complexity"
        h.wait(h.SHORT_DELAY)

    def test_create_complex_with_blocks(self, stack, store):
        resp = stack.content_types().create(ct_data.complex_content_type())
        h.assert_status(resp, 201)
        ct = h.validate_content_type_response(resp, expected_uid="complex_page")
        sections = next((f for f in ct["schema"] if f["uid"] == "sections"), None)
        h.tracked_assert(sections and sections["data_type"], "sections field type").equals("blocks")
        block_uids = {b["uid"] for b in (sections or {}).get("blocks", [])}
        for b in ("hero_section", "content_block", "card_grid", "accordion"):
            h.tracked_assert(b in block_uids, f"block {b} round-tripped").equals(True)
        # group field present
        h.tracked_assert(any(f["data_type"] == "group" for f in ct["schema"]), "has group field").equals(True)
        store["content_types"]["complex"] = "complex_page"
        h.wait(h.SHORT_DELAY)

    def test_create_author(self, stack, store):
        resp = stack.content_types().create(ct_data.author_content_type())
        h.assert_status(resp, 201)
        h.validate_content_type_response(resp, expected_uid="author")
        store["content_types"]["author"] = "author"
        h.wait(h.SHORT_DELAY)

    def test_create_article_with_references(self, stack, store):
        # 'author' must already exist (created above) for the reference to resolve.
        resp = stack.content_types().create(ct_data.article_content_type())
        h.assert_status(resp, 201)
        ct = h.validate_content_type_response(resp, expected_uid="article")
        refs = [f for f in ct["schema"] if f["data_type"] == "reference"]
        h.tracked_assert(len(refs) >= 2, "article has reference fields").equals(True)
        store["content_types"]["article"] = "article"
        h.wait(h.SHORT_DELAY)

    def test_create_singleton(self, stack, store):
        resp = stack.content_types().create(ct_data.singleton_content_type())
        h.assert_status(resp, 201)
        ct = h.validate_content_type_response(resp, expected_uid="site_settings")
        h.tracked_assert(ct.get("options", {}).get("singleton"), "singleton flag").equals(True)
        store["content_types"]["singleton"] = "site_settings"


class TestContentTypeSchemaOps:
    def test_add_field_to_schema(self, stack):
        ct = h.body(stack.content_types("simple_test").fetch())["content_type"]
        ct["schema"].append(ct_data.schema_update_add_field())
        resp = stack.content_types("simple_test").update({"content_type": ct})
        h.assert_status(resp, 200)
        updated = h.body(resp)["content_type"]
        h.tracked_assert(
            any(f["uid"] == "new_field" for f in updated["schema"]), "new_field added"
        ).equals(True)

    def test_set_field_visibility_rules(self, stack):
        # Create a dedicated CT with two extra text fields, then add a field rule
        # that shows 'ml' when 'sl' equals a value.
        uid = h.generate_valid_uid("ct_fvr")
        schema = [
            {"display_name": "Title", "uid": "title", "data_type": "text",
             "field_metadata": {"_default": True}, "mandatory": True, "unique": True, "multiple": False},
            {"display_name": "SL", "uid": "sl", "data_type": "text",
             "field_metadata": {"_default": True}, "multiple": False},
            {"display_name": "ML", "uid": "ml", "data_type": "text",
             "field_metadata": {"_default": True}, "multiple": False},
        ]
        stack.content_types().create({"content_type": {"title": "FVR", "uid": uid, "schema": schema}})
        h.wait(h.SHORT_DELAY)
        payload = {"content_type": {
            "title": "FVR", "uid": uid, "schema": schema,
            "field_rules": [{
                "conditions": [{"operand_field": "sl", "operator": "equals", "value": "x"}],
                "match_type": "all",
                "actions": [{"action": "show", "target_field": "ml"}],
            }],
        }}
        resp = stack.content_types(uid).set_field_visibility_rules(payload)
        h.assert_status(resp, 200, 201)


class TestContentTypeNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.content_types("does_not_exist_xyz").fetch()
        h.assert_status(resp, 404, 422)
        h.validate_error_body(resp)

    def test_create_duplicate_uid(self, stack):
        resp = stack.content_types().create(ct_data.simple_content_type())  # simple_test already exists
        h.assert_status(resp, 409, 422)
        h.validate_error_body(resp)

    def test_create_missing_title_field(self, stack):
        uid = h.generate_valid_uid("ct_bad")
        resp = stack.content_types().create(ct_data.invalid_content_type_missing_title(uid))
        h.assert_status(resp, 400, 422)
        h.validate_error_body(resp)

    def test_update_without_uid_raises(self, stack):
        with pytest.raises(Exception):
            stack.content_types().update({"content_type": {"title": "x"}})


class TestContentTypeDelete:
    def test_delete(self, stack):
        uid = h.generate_valid_uid("ct_del")
        stack.content_types().create(ct_data.simple_content_type(uid=uid, title="Temp Delete"))
        h.wait(h.SHORT_DELAY)
        resp = stack.content_types(uid).delete()
        h.assert_status(resp, 200)

    def test_fetch_after_delete_is_404(self, stack):
        uid = h.generate_valid_uid("ct_del2")
        stack.content_types().create(ct_data.simple_content_type(uid=uid, title="Temp 404"))
        h.wait(h.SHORT_DELAY)
        stack.content_types(uid).delete()
        h.wait(h.SHORT_DELAY)
        resp = stack.content_types(uid).fetch()
        h.assert_status(resp, 404, 422)
