"""
Entry API tests — CRUD plus complex field round-trip, references, atomic operations,
localization, and version naming.

Consumes content types created by test_12 (medium/complex/author/article) via `store`,
creating fallbacks if run in isolation.
"""

import pytest

from data import content_types as ct_data
from data import entries as entry_data
from framework import helpers as h

pytestmark = pytest.mark.order(14)


def _ensure_ct(stack, store, key, factory, uid):
    existing = store.get("content_types", {}).get(key)
    if existing:
        return existing
    stack.content_types().create(factory())
    h.wait(h.SHORT_DELAY)
    store.setdefault("content_types", {})[key] = uid
    return uid


@pytest.fixture(scope="class")
def medium_ct(stack, store):
    return _ensure_ct(stack, store, "medium", ct_data.medium_content_type, "medium_complexity")


@pytest.fixture(scope="class")
def author_ct(stack, store):
    return _ensure_ct(stack, store, "author", ct_data.author_content_type, "author")


@pytest.fixture(scope="class")
def article_ct(stack, store):
    _ensure_ct(stack, store, "author", ct_data.author_content_type, "author")
    return _ensure_ct(stack, store, "article", ct_data.article_content_type, "article")


@pytest.fixture(scope="class")
def environment_name(stack, store):
    name = store.get("environments", {}).get("main")
    if name:
        return name
    name = h.generate_valid_uid("env_entry")
    stack.environments().create(
        {"environment": {"name": name, "urls": [{"url": "https://e.example.com", "locale": "en-us"}]}}
    )
    h.wait(h.SHORT_DELAY)
    store.setdefault("environments", {})["main"] = name
    return name


class TestEntryCRUD:
    def test_create(self, stack, store, medium_ct):
        resp = stack.content_types(medium_ct).entry().create(
            entry_data.medium_entry(h.generate_unique_title("Entry"))
        )
        h.assert_status(resp, 201)
        data = h.validate_entry_response(resp, medium_ct)
        # Round-trip check of populated field types.
        h.tracked_assert(data.get("view_count"), "number field round-trip").equals(1250)
        h.tracked_assert(data.get("is_featured"), "boolean field round-trip").equals(True)
        h.tracked_assert(data.get("categories"), "checkbox multi round-trip").is_type(list)
        store["entries"]["main"] = data["uid"]
        h.wait(h.SHORT_DELAY)

    def test_fetch(self, stack, store, medium_ct):
        resp = stack.content_types(medium_ct).entry(store["entries"]["main"]).fetch()
        h.assert_status(resp, 200)
        h.validate_entry_response(resp, medium_ct)

    def test_find_all(self, stack, medium_ct):
        resp = stack.content_types(medium_ct).entry().find()
        h.assert_status(resp, 200)
        h.tracked_assert(h.body(resp).get("entries"), "entries list").is_type(list)

    def test_find_with_pagination(self, stack, medium_ct):
        query = stack.content_types(medium_ct).entry()
        query.add_param("limit", 1)
        resp = query.find()
        h.assert_status(resp, 200)
        h.tracked_assert(len(h.body(resp).get("entries", [])) <= 1, "limit").equals(True)

    def test_update(self, stack, store, medium_ct):
        entry_uid = store["entries"]["main"]
        current = h.body(stack.content_types(medium_ct).entry(entry_uid).fetch())["entry"]
        current["summary"] = "updated summary"
        resp = stack.content_types(medium_ct).entry(entry_uid).update({"entry": current})
        h.assert_status(resp, 200, 201)

    def test_references(self, stack, store, medium_ct):
        resp = stack.content_types(medium_ct).entry(store["entries"]["main"]).references()
        h.assert_status(resp, 200)

    def test_languages(self, stack, store, medium_ct):
        resp = stack.content_types(medium_ct).entry(store["entries"]["main"]).languages()
        h.assert_status(resp, 200)


class TestComplexEntries:
    def test_create_complex_entry(self, stack, store):
        ct = _ensure_ct(stack, store, "complex", ct_data.complex_content_type, "complex_page")
        resp = stack.content_types(ct).entry().create(entry_data.complex_entry())
        h.assert_status(resp, 201)
        data = h.validate_entry_response(resp, ct)
        # Modular blocks + group round-trip.
        h.tracked_assert(data.get("sections"), "modular blocks round-trip").is_type(list)
        h.tracked_assert(data.get("seo", {}).get("meta_title"), "group field round-trip").truthy()
        store["entries"]["complex"] = data["uid"]
        h.wait(h.SHORT_DELAY)

    def test_create_author_entry(self, stack, store, author_ct):
        resp = stack.content_types(author_ct).entry().create(entry_data.author_entry("John Doe"))
        h.assert_status(resp, 201)
        data = h.validate_entry_response(resp, author_ct)
        store["entries"]["author"] = data["uid"]
        h.wait(h.SHORT_DELAY)

    def test_create_article_entry(self, stack, store, article_ct):
        resp = stack.content_types(article_ct).entry().create(entry_data.article_entry())
        h.assert_status(resp, 201)
        data = h.validate_entry_response(resp, article_ct)
        store["entries"]["article"] = data["uid"]
        h.wait(h.SHORT_DELAY)

    def test_create_article_with_reference(self, stack, store, article_ct):
        # Wire the article -> author single reference using the created author entry.
        author_uid = store.get("entries", {}).get("author")
        if not author_uid:
            pytest.skip("author entry not available for reference")
        resp = stack.content_types(article_ct).entry().create(
            entry_data.article_entry_with_references(author_uid=author_uid)
        )
        h.assert_status(resp, 201)
        data = h.validate_entry_response(resp, article_ct)
        h.tracked_assert(data.get("author"), "reference field round-trip").truthy()


