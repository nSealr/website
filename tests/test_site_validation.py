import unittest
from pathlib import Path

from scripts.validate_site import validate_site


ROOT = Path(__file__).resolve().parents[1]


class WebsiteValidationTests(unittest.TestCase):
    def test_static_site_is_valid(self) -> None:
        validate_site(ROOT / "public")

    def test_static_site_names_current_safety_contracts(self) -> None:
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")

        self.assertIn("approval_digest", html)
        self.assertIn("signing_disabled", html)
        self.assertIn("NIP-46 bridge decisions", html)
        self.assertIn("nseal nip46 decide", html)
        self.assertIn("nseal serial-line exchange", html)
        self.assertIn("sign-event-disabled smoke", html)
        self.assertIn("firmware protocol evidence", html)
        self.assertIn("Unicode fallback", html)
        self.assertIn("review detail pages", html)
        self.assertIn("T-Display S3 review scenario smoke", html)
        self.assertIn("Raspberry/Pi kit requirements", html)
        self.assertIn("Raspberry/Pi OS profile", html)

    def test_static_site_names_five_first_class_signer_families(self) -> None:
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")

        for family in (
            "Raspberry/Pi Stateless QR Vault",
            "ESP32 Stateless QR Vault",
            "ESP32 USB/NIP-46 Signer",
            "JavaCard/NFC Smartcard Signer",
            "Custom Nostr Hardware Wallet With Persistent Secret",
        ):
            with self.subTest(family=family):
                self.assertIn(family, html)

    def test_static_site_links_to_raspberry_repo_not_old_vault_repo(self) -> None:
        html = (ROOT / "public/index.html").read_text(encoding="utf-8")

        self.assertIn("https://github.com/NostrSeal/raspberry", html)
        old_repo_url = "https://github.com/NostrSeal/" + "vault"
        self.assertNotIn(old_repo_url, html)


if __name__ == "__main__":
    unittest.main()
