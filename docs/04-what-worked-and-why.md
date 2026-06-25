# What Worked And Why

## DNS Tunnel Plus UDP Relay

Evidence: Confirmed from project field notes.

Why it worked:

- It provided full-device Android behavior in the private field notes.
- It supported call-like traffic better than the other tested private routes.
- It used a path that was not equivalent to a normal direct TLS proxy.

Main limitation:

- The visible endpoint can still be the direct private server unless a resolver or relay is actually in the path.

Public lesson:

- DNS-shaped transport can be valuable, but endpoint visibility and resolver behavior must be measured explicitly.

## Direct TLS Camouflage

Evidence: Confirmed from project field notes.

Why it worked:

- Low overhead.
- Good support in common Xray-compatible clients.
- Stronger camouflage than older obvious proxy handshakes when configured well.

Main limitation:

- It does not hide provider or endpoint reputation.

Public lesson:

- Fast does not mean hard to block. It may be the right route during ordinary filtering and the wrong route during provider-prefix blocking.

## WebSocket/TLS CDN Route

Evidence: Confirmed from project field notes and inference from CDN behavior.

Why it worked:

- Common clients can import it.
- CDN edge can hide origin from the access ISP when the CDN is truly in the path.
- Host, SNI, and path can be separated from the origin address.

Main limitation:

- Old WebSocket proxy shapes are widely studied. Origin protection and fallback behavior matter.

Public lesson:

- CDN route quality is not only protocol choice. It includes hostname strategy, edge selection, origin locking, path hygiene, and fallback site behavior.

## Domestic-Service/WebRTC Relay

Evidence: Confirmed from project field notes.

Why it worked:

- The access network saw domestic-service or WebRTC-style traffic rather than a direct private server endpoint.
- It carried basic web and messaging traffic in a private test.

Main limitation:

- It did not pass real-time calling reliably in that test.
- It has account, metadata, and trust risks.

Public lesson:

- Whitelist-survival routes can be useful but should be labeled honestly by capability: web, messaging, or calls.
