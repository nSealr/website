# Architecture

`nSealr/website` is the public-facing documentation and project site.

## Responsibilities

- Explain nSealr clearly.
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
- `content/` and `design/`: tracked scaffolds for the future Astro content
  model and design system.

The landing page must name the five first-class signer families explicitly:
Raspberry/Pi Stateless QR Vault, ESP32 Stateless QR Vault, ESP32 USB/NIP-46
Signer, JavaCard/NFC Smartcard Signer, and Custom Nostr Hardware Wallet With
Persistent Secret. This keeps the public product shape aligned with the lab
taxonomy without turning companion, specs, lab, or hardware artifacts into
signing-solution families.

Feature status copy should be derived from `nSealr/specs`
`vectors/features/signer-feature-matrix-v0.json`. The site may simplify the
language, but it must preserve the same distinction between target and current
status and must not imply a feature behaves differently across implementations
when the shared specs matrix assigns the same `contract_id`.

This keeps publishing simple while the project is private and the content model
is still stabilizing. A later Astro migration should preserve the same content
tests before adding routing, MDX, or generated status pages.
