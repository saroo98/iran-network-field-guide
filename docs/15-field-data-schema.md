# Field Data Schema

This schema describes public-safe examples and sanitized field reports. It is intentionally small so reports remain easy to compare.

## Required Context Fields

| Field | Meaning | Example |
|---|---|---|
| `timestamp_utc` | Approximate UTC test time | `2026-06-25T00:00:00Z` |
| `route_family` | Public route-family label | `WebSocket/TLS CDN` |
| `hostname` | Placeholder hostname only | `EXAMPLE_HOSTNAME` |
| `isp_operator` | Operator label or placeholder | `EXAMPLE_ISP` |
| `region` | Region label or placeholder | `EXAMPLE_REGION` |
| `network_type` | `mobile`, `fixed`, `wifi`, or `unknown` | `mobile` |
| `client_app` | Public client name or placeholder | `EXAMPLE_CLIENT_NAME` |
| `client_version` | Public client version or placeholder | `EXAMPLE_VERSION` |
| `error_stage` | Primary failing stage or `none` | `tls` |
| `failure_label` | Controlled failure label | `tls-fail` |

## Required Stage Fields

Each stage row must include:

| Field | Meaning |
|---|---|
| `stage` | One of the allowed stage names |
| `status` | `ok`, `fail`, or `not_tested` |
| `latency_ms` | Integer milliseconds, or blank when not tested |

Allowed stages:

- `dns`
- `tcp`
- `tls`
- `http`
- `http3`
- `udp`
- `proxy`
- `app`

Allowed failure labels:

- `dns-fail`
- `tcp-fail`
- `tls-fail`
- `http-fail`
- `udp-fail`
- `proxy-fail`
- `upload-stall`
- `grey-connect`
- `random-reset`
- `client-import`
- `works`

## JSON Shape

```json
{
  "schema": "iran-network-field-guide-results-v1",
  "privacy": "Sanitized examples with placeholders only.",
  "results": [
    {
      "timestamp_utc": "2026-06-25T00:00:00Z",
      "route_family": "WebSocket/TLS CDN",
      "hostname": "EXAMPLE_HOSTNAME",
      "isp_operator": "EXAMPLE_ISP",
      "region": "EXAMPLE_REGION",
      "network_type": "mobile",
      "client_app": "EXAMPLE_CLIENT_NAME",
      "client_version": "EXAMPLE_VERSION",
      "stages": [
        {
          "stage": "dns",
          "status": "ok",
          "latency_ms": 12,
          "detail": "placeholder"
        }
      ],
      "error_stage": "none",
      "failure_label": "works"
    }
  ]
}
```

## CSV Shape

CSV examples should use the flattened stage format:

```csv
timestamp_utc,route_family,hostname,isp_operator,region,network_type,client_app,client_version,stage,status,latency_ms,error_stage,failure_label
2026-06-25T00:00:00Z,WebSocket/TLS CDN,EXAMPLE_HOSTNAME,EXAMPLE_ISP,EXAMPLE_REGION,mobile,EXAMPLE_CLIENT_NAME,EXAMPLE_VERSION,dns,ok,12,none,works
```

## Validation

Run:

```bash
python tools/validate_examples.py data/examples
```

The validator rejects:

- Missing required fields.
- Unknown stages, statuses, network types, or failure labels.
- Real-looking IP address values.
- URL-shaped values.
- Hostnames that are not placeholders.
