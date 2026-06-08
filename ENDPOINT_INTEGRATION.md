# Region Endpoint Integration — Management Python SDK

## Overview

Contentstack services are deployed across multiple cloud providers and geographic regions. The Management Python SDK resolves service endpoints dynamically using the Contentstack Regions Registry rather than relying on hardcoded URLs.

This ensures:

- Consistent endpoint resolution across all SDKs
- Automatic support for newly introduced regions
- Automatic support for newly introduced services
- Single source of truth for endpoint configuration
- Elimination of region-specific host logic inside the SDK

---

## Regions Registry

All endpoint information is maintained in the Contentstack Regions Registry.

### Registry URL

```text
https://artifacts.contentstack.com/regions.json
```

The registry contains:

- Region identifiers
- Region aliases
- Default region information
- Service endpoint mappings

### Example

```json
{
  "regions": [
    {
      "id": "na",
      "alias": ["us", "aws-na"],
      "isDefault": true,
      "endpoints": {
        "contentDelivery": "https://cdn.contentstack.io",
        "contentManagement": "https://api.contentstack.io"
      }
    }
  ]
}
```

---

## Endpoint Resolution Contract

The SDK exposes a public endpoint resolution API via the `Endpoint` class.

```text
Endpoint.get_contentstack_endpoint(
    region,
    service    = '',
    omit_https = False
)
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `region` | Region identifier or alias (e.g. `'us'`, `'eu'`, `'azure-na'`) |
| `service` | Service key (e.g. `'contentManagement'`, `'contentDelivery'`). When empty, all endpoints for the region are returned. |
| `omit_https` | When `True`, strips `https://` from the returned URL — useful when constructing the `Client` endpoint string |

### Returns

- `str` — service URL when a service key is provided
- `dict[str, str]` — complete endpoint map when service is omitted

### Raises

| Exception | When |
|-----------|------|
| `ValueError` | Empty region, unknown region, or unknown service |
| `RuntimeError` | `regions.json` cannot be read or parsed |

---

## Region Resolution Rules

Region matching must:

- Ignore case
- Trim whitespace
- Support aliases
- Support both dash (`-`) and underscore (`_`) variants where defined

### Examples

| Input | Resolved Region |
|-------|----------------|
| `na` | `na` |
| `us` | `na` |
| `aws-na` | `na` |
| `AWS_NA` | `na` |
| `eu` | `eu` |
| `azure-na` | `azure-na` |
| `gcp-eu` | `gcp-eu` |

If no region is found:

```text
ValueError: Invalid region
```

---

## Service Resolution Rules

The SDK will:

1. Locate the resolved region in the registry.
2. Locate the service key within the region endpoints.
3. Return the endpoint URL.

### Example

```text
Region:  eu
Service: contentManagement

Result:
https://eu-api.contentstack.com
```

If the service key is not present:

```text
ValueError: Service not found
```

---

## Supported Service Keys

- `contentManagement`
- `contentDelivery`
- `graphqlDelivery`
- `graphqlPreview`
- `preview`
- `auth`
- `application`
- `images`
- `assets`
- `automate`
- `launch`
- `developerHub`
- `brandKit`
- `genAI`
- `personalizeManagement`
- `personalizeEdge`
- `composableStudio`

The SDK does not hardcode this list. The registry remains the source of truth.

---

## Registry Loading Requirements

Resolution order:

1. **In-memory cache** — `Endpoint._regions_data` class-level variable. Zero I/O after first call.
2. **Local registry file** — `contentstack_management/data/regions.json` on disk, bundled at install time.
3. **Live download fallback** — `GET https://artifacts.contentstack.com/regions.json` via `requests`.

```text
get_contentstack_endpoint()
          │
          ▼
  In-memory cache hit?
     Yes → return
     No  ↓
          ▼
  regions.json on disk?
     Yes → load, cache, return
     No  ↓
          ▼
  Download from CDN
     Success → write to disk, cache, return
     Failure → RuntimeError
```

---

## Registry Management

The `regions.json` file is stored locally at `contentstack_management/data/regions.json` and managed via a download script.

> **Note:** The registry is stored under `data/` rather than `assets/` because `contentstack_management/assets/` is already a Python package used for the Assets Management API.

### Initial Download

Run once after cloning or installing the SDK:

```bash
python3 scripts/download_regions.py
```

This downloads the latest `regions.json` from the Contentstack Regions Registry and stores it in:

```text
contentstack_management/data/regions.json
```

### Refresh Registry

To manually refresh and overwrite the existing file:

```bash
python3 scripts/download_regions.py
```

This command:

