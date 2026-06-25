# Cloudflare And CDN Edge Notes

This document discusses CDN behavior in generic terms. It does not publish private zones, hostnames, origin addresses, or edge lists.

## CDN Is Not One Feature

Inference: A CDN-based route can fail or succeed because of any of these independent factors:

- Hostname reputation.
- Orange-cloud versus DNS-only behavior.
- Origin protection.
- WebSocket support.
- HTTP version negotiation.
- Edge IP quality on a specific ISP.
- TLS mode and certificate behavior.
- Fallback site realism.
- Path design.
- Firewall and origin allowlist policy.

## Clean Edge Testing

Evidence: Unverified field report plus local planning.

Some field reports claim that specific CDN edge addresses behave better on some Iranian operators. Public documentation should not publish edge lists as universal answers.

Safe public method:

1. Use only a hostname you own.
2. Test only explicit edge candidates you have authorization to test.
3. Keep SNI and Host set to `EXAMPLE_HOSTNAME`.
4. Record ISP, network type, timestamp, TCP, TLS, HTTP, and proxy-stage results.
5. Promote an edge only if it beats hostname-only behavior for the same tester and network.

## Worker And Tunnel Caveats

Inference:

- Worker-style routing is useful for HTTP-like paths but is not a generic raw TCP front.
- Tunnel-style routes can hide origin exposure but may have recognizable behavior if overused or poorly configured.
- A fallback website that behaves like a real site can reduce active-probing risk compared with a dead or obviously fake origin.

## Change Classification

| Change type | Public repo action | Live deployment action |
|---|---|---|
| Document hostname strategy | Safe | No live change |
| Plan separate hostnames by route family | Safe | Requires DNS approval later |
| Test clean edge candidates | Safe only on owned hostnames | Requires explicit candidate list |
| Change CDN settings | Document only | Requires dashboard or API approval |
| Change origin firewall | Document only | Requires production approval |
