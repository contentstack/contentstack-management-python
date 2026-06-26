# CHANGELOG

## Content Management SDK For Python
---
## v1.10.1

#### Date: 26 June 2026

- Fixed `Asset.update()` to send the JSON body with `Content-Type: application/json` instead of an invalid bare `multipart/form-data`, which the API rejected with 422.
- Fixed `Asset.replace()` to let the HTTP layer set `multipart/form-data` with a proper boundary (a bare `multipart/form-data` header without a boundary previously caused a 422). Both fixes also remove a side effect that leaked the wrong `Content-Type` onto subsequent requests.

---
## v1.10.0

#### Date: 22 June 2026

- Dynamic region endpoint resolution via the Contentstack Regions Registry (`regions.json`).
- Added `Endpoint` class with 3-tier resolution: in-memory cache → bundled `data/regions.json` → live CDN download.
- Exposed `contentstack_management.get_contentstack_endpoint(region, service, omit_https)` module-level proxy.
- `Client` now resolves the `contentManagement` endpoint from the registry instead of a hardcoded host pattern.
- Bundled `contentstack_management/data/regions.json` included in `package_data` — always present after `pip install`.
- `setup.py` auto-refreshes `regions.json` at build time via a custom `BuildPyWithRegions` command; network failures warn but never block the build.
- Runtime fallback: if `regions.json` is absent, the SDK downloads it live on the first `Endpoint` call.
- New regions and services require no SDK code changes — registry update is sufficient.
- Added `refresh_regions()` utility to programmatically download the latest regions manifest from the Contentstack CDN and overwrite the bundled `data/regions.json` (`from contentstack_management import refresh_regions`).
- Added `python3 -m contentstack_management.region_refresh` CLI command for refreshing the registry after `pip install` (source-tree script `scripts/download_regions.py` is for contributors only).

---
## v1.9.0

#### Date:  01 June 2026

- Removed unused `bson` dependency so the package installs on Python 3.12+ and 3.14 (the standalone `bson` 0.5.x package fails to build on newer Python versions).

---
## v1.8.1

#### Date:  15 April 2026

- Fixed Security issues

---
## v1.8.0

#### Date:  30 March 2026

- Added unit, API, and mock tests for asset localization using query parameter (for example `en-us` via `add_param`).

---
## v1.7.2

#### Date:  02 February 2026

- removed content-type header in the release delete method.

---
## v1.7.1

#### Date:  12 January 2026

- Improved Error messages.
---
## v1.7.0

#### Date:  15 September 2025

- OAuth 2.0 support.
---
## v1.6.0

#### Date:  01 September 2025

- AWS AU region support.

---
## v1.5.0

#### Date:  25 August 2025

- Variants feature support.

---
## v1.4.0

#### Date:  09 June 2025

- Release 2.0 support.
- Nested Global fields support
---
## v1.3.3

#### Date:  12 May 2025

- Setuptools package version bump.
---
## v1.3.2

#### Date:  07 April 2025

- Allow users to override the query parameters.
---
## v1.3.1

#### Date:  06 February 2025

- Added branch in header when provided as input to ContentType.
---
## v1.3.0

#### Date:  04 September 2024

- Added Early access support.
---

## v1.2.0

#### Date:  08 July 2024

- Added testcases for creation of Roles with taxonomy permission.
---

## v1.1.1

#### Date: 21 May 2024

- Fixed Assets upload issue.
---

## v1.1.0

#### Date: 14 May 2024

- Added GCP NA region support
---

## v1.0.1

#### Date: 12 December 2023

- Fixed pagination issue, added custom payload option in all methods 
---

## v1.0.0

#### Date: October-23

### Initial Release

##### Initial Release for contentstack management sdk

---
