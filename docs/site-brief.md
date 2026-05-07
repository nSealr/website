# Site Brief

## Audience

- Nostr users who want safer private-key custody.
- Developers integrating Nostr signers into clients.
- Builders who want to assemble or modify open hardware.
- Security reviewers evaluating threat models and firmware behavior.

## Primary Message

NostrSeal is not a closed hardware wallet product. It is an open, reproducible
program for Nostr signing devices, companion software, shared specs, and build
documentation.

## Product Narrative

The practical product is a shared companion plus several signer forms:

- QR vault for air-gapped review and signing.
- ESP32-S3 USB/NIP-46 signer for daily desktop use.
- ESP32-S3 QR signer for smaller self-contained devices.
- Classic ESP32/TTGO compatibility target where feasible.
- JavaCard/NFC/contact smartcard line for compact secure-element custody.
- TROPIC01 research and possible embedded hardening through the ESP32 line.

The site should show these as one ecosystem, not as unrelated experiments.

## Trust Claims

Allowed:

- keys should not be exposed to ordinary Nostr clients;
- sensitive signing should require explicit user review where hardware allows it;
- the companion is not trusted with key custody;
- maturity differs by signer line.

Avoid until verified:

- production-ready security claims;
- secure-element guarantees without hardware tests;
- claims that a display-less smartcard provides trusted event review;
- claims that TROPIC01 directly signs Nostr/BIP-340.

## First Release Content

- Homepage with project overview and current maturity state.
- Current safety-contract wording for `approval_digest` and
  `signing_disabled` so the public site does not overstate maturity.
- Hardware line comparison page.
- Companion overview page.
- Security model page.
- Build status page linking to each implementation repo.
- Contribution page.
