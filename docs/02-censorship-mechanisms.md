# Censorship Mechanisms

## Mechanism Matrix

| Mechanism | Observable symptom | Diagnostic clue | Mitigation direction |
|---|---|---|---|
| DNS poisoning or resolver failure | Hostname does not resolve, resolves inconsistently, or resolves to suspicious answers | Local resolver differs from trusted resolver | Resolver comparison, DoH/DoT where supported, DNS-only route tests |
| IP or prefix blocking | TCP connection fails before TLS | Other hostnames on same endpoint fail too | Provider diversity, CDN proxying, relay path |
| SNI or TLS classification | TCP connects but TLS handshake fails or resets | Same endpoint may work with different server name or TLS behavior | Better TLS camouflage, real fallback site, REALITY-like designs |
| HTTP path or Host filtering | TLS succeeds but HTTP fallback or WebSocket upgrade fails | Public fallback status differs by path or Host | Path separation, real origin behavior, CDN rule review |
| QUIC or UDP suppression | UDP-based routes fail or are throttled | TCP routes work on same network | TCP fallback, UDP-specific testing, avoid assuming QUIC availability |
| Active probing | Route works briefly then endpoint is classified | Unknown clients probing the endpoint reveal proxy behavior | Probe-resistant frontends, real fallback behavior, origin protection |
| CDN edge degradation | CDN hostname resolves but a specific edge stalls | Pinned edge differs from hostname-only result | Clean edge comparison, per-ISP edge telemetry |
| Upload throttling or grey connection | Downloads work but messages, uploads, or media fail | HTTP status works, proxy traffic stalls | Payload tests, MTU/fragmentation lab, route family comparison |

## Why The Visible Endpoint Matters

Inference: Encryption hides payload content, not the destination endpoint. If a phone connects directly to a private server address, the access ISP can still see the endpoint and port.

Confirmed from project field notes: Private tests showed that hiding the final server address requires a real intermediary in the packet path, such as a CDN, recursive resolver, cloud API relay, domestic-service relay, or bridge host.

## Why ClientHello And Fingerprints Matter

Inference: Modern filtering can classify traffic using TLS ClientHello fields, ALPN, SNI, packet sizes, timing, WebSocket behavior, QUIC behavior, and server fallback behavior. A route can fail even when the endpoint is reachable.

Unknown: Which exact fingerprinting rules are active at a specific time on a specific Iranian operator. Test data must be collected per operator and date.
