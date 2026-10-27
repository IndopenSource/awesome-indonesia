#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOS_FILE = ROOT / "repos.json"
REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def main():
    repos = json.loads(REPOS_FILE.read_text(encoding="utf-8"))
    if not isinstance(repos, list):
        raise SystemExit("repos.json must contain a JSON array.")

    seen = set()
    for index, repo in enumerate(repos, 1):
        if not isinstance(repo, str):
            raise SystemExit(f"Entry #{index} must be a string.")
        if not REPO_PATTERN.match(repo):
            raise SystemExit(f"Entry #{index} is not a valid owner/repo value: {repo}")

        normalized = repo.lower()
        if normalized in seen:
            raise SystemExit(f"Duplicate repository entry: {repo}")
        seen.add(normalized)

    # Alphabetical order keeps each addition in its own spot, so two PRs
    # rarely touch the same line of repos.json.
    for previous, repo in zip(repos, repos[1:]):
        if repo.lower() < previous.lower():
            raise SystemExit(
                f"repos.json must be in alphabetical order: put {repo} before {previous}."
            )

    print(f"Validated {len(repos)} repositories.")


if __name__ == "__main__":
    main()
