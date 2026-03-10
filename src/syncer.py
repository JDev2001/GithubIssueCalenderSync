from github_client import Issue
from google_tasks_client import GoogleTasksClient


class Syncer:
    def __init__(self, tasks_client: GoogleTasksClient, tasklist_id: str):
        self._client = tasks_client
        self._tasklist_id = tasklist_id

    def _build_url_index(self, tasks: list[dict]) -> dict[str, dict]:
        """Map GitHub issue URL -> existing task for deduplication."""
        index: dict[str, dict] = {}
        for task in tasks:
            for line in task.get("notes", "").splitlines():
                line = line.strip()
                if line.startswith("https://github.com/"):
                    index[line] = task
                    break
        return index

    def sync(self, issues: list[Issue]) -> None:
        existing = self._client.get_all_tasks(self._tasklist_id)
        print(f"Found {len(existing)} existing task(s)")
        url_to_task = self._build_url_index(existing)

        added = updated = skipped = 0

        for issue in issues:
            title = issue.task_title
            if issue.url in url_to_task:
                task = url_to_task[issue.url]
                currently_completed = task.get("status") == "completed"
                if issue.is_closed and not currently_completed:
                    self._client.complete_task(self._tasklist_id, task)
                    print(f"  Completed : {title}")
                    updated += 1
                elif not issue.is_closed and currently_completed:
                    self._client.reopen_task(self._tasklist_id, task)
                    print(f"  Reopened  : {title}")
                    updated += 1
                else:
                    skipped += 1
            else:
                self._client.insert_task(
                    self._tasklist_id,
                    {
                        "title": title,
                        "notes": issue.url,
                        "status": "completed" if issue.is_closed else "needsAction",
                    },
                )
                print(f"  Added     : {title}")
                added += 1

        print(f"\nSync complete — added: {added}, updated: {updated}, unchanged: {skipped}")
