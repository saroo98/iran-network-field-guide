# Open Questions

## Technical Unknowns

| Question | Evidence status | How to test safely |
|---|---|---|
| Which Iranian operators suppress UDP most aggressively? | Unknown | Per-ISP UDP and TCP comparison using owned endpoints |
| Does clean edge pinning beat hostname-only CDN routing consistently? | Unverified field report | Same hostname, same tester, same time window, explicit edge candidates |
| Which clients preserve XHTTP fields correctly? | Unknown | Import/export comparison and core-version recording |
| Are fragmentation features useful on common Android apps? | Unknown | Lab-only profile with exact app/core version |
| Can domestic-service relay routes support real-time calls reliably? | Unknown | Short controlled call tests with metadata-risk review |
| Which failures are endpoint reputation versus protocol fingerprint? | Inference | Same protocol on different providers and different protocols on same provider |

## Research Discipline

Inference: One success is a signal, not proof. A public recommendation should require repeated tests across users, operators, and time windows.

## Data We Need

- DNS result differences.
- TCP connect result.
- TLS result.
- HTTP fallback status.
- UDP or HTTP/3 result when relevant.
- Proxy handshake result when safe.
- App behavior for web, messaging, upload, and calls.
- Client app and version.
- Network type and operator.
