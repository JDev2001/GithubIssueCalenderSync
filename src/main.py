from config import REPOS, TASK_LIST_NAME
from github_client import GitHubClient
from google_tasks_client import GoogleTasksClient
from syncer import Syncer


def main() -> None:
    print("Fetching GitHub issues...")
    github = GitHubClient(repos=REPOS)
    issues = github.fetch_issues()
    print(f"Found {len(issues)} issue(s) across {len(REPOS)} repo(s)\n")

    print("Authenticating with Google Tasks...")
    tasks_client = GoogleTasksClient()
    tasklist_id = tasks_client.get_or_create_task_list(TASK_LIST_NAME)
    print(f"Task list: '{TASK_LIST_NAME}'\n")

    syncer = Syncer(tasks_client, tasklist_id)
    syncer.sync(issues)


if __name__ == "__main__":
    main()

