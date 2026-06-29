"""
AM 2.0 (DAM 2.0) asset tests — run only against the AM-enabled org (AM_ORG_UID).

What's AM 2.0-specific vs the normal-org scan tests (test_06):
  - asset UIDs are 'am'-prefixed (vs 'blt')
  - the `api_version: 3.2` header is required on publish (single/bulk) and is
    publish-only — applying it to fetch/upload returns 404

Asset scanning itself behaves identically in both orgs (verified): the
include_asset_scan_status=true param surfaces _asset_scan_status with values
pending -> clean | quarantined. The whole file skips when AM_ORG_UID is unset.
"""

import os

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(31)

_ASSET_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "assets", "sample.png")


class TestAMAssetBasics:
    def test_upload_has_am_uid_prefix(self, am_stack):
        resp = am_stack.assets().upload(_ASSET_PATH)
        h.assert_status(resp, 201)
        uid = h.body(resp).get("asset", {}).get("uid", "")
        h.tracked_assert(uid[:2], "AM 2.0 asset uid prefix").equals("am")

    def test_crud_round_trip(self, am_stack):
        uid = h.body(am_stack.assets().upload(_ASSET_PATH)).get("asset", {}).get("uid")
        h.wait(h.SHORT_DELAY)
        h.assert_status(am_stack.assets(uid).fetch(), 200)
        h.assert_status(am_stack.assets().find(), 200)
        h.assert_status(am_stack.assets(uid).version(), 200)
        h.assert_status(am_stack.assets(uid).delete(), 200)


class TestAMAssetScan:
    def test_upload_returns_pending(self, am_stack):
        asset = am_stack.assets()
        asset.add_param("include_asset_scan_status", "true")
        resp = asset.upload(_ASSET_PATH)
        h.assert_status(resp, 201)
        h.tracked_assert(
            h.body(resp).get("asset", {}).get("_asset_scan_status"), "scan status on upload"
        ).equals("pending")

    def test_clean_asset_scanned_clean(self, am_stack):
        uid = h.body(am_stack.assets().upload(_ASSET_PATH)).get("asset", {}).get("uid")
        status = h.wait_for_scan(am_stack, uid, "clean")
        h.tracked_assert(status, "clean file scan result").equals("clean")

    def test_malware_asset_quarantined(self, am_stack, eicar_file):
        uid = h.body(am_stack.assets().upload(eicar_file)).get("asset", {}).get("uid")
        status = h.wait_for_scan(am_stack, uid, "quarantined")
        h.tracked_assert(status, "EICAR scan result").equals("quarantined")

    def test_scan_status_absent_without_param(self, am_stack):
        uid = h.body(am_stack.assets().upload(_ASSET_PATH)).get("asset", {}).get("uid")
        asset = h.body(am_stack.assets(uid).fetch()).get("asset", {})
        h.tracked_assert("_asset_scan_status" not in asset, "field absent w/o param").equals(True)


class TestAMAssetPublish:
    def test_publish_with_api_version_3_2(self, am_stack):
        uid = h.body(am_stack.assets().upload(_ASSET_PATH)).get("asset", {}).get("uid")
        # upload() pops Content-Type; restore it before the JSON requests below.
        am_stack.client.headers["Content-Type"] = "application/json"
        env = h.generate_valid_uid("env_am")
        am_stack.environments().create(
            {"environment": {"name": env, "urls": [{"url": "https://e.example.com", "locale": "en-us"}]}}
        )
        h.wait(h.SHORT_DELAY)
        am_stack.client.headers["Content-Type"] = "application/json"
        asset = am_stack.assets(uid)
        asset.add_header("api_version", "3.2")
        resp = asset.publish({"asset": {"locales": ["en-us"], "environments": [env]}, "version": 1})
        # Publish always returns success; scan validation happens async on the CDA side.
        h.assert_status(resp, 200, 201)

    def test_api_version_3_2_is_publish_only(self, am_stack):
        # The api_version: 3.2 header is publish-only — on fetch it 404s.
        uid = h.body(am_stack.assets().upload(_ASSET_PATH)).get("asset", {}).get("uid")
        asset = am_stack.assets(uid)
        asset.add_header("api_version", "3.2")
        resp = asset.fetch()
        h.assert_status(resp, 404)