class TestEntryAtomicOps:
    """Atomic field operations (PUSH/PULL/UPDATE on arrays, ADD/SUB on numbers)."""

    def test_push_tags(self, stack, store, medium_ct):
        entry_uid = store["entries"]["main"]
        resp = stack.content_types(medium_ct).entry(entry_uid).update(entry_data.atomic_push_entry())
        h.assert_status(resp, 200, 201)

    def test_pull_tags(self, stack, store, medium_ct):
        entry_uid = store["entries"]["main"]
        resp = stack.content_types(medium_ct).entry(entry_uid).update(entry_data.atomic_pull_entry())
        h.assert_status(resp, 200, 201)

    def test_update_tag(self, stack, store, medium_ct):
        entry_uid = store["entries"]["main"]
        resp = stack.content_types(medium_ct).entry(entry_uid).update(entry_data.atomic_update_entry())
        h.assert_status(resp, 200, 201)

    def test_add_view_count(self, stack, store, medium_ct):
        entry_uid = store["entries"]["main"]
        resp = stack.content_types(medium_ct).entry(entry_uid).update(entry_data.atomic_add_subtract())
        h.assert_status(resp, 200, 201)

    def test_subtract_view_count(self, stack, store, medium_ct):
        entry_uid = store["entries"]["main"]
        resp = stack.content_types(medium_ct).entry(entry_uid).update(entry_data.atomic_subtract())
        h.assert_status(resp, 200, 201)


class TestEntryLifecycle:
    """export + publish/unpublish."""

    def test_export(self, stack, store, medium_ct):
        resp = stack.content_types(medium_ct).entry(store["entries"]["main"]).export()
        h.assert_status(resp, 200)

    def test_publish(self, stack, store, medium_ct, environment_name):
        resp = stack.content_types(medium_ct).entry(store["entries"]["main"]).publish(
            entry_data.publish_config(environment_name)
        )
        h.assert_status(resp, 200, 201)
        h.wait(h.SHORT_DELAY)

    def test_unpublish(self, stack, store, medium_ct, environment_name):
        resp = stack.content_types(medium_ct).entry(store["entries"]["main"]).unpublish(
            entry_data.unpublish_config(environment_name)
        )
        h.assert_status(resp, 200, 201)


class TestEntryVersioning:
    def test_version_naming(self, stack, store, medium_ct):
        entry_uid = store["entries"]["main"]
        # Name the entry's CURRENT version (it has been updated several times, so
        # version 1 may no longer be the latest). Payload must be wrapped in 'entry'.
        current = h.body(stack.content_types(medium_ct).entry(entry_uid).fetch())["entry"]
        version = current.get("_version", 1)
        resp = stack.content_types(medium_ct).entry(entry_uid).version_naming(
            version, entry_data.version_name_config()
        )
        h.assert_status(resp, 200, 201)


class TestEntryLocalization:
    def test_localize(self, stack, store, medium_ct):
        entry_uid = store["entries"]["main"]
        # Ensure a fr-fr locale exists (created in test_04; create if missing).
        stack.locale().create({"locale": {"name": "French", "code": "fr-fr"}})
        h.wait(h.SHORT_DELAY)
        resp = stack.content_types(medium_ct).entry(entry_uid).localize(
            entry_data.localized_entry_fr_fr(), locale="fr-fr"
        )
        h.assert_status(resp, 200, 201)

    def test_unlocalize(self, stack, store, medium_ct):
        entry_uid = store["entries"]["main"]
        resp = stack.content_types(medium_ct).entry(entry_uid).unlocalize(locale="fr-fr")
        h.assert_status(resp, 200, 201)


class TestEntryNegative:
    def test_fetch_nonexistent(self, stack, medium_ct):
        resp = stack.content_types(medium_ct).entry("does_not_exist_uid").fetch()
        h.assert_status(resp, 404, 422)
        h.validate_error_body(resp)

    def test_create_in_nonexistent_content_type(self, stack):
        resp = stack.content_types("no_such_ct_xyz").entry().create(
            entry_data.simple_entry(h.generate_unique_title("Orphan"))
        )
        h.assert_status(resp, 404, 422)
        h.validate_error_body(resp)

    def test_fetch_without_uid_raises(self, stack, medium_ct):
        with pytest.raises(Exception):
            stack.content_types(medium_ct).entry().fetch()


class TestEntryDelete:
    def test_delete(self, stack, medium_ct):
        created = h.body(
            stack.content_types(medium_ct).entry().create(
                entry_data.simple_entry(h.generate_unique_title("DelEntry"))
            )
        )["entry"]
        h.wait(h.SHORT_DELAY)
        resp = stack.content_types(medium_ct).entry(created["uid"]).delete()
        h.assert_status(resp, 200)
