# Route Family Matrix

This matrix compares public-safe route families. It is not a deployment recommendation for any private endpoint.

| Route family | Evidence label | Best use | Likely failure | Common clients | Public recommendation |
|---|---|---|---|---|---|
| DNS tunnel plus UDP relay | Confirmed from project field notes | Full-device Android and call-like traffic when DNS path survives | Visible endpoint exposure, resolver blocking, DNS traffic classification | App-specific DNS tunnel clients | Production candidate only when privately tested; public docs should stay generic. |
| Direct TLS camouflage | Confirmed from project field notes | Fast ordinary-filtering route | Endpoint or provider reputation block, TLS fingerprinting | Xray-compatible, sing-box-compatible, Hiddify-like, NekoBox-like clients | Good fast branch, not an IP-hiding branch. |
| WebSocket/TLS CDN | Confirmed from project field notes | CDN-fronted compatibility with common clients | Old WS fingerprints, bad fallback behavior, CDN path mismatch | Xray-compatible, Mihomo-like, Hiddify-like clients | Practical public concept if placeholders are used. |
| XHTTP-style transport | Confirmed from project field notes | Newer HTTP-shaped experiments | Client import mismatch, core version drift | Newer Xray-compatible clients | Staged experiment. Verify app support first. |
| CDN edge pinning | Unverified field report plus local planning | Per-ISP edge comparison | Edge candidates age quickly, not all apps support address/SNI split | Xray-compatible, sing-box-compatible, Mihomo-like clients | Test method is public-safe; edge lists are not. |
| Google/API relay | Confirmed from upstream source/docs plus private lab notes | Whitelist-like periods where Google-facing paths survive | Quotas, latency, account risk, poor call support | Project-specific clients | Useful staged experiment, not universal. |
| Domestic-service/WebRTC relay | Confirmed from project field notes | Web and messaging during whitelist-like states | Metadata exposure, unstable calls, session churn | Project-specific apps | Emergency route family with strong safety caveats. |
| Fragmentation and DPI desync | Confirmed from upstream source/docs plus unverified field reports | Lab testing against DPI classification | Privileged drivers, fragile behavior, client/core mismatch | Specific cores or desktop wrappers | Lab-only unless normal clients expose support. |
| QUIC or UDP proxy | Inference | Fast route when UDP is open | UDP blocking, throttling, QUIC fingerprinting | sing-box-compatible, Hiddify-like, NekoBox-like clients | Test as a branch, not as the only route. |
| Public config aggregators | Inference | Emergency short-term access | Privacy risk, rapid burn, unknown operators | Common proxy clients | Last resort only. |

## Candidate Decision Rules

- If calls are required, prove calls with a short controlled test.
- If endpoint hiding is required, use a real intermediary, not only a domain name.
- If the app silently drops fields, reject that client/profile combination.
- If a route only works from one non-Iran network, do not promote it.
- If a route needs privileged packet manipulation, label it lab-only.
