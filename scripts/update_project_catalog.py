#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

START = "<!-- PROJECT_CATALOG:START -->"
END = "<!-- PROJECT_CATALOG:END -->"
ALLOWED_STATUSES = {"PRODUCTION", "BETA", "PROTOTYPE", "RESEARCH", "CONCEPT"}
REPOSITORY_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


def _require_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def validate_manifest(manifest):
    if not isinstance(manifest, dict):
        raise ValueError("Manifest must be a JSON object")

    owner = _require_text(manifest.get("owner"), "owner")
    if not REPOSITORY_NAME.fullmatch(owner):
        raise ValueError("owner contains unsupported characters")

    projects = manifest.get("projects")
    if not isinstance(projects, list):
        raise ValueError("projects must be a list")

    seen_repositories = set()
    for index, project in enumerate(projects):
        if not isinstance(project, dict):
            raise ValueError(f"projects[{index}] must be an object")

        repo = _require_text(project.get("repo"), f"projects[{index}].repo")
        if not REPOSITORY_NAME.fullmatch(repo):
            raise ValueError(f"Repository name contains unsupported characters: {repo}")
        key = repo.casefold()
        if key in seen_repositories:
            raise ValueError(f"Duplicate project repository: {repo}")
        seen_repositories.add(key)

        _require_text(project.get("domain"), f"projects[{index}].domain")
        status = _require_text(project.get("status"), f"projects[{index}].status")
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"Unsupported project status: {status}")

        priority = project.get("priority", 999)
        if not isinstance(priority, int) or isinstance(priority, bool) or priority < 0:
            raise ValueError(f"projects[{index}].priority must be a non-negative integer")

    return manifest


def _markdown_cell(value):
    text = str(value if value is not None else "—")
    text = " ".join(text.replace("\r", "\n").splitlines())
    text = text.replace("\\", "\\\\").replace("|", "\\|")
    return text.strip() or "—"


def fetch_repo(owner, repo, token=None):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}",
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "mojealterego-profile-catalog",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response)


def render_catalog(manifest, resolver):
    validate_manifest(manifest)
    owner = manifest["owner"]
    rows = []

    for project in sorted(
        manifest["projects"],
        key=lambda p: (p.get("priority", 999), p["repo"].lower()),
    ):
        try:
            live = resolver(owner, project["repo"]) or {}
        except Exception:
            live = {}

        if not isinstance(live, dict):
            live = {}

        language = live.get("language") or project.get("language") or "—"
        pushed = live.get("pushed_at") or project.get("last_verified") or "—"
        if pushed != "—":
            pushed = str(pushed)[:10]

        description = live.get("description") or project.get("summary") or "—"
        if live.get("archived"):
            description = f"{description} (archived)"

        tick = chr(96)
        repo_link = f"[{tick}{project['repo']}{tick}](https://github.com/{owner}/{project['repo']})"
        rows.append(
            "| "
            + " | ".join(
                [
                    repo_link,
                    _markdown_cell(project["domain"]),
                    f"**{_markdown_cell(project['status'])}**",
                    _markdown_cell(language),
                    _markdown_cell(pushed),
                    _markdown_cell(description),
                ]
            )
            + " |"
        )

    header = (
        "| Project | Domain | Status | Primary language | Last activity | Scope |\n"
        "|---|---|---|---|---|---|"
    )
    return header + ("\n" + "\n".join(rows) if rows else "")


def replace_catalog(readme, rendered):
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one project catalog marker pair")

    before, rest = readme.split(START, 1)
    generated, after = rest.split(END, 1)
    if END in generated:
        raise ValueError("README project catalog markers are malformed")

    return f"{before}{START}\n{rendered}\n{END}{after}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=".github/project-catalog.json")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    validate_manifest(manifest)

    token = os.getenv("GITHUB_TOKEN")
    resolver = lambda owner, repo: fetch_repo(owner, repo, token)

    readme_path = Path(args.readme)
    current = readme_path.read_text(encoding="utf-8")
    updated = replace_catalog(current, render_catalog(manifest, resolver))

    if args.check:
        if updated != current:
            print("README project catalog is stale.", file=sys.stderr)
            return 1
        print("README project catalog is current.")
        return 0

    if updated != current:
        readme_path.write_text(updated, encoding="utf-8")
        print("README project catalog updated.")
    else:
        print("README project catalog already current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
