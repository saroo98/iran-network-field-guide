# Iran Network Field Guide

Public field guide for understanding, testing, and discussing internet disruption and censorship in Iran without publishing live infrastructure details.

This repository is built from sanitized project notes, field observations, and public research synthesis. It does not contain active server addresses, domains, credentials, subscription links, QR codes, private logs, cookies, account identifiers, or provider-specific operational details.

## Purpose

Iran's connectivity problems are not one problem. Different users can see different failures on the same day depending on operator, city, network type, time window, protocol, endpoint reputation, DNS path, UDP handling, CDN edge, and client app behavior.

This repo is meant to help people outside Iran understand what is being observed and help testers inside Iran collect safe, comparable results.

## Evidence Labels

Claims in this repo use these labels:

- Confirmed from project field notes: observed in the private project notes, then rewritten without live identifiers.
- Confirmed from upstream source/docs: based on upstream project documentation or source-code behavior.
- Inference: engineering conclusion from known protocol behavior or multiple observations.
- Unverified field report: reported by testers or public posts but not independently repeated.
- Unknown: not enough evidence.

## What Is In Scope

- Censorship and failure-mode taxonomy.
- Route-family analysis, not private route disclosure.
- Client compatibility notes for common Android and desktop proxy apps.
- Cloudflare/CDN edge behavior as a design and testing topic.
- DNS, UDP, QUIC, TLS, WebSocket, XHTTP, traffic fingerprinting, fragmentation, and active-probing concepts.
- Public-safe diagnostic scripts that test only endpoints owned or explicitly authorized by the person running them.

## What Is Out Of Scope

- Live endpoints, domains, account names, provider names, credentials, UUIDs, keys, cookies, subscription links, QR codes, and private user logs.
- Instructions for Tor or Tor-dependent systems.
- Mass scanning, third-party endpoint testing, or publication of bypass profiles for live private infrastructure.

## Repository Map

- `docs/`: technical overview and synthesis.
- `guides/`: practical testing and reporting guides.
- `templates/`: placeholders for safe examples and planning.
- `tools/`: local diagnostic scripts.
- `data/examples/`: sanitized sample outputs.
- `.github/`: issue templates and local validation workflow.

## Safe Starting Points

1. Read `docs/01-iran-internet-overview.md`.
2. Read `docs/00-source-and-safety-method.md` to understand how private material was sanitized.
3. Use `docs/13-route-family-matrix.md` and `guides/choosing-a-route-family.md` to match symptoms to route families.
4. Use `guides/testing-from-iran.md` for a safe test workflow.
5. Use `tools/connectivity_probe.py` only on hostnames you own or are authorized to test.

## Public Safety Rule

If a value could let someone identify, block, probe, hijack, or burn a real deployment, do not publish it. Use placeholders such as `EXAMPLE_HOSTNAME`, `EXAMPLE_IP`, `EXAMPLE_UUID`, and `EXAMPLE_PATH`.
