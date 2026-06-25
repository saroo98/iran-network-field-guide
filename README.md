<div align="center">

# Iran Network Field Guide

<img src="assets/iran-network-field-guide-cover.png" alt="Iran connectivity testing map for VPN route families, DNS, TCP, TLS, HTTP, UDP, QUIC, and CDN edge measurement" width="100%">

**A practical field guide for Iran connectivity testing, VPN route-family decisions, and censorship-resilience measurement.**

[Start here](#start-here) ·
[Choose a route](guides/choosing-a-route-family.md) ·
[Operator playbook](guides/operator-playbook.md) ·
[Run tests](guides/testing-from-iran.md) ·
[Route matrix](docs/13-route-family-matrix.md) ·
[Report safely](templates/field-report-template.md)

</div>

---

## What This Helps With

Iran connectivity failures are rarely one clean block. The same route can behave differently by operator, city, network type, time window, client app, DNS path, CDN edge, endpoint reputation, UDP handling, QUIC handling, and TLS behavior.

This guide helps researchers, VPN operators, circumvention-tool builders, and field testers answer practical questions:

| Question | Where to start |
|---|---|
| What kind of failure is this? | [Censorship mechanisms](docs/02-censorship-mechanisms.md) |
| Which VPN route family should be tested next? | [Choosing a route family](guides/choosing-a-route-family.md) |
| How should a route be promoted or rejected? | [Operator playbook](guides/operator-playbook.md) |
| Which client apps can realistically use it? | [Client compatibility](docs/06-client-compatibility.md) |
| How do we collect comparable field results? | [Testing from Iran](guides/testing-from-iran.md) |

## Start Here

| Reader path | First document | Useful outcome |
|---|---|---|
| Diagnose a failed connection | [Testing from Iran](guides/testing-from-iran.md) | Identify whether the failure is DNS, TCP, TLS, HTTP, UDP/QUIC, proxy, or app behavior |
| Choose a route family | [Choosing a route family](guides/choosing-a-route-family.md) | Compare route families by symptom instead of guessing by protocol name |
| Improve an operating workflow | [Operator playbook](guides/operator-playbook.md) | Promote only routes with repeated, comparable, sanitized evidence |
| Collect a safe field report | [Field report template](templates/field-report-template.md) | Share useful observations without live values |
| Compare client support | [Client compatibility](docs/06-client-compatibility.md) | Check whether a common app preserves the fields a route needs |

## Fast Path

1. Read the [overview](docs/01-iran-internet-overview.md) to understand the network states.
2. Match symptoms with [choosing a route family](guides/choosing-a-route-family.md).
3. Use the [operator playbook](guides/operator-playbook.md) to pick two comparable branches.
4. Run a staged probe with [connectivity_probe.py](tools/connectivity_probe.py).
5. Summarize the result with [result_summarizer.py](tools/result_summarizer.py).
6. Share only a sanitized report using the [field report template](templates/field-report-template.md).

## Failure Stage Map

| Stage | What it means | Useful next move |
|---|---|---|
| DNS | Hostname does not resolve or resolves inconsistently | Compare resolvers and record answers |
| TCP | Endpoint or port cannot be reached | Compare provider, CDN, or relay paths |
| TLS | Handshake fails after TCP connects | Review SNI, certificate, ALPN, and fingerprint behavior |
| HTTP | Fallback page or upgrade path fails | Check Host, path, CDN rules, and origin behavior |
| UDP/QUIC | UDP-style transport fails or stalls | Compare with a TCP branch before promoting it |
| Proxy/app | Connection opens but useful traffic fails | Record client version, route family, and user-visible behavior |

## What To Look For

| Signal | Why it matters |
|---|---|
| Failure stage | Prevents treating DNS, TLS, UDP, and app failures as one generic block |
| Operator and network type | Iran filtering can differ by mobile, fixed, Wi-Fi, region, and operator |
| Client app and core version | Some apps import a profile but drop route-critical fields |
| DNS, TCP, TLS, HTTP, UDP/QUIC results | A public fallback working over TCP does not prove UDP or proxy traffic works |
| User-visible behavior | Web, messaging, upload, voice messages, calls, and idle stability can fail differently |
| Repeated time windows | One success is a signal, not proof of stability |

## What Not To Trust Alone

| Weak signal | Why it is not enough |
|---|---|
| One success report | It may be operator-specific, time-specific, or client-specific |
| Generic speed tests | They do not identify censorship failure stage or route capability |
| A client "connected" icon | The route may connect but fail to move useful traffic |
| Tests from outside Iran | They do not reproduce access-network filtering conditions |
| Screenshots with sensitive fields | They can expose values while still missing the technical failure stage |
| Vague "works" or "does not work" claims | They cannot guide route-family selection without stage and context |

## Current Field Snapshot

Observed on 25 June 2026 with Happ on Mobinnet internet in Iran. Config names and ping numbers are omitted. This is a single field snapshot, not a universal recommendation.

| Order | Protocol | Port | Observed status |
|---:|---|---:|---|
| 1 | VLESS / TCP / TLS | 7445 | Best observed |
| 2 | VLESS / WS / TLS | 443 | Responsive, mixed quality |
| 3 | VLESS / TCP / REALITY | 6102 | Responsive |
| 4 | VLESS / TCP / TLS | 7444 | Responsive |
| 5 | VLESS / TCP / REALITY | 8449 | Responsive |
| 6 | VLESS / TCP / REALITY | 8446 | Responsive |
| 7 | VLESS / TCP / REALITY | 6101 | Responsive |
| 8 | VLESS / TCP / REALITY | 8447 | Responsive |
| 9 | VLESS / WS / TLS | 2054 | Responsive |
| 10 | VLESS / WS / TLS | 2055 | Responsive |
| 11 | VLESS / WS / TLS | 8448 | Responsive |
| 12 | VLESS / XHTTP / TLS | 443 | Inconsistent |

## Route Family Snapshot

| Route family | Best use | Common risk | Practical status |
|---|---|---|---|
| DNS tunnel plus UDP relay | Full-device Android and call-like traffic when DNS paths survive | Endpoint visibility and resolver behavior | Strong private field signal |
| Direct TLS camouflage | Fast ordinary-filtering route | Endpoint or provider reputation | Useful fast branch |
| WebSocket/TLS CDN | Common-client compatibility with CDN indirection | Old WebSocket fingerprints and path mismatch | Practical, needs careful setup |
| XHTTP-style transport | Newer HTTP-shaped experiments | Uneven client support | Staged experiment |
| CDN edge comparison | Per-operator edge behavior testing | Candidate edges age quickly | Use as a measurement method |
| Google/API relay | Whitelist-like periods where selected platforms remain reachable | Quotas, latency, account risk | Useful fallback research |
| Domestic-service/WebRTC relay | Web and messaging in whitelist-like states | Metadata exposure and unstable calls | Emergency web/messaging branch |
| Fragmentation or DPI desync | Lab testing against traffic classification | Platform privileges and version drift | Lab-only unless common clients support it |

## Tools

Run only against endpoints you own or are explicitly authorized to test.

```bash
python tools/connectivity_probe.py --hostname EXAMPLE_HOSTNAME --route-family "WebSocket/TLS CDN"
```

```bash
python tools/cloudflare_edge_probe.py --hostname EXAMPLE_HOSTNAME --ip EXAMPLE_CDN_EDGE_IP
```

```bash
python tools/result_summarizer.py data/examples/sanitized-results.json data/examples/sanitized-scenarios.json
```

```bash
python tools/validate_examples.py data/examples
```

```bash
python tools/redaction_scan.py .
```

## Evidence Labels

| Label | Meaning |
|---|---|
| Confirmed from project field notes | Observed in private field work, then rewritten as public route-family guidance |
| Confirmed from public source | Supported by public measurement data, upstream documentation, or source behavior |
| Inference | Engineering conclusion from protocol behavior or repeated observations |
| Unverified field report | Reported but not independently repeated |
| Unknown | Not enough evidence |

## Repository Map

| Path | Purpose |
|---|---|
| `docs/` | Technical overview, mechanisms, route-family analysis, public sources, schema, open questions |
| `guides/` | Field testing, route selection, practical operating workflow, user readiness |
| `templates/` | Placeholder profiles, test matrices, report templates |
| `tools/` | Local diagnostics, example validation, redaction checks |
| `data/examples/` | Sanitized sample outputs |

## Scope

This project documents methods, route families, and measurement workflows. It does not publish live deployments.

Tor-dependent workflows are out of scope; see [the scope note](docs/12-no-tor-scope-note.md).

## Contributing

Good contributions are specific, evidence-labeled, and practical:

- A sanitized field report.
- A client compatibility correction.
- A route-family failure analysis.
- A safer diagnostic workflow.
- A clearer explanation for people outside Iran.

Before submitting, run:

```bash
python tools/redaction_scan.py .
python tools/validate_examples.py data/examples
python -m unittest discover -s tests
python -m py_compile tools/*.py
```
