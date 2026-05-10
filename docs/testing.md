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
- Current shared-review and hardware status text mentions review detail pages,
  Raspberry/Pi kit requirements, and the Raspberry/Pi OS profile.
- Current ESP32 status text mentions T-Display S3 review scenario smoke while
  keeping `signing_disabled` present.
- Current smartcard status text mentions `nseal-smartcard` CLI probes while
  preserving the no-trusted-review and no-real-card-compatibility boundary.
- Local stylesheet and asset references resolve.
- Unsupported production security claims are rejected.

## Required Tests

- Static site build.
- Link check.
- Content lint.
- No broken repository links.
- Security and maturity claims checked against `NostrSeal/lab`.

The site remains private until publication is explicitly approved.
