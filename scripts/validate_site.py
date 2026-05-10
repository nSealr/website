#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_TEXT = [
    "NostrSeal",
    "open-source",
    "non-profit",
    "Companion",
    "Raspberry",
    "ESP32",
    "Smartcard",
    "Hardware",
    "approval_digest",
    "signing_disabled",
    "NIP-46 bridge decisions",
    "nseal nip46 decide",
    "request-bound capture checks",
    "review detail pages",
    "T-Display S3 review scenario smoke",
    "companion-to-device serial smoke",
    "Raspberry/Pi kit requirements",
    "Raspberry/Pi OS profile",
    "nseal-smartcard CLI probes",
    "no trusted review or real-card compatibility claim",
    "No production security claim",
]

FORBIDDEN_CLAIMS = [
    "production ready",
    "military-grade",
    "unhackable",
    "guaranteed secure",
    "most secure",
]


def _local_refs(html: str, attribute: str) -> list[str]:
    pattern = re.compile(rf'{attribute}="([^":#][^"]*)"', re.IGNORECASE)
    return [match.group(1) for match in pattern.finditer(html)]


def validate_site(public_root: Path) -> None:
    index = public_root / "index.html"
    if not index.exists():
        raise ValueError("public/index.html is required")
    html = index.read_text(encoding="utf-8")
    lower_html = html.lower()
    for text in REQUIRED_TEXT:
        if text not in html:
            raise ValueError(f"missing required text: {text}")
    for claim in FORBIDDEN_CLAIMS:
        if claim in lower_html:
            raise ValueError(f"forbidden unsupported claim: {claim}")
    for rel in _local_refs(html, "href") + _local_refs(html, "src"):
        if rel.startswith(("https://", "http://", "mailto:")):
            continue
        path = public_root / rel
        if not path.exists():
            raise ValueError(f"broken local asset reference: {rel}")


def main() -> int:
    validate_site(ROOT / "public")
    print("NostrSeal website validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
