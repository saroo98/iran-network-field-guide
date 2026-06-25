# Traffic Fingerprinting

## What Can Be Fingerprinted

Inference: A censor does not need payload visibility to classify a route. Signals may include:

- Destination endpoint and port.
- DNS query behavior.
- TLS ClientHello fields.
- ALPN.
- SNI.
- Certificate behavior.
- QUIC version and transport parameters.
- WebSocket upgrade patterns.
- HTTP path and Host behavior.
- Packet size and timing.
- Failed active probes.

## TLS And SNI

Inference: Matching normal browser-like behavior can help, but fake browser labels alone are not enough. Server behavior, fallback behavior, and route consistency matter.

## Fragmentation And DPI Desync

Evidence: Confirmed from upstream source/docs plus unverified field reports.

Fragmentation and DPI-desync techniques try to make a censor parse different bytes from the real endpoint. These can be powerful but fragile.

Public recommendation:

- Treat as lab-only unless a common client exposes the feature clearly.
- Record exact client and core version.
- Do not ask non-technical users to install privileged packet drivers.
- Compare against a normal control profile on the same network.

## Active Probing

Inference: If an endpoint behaves like a proxy when probed by unknown clients, it can be classified faster. Real fallback behavior and origin protection reduce but do not eliminate this risk.
