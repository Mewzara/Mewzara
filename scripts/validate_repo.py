#!/usr/bin/env python3
"""Dependency-free checks for the profile README repository."""

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")

PROJECTS = [
    "raddraft-cxr-research-showcase",
    "mino-ai-assistant-showcase",
    "nura-reflection-assistant",
]

errors: list[str] = []

if "Abdulrahman Ali" not in README:
    errors.append("README must identify Abdulrahman Ali")
if "Computer Science Student and Responsible AI Builder" not in README:
    errors.append("README must include the approved role line")
if "I build responsible AI tools from idea to tested application" not in README:
    errors.append("README must include the approved introduction")

positions = [README.find(project) for project in PROJECTS]
if any(position < 0 for position in positions):
    errors.append("README must link all three approved featured projects")
elif positions != sorted(positions):
    errors.append("Featured projects must appear in the approved order")

featured = README.split("## Featured projects", 1)[-1].split("## How I work", 1)[0]
if len(re.findall(r"^### ", featured, flags=re.MULTILINE)) != 3:
    errors.append("Featured projects must contain exactly three entries")

for forbidden in ("patient data", "clinical decision support"):
    if forbidden.lower() in README.lower():
        errors.append(f"README contains prohibited phrase: {forbidden}")

for required in ("ASSET_PROVENANCE.md", "SECURITY.md", "LICENSE", "assets/profile-header.svg"):
    if not (ROOT / required).is_file():
        errors.append(f"Missing required file: {required}")

try:
    ET.parse(ROOT / "assets/profile-header.svg")
except (ET.ParseError, OSError) as exc:
    errors.append(f"Profile header is not valid SVG: {exc}")

tracked_candidates = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
for path in tracked_candidates:
    if path.name.startswith(".env") or path.suffix.lower() in {".pem", ".key", ".p12"}:
        errors.append(f"Potential secret-bearing file: {path.relative_to(ROOT)}")

if errors:
    print("Profile validation failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Profile validation passed: identity, three-project scope, ordering, assets, and safety checks are valid.")
