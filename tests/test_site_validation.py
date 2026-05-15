import unittest
from pathlib import Path

from scripts.validate_site import (
    validate_home,
    validate_security,
    validate_signers,
    validate_global_no_forbidden_repo,
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


if __name__ == "__main__":
    unittest.main()
