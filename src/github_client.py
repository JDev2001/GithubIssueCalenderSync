import json
import os
import shutil
import subprocess
from dataclasses import dataclass

from config import REPOS

_GH_FALLBACK_PATHS = [
    r"C:\Program Files\GitHub CLI\gh.exe",
    r"C:\Program Files (x86)\GitHub CLI\gh.exe",
]


def _find_gh() -> str:
    found = shutil.which("gh")
    if found:
        return found
    for path in _GH_FALLBACK_PATHS:
        if os.path.isfile(path):
            return path
    return "gh"


@dataclass
class Issue:
    number: int
    title: str
    url: str
    state: str
    repo: str

    @property
    def is_closed(self) -> bool:
        return self.state == "CLOSED"

    @property
    def task_title(self) -> str:
        return f"[{self.repo}] #{self.number}: {self.title}"


class GitHubClient:
    def __init__(self, repos: list[str] = REPOS):
        self.repos = repos

    def fetch_issues(self) -> list[Issue]:
        issues: list[Issue] = []
        for repo in self.repos:
            result = subprocess.run(
                [
                    _find_gh(), "issue", "list",
                    "-R", repo,
                    "--assignee", "@me",
                    "--state", "open",
                    "--limit", "200",
                    "--json", "number,title,url,state",
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(f"Error fetching issues from {repo}: {result.stderr.strip()}")
                continue
            for raw in json.loads(result.stdout):
                if raw["title"].lower().startswith("later:"):
                    continue
                issues.append(
                    Issue(
                        number=raw["number"],
                        title=raw["title"],
                        url=raw["url"],
                        state=raw["state"],
                        repo=repo,
                    )
                )
        return issues


if __name__ == "__main__":
    client = GitHubClient()
    for issue in client.fetch_issues():
        print(issue)