# CDN Edge Planning Template

This template is for planning only. Do not publish real zones, hostnames, origins, edge candidates, or account details.

## Hostname

Public placeholder: `EXAMPLE_HOSTNAME`

## Origin

Origin placeholder: `EXAMPLE_IP`

## Candidate Edge Test

| Field | Value |
|---|---|
| Connect address | `EXAMPLE_CDN_EDGE_IP` |
| TLS SNI | `EXAMPLE_SNI` |
| HTTP Host | `EXAMPLE_HOST_HEADER` |
| HTTP path | `EXAMPLE_PATH` |
| ISP/operator | `EXAMPLE_ISP` |
| Region | `EXAMPLE_REGION` |

## Promotion Rule

Promote only if the edge candidate beats hostname-only behavior for the same tester, same network, same client, and same time window.

## Changes Requiring Approval

- DNS changes.
- CDN dashboard changes.
- Origin firewall changes.
- Worker or tunnel changes.
- Production endpoint changes.
