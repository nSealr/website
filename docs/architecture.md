# Architecture

`NostrSeal/website` is the public-facing documentation and project site.

## Responsibilities

- Explain NostrSeal clearly.
- Present product shape and maturity honestly.
- Link to specs, companion, Raspberry, ESP32, smartcard, hardware, and lab work.
- Publish security model and build status when public.

## Non-Responsibilities

- No private planning notes.
- No unverifiable production claims.
- No replacement for canonical specs or lab research.

Astro is the default static-site candidate for the first implementation.

## Implemented Foundation

The first implementation is plain static HTML/CSS:

- `public/index.html`: documentation-first landing page.
- `public/styles.css`: responsive layout and system-map styling.
- `scripts/validate_site.py`: required-content, local-link, and unsupported
  security-claim checks.

This keeps publishing simple while the project is private and the content model
is still stabilizing. A later Astro migration should preserve the same content
tests before adding routing, MDX, or generated status pages.