1. Downloads the latest `regions.json` from the registry.
2. Replaces the existing local copy.
3. Makes newly added regions and services immediately available without requiring SDK code changes.

### Example Workflow

```text
python3 scripts/download_regions.py
                │
                ▼
Download latest regions.json
                │
                ▼
Store in contentstack_management/data/regions.json
                │
                ▼
Available on next Endpoint call
```

> **Note:** If `regions.json` is absent at runtime, the SDK performs a live download automatically on the first `Endpoint` call. The script is recommended for production environments to avoid the startup latency.

---

## SDK Integration

```text
Resolve Region
      ↓
Resolve contentManagement Endpoint
      ↓
Configure Client Endpoint
      ↓
Execute Management API Requests
```

`Client` automatically resolves its endpoint via `Endpoint` during initialization. The endpoint is configured from the resolved `contentManagement` URL rather than a hardcoded hostname.

### Resolution Priority

| Condition | Endpoint Source |
|-----------|----------------|
| Custom `host` provided | Custom host wins — Endpoint is not consulted |
| No custom `host` | `Endpoint.get_contentstack_endpoint(region, 'contentManagement')` |
| Unknown region (fallback) | Legacy pattern: `{region}-api.contentstack.com` |

---

## Error Handling

| Scenario | Exception | Message |
|----------|-----------|---------|
| Empty region | `ValueError` | `Empty region provided. Please put valid region.` |
| Unknown region | `ValueError` | `Invalid region: <value>` |
| Unknown service | `ValueError` | `Service "<key>" not found for region "<id>"` |
| Registry unavailable | `RuntimeError` | `regions.json not found and could not be downloaded.` |
| Registry corrupt | `RuntimeError` | `regions.json is corrupt. Run scripts/download_regions.py to re-download it.` |

---

## Caching Requirements

Goals:

- Avoid repeated disk reads
- Avoid repeated network requests
- Improve endpoint lookup performance

The Management Python SDK uses a class-level variable `Endpoint._regions_data` as the in-memory cache. It is populated on first use and persists for the lifetime of the process. Call `Endpoint.reset_cache()` to invalidate (intended for testing only).

---

## Future Compatibility

SDK implementations must not:

- Hardcode endpoint URLs
- Hardcode region mappings
- Hardcode service mappings

All endpoint information must originate from the Regions Registry.

---

## Management Python SDK Example

```python
import contentstack_management
from contentstack_management.endpoint import Endpoint
from contentstack_management.contentstack import Region, Client

# --- Resolve a single service URL ---
url = Endpoint.get_contentstack_endpoint('eu', 'contentManagement')
# https://eu-api.contentstack.com

# --- Resolve without scheme (for use as a host string) ---
host = Endpoint.get_contentstack_endpoint('gcp-na', 'contentManagement', omit_https=True)
# gcp-na-api.contentstack.com

# --- Resolve all services for a region ---
endpoints = Endpoint.get_contentstack_endpoint('azure-na')
# {
#   'contentDelivery':   'https://azure-na-cdn.contentstack.com',
#   'contentManagement': 'https://azure-na-api.contentstack.com',
#   ...
# }

# --- Module-level proxy ---
url = contentstack_management.get_contentstack_endpoint('eu', 'contentManagement')
# https://eu-api.contentstack.com

# --- Client endpoint is auto-resolved via Endpoint ---
client = Client(
    authtoken='<AUTHTOKEN>',
    region=Region.EU.value
)
# client.endpoint → 'https://eu-api.contentstack.com/v3/'

# Custom host still overrides Endpoint resolution
client = Client(
    authtoken='<AUTHTOKEN>',
    region='au',
    host='custom.example.com'
)
# client.endpoint → 'https://au-api.custom.example.com/v3/'

# --- Make Management API calls using the resolved endpoint ---
response = client.stack('<API_KEY>').content_types().find()
```

---

## Supported Regions

| Region ID | Aliases | Content Management URL |
|-----------|---------|----------------------|
| `na` | `us`, `aws-na`, `aws_na` | `https://api.contentstack.io` |
| `eu` | — | `https://eu-api.contentstack.com` |
| `au` | — | `https://au-api.contentstack.com` |
| `azure-na` | `azure_na` | `https://azure-na-api.contentstack.com` |
| `azure-eu` | `azure_eu` | `https://azure-eu-api.contentstack.com` |
| `gcp-na` | `gcp_na` | `https://gcp-na-api.contentstack.com` |
| `gcp-eu` | `gcp_eu` | `https://gcp-eu-api.contentstack.com` |

Region aliases are case-insensitive. `AWS-NA`, `aws-na`, and `aws_na` all resolve to the `na` region.
