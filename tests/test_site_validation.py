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


if __name__ == "__main__":
    unittest.main()
