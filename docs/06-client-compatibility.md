# Client Compatibility

## Compatibility Matrix

| Route family | Common apps | Shareable config | Managed profile output | Custom client needed | Non-technical user fit | Main compatibility break |
|---|---|---|---|---|---|---|
| DNS tunnel plus UDP relay | App-specific DNS tunnel clients | Usually app-specific | Sometimes | Often yes | Medium if preconfigured | Import format and UDP relay support |
| Direct TLS camouflage | Xray, v2rayNG, NekoBox, Hiddify-like clients | Usually yes | Yes | No | High if profile is tested | Unsupported flow, fingerprint, or TLS fields |
| WebSocket/TLS CDN | Xray, v2rayNG, NekoBox, Hiddify-like clients, Mihomo-style clients | Usually yes | Yes | No | High | Host, SNI, path, ALPN, or CDN mismatch |
| XHTTP-style route | Newer Xray-compatible clients | Sometimes | Yes when client supports fields | No, if core supports it | Medium | Client silently ignores transport fields |
| Clean edge pinning | Xray/sing-box/Mihomo-style clients with separate address and SNI fields | Sometimes | Yes | No | Medium | App cannot separate connect address from SNI/Host |
| Google/API relay | Project-specific clients | App-specific | Usually no | Often yes | Medium to low | Account setup, quotas, latency |
| Domestic-service/WebRTC relay | Project-specific apps | App-specific | Usually no | Yes | Medium | Account/session setup and reliability |
| Fragmentation or DPI desync | Specific cores or desktop wrappers | Rarely as normal profile | Rarely | Sometimes | Low | Platform privileges and exact version support |

## Client Selection Rules

Inference:

- Prefer clients that expose all fields needed by the route family.
- Do not assume import success means the app preserved the route correctly.
- Test Android and desktop separately.
- Record app name, app version, and core version in field reports.

## Non-Technical User Rule

Inference: A route for non-technical users should have one import path, one profile name, clear pass/fail labels, and no manual field editing after import.
