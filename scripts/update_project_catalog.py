#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

START = "<!-- PROJECT_CATALOG:START -->"
END = "<!-- PROJECT_CATALOG:END -->"

def fetch_repo(owner, repo, token=None):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "mojealterego-profile-catalog",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response)

def render_catalog(manifest, resolver):
    owner = manifest["owner"]
    rows = []
    for project in sorted(manifest["projects"], key=lambda p: (p.get("priority", 999), p["repo"].lower())):
        try:
            live = resolver(owner, project["repo"]) or {}
        except Exception:
            live = {}
        language = live.get("language") or project.get("language") or "—"
        pushed = live.get("pushed_at") or project.get("last_verified") or "—"
        if pushed != "—":
            pushed = pushed[:10]
        description = live.get("description") or project.get("summary") or "—"
        if live.get("archived"):
            description = f"{description} (archived)"
        tick = chr(96)
        repo_link = f"[{tick}{project['repo']}{tick}](https://github.com/{owner}/{project['repo']})"
        rows.append(f"| {repo_link} | {project['domain']} | **{project['status']}** | {language} | {pushed} | {description} |")
    header = "| Project | Domain | Status | Primary language | Last activity | Scope |\n|---|---|---|---|---|---|"
    return header + ("\n" + "\n".join(rows) if rows else "")

def replace_catalog(readme, rendered):
    if START not in readme or END not in readme:
        raise ValueError("README catalog markers are missing")
    before, rest = readme.split(START, 1)
    _, after = rest.split(END, 1)
    return f"{before}{START}\n{rendered}\n{END}{after}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=".github/project-catalog.json")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
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
