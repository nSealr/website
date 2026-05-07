# NostrSeal Website

Public website and documentation hub for NostrSeal.

The website should explain the project without turning the core work into a
proprietary product. It should make the open-source hardware/software program
understandable, reproducible, and easy to join.

## Goals

- Present NostrSeal as a non-profit open-source signer ecosystem.
- Explain the main product shape: companion software plus multiple signer
  implementations.
- Publish status pages for each first-class signer family and supporting
  infrastructure track.
- Link to specs, lab research, firmware, hardware, and smartcard work.
- Host build guides, security notes, and release documentation.
- Avoid marketing claims before prototypes are independently tested.

## Initial Site Sections

- `Overview`: what NostrSeal is and why hardware signing matters for Nostr.
- `Use`: how users will connect a client, companion, and signer.
- `Build`: reproducible build guides for each hardware line.
- `Security`: threat model, trust boundaries, and known limitations.
- `Roadmap`: current maturity of companion, Raspberry/Pi stateless QR, ESP32
  stateless QR, ESP32 USB/NIP-46, smartcard, custom hardware-wallet, and
  hardware artifact work.
- `Developers`: specs, test vectors, transports, and contribution paths.

## Current Capabilities

- Static first page under `public/index.html`.
- System-map visual explaining client, companion, and signer lines.
- Honest maturity status for specs, companion, Raspberry/Pi, ESP32, smartcard,
  custom hardware-wallet, and hardware work.
- Site validation script that checks required text, local asset links, and
  unsupported production security claims.

## Candidate Stack

Astro is the default candidate for the first implementation because the site is
mostly static, documentation-heavy, and can later publish from GitHub Pages or a
simple static host.

Final framework selection should happen after the content model is stable. The
current foundation is plain static HTML/CSS to avoid introducing build
complexity too early.

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
- `NostrSeal/raspberry`: Raspberry/Pi software for the stateless QR vault
  family.
- `NostrSeal/esp32`: ESP32 firmware for stateless QR and USB/NIP-46 families.
- `NostrSeal/smartcard`: JavaCard/NFC/contact smartcard signer work.
- `NostrSeal/hardware`: open hardware designs and assembly docs.

## Quality Baseline

Run the repository verification loop with:

```sh
make ci
```

Open `public/index.html` directly in a browser to inspect the current static
site.

## License

Website code is released under the MIT License unless a file says otherwise.
Website content is intended to be released under CC0-1.0 when the project is
ready for publication.
