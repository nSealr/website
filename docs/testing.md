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
- Local stylesheet and asset references resolve.
- Unsupported production security claims are rejected.

## Required Tests

- Static site build.
- Link check.
- Content lint.
- No broken repository links.
- Security and maturity claims checked against `NostrSeal/lab`.

The site remains private until publication is explicitly approved.
