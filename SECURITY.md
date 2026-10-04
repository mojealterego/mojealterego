# Security policy

## Scope

This repository is a GitHub profile and ecosystem index. Its executable surface is limited to repository automation under `.github/workflows/` and Python tooling under `scripts/`.

## Reporting a vulnerability

Do not publish credentials, tokens, private data, exploit details, or other sensitive security information in a public issue.

Use GitHub private vulnerability reporting from the repository **Security** tab when that feature is available. If private reporting is unavailable, open a public issue containing only a request to establish a private contact channel; do not include sensitive technical details.

## Supported version

Security fixes target the current `main` branch. Historical profile revisions are not maintained as supported releases.

## Secrets

No long-lived credentials should be committed to this repository. GitHub Actions must use the minimum required permissions and short-lived `GITHUB_TOKEN` access wherever possible.
