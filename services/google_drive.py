# services/google_drive.py
from __future__ import annotations

import os
from typing import Optional, Tuple
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ---------------------------------------------------------------------
# --------------------------- CONFIG ---------------------------------
# ---------------------------------------------------------------------

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CREDENTIALS_FILE = os.getenv("GOOGLE_DRIVE_CREDENTIALS", "credentials.json")
TOKEN_FILE = os.getenv("GOOGLE_DRIVE_TOKEN", "token.json")


# ---------------------------------------------------------------------
# -------------------- AUTHENTICATION SETUP ---------------------------
# ---------------------------------------------------------------------

def _get_drive_service():
    """Load or refresh OAuth token and return Google Drive service."""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Google Drive credentials not found at {os.path.abspath(CREDENTIALS_FILE)}"
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


# ---------------------------------------------------------------------
# --------------------------- FILE HELPERS ----------------------------
# ---------------------------------------------------------------------

def _find_existing_file_id(service, name: str, folder_id: Optional[str]) -> Optional[str]:
    """Check if a file with the given name already exists inside the folder."""
    # Avoid f-string backslash issues by using simple concatenation
    query_parts = ["name = '" + name.replace("'", "\\'") + "'", "trashed = false"]
    if folder_id:
        query_parts.append(f"'{folder_id}' in parents")
    query = " and ".join(query_parts)

    res = service.files().list(q=query, fields="files(id,name)").execute()
    files = res.get("files", [])
    return files[0]["id"] if files else None


def get_or_create_folder(service, folder_name: str = "CDL Intake Data") -> str:
    """Find or create the folder in Drive, return its ID."""
    query = (
        "mimeType='application/vnd.google-apps.folder' "
        f"and name='{folder_name}' and trashed=false"
    )
    res = service.files().list(q=query, fields="files(id,name)").execute()
    folders = res.get("files", [])
    if folders:
        return folders[0]["id"]

    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    return folder["id"]


# ---------------------------------------------------------------------
# ------------------------- SYNC FUNCTION -----------------------------
# ---------------------------------------------------------------------

def sync_csv_to_drive(local_csv_path: str, remote_name: str = "entries.csv") -> Tuple[str, bool]:
    """
    Uploads or updates CSV to Google Drive inside 'CDL Intake Data' folder.
    Returns (file_id, created_flag)
    """
    service = _get_drive_service()
    folder_id = get_or_create_folder(service, "CDL Intake Data")

    file_id = _find_existing_file_id(service, remote_name, folder_id)
    media = MediaFileUpload(local_csv_path, mimetype="text/csv", resumable=False)

    if file_id:
        updated = service.files().update(fileId=file_id, media_body=media).execute()
        return updated["id"], False
    else:
        file_metadata = {"name": remote_name, "parents": [folder_id]}
        created = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        return created["id"], True
