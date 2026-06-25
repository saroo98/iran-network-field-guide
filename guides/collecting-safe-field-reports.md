# Collecting Safe Field Reports

## Minimum Useful Fields

- Date and approximate local time.
- ISP or operator.
- Region, if safe.
- Network type.
- Route family.
- Client app and version.
- DNS result.
- TCP result.
- TLS result.
- HTTP fallback status.
- UDP or HTTP/3 result, if relevant.
- Proxy or app result, if safe.
- User-visible behavior.
- Error stage.

## Redaction Checklist

Remove:

- Active endpoint values.
- Real hostnames or paths.
- Client import material.
- QR codes.
- Cookies and account identifiers.
- Private logs with user identifiers.
- Provider-specific deployment names.
- User names or contact details.

Replace with:

- `EXAMPLE_HOSTNAME`
- `EXAMPLE_IP`
- `EXAMPLE_PATH`
- `EXAMPLE_CLIENT_PROFILE`
- `EXAMPLE_ISP`
- `EXAMPLE_REGION`

## Local Checks

From the public repo root:

```bash
python tools/redaction_scan.py .
python -m py_compile tools/*.py
python tools/result_summarizer.py data/examples/sanitized-results.json
```

If a redaction scan reports a high-risk hit, remove the value before sharing.
