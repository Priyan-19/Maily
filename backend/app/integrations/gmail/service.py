import base64
from email.utils import parsedate_to_datetime

from google.oauth2.credentials import Credentials

from app.integrations.gmail.client import create_gmail_client
from app.schemas.email import EmailMessage


def _get_header(headers: list[dict], name: str) -> str:
    """
    Get a specific email header.
    """

    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")

    return ""


def _decode_body(data: str | None) -> str:
    """
    Decode Gmail's base64url encoded body.
    """

    if not data:
        return ""

    try:
        decoded = base64.urlsafe_b64decode(
            data.encode("UTF-8")
        )

        return decoded.decode(
            "utf-8",
            errors="replace",
        )

    except Exception:
        return ""


def _extract_body(payload: dict) -> str:
    """
    Extract plain-text body from a Gmail message.
    """

    mime_type = payload.get("mimeType", "")

    body_data = payload.get("body", {}).get("data")

    if mime_type == "text/plain" and body_data:
        return _decode_body(body_data)

    parts = payload.get("parts", [])

    for part in parts:
        part_body = _extract_body(part)

        if part_body:
            return part_body

    return ""


def _parse_message(message: dict) -> EmailMessage:
    """
    Convert Gmail API message into our EmailMessage schema.
    """

    payload = message.get("payload", {})

    headers = payload.get("headers", [])

    sender = _get_header(headers, "From")
    recipient = _get_header(headers, "To")
    subject = _get_header(headers, "Subject")
    date_value = _get_header(headers, "Date")

    received_at = None

    if date_value:
        try:
            received_at = parsedate_to_datetime(date_value)
        except (TypeError, ValueError):
            received_at = None

    body = _extract_body(payload)

    return EmailMessage(
        id=message.get("id", ""),
        thread_id=message.get("threadId"),
        sender=sender,
        recipient=recipient,
        subject=subject,
        snippet=message.get("snippet", ""),
        body=body,
        received_at=received_at,
        labels=message.get("labelIds", []),
    )


def list_messages(
    credentials: Credentials,
    max_results: int = 10,
    query: str | None = None,
) -> tuple[list[EmailMessage], str | None]:

    gmail = create_gmail_client(credentials)

    request_params = {
        "userId": "me",
        "maxResults": max_results,
    }

    if not query:
        query = "category:primary -category:promotions -category:social"

    request_params["q"] = query

    response = (
        gmail.users()
        .messages()
        .list(**request_params)
        .execute()
    )

    messages = response.get("messages", [])

    emails: list[EmailMessage] = []

    for message in messages:
        message_id = message["id"]

        full_message = (
            gmail.users()
            .messages()
            .get(
                userId="me",
                id=message_id,
                format="full",
            )
            .execute()
        )

        parsed_email = _parse_message(full_message)

        emails.append(parsed_email)

    return emails, response.get("nextPageToken")

def get_gmail_profile(credentials: Credentials) -> dict:
    gmail = create_gmail_client(credentials)

    return (
        gmail.users()
        .getProfile(userId="me")
        .execute()
    )


def create_draft_reply(
    credentials: Credentials,
    thread_id: str | None,
    to_email: str,
    subject: str,
    body_text: str,
) -> dict:
    from email.message import EmailMessage as MIMEEmailMessage

    gmail = create_gmail_client(credentials)

    mime_message = MIMEEmailMessage()
    mime_message.set_content(body_text)
    mime_message["To"] = to_email
    mime_message["Subject"] = subject if subject.startswith("Re:") else f"Re: {subject}"

    encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    if thread_id:
        create_message["threadId"] = thread_id

    draft = (
        gmail.users()
        .drafts()
        .create(
            userId="me",
            body={"message": create_message},
        )
        .execute()
    )

    return draft