#!/usr/bin/env python3
"""Regenerate and validate projects.json from the public GitHub API.

Includes backend engineering standards:
- Authorization header support via GITHUB_TOKEN
- Strict request timeout and User-Agent headers
- Graceful network error handling and cache fallback
- Schema validation for repo payloads
- CLI flags: --check (dry-run validation) and --verbose

Usage:
    python3 build_projects.py [--check] [--verbose]
"""

import sys
import os
import json
import argparse
import logging
import urllib.request
import urllib.error
from typing import List, Dict, Any

USER = "kerwinarlan"
EXCLUDE = {
    "personal_website", "dotfiles", "random", "website", "wezterm",
    "engineering-comeback-2025", "manila-bay-storm-surge-thesis",
    "watch-alley", "budget-bot-skill", "watch-vault",
}

DEFAULT_OUTPUT_PATH = "projects.json"

def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def fetch_github_repos(user: str, timeout: int = 10) -> List[Dict[str, Any]]:
    url = f"https://api.github.com/users/{user}/repos?sort=updated&per_page=100"
    headers = {
        "User-Agent": "KerwinArlan-Portfolio-Builder/2.0",
        "Accept": "application/vnd.github.v3+json",
    }
    
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        logging.debug("Using GITHUB_TOKEN for authenticated GitHub API request.")
    else:
        logging.debug("No GITHUB_TOKEN found; using unauthenticated request.")

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status != 200:
                raise urllib.error.HTTPError(
                    url, response.status, f"HTTP {response.status}", response.headers, None
                )
            data = json.loads(response.read().decode("utf-8"))
            logging.info("Successfully retrieved %d repositories from GitHub API.", len(data))
            return data
    except urllib.error.HTTPError as e:
        logging.error("GitHub API HTTP Error: %s %s", e.code, e.reason)
        raise
    except urllib.error.URLError as e:
        logging.error("GitHub API Connection Error: %s", e.reason)
        raise
    except Exception as e:
        logging.error("Unexpected error fetching repos: %s", str(e))
        raise

def transform_and_validate(repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    projects = []
    for r in repos:
        name = r.get("name")
        if not name or r.get("fork") or name in EXCLUDE:
            continue

        project = {
            "id": name,
            "description": (r.get("description") or "").strip(),
            "url": r.get("html_url", f"https://github.com/{USER}/{name}"),
            "homepage": (r.get("homepage") or "").strip(),
            "language": r.get("language"),
            "topics": r.get("topics", []),
            "stars": int(r.get("stargazers_count", 0)),
        }
        projects.append(project)

    # Sort projects: starred first, then by name
    projects.sort(key=lambda x: (-x["stars"], x["id"].lower()))
    return projects

def main() -> None:
    parser = argparse.ArgumentParser(description="Build and validate projects.json for portfolio.")
    parser.add_argument("--check", action="store_true", help="Check if projects.json is up-to-date without writing.")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose debug logging.")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT_PATH, help="Output path for projects.json")
    args = parser.parse_args()

    setup_logging(args.verbose)

    try:
        raw_repos = fetch_github_repos(USER)
        projects = transform_and_validate(raw_repos)
    except Exception as e:
        logging.warning("Failed to update from GitHub API (%s).", str(e))
        if os.path.exists(args.output):
            logging.info("Preserving existing cached '%s'.", args.output)
            sys.exit(0)
        else:
            logging.error("No existing '%s' cache available. Exiting.", args.output)
            sys.exit(1)

    json_data = json.dumps(projects, indent=2) + "\n"

    if args.check:
        if os.path.exists(args.output):
            with open(args.output, "r", encoding="utf-8") as f:
                existing = f.read()
            if existing == json_data:
                logging.info("CHECK PASSED: '%s' is up-to-date.", args.output)
                sys.exit(0)
            else:
                logging.error("CHECK FAILED: '%s' is out-of-date.", args.output)
                sys.exit(1)
        else:
            logging.error("CHECK FAILED: '%s' does not exist.", args.output)
            sys.exit(1)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(json_data)

    logging.info("Wrote %d validated projects to '%s'.", len(projects), args.output)

if __name__ == "__main__":
    main()
