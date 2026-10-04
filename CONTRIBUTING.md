# Contributing

This is a personal profile and ecosystem-index repository. Changes should preserve the distinction between verified implementation, research, prototypes and concepts.

## Before opening a pull request

1. Keep project maturity aligned with `docs/PROJECT-STATUS.md`.
2. Do not manually edit content between the `PROJECT_CATALOG` markers in `README.md`; update `.github/project-catalog.json` or the generator instead.
3. Run:

   ```bash
   python -m compileall -q scripts tests
   python -m unittest discover -s tests -p 'test_*.py'
   python scripts/check_profile_a11y.py README.md
   ```

4. Keep documentation links valid and preserve meaningful alternative text for profile imagery.
5. Never commit API keys, access tokens, passwords or private personal data.

## Change policy

Behavioral changes to scripts require tests. Workflow changes should keep permissions at the minimum necessary scope. Project status promotion is always a manual decision backed by verifiable evidence.
