"""Entry Variants API tests — find/fetch entry variants, negative cases.

Requires Personalize + an entry. Skips gracefully when prerequisites are missing.
"""

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(17)


@pytest.fixture(scope="class")
def entry_ctx(store):
    entry_uid = store.get("entries", {}).get("main")
    ct_uid = store.get("content_types", {}).get("medium")
    if not (entry_uid and ct_uid):
        pytest.skip("no entry available for entry variants")
    return ct_uid, entry_uid


class TestEntryVariants:
    def test_find(self, stack, entry_ctx):
        ct_uid, entry_uid = entry_ctx
        resp = stack.content_types(ct_uid).entry(entry_uid).variants().find()
        h.assert_status(resp, 200)

    def test_include_variants_requires_variant_uid(self, stack, entry_ctx):
        # EntryVariants.includeVariants() guards on a missing variant_uid and
        # raises before issuing the HTTP call.
        ct_uid, entry_uid = entry_ctx
        with pytest.raises(Exception):
            stack.content_types(ct_uid).entry(entry_uid).variants().includeVariants()


class TestEntryVariantsNegative:
    def test_fetch_nonexistent(self, stack, entry_ctx):
        ct_uid, entry_uid = entry_ctx
        resp = stack.content_types(ct_uid).entry(entry_uid).variants("no_such_variant").fetch()
        # Variants API returns 412 (precondition failed, code 1010) for unknown variant.
        h.assert_status(resp, 404, 412, 422)
