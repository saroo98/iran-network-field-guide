# Distribution And Burn Risk

## Why Distribution Hygiene Matters

Inference: A technically strong route can fail quickly if it is distributed too broadly, posted publicly, or reused across unrelated user groups.

## Safer Practices

- Use cohort-specific profiles.
- Avoid publishing live import links.
- Avoid sharing screenshots that contain endpoint fields.
- Keep route families separate so one burned hostname does not burn every path.
- Rotate only with a documented reason and user migration plan.
- Label routes by capability: primary, fast fallback, messaging-only, lab-only, emergency.

## Public Reporting Rules

Public-safe reports should keep:

- ISP or operator as `EXAMPLE_ISP` if sensitive.
- Region as `EXAMPLE_REGION` if sensitive.
- Route family, not private route name.
- Error stage.
- Client app and version.
- Sanitized timestamps if exact timing is risky.

Public reports should remove:

- Endpoint values.
- Account identifiers.
- Client import material.
- User-specific profile names.
- Cookies and logs with identifiers.
