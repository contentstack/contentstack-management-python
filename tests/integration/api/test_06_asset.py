"""
Asset API tests — full method coverage: upload/CRUD, versions, folders, publishing,
RTE, type filters, and negative/edge cases.

Independent of content types. Uses a real PNG under data/assets/.
"""

import json
import os

import pytest

from framework import helpers as h

pytestmark = pytest.mark.order(6)

_ASSET_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "assets", "sample.png")


@pytest.fixture(scope="class")
def environment_name(stack, store):
    name = store.get("environments", {}).get("main")
    if name:
        return name
    name = h.generate_valid_uid("env_asset")
    stack.environments().create(
        {"environment": {"name": name, "urls": [{"url": "https://e.example.com", "locale": "en-us"}]}}
    )
    h.wait(h.SHORT_DELAY)
    store.setdefault("environments", {})["main"] = name
    return name


class TestAssetCRUD:
    def test_upload(self, stack, store):
        resp = stack.assets().upload(_ASSET_PATH)
        h.assert_status(resp, 201)
        data = h.validate_asset_response(resp)
        store["assets"]["main"] = data["uid"]
        h.wait(h.SHORT_DELAY)

    def test_fetch(self, stack, store):
        resp = stack.assets(store["assets"]["main"]).fetch()
        h.assert_status(resp, 200)
        h.validate_asset_response(resp)

    def test_find_all(self, stack):
        resp = stack.assets().find()
        h.assert_status(resp, 200)
        h.tracked_assert(h.body(resp).get("assets"), "assets list").is_type(list)

    @pytest.mark.xfail(reason="SDK bug: Assets.update() sets Content-Type "
                              "multipart/form-data but sends a JSON body -> 422", strict=False)
    def test_update_title(self, stack, store):
        resp = stack.assets(store["assets"]["main"]).update({"asset": {"title": "Updated Asset"}})
        h.assert_status(resp, 200, 201)

    @pytest.mark.xfail(reason="SDK bug: Assets.replace() sets Content-Type "
                              "multipart/form-data manually while also passing files=, so "
                              "requests cannot set the multipart boundary -> 422", strict=False)
    def test_replace(self, stack, store):
        resp = stack.assets(store["assets"]["main"]).replace(_ASSET_PATH)
        h.assert_status(resp, 200, 201)

    def test_references(self, stack, store):
        resp = stack.assets(store["assets"]["main"]).references()
        h.assert_status(resp, 200)


class TestAssetVersions:
    def test_version_naming(self, stack, store):
        resp = stack.assets(store["assets"]["main"]).version_naming(1, {"upload": {"_version_name": "v1"}})
        h.assert_status(resp, 200, 201)

    def test_versions(self, stack, store):
        resp = stack.assets(store["assets"]["main"]).version()
        h.assert_status(resp, 200)

    def test_version_delete(self, stack, store):
        resp = stack.assets(store["assets"]["main"]).version_delete(1)
        h.assert_status(resp, 200)

    def test_update_asset_revision(self, stack, store):
        resp = stack.assets(store["assets"]["main"]).update_asset_revision(
            {"asset": {"title": "Revised"}, "version": 1}
        )
        h.assert_status(resp, 200, 201)

    def test_generate_permanent_url(self, stack, store):
        asset_uid = store["assets"]["main"]
        host = os.getenv("HOST", "api.contentstack.io")
        api_key = stack.client.headers.get("api_key")
        resp = stack.assets(asset_uid).generate(
            {"asset": {"permanent_url": f"https://{host}/v3/assets/{api_key}/{asset_uid}/slug.png"}}
        )
        h.assert_status(resp, 200, 201)

    def test_download_without_slug_is_404(self, stack, store):
        # download() builds assets/{api_key}/{uid} without a slug, so the permanent-
        # URL endpoint returns 404 for a normally-uploaded asset.
        resp = stack.assets(store["assets"]["main"]).download()
        h.assert_status(resp, 404)


class TestAssetTypesAndRte:
    def test_rte(self, stack):
        resp = stack.assets().rte()
        h.assert_status(resp, 200)

    def test_specific_asset_type_images(self, stack):
        resp = stack.assets().specific_asset_type("images")
        h.assert_status(resp, 200)


