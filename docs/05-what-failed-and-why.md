# What Failed And Why

## Failure Categories

| Failure | Evidence label | Practical meaning |
|---|---|---|
| Direct endpoint exposure | Confirmed from project field notes | A domain name alone does not hide the server address if it resolves directly to it. |
| Web-only success mislabeled as call-ready | Confirmed from project field notes | Messaging can work while calls fail due to UDP, WebRTC, latency, or relay constraints. |
| Client import mismatch | Confirmed from project field notes | A protocol may be valid but unusable if the target app silently drops fields. |
| CDN misunderstanding | Inference | Ordinary CDN proxying handles HTTP-like traffic, not arbitrary raw TCP. |
| UDP assumptions | Inference | QUIC-like or UDP-heavy routes can be fast only when UDP is allowed and not throttled. |
| Public config dependency | Inference | Public proxies are often burned quickly and can carry privacy risk. |

## Domain Names Do Not Hide Endpoints By Themselves

Evidence: Confirmed from project field notes.

If the client connects directly to the final server address, the access ISP can see that endpoint. A hostname helps only when it resolves to a real intermediary or when the route uses an actual relay.

## "Connected" Does Not Mean "Usable"

Evidence: Confirmed from project field notes.

A route can complete DNS, TCP, and TLS stages but fail once proxy traffic begins. This is why field reports should record error stage and user-visible app behavior separately.

## Why Some Ideas Stay Lab-Only

Evidence: Confirmed from upstream source/docs and inference.

Fragmentation, fake-SNI, and DPI-desync tools can be valuable research paths. They are not automatically suitable for non-technical users because they may require privileged drivers, platform-specific packet handling, or exact core versions.
