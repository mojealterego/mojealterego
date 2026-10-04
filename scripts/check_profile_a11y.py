#!/usr/bin/env python3
import sys
from html.parser import HTMLParser
from pathlib import Path

class ImageAltParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.missing = 0

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "img":
            return
        values = dict(attrs)
        if not (values.get("alt") or "").strip():
            self.missing += 1

def _heading_levels(text):
    levels = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if not stripped.startswith("#"):
            continue
        level = len(stripped) - len(stripped.lstrip("#"))
        if 1 <= level <= 6 and len(stripped) > level and stripped[level] == " ":
            levels.append(level)
    return levels

def _markdown_images_without_alt(text):
    missing = 0
    for line in text.splitlines():
        offset = 0
        while True:
            start = line.find("![", offset)
            if start < 0:
                break
            end = line.find("](", start + 2)
            if end >= 0 and not line[start + 2:end].strip():
                missing += 1
            offset = start + 2
    return missing

def audit_markdown(text):
    issues = []

    for _ in range(_markdown_images_without_alt(text)):
        issues.append("Markdown image is missing meaningful alt text.")

    parser = ImageAltParser()
    parser.feed(text)
    for _ in range(parser.missing):
        issues.append("HTML image is missing meaningful alt text.")

    levels = _heading_levels(text)
    if levels:
        if levels[0] != 1:
            issues.append("Heading hierarchy must start with a level-1 heading.")
        previous = levels[0]
        for level in levels[1:]:
            if level > previous + 1:
                issues.append(f"Heading hierarchy jumps from H{previous} to H{level}.")
            previous = level

    if sum(1 for level in levels if level == 1) > 1:
        issues.append("Profile README should contain a single level-1 heading.")

    return issues

def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "README.md")
    issues = audit_markdown(path.read_text(encoding="utf-8"))
    if issues:
        for issue in issues:
            print(f"::error::{issue}")
        return 1
    print("Profile accessibility static checks passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