class TestAssetFolders:
    def test_create_folder(self, stack, store):
        resp = stack.assets().create_folder(json.dumps({"asset": {"name": h.generate_unique_title("Folder")}}))
        h.assert_status(resp, 201)
        store["folders"]["main"] = h.body(resp).get("asset", {}).get("uid")
        h.wait(h.SHORT_DELAY)

    def test_folder(self, stack, store):
        resp = stack.assets().folder(store["folders"]["main"])
        h.assert_status(resp, 200)

    def test_specific_folder(self, stack, store):
        resp = stack.assets().specific_folder(store["folders"]["main"])
        h.assert_status(resp, 200)

    def test_subfolders(self, stack, store):
        resp = stack.assets().subfolders(store["folders"]["main"])
        h.assert_status(resp, 200)

    def test_get_subfolders(self, stack, store):
        resp = stack.assets().get_subfolders(store["folders"]["main"])
        h.assert_status(resp, 200)

    def test_folder_by_name(self, stack):
        resp = stack.assets().folder_by_name()
        h.assert_status(resp, 200)

    def test_update_or_move(self, stack, store):
        resp = stack.assets().update_or_move(
            store["folders"]["main"], {"asset": {"name": h.generate_unique_title("Folder2")}}
        )
        h.assert_status(resp, 200, 201)

    def test_delete_folder(self, stack, store):
        folder_uid = store.get("folders", {}).get("main")
        if not folder_uid:
            pytest.skip("folder was not created")
        resp = stack.assets().delete_folder(folder_uid)
        h.assert_status(resp, 200)


class TestAssetPublish:
    def test_publish(self, stack, store, environment_name):
        resp = stack.assets(store["assets"]["main"]).publish(
            {"asset": {"locales": ["en-us"], "environments": [environment_name]}, "version": 1}
        )
        h.assert_status(resp, 200, 201)
        h.wait(h.SHORT_DELAY)

    def test_unpublish(self, stack, store, environment_name):
        resp = stack.assets(store["assets"]["main"]).unpublish(
            {"asset": {"locales": ["en-us"], "environments": [environment_name]}, "version": 1}
        )
        h.assert_status(resp, 200, 201)


class TestAssetNegative:
    def test_fetch_nonexistent(self, stack):
        resp = stack.assets("does_not_exist_uid").fetch()
        h.assert_status(resp, 404, 422)
        h.validate_error_body(resp)

    def test_specific_asset_type_requires_type(self, stack):
        with pytest.raises(Exception):
            stack.assets().specific_asset_type(None)


class TestAssetScan:
    """Asset scanning (AM 2.0) — verified enabled on the normal ORGANIZATION too.

    The scan status is exposed only when include_asset_scan_status=true is passed;
    the response field is _asset_scan_status with values pending -> clean | quarantined.
    """

    def test_upload_returns_pending(self, stack):
        asset = stack.assets()
        asset.add_param("include_asset_scan_status", "true")
        resp = asset.upload(_ASSET_PATH)
        h.assert_status(resp, 201)
        status = h.body(resp).get("asset", {}).get("_asset_scan_status")
        h.tracked_assert(status, "scan status on upload").equals("pending")

    def test_scan_status_absent_without_param(self, stack):
        # The field must be absent unless the include param is passed.
        created = h.body(stack.assets().upload(_ASSET_PATH)).get("asset", {})
        resp = stack.assets(created["uid"]).fetch()
        h.assert_status(resp, 200)
        h.tracked_assert(
            "_asset_scan_status" not in h.body(resp).get("asset", {}), "field absent w/o param"
        ).equals(True)

    def test_clean_asset_scanned_clean(self, stack):
        created = h.body(stack.assets().upload(_ASSET_PATH)).get("asset", {})
        status = h.wait_for_scan(stack, created["uid"], "clean")
        h.tracked_assert(status, "clean file scan result").equals("clean")

    def test_malware_asset_quarantined(self, stack, eicar_file):
        created = h.body(stack.assets().upload(eicar_file)).get("asset", {})
        status = h.wait_for_scan(stack, created["uid"], "quarantined")
        h.tracked_assert(status, "EICAR scan result").equals("quarantined")

    def test_find_includes_scan_status(self, stack):
        query = stack.assets()
        query.add_param("include_asset_scan_status", "true")
        resp = query.find()
        h.assert_status(resp, 200)
        assets = h.body(resp).get("assets", [])
        if assets:
            h.tracked_assert(
                "_asset_scan_status" in assets[0], "scan status in listing"
            ).equals(True)


class TestAssetDelete:
    def test_delete(self, stack):
        created = h.body(stack.assets().upload(_ASSET_PATH))
        asset_uid = created.get("asset", {}).get("uid")
        h.wait(h.SHORT_DELAY)
        resp = stack.assets(asset_uid).delete()
        h.assert_status(resp, 200)
