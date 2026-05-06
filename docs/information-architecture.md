# Information Architecture

## Top Navigation

- Overview
- Use
- Build
- Security
- Developers
- Roadmap

## Overview

Purpose: explain the project in one page.

Required content:

- open-source and non-profit positioning;
- companion plus signer ecosystem model;
- current prototype status;
- links to GitHub organization and lab research.

## Use

Purpose: explain how a future user will interact with NostrSeal.

Required content:

- Nostr client requests a signature;
- companion normalizes, transports, and verifies requests;
- signer reviews or enforces policy;
- signed event returns to the client or relay workflow.

## Build

Purpose: turn the project into reproducible hardware/software.

Required content:

- vault build path;
- ESP32-S3 build path;
- smartcard test path;
- hardware assembly path;
- firmware flashing and verification notes.

## Security

Purpose: make trust boundaries explicit.

Required content:

- key custody model;
- trusted display limits;
- host compromise model;
- firmware/update model;
- known open questions.

## Developers

Purpose: help external implementers reuse the work.

Required content:

- specs and test vectors;
- transport adapters;
- event canonicalization;
- BIP-340 signing vectors;
- compatibility notes for NIP-46 and NIP-07 bridges.

## Roadmap

Purpose: show maturity without overclaiming.

Required content:

- planned phases;
- active repos;
- blocked research;
- go/no-go gates for each signer line.
