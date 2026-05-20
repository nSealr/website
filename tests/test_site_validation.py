import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.validate_site import (
    validate_home,
    validate_security,
    validate_signers,
    validate_global_no_forbidden_repo,
    validate_global_no_stale_cli_commands,
    parse_required_text_from_frontmatter,
)


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SIGNERS = ROOT / "src" / "content" / "signers"


@unittest.skipUnless(DIST.exists(), "dist/ not built; run `pnpm run build` first")
class WebsiteValidationTests(unittest.TestCase):
    def test_home_required_text(self) -> None:
        validate_home(DIST)

    def test_security_required_text(self) -> None:
        validate_security(DIST)

    def test_signers_required_text(self) -> None:
        validate_signers(DIST)

    def test_no_forbidden_repo_links(self) -> None:
        validate_global_no_forbidden_repo(DIST)

    def test_no_stale_cli_commands(self) -> None:
        validate_global_no_stale_cli_commands(DIST)


class FrontmatterParserTests(unittest.TestCase):
    def test_each_signer_declares_required_text(self) -> None:
        for mdx in SIGNERS.glob("*.mdx"):
            with self.subTest(file=mdx.name):
                self.assertTrue(
                    parse_required_text_from_frontmatter(mdx),
                    f"{mdx.name} has empty requiredText",
                )

    def test_five_signer_files_present(self) -> None:
        names = {p.stem for p in SIGNERS.glob("*.mdx")}
        self.assertEqual(
            names,
            {"raspberry-qr", "esp32-qr", "esp32-usb", "smartcard", "custom-wallet"},
        )


class StaleCliCommandTests(unittest.TestCase):
    def test_rejects_legacy_companion_commands(self) -> None:
        forbidden = [
            "nsealr route --request req.json --signer raspberry-qr",
            "nsealr verify --request req.json --response resp.json",
            "nsealr request --kind 1 --content hello",
            "nsealr request validate --file req.json",
            "nsealr audit export --request req.json",
            "nsealr signers list",
            "nsealr contracts list",
            "nsealr fixture verify --route esp32-usb --fixture sign-event-disabled",
            "nsealr nip46 decide --payload-file decrypted.json",
        ]
        for snippet in forbidden:
            with self.subTest(snippet=snippet), TemporaryDirectory() as tmp:
                page = Path(tmp) / "index.html"
                page.write_text(f"<html><body><code>{snippet}</code></body></html>", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "stale companion CLI command"):
                    validate_global_no_stale_cli_commands(Path(tmp))

    def test_allows_current_companion_commands(self) -> None:
        allowed = [
            "nsealr request sign-event --event-template event.json --out req.json",
            "nsealr review-request --request req.json --screen-review --out review.json",
            "nsealr verify-response --request req.json --response resp.json",
            "nsealr fixture verify --specs ../specs",
            "nsealr serial-line exchange --port /dev/cu.usbmodem1101 --request req.json",
            "nsealr nip46 decide --message decrypted.json --permissions sign_event:1",
        ]
        with TemporaryDirectory() as tmp:
            page = Path(tmp) / "index.html"
            page.write_text(
                "<html><body>"
                + "\n".join(f"<code>{snippet}</code>" for snippet in allowed)
                + "</body></html>",
                encoding="utf-8",
            )
            validate_global_no_stale_cli_commands(Path(tmp))


if __name__ == "__main__":
    unittest.main()
