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

The practical product is a shared companion plus five signer families:

- Raspberry/Pi Stateless QR Vault for air-gapped RAM-only review and signing.
- ESP32 Stateless QR Vault for smaller self-contained camera/display devices.
- ESP32 USB/NIP-46 Signer for daily desktop use, with Classic ESP32/TTGO as a
  compatibility target where feasible.
- JavaCard/NFC Smartcard Signer for compact secure-element custody without
  trusted event review by itself.
- Custom Nostr Hardware Wallet With Persistent Secret for later TROPIC01,
  custom PCB, and Trezor Safe 7 firmware research.

The site should show these as one ecosystem, not as unrelated experiments.

Account/custody copy should stay precise: QR vaults are stateless RAM-only
session signers; ESP32 USB/NIP-46 and custom hardware-wallet lines are future
persistent encrypted device-vault signers; smartcards are display-less
slot-backed custody; companion is secretless routing and verification
infrastructure. Policy records are internal NostrSeal records, not Nostr
events, and the final per-account policy UX is still under design.

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
