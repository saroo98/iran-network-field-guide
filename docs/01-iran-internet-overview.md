# Iran Internet Overview

## Core Observation

Confirmed from project field notes: Iran connectivity failures vary by operator, city, access technology, time window, route family, client app, and endpoint reputation. A route that works for one tester can fail for another tester on the same day.

Inference: Treat the environment as multiple network states instead of one national filter. Useful route planning starts by identifying the failure stage.

## Common Network States

| Network state | Typical symptoms | Route families worth testing |
|---|---|---|
| Ordinary filtering | Some sites and apps fail, foreign connectivity remains usable | Direct TLS camouflage, WebSocket/TLS CDN, XHTTP, DNS tunnel |
| DPI-heavy filtering | TLS or proxy handshakes reset, fallback websites may load | Better TLS behavior, HTTP-shaped transports, CDN edge testing, fragmentation lab |
| UDP or QUIC suppression | QUIC-like routes fail or stall, TCP routes still work | TCP-based camouflage, WebSocket/TLS, DNS over resolver path |
| Provider or IP reputation block | One datacenter path fails while another works | Provider diversity, endpoint rotation, CDN-fronted route families |
| Whitelist-like period | Domestic or selected global services work, many foreign paths fail | Domestic-service relay, Google/API relay, emergency web-only paths |
| Grey connection | Connect succeeds but uploads, media, or proxy traffic stalls | Stage-by-stage diagnostics, clean edge comparison, payload-size testing |

## What This Means For Users

Inference: No single protocol is the answer. A resilient plan needs several independent route families, each with clear pass and fail criteria.

Confirmed from project field notes: A DNS tunnel plus UDP relay route was the strongest private field result for full-device Android and call-like use. It is not automatically private from an access-network perspective because the visible endpoint still matters.

Confirmed from project field notes: A domestic-service/WebRTC relay route was useful for web and messaging in a private field test, but real-time calls were not reliable enough to label it call-capable.

Unknown: Whether any route family remains stable across all Iranian operators during severe disruption.
