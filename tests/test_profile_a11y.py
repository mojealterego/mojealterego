import unittest
from scripts.check_profile_a11y import audit_markdown

class AccessibilityTests(unittest.TestCase):
    def test_valid_profile_passes(self):
        text = "# Title\n\n## Section\n\n![Useful alt](image.svg)\n"
        self.assertEqual(audit_markdown(text), [])

    def test_missing_image_alt_fails(self):
        issues = audit_markdown("# Title\n\n![](image.svg)\n")
        self.assertTrue(any("alt" in issue.lower() for issue in issues))

    def test_heading_level_jump_fails(self):
        issues = audit_markdown("# Title\n\n### Jumped\n")
        self.assertTrue(any("heading" in issue.lower() for issue in issues))

if __name__ == "__main__":
    unittest.main()
