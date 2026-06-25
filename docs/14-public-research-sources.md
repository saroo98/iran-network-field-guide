# Public Research Sources

This page lists public sources that support the field guide's measurement discipline. Use these sources to understand failure modes, not as proof that a route family works on a current Iranian network.

## Source Table

| Source | Supports | How to use it in this repo |
|---|---|---|
| [OONI Explorer: Iran](https://explorer.ooni.org/country/IR) | Long-running public measurements from Iranian networks | Use as background evidence for network interference and operator variance |
| [OONI technical report on Iran shutdowns during the 2022 protests](https://ooni.org/post/2022-iran-technical-multistakeholder-report/) | DNS-based tampering, TLS-level interference, mobile disruption, and shutdown measurement | Support the DNS/TLS failure-stage taxonomy |
| [OONI HTTP/3 censorship research](https://ooni.org/post/2022-http3-measurements-paper/) | HTTP/3 and UDP behavior can differ from HTTPS-over-TCP behavior | Support separate UDP/QUIC testing instead of assuming TCP results apply |
| [IODA comparison of Iran shutdowns](https://ioda.inetintel.cc.gatech.edu/reports/a-comparative-look-at-internet-shutdowns-in-iran-2019-2022-2026-and-2026/) | Shutdowns can preserve some global routing signals while access conditions still change for users | Support the distinction between macro reachability and user-visible access |
| [Project X transport documentation](https://xtls.github.io/en/config/transport.html) | Transport method, transport security, and configuration compatibility concepts | Support client/core compatibility notes without publishing working profiles |
| [sing-box TLS documentation](https://sing-box.sagernet.org/configuration/shared/tls/) | TLS and ALPN fields exposed by a common proxy core | Support field-preservation checks during client compatibility testing |
| [Cloudflare Workers WebSockets documentation](https://developers.cloudflare.com/workers/runtime-apis/websockets/) | WebSocket behavior and runtime constraints | Support CDN/WebSocket caveats and avoid treating all CDN paths as equivalent |
| [Cloudflare Tunnel protocol documentation](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/routing-to-tunnel/protocols/) | Published application protocol handling and TCP-over-WebSocket concepts | Support the distinction between HTTP-shaped paths and generic raw transport |

## Evidence Use Rules

- Prefer current public documentation for version-sensitive transport and client behavior.
- Treat public measurement reports as context, not as proof that a private route will work today.
- Do not promote a route family from public sources alone; require comparable field reports.
- Keep public claims tied to observable stages: DNS, TCP, TLS, HTTP, HTTP/3, UDP, proxy, or app behavior.
- Record source-backed claims as `Confirmed from public source`.

## Gaps Public Sources Cannot Fill

Public sources cannot tell you:

- Which route family works for a specific tester at a specific time.
- Whether a common app preserved every field in a profile import.
- Whether a branch supports calls, uploads, or idle stability.
- Whether one CDN edge candidate is better on a current operator.

Those require sanitized field results collected with the same method across comparable test windows.
