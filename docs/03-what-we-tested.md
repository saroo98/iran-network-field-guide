# What We Tested

This file summarizes private project testing in public-safe route-family terms. It intentionally omits live endpoints, route names, providers, credentials, and user identifiers.

## Tested Route Families

| Route family | Evidence label | Public-safe result |
|---|---|---|
| DNS tunnel plus UDP relay | Confirmed from project field notes | Strongest private result for full-device Android and call-like use. Visible endpoint remained important. |
| Direct TLS camouflage | Confirmed from project field notes | Fast when reachable, but still exposed direct endpoint reputation and provider risk. |
| WebSocket/TLS CDN route | Confirmed from project field notes | Useful compatibility with common clients; behavior depends heavily on CDN edge, Host, SNI, path, and origin handling. |
| XHTTP-style route | Confirmed from project field notes | Promising as an HTTP-shaped transport, but client compatibility varied. |
| CDN edge pinning | Unverified field report plus local planning | Worth testing per ISP; no public edge list should be published. |
| Domestic-service/WebRTC relay | Confirmed from project field notes | Worked for web and messaging in a private field test; calls were not reliable in that test. |
| Google/API relay | Confirmed from upstream source/docs plus private lab notes | Useful when Google-facing paths survive; quota, latency, privacy, and call support remain limiting factors. |
| Fragmentation or DPI desync | Confirmed from upstream source/docs plus unverified field reports | Advanced/lab-only unless the client app and core clearly support it. |
| Public config aggregators | Inference | Emergency-only due to privacy, trust, and burn risk. |

## What Was Not Published

The private project contained operational material that is not suitable for a public repository:

- Active endpoint values.
- Provider-specific deployment details.
- Client import links.
- Credentials and cookies.
- Private logs.
- User labels tied to real subscriptions.
- QR codes or profile bundles.

## Interpretation

Inference: The best public output is not a list of routes. It is a field guide for choosing, testing, and safely discussing route families without burning deployments.
