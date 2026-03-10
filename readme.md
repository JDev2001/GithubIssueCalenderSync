# GitHub Issue Calendar Sync

Syncs GitHub issues assigned to you from multiple repositories into a Google Tasks list called **🗓️ Reclaim**.

- Open issues are added as pending tasks.
- Closed issues are marked as completed.
- Reopened issues are un-completed automatically.
- Deduplication is handled via the issue URL stored in each task's notes.

## Project structure

```
main.py               # Entry point
config.py             # Repos, task list name, and Google auth constants
github_client.py      # GitHubClient — fetches issues via the gh CLI
google_tasks_client.py# GoogleTasksClient — wraps the Google Tasks REST API
syncer.py             # Syncer — reconciles issues with existing tasks
pyproject.toml        # uv / PEP 517 project file
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed (`pip install uv` or `winget install astral-sh.uv`)
- [GitHub CLI (`gh`)](https://cli.github.com/) installed and authenticated (`gh auth login`)
- A Google Cloud project with the **Tasks API** enabled

## Setup

### 1. Install dependencies

```powershell
uv sync
```

### 2. Enable the Google Tasks API and download credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/) and enable the **Tasks API** for your project.
2. Create an **OAuth 2.0 Client ID** (type: *Desktop app*) and download the JSON file.
3. Rename the downloaded file to `credentials.json` and place it in the project root.

On the first run the browser will open for the OAuth consent screen. After authorizing, a `token.json` file is created in the project root and reused for all subsequent runs.

> **Error 403: access_denied?** Your OAuth app is in *Testing* mode, so only explicitly approved accounts can sign in. Go to **Google Cloud Console → APIs & Services → OAuth consent screen → Test users** and add your Google account. Then try again.

### 3. Run

```powershell
uv run python main.py
```

## Source repositories tracked

```
gh issue list -R JDev2001/msc-thesis-eligibility-criteria --assignee "@me"
gh issue list -R Evuloc/backend --assignee "@me"
```

Add or remove entries in `config.py` → `REPOS` to change which repositories are synced.


