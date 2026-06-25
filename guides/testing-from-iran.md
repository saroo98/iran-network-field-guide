# Testing From Iran

Use this guide to collect comparable results without exposing private deployments.

For route promotion decisions, pair this with the [operator playbook](operator-playbook.md).

## Before Testing

1. Confirm you are testing only endpoints you own or are authorized to test.
2. Disable other VPN or proxy apps unless the test explicitly requires them.
3. Record client app name and version.
4. Record network type: mobile, fixed, wifi, or unknown.
5. Use route-family names, not private profile names.

## Stage Order

| Stage | What it tells you |
|---|---|
| DNS | Whether the hostname can be resolved through the local resolver |
| TCP | Whether the endpoint and port are reachable |
| TLS | Whether SNI, certificate, and TLS negotiation survive |
| HTTP fallback | Whether a normal public fallback path works |
| HTTP/3 or UDP | Whether UDP-like paths are usable |
| Proxy/app | Whether the actual client profile moves useful traffic |

## Pass Criteria

Do not call a route "working" only because it connects. Record the user-visible behavior:

- Web page loads.
- Messaging text works.
- Media download works.
- Upload works.
- Voice message works.
- Real-time call works.
- Idle connection survives.

## Failure Labels

Use one primary label:

- `dns-fail`
- `tcp-fail`
- `tls-fail`
- `http-fail`
- `udp-fail`
- `proxy-fail`
- `upload-stall`
- `grey-connect`
- `random-reset`
- `client-import`
- `works`

## Comparable Test Pair

When comparing route families, keep these fields the same:

- Tester.
- Operator.
- Network type.
- Time window.
- Client app and version.
- Test order.
- User-visible behavior checks.

Change only the route-family branch being tested. If several fields changed at once, label the result as inconclusive.

## Stop-Testing Rules

Stop and mark the result clearly when:

- DNS fails and no later stage can be tested.
- TCP fails repeatedly on the same branch and network.
- TLS fails after TCP succeeds.
- The app imports a profile but drops required fields.
- The route works for web only and the goal requires upload or calls.

## Safety

Do not paste raw logs unless you have removed endpoint values, account identifiers, cookies, credentials, client import material, QR codes, and private user data.
