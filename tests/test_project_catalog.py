import unittest
from scripts.update_project_catalog import render_catalog, replace_catalog

class ProjectCatalogTests(unittest.TestCase):
    def test_render_catalog_uses_live_metadata_and_preserves_declared_status(self):
        manifest = {"owner":"example","projects":[{"repo":"demo","domain":"AI","status":"PROTOTYPE","summary":"Fallback","language":"Python"}]}
        def resolver(owner, repo):
            return {"description":"Live description","language":"TypeScript","pushed_at":"2026-10-04T10:00:00Z","archived":False}
        rendered = render_catalog(manifest, resolver)
        tick = chr(96)
        self.assertIn(f"[{tick}demo{tick}](https://github.com/example/demo)", rendered)
        self.assertIn("PROTOTYPE", rendered)
        self.assertIn("TypeScript", rendered)
        self.assertIn("2026-10-04", rendered)

    def test_replace_catalog_only_replaces_generated_region(self):
        source = "before\n<!-- PROJECT_CATALOG:START -->\nold\n<!-- PROJECT_CATALOG:END -->\nafter\n"
        updated = replace_catalog(source, "new")
        self.assertEqual(updated, "before\n<!-- PROJECT_CATALOG:START -->\nnew\n<!-- PROJECT_CATALOG:END -->\nafter\n")

if __name__ == "__main__":
    unittest.main()
