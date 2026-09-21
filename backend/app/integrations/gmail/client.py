from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def create_gmail_client(credentials: Credentials):
    """
    Create a Gmail API service using OAuth credentials.
    """

    return build(
        "gmail",
        "v1",
        credentials=credentials,
        cache_discovery=False,
    )