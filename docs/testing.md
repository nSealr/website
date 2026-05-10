# Testing

## Current Baseline

```sh
make ci
```

The baseline runs repository verification, site validation tests, bytecode
compilation, and direct site validation.

## Implemented Tests

- `public/index.html` exists.
- Required project, status, and security-boundary text is present.
- Current safety-contract text mentions `approval_digest` and
  `signing_disabled`.
- Current companion boundary text mentions NIP-46 bridge decisions and
  `nseal nip46 decide`.
- Current shared-review and hardware status text mentions review detail pages
  and Raspberry/Pi kit requirements.
- Local stylesheet and asset references resolve.
- Unsupported production security claims are rejected.

## Required Tests

- Static site build.
- Link check.
- Content lint.
- No broken repository links.
- Security and maturity claims checked against `NostrSeal/lab`.

The site remains private until publication is explicitly approved.
