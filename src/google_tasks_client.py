import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import GOOGLE_SCOPES

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"


class GoogleTasksClient:
    def __init__(self):
        self._service = self._authenticate()

    def _authenticate(self):
        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, GOOGLE_SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, GOOGLE_SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
        return build("tasks", "v1", credentials=creds)

    def get_or_create_task_list(self, name: str) -> str:
        result = self._service.tasklists().list(maxResults=100).execute()
        for task_list in result.get("items", []):
            if task_list["title"] == name:
                return task_list["id"]
        new_list = self._service.tasklists().insert(body={"title": name}).execute()
        print(f"Created task list: {name}")
        return new_list["id"]

    def get_all_tasks(self, tasklist_id: str) -> list[dict]:
        tasks: list[dict] = []
        page_token = None
        while True:
            result = self._service.tasks().list(
                tasklist=tasklist_id,
                showCompleted=True,
                showHidden=True,
                pageToken=page_token,
                maxResults=100,
            ).execute()
            tasks.extend(result.get("items", []))
            page_token = result.get("nextPageToken")
            if not page_token:
                break
        return tasks

    def complete_task(self, tasklist_id: str, task: dict) -> None:
        self._service.tasks().update(
            tasklist=tasklist_id,
            task=task["id"],
            body={**task, "status": "completed"},
        ).execute()

    def reopen_task(self, tasklist_id: str, task: dict) -> None:
        body = {**task, "status": "needsAction"}
        body.pop("completed", None)
        self._service.tasks().update(
            tasklist=tasklist_id,
            task=task["id"],
            body=body,
        ).execute()

    def insert_task(self, tasklist_id: str, body: dict) -> None:
        self._service.tasks().insert(tasklist=tasklist_id, body=body).execute()
