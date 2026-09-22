from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.email import Email


def get_email_by_gmail_id(
    db: Session,
    email_account_id: int,
    gmail_message_id: str,
) -> Email | None:

    statement = select(Email).where(
        Email.email_account_id == email_account_id,
        Email.gmail_message_id == gmail_message_id,
    )

    return db.scalar(statement)


def create_email(
    db: Session,
    email_account_id: int,
    gmail_message_id: str,
    thread_id: str | None,
    sender: str,
    recipient: str,
    subject: str,
    snippet: str,
    body: str,
    received_at,
    is_read: bool,
) -> Email:

    email = Email(
        email_account_id=email_account_id,
        gmail_message_id=gmail_message_id,
        thread_id=thread_id,
        sender=sender,
        recipient=recipient,
        subject=subject,
        snippet=snippet,
        body=body,
        received_at=received_at,
        is_read=is_read,
    )

    db.add(email)
    db.commit()
    db.refresh(email)

    return email


def save_email(
    db: Session,
    email_account_id: int,
    gmail_message_id: str,
    thread_id: str | None,
    sender: str,
    recipient: str,
    subject: str,
    snippet: str,
    body: str,
    received_at,
    is_read: bool,
) -> Email:

    # Defensive formatting
    sender = (sender or "")[:2000]
    recipient = (recipient or "")[:4000]
    subject = (subject or "")[:2000]

    existing_email = get_email_by_gmail_id(
        db=db,
        email_account_id=email_account_id,
        gmail_message_id=gmail_message_id,
    )

    if existing_email:
        existing_email.thread_id = thread_id
        existing_email.sender = sender
        existing_email.recipient = recipient
        existing_email.subject = subject
        existing_email.snippet = snippet
        existing_email.body = body
        existing_email.received_at = received_at
        existing_email.is_read = is_read

        db.commit()
        db.refresh(existing_email)

        return existing_email

    return create_email(
        db=db,
        email_account_id=email_account_id,
        gmail_message_id=gmail_message_id,
        thread_id=thread_id,
        sender=sender,
        recipient=recipient,
        subject=subject,
        snippet=snippet,
        body=body,
        received_at=received_at,
        is_read=is_read,
    )
def get_emails(
    db: Session,
    email_account_id: int,
    limit: int = 20,
    offset: int = 0,
) -> list[Email]:

    statement = (
        select(Email)
        .where(
            Email.email_account_id == email_account_id
        )
        .order_by(
            Email.received_at.desc()
        )
        .limit(limit)
        .offset(offset)
    )

    return list(db.scalars(statement).all())