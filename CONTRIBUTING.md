# Contributing

Contributions are welcome if they preserve user safety and evidence quality.

## Before Opening A Pull Request

- Remove live endpoints, account identifiers, credentials, cookies, import links, QR codes, and private user data.
- Replace deployment-specific values with placeholders.
- Label claims using the evidence labels from the README.
- Avoid instructions for Tor or Tor-dependent workflows.
- Keep examples small and test only owned or authorized endpoints.
- Run the redaction and syntax checks described in `guides/collecting-safe-field-reports.md`.

## Good Contributions

- A sanitized field report that uses the template in `templates/field-report-template.md`.
- A compatibility note for a common client app.
- A diagnostic result summary with endpoint values replaced by placeholders.
- A correction that distinguishes confirmed facts from inference.

## Not Accepted

- Live private profiles.
- Working profile bundles or import links.
- Real user identifiers.
- Endpoint lists collected by scanning third parties.
- Provider-specific private deployment details.
