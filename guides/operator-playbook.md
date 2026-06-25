# Operator Playbook

Use this playbook when deciding whether a route family is ready for wider use. It is written for public-safe planning and comparison, not for publishing live values.

## Route-Family Workflow

1. Identify the current network state using [Iran Internet Overview](../docs/01-iran-internet-overview.md).
2. Pick one control branch and one candidate branch from [Choosing A Route Family](choosing-a-route-family.md).
3. Run the same staged test on both branches using [Testing From Iran](testing-from-iran.md).
4. Record the same fields for each branch: operator, network type, client app, client version, DNS, TCP, TLS, HTTP, UDP or HTTP/3, proxy/app result, and user-visible behavior.
5. Compare the candidate against the control for the same tester, same network, and same time window.
6. Promote only after repeated field signals show the same improvement across more than one tester, operator, or time window.

## Promotion Rules

| Promote when | Practical meaning |
|---|---|
| The candidate beats the control at the same failure stage | It solves a measured problem, not a guessed problem |
| Client import and export preserve required fields | The route can survive real user setup |
| User-visible behavior matches the route label | A messaging branch is not mislabeled as call-capable |
| The route has a fallback branch | One failure does not leave the user with no path |
| Reports are sanitized and repeatable | Results can be discussed without exposing live values |

## Reject Rules

Reject or keep as lab-only when:

- The client connects but web, messaging, upload, or call behavior fails.
- The target app drops fields the route requires.
- Only one tester confirms it.
- Call support is claimed without a short controlled call test.
- A UDP-heavy route has no TCP fallback.
- The route only works outside Iran.
- The test cannot identify the failure stage.
- The route needs privileged packet handling that normal users cannot operate safely.

## Reader-Facing Labels

Use labels that set expectations:

| Label | Use when |
|---|---|
| Primary | Repeated field results show broad usability |
| Fast fallback | It is fast during ordinary filtering but may fail during stricter periods |
| CDN branch | CDN behavior is part of the path and must be monitored separately |
| Messaging-only | Web and messaging work, but calls or uploads are not proven |
| Emergency | Useful in whitelist-like periods with clear tradeoffs |
| Lab-only | Requires special clients, exact versions, or fragile packet behavior |

## Minimum Release Note

Before a route family is recommended to testers, write a public-safe note with:

- Route family.
- Intended client app and version.
- Expected behavior.
- Known failure label.
- Fallback branch.
- Stop-testing rule.
- Evidence label.

Do not use screenshots as the primary evidence. Use the staged fields so the result can be compared later.
