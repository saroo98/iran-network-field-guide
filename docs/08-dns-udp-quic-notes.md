# DNS, UDP, And QUIC Notes

## DNS Tunnels

Evidence: Confirmed from project field notes and upstream source/docs.

DNS-tunnel routes can be valuable where ordinary direct proxy traffic is blocked. They are not magic. The access network can still observe the resolver or endpoint contacted by the client, packet sizes, timing, and DNS-like behavior.

Inference: Resolver-mediated designs can hide the final server from the access ISP's immediate packet view, but the resolver and public delegation still matter.

## UDP And QUIC

Inference: UDP-heavy transports can be fast and resilient on lossy networks when UDP is allowed. They can fail completely when UDP is blocked, deprioritized, or classified.

Testing requirement:

- Test UDP route families separately from TCP route families.
- Record whether the failure is DNS, TCP, TLS, HTTP, UDP, QUIC, proxy handshake, or app behavior.
- Do not promote a route as call-capable unless calls are actually tested.

## HTTP/3

Inference: HTTP/3 availability can vary by network and client. A public HTTPS fallback working over TCP does not prove QUIC works.

The diagnostic scripts in `tools/` keep HTTP/3 optional because local client support varies.

## Public-Source Alignment

Confirmed from public source: OONI's HTTP/3 censorship research shows why HTTP/3 and UDP behavior should be tested independently from HTTPS-over-TCP behavior.

Practical rule: A route family that depends on UDP, QUIC, or HTTP/3 should have a TCP-based comparison branch and a clear failure label when UDP stalls or fails.

See [Public Research Sources](14-public-research-sources.md) for source links.
