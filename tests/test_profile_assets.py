import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
HERO = ROOT / "assets" / "branding" / "profile-hero.svg"


class ProfileAssetTests(unittest.TestCase):
    def test_profile_uses_render_safe_svg_hero(self):
        source = README.read_text(encoding="utf-8")
        self.assertTrue(HERO.exists(), "profile hero SVG is missing")
        self.assertIn("./assets/branding/profile-hero.svg", source)
        self.assertNotIn("mojealterego-logo.webp", source)

    def test_every_local_readme_image_exists(self):
        source = README.read_text(encoding="utf-8")
        markdown_images = re.findall(r"!\[[^\]]*\]\((\./[^)]+)\)", source)
        html_images = re.findall(r'<img[^>]+src="(\./[^"]+)"', source)
        for relative in markdown_images + html_images:
            target = ROOT / relative.removeprefix("./")
            self.assertTrue(target.is_file(), f"README image does not exist: {relative}")

    def test_hero_svg_has_accessible_metadata(self):
        svg = HERO.read_text(encoding="utf-8")
        self.assertIn('role="img"', svg)
        self.assertIn("<title>", svg)
        self.assertIn("<desc>", svg)


if __name__ == "__main__":
    unittest.main()
