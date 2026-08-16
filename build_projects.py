#!/usr/bin/env python3
"""Regenerate projects.json from the public GitHub API.

Run before deploying, then commit the updated projects.json:
    python3 build_projects.py
"""
import json
import urllib.request

USER = "kerwinarlan"
# Not projects: junk repos, dupe renames, dotfiles, the site itself.
EXCLUDE = {
    "personal_website", "dotfiles", "random", "website", "wezterm",
    "engineering-comeback-2025", "manila-bay-storm-surge-thesis",
    "watch-alley", "budget-bot-skill", "watch-vault",
}

repos = json.load(urllib.request.urlopen(
    f"https://api.github.com/users/{USER}/repos?sort=updated&per_page=100"))

projects = [{
    "id": r["name"],
    "description": r["description"] or "",
    "url": r["html_url"],
    "homepage": r["homepage"] or "",
    "language": r["language"],
    "topics": r["topics"],
    "stars": r["stargazers_count"],
} for r in repos if not r["fork"] and r["name"] not in EXCLUDE]

with open("projects.json", "w") as f:
    json.dump(projects, f, indent=2)

print(f"Wrote {len(projects)} projects to projects.json")
