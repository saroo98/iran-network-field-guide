# Source And Safety Method

This repository is a public-safe synthesis. It is not a mirror of the private working folder.

## Private Source Categories Reviewed

| Private source category | Type | Public-safe? | Contains sensitive details? | Use in this repo? | Notes |
|---|---|---|---|---|---|
| Local status and context notes | Operational docs | No | Yes | Synthesized only | Converted to route-family language. |
| Research reports | Research docs | Partly | Sometimes | Synthesized only | Claims are evidence-labeled. |
| Field test logs | Logs | No | Yes | Aggregated only | User-visible outcomes are summarized without identifiers. |
| Lab templates | Config examples | Partly | Sometimes | Rewritten | Public templates use placeholders only. |
| Diagnostic scripts | Tools | Partly | Sometimes | Rewritten | Public tools avoid private defaults. |
| Secret-bearing folder | Credentials and profiles | No | Yes | Excluded | Not copied, not summarized by value. |
| Cookies and raw relay logs | Runtime artifacts | No | Yes | Excluded | Only high-level behavior is described. |
| Upstream research repository | Source/docs | Partly | No private deployment details | Referenced conceptually | Used for compatibility and architecture evidence. |

## Conversion Rules

- Private route names became route-family names.
- Endpoint values became placeholders.
- Provider-specific details were removed.
- Profile import material was not copied.
- Private logs were summarized by behavior and failure stage.
- Unverified field reports stayed labeled as unverified.
- Inferences are labeled as inferences.

## Publication Boundary

The public repo may say:

- A DNS tunnel plus UDP relay was useful in private field notes.
- A domestic-service relay carried web and messaging but not reliable calls in one private test.
- CDN edge behavior may vary by operator.
- Client compatibility differs by app and core version.

The public repo must not say:

- Which active endpoint, account, provider, profile, route name, path, key, or user cohort was used.
- Which live clean edge candidates were tested.
- Which exact private profile or import material exists.
