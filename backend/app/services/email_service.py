from sqlalchemy.orm import Session

from app.integrations.gmail.service import list_messages
from app.repositories.email_repository import save_email


def sync_gmail_emails(
    db: Session,
    credentials,
    email_account_id: int,
    max_results: int = 10,
    query: str | None = None,
):
    emails, next_page_token = list_messages(
        credentials=credentials,
        max_results=max_results,
        query=query,
    )

    saved_emails = []

    for email in emails:
        labels = email.labels or []
        # Skip promotional and social emails
        if "CATEGORY_PROMOTIONS" in labels or "CATEGORY_SOCIAL" in labels:
            continue

        is_read = "UNREAD" not in labels

        saved_email = save_email(
            db=db,
            email_account_id=email_account_id,
            gmail_message_id=email.id,
            thread_id=email.thread_id,
            sender=email.sender,
            recipient=email.recipient,
            subject=email.subject,
            snippet=email.snippet,
            body=email.body,
            received_at=email.received_at,
            is_read=is_read,
        )

        saved_emails.append(saved_email)

    return saved_emails, next_page_token