# NostrSeal Website

Public website and documentation hub for NostrSeal.

The website should explain the project without turning the core work into a
proprietary product. It should make the open-source hardware/software program
understandable, reproducible, and easy to join.

## Goals

- Present NostrSeal as a non-profit open-source signer ecosystem.
- Explain the main product shape: companion software plus multiple signer
  implementations.
- Publish status pages for each hardware line.
- Link to specs, lab research, firmware, hardware, and smartcard work.
- Host build guides, security notes, and release documentation.
- Avoid marketing claims before prototypes are independently tested.

## Initial Site Sections

- `Overview`: what NostrSeal is and why hardware signing matters for Nostr.
- `Use`: how users will connect a client, companion, and signer.
- `Build`: reproducible build guides for each hardware line.
- `Security`: threat model, trust boundaries, and known limitations.
- `Roadmap`: current maturity of companion, vault, ESP32, smartcard, and hardware.
- `Developers`: specs, test vectors, transports, and contribution paths.

## Candidate Stack

Astro is the default candidate for the first implementation because the site is
mostly static, documentation-heavy, and can later publish from GitHub Pages or a
simple static host.

Final stack selection should happen after the content model is stable.

## Initial Layout

- `docs/`: site plan, information architecture, design notes, and publishing
  decisions.
- `content/`: future Markdown/MDX source content.
- `public/`: static assets.
- `design/`: brand, typography, and visual references.

## Related Repositories

- `NostrSeal/lab`: source-backed research and roadmap.
- `NostrSeal/specs`: shared protocol and test vectors.
- `NostrSeal/companion`: host-side companion software.
- `NostrSeal/vault`: Pi Zero / SeedSigner-style QR vault.
- `NostrSeal/esp32`: ESP32 firmware targets.
- `NostrSeal/smartcard`: JavaCard/NFC/contact smartcard signer work.
- `NostrSeal/hardware`: open hardware designs and assembly docs.

## Quality Baseline

Run the repository verification loop with:

```sh
make ci
```

## License

Website code is released under the MIT License unless a file says otherwise.
Website content is intended to be released under CC0-1.0 when the project is
ready for publication.
