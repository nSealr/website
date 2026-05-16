#!/usr/bin/env python3
"""Validate the built Astro site under dist/.

Asserts that:
  * Required home strings appear on dist/index.html.
  * Each signer family page contains its declared `requiredText` phrases.
  * The /docs/security/trust-boundaries/ page contains the safety-contract phrases.
  * No forbidden production claims appear anywhere in dist/.
  * No forbidden /vault repository link appears anywhere in dist/.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SIGNERS_SRC = ROOT / "src" / "content" / "signers"


HOME_REQUIRED_TEXT = [
    "nSealr",
    "open-source",
    "non-profit",
    "Companion",
    "Raspberry",
    "ESP32",
    "Smartcard",
    "Hardware",
    "Raspberry/Pi Stateless QR Vault",
    "ESP32 Stateless QR Vault",
    "ESP32 USB/NIP-46 Signer",
    "JavaCard/NFC Smartcard Signer",
    "Custom Nostr Hardware Wallet With Persistent Secret",
    "approval_digest",
    "signing_disabled",
    "NIP-46 bridge decisions",
    "nsealr nip46 decide",
    "request-bound capture checks",
    "nsealr serial-line exchange",
    "sign-event-disabled smoke",
    "review detail pages",
    "T-Display S3 review scenario smoke",
    "companion-to-device serial smoke",
    "firmware protocol evidence",
    "Unicode fallback",
    "Raspberry/Pi kit requirements",
    "Raspberry/Pi OS profile",
    "nsealr-smartcard CLI probes",
    "no trusted review or real-card compatibility claim",
    "No production security claim",
]

SECURITY_REQUIRED_TEXT = [
    "approval_digest",
    "signing_disabled",
    "NIP-46 bridge decisions",
    "nsealr nip46 decide",
    "request-bound capture checks",
    "review detail pages",
    "T-Display S3 review scenario smoke",
    "companion-to-device serial smoke",
    "sign-event-disabled smoke",
    "firmware protocol evidence",
    "Unicode fallback",
]

FORBIDDEN_CLAIMS = [
    "production ready",
    "military-grade",
    "unhackable",
    "guaranteed secure",
    "most secure",
]

FORBIDDEN_REPOSITORY_LINK_RE = re.compile(
    r"https://github\.com/[A-Za-z0-9_.-]+/vault(?:[\"/#?]|$)"
)


def read(path: Path) -> str:
    if not path.exists():
        raise ValueError(f"missing built file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def assert_contains_all(html: str, phrases: Iterable[str], page: str) -> None:
    missing = [p for p in phrases if p not in html]
    if missing:
        raise ValueError(f"{page}: missing required text: {missing}")


def assert_forbids_all(html: str, claims: Iterable[str], page: str) -> None:
    lower = html.lower()
    hits = [c for c in claims if c in lower]
    if hits:
        raise ValueError(f"{page}: forbidden unsupported claim: {hits}")


def parse_required_text_from_frontmatter(mdx_path: Path) -> list[str]:
    """Read `requiredText:` list from a signers/*.mdx frontmatter."""
    text = mdx_path.read_text(encoding="utf-8")
    m = re.match(r"---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return []
    block = m.group(1)
    lst_m = re.search(r"requiredText:\s*\n((?:\s+-\s+.*\n?)+)", block)
    if not lst_m:
        return []
    out: list[str] = []
    for line in lst_m.group(1).splitlines():
        item = re.match(r"\s+-\s+(?:'([^']+)'|\"([^\"]+)\"|(.+))", line)
        if item:
            out.append(item.group(1) or item.group(2) or (item.group(3) or "").strip())
    return [s for s in out if s]


def validate_home(dist: Path) -> None:
    html = read(dist / "index.html")
    assert_contains_all(html, HOME_REQUIRED_TEXT, "/")
    assert_forbids_all(html, FORBIDDEN_CLAIMS, "/")
    if FORBIDDEN_REPOSITORY_LINK_RE.search(html):
        raise ValueError("/ contains forbidden /vault github link")


def validate_security(dist: Path) -> None:
    html = read(dist / "docs" / "security" / "trust-boundaries" / "index.html")
    assert_contains_all(html, SECURITY_REQUIRED_TEXT, "/docs/security/trust-boundaries/")
    assert_forbids_all(html, FORBIDDEN_CLAIMS, "/docs/security/trust-boundaries/")


def validate_signers(dist: Path) -> None:
    for mdx in sorted(SIGNERS_SRC.glob("*.mdx")):
        slug = mdx.stem
        page = dist / "docs" / "signers" / slug / "index.html"
        html = read(page)
        required = parse_required_text_from_frontmatter(mdx)
        if not required:
            raise ValueError(f"signers/{slug}.mdx has empty requiredText")
        assert_contains_all(html, required, f"/docs/signers/{slug}/")
        assert_forbids_all(html, FORBIDDEN_CLAIMS, f"/docs/signers/{slug}/")


def validate_global_no_forbidden_repo(dist: Path) -> None:
    for path in dist.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        if FORBIDDEN_REPOSITORY_LINK_RE.search(text):
            raise ValueError(f"{path.relative_to(dist)}: forbidden /vault github link")


def main() -> int:
    if not DIST.exists():
        print("validate_site: dist/ missing — run `pnpm run build` first", file=sys.stderr)
        return 1
    validate_home(DIST)
    validate_security(DIST)
    validate_signers(DIST)
    validate_global_no_forbidden_repo(DIST)
    print("nSealr website validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
