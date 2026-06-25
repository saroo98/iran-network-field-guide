# Choosing A Route Family

Use this guide after identifying the failure stage. For promotion, rejection, and user-readiness rules, use the [operator playbook](operator-playbook.md).

## Symptom-To-Route Guide

| Symptom | First route families to compare | Notes |
|---|---|---|
| Direct TLS connects fast on one network but fails on another | Direct TLS camouflage, provider-diverse direct route | Could be endpoint reputation or provider blocking |
| Hostname resolves but TLS fails | TLS camouflage, real fallback site, CDN route | Check SNI and certificate behavior |
| CDN hostname works for fallback page but proxy fails | WebSocket/TLS CDN, XHTTP, origin protection | Path, Host, and upgrade behavior matter |
| UDP routes fail immediately | TCP-based routes | Do not assume QUIC availability |
| Web works but uploads stall | Clean edge comparison, fragmentation lab, MTU-sensitive routes | Label as grey connection until repeated |
| Messaging works but calls fail | DNS tunnel plus UDP relay, domestic-service relay | Do not call a web route call-capable |
| Foreign endpoints mostly unreachable but selected platforms work | Google/API relay, domestic-service relay | Expect quota, account, and metadata tradeoffs |

## Practical Route Stack

Inference: A resilient setup should keep independent branches:

1. A call-capable branch.
2. A fast ordinary-filtering branch.
3. A CDN-fronted branch.
4. A relay/API branch for whitelist-like states.
5. A lab-only branch for advanced DPI experiments.

Do not replace a working branch with an experiment. Test additive candidates first.

## Comparison Rule

Pick one control branch and one candidate branch. Test them from the same network, with the same client app, during the same time window. If the candidate only improves a result from outside Iran or only improves a different failure stage, do not promote it.

## Quick Reject Rules

Reject the route-family and client combination when:

- The app imports the profile but drops fields the route requires.
- The route connects but useful traffic fails.
- A call-capable label is used without a call test.
- UDP behavior is assumed from a TCP-only test.
- The result cannot be repeated by another tester or time window.
