import unittest
from scripts.update_project_catalog import render_catalog, replace_catalog, validate_manifest

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

    def test_render_catalog_escapes_markdown_table_cells(self):
        manifest = {"owner":"example","projects":[{"repo":"demo","domain":"AI | Agents","status":"PROTOTYPE","summary":"Fallback","language":"Python"}]}
        def resolver(owner, repo):
            return {"description":"Line one | unsafe\nline two","language":"TypeScript","pushed_at":"2026-10-04T10:00:00Z","archived":False}
        rendered = render_catalog(manifest, resolver)
        self.assertIn("AI \\| Agents", rendered)
        self.assertIn("Line one \\| unsafe line two", rendered)

    def test_validate_manifest_rejects_unknown_status(self):
        manifest = {"owner":"example","projects":[{"repo":"demo","domain":"AI","status":"DONE","summary":"x"}]}
        with self.assertRaisesRegex(ValueError, "Unsupported project status"):
            validate_manifest(manifest)

    def test_validate_manifest_rejects_duplicate_repository(self):
        manifest = {
            "owner":"example",
            "projects":[
                {"repo":"demo","domain":"AI","status":"PROTOTYPE","summary":"x"},
                {"repo":"demo","domain":"Research","status":"RESEARCH","summary":"y"}
            ]
        }
        with self.assertRaisesRegex(ValueError, "Duplicate project repository"):
            validate_manifest(manifest)

    def test_replace_catalog_only_replaces_generated_region(self):
        source = "before\n<!-- PROJECT_CATALOG:START -->\nold\n<!-- PROJECT_CATALOG:END -->\nafter\n"
        updated = replace_catalog(source, "new")
        self.assertEqual(updated, "before\n<!-- PROJECT_CATALOG:START -->\nnew\n<!-- PROJECT_CATALOG:END -->\nafter\n")

if __name__ == "__main__":
    unittest.main()
