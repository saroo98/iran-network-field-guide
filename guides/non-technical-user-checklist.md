# Non-Technical User Checklist

## Good Profile Qualities

- One clear name.
- One import action.
- No manual field editing.
- Clear expected result.
- Clear failure label.
- Known compatible app.
- A simple "stop testing" rule.

## Readiness Checklist

Before a normal user receives a test profile, confirm:

- The intended app and version are known.
- The expected result is written in one sentence.
- The failure label is known.
- A fallback branch exists.
- No manual field editing is required after import.
- The user knows when to stop and report the result.

## Before Sending A Profile

Confirm:

- It uses placeholders in public docs.
- It was tested on the intended client app.
- It does not require hidden advanced settings.
- It has a fallback route if it fails.
- The user knows not to run two VPN apps at the same time unless explicitly instructed.

## What To Ask The Tester

Ask for:

- Operator.
- Network type.
- App name and version.
- Whether it connected.
- Whether a normal webpage opened.
- Whether messaging text worked.
- Whether media upload worked.
- Whether a short call worked, if call capability is being tested.

Do not ask for screenshots that reveal endpoint fields.

## Clear Failure Labels For Users

Use simple labels in user-facing notes:

- `does-not-import`
- `connects-no-web`
- `web-only`
- `upload-stalls`
- `messages-only`
- `calls-fail`
- `works`

Map those notes back to the technical labels in [Testing From Iran](testing-from-iran.md) before publishing a report.
