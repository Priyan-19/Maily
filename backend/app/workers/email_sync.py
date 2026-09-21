from app.core.database import SessionLocal
from app.models.email_account import EmailAccount
from app.services.email_service import sync_gmail_emails

from google.oauth2.credentials import Credentials


def run_email_sync(
    email_account_id: int,
    access_token: str,
    refresh_token: str | None,
    token_expiry=None,
):
    db = SessionLocal()

    try:

        account = (
            db.query(EmailAccount)
            .filter(
                EmailAccount.id == email_account_id
            )
            .first()
        )

        if not account:
            raise ValueError(
                "Email account not found"
            )

        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=None,
            client_secret=None,
            scopes=[
                "https://www.googleapis.com/auth/gmail.readonly"
            ],
        )

        emails, next_page_token = sync_gmail_emails(
            db=db,
            credentials=credentials,
            email_account_id=email_account_id,
            max_results=50,
        )

        print(
            f"Email sync completed: {len(emails)} emails"
        )

        return emails

    finally:
        db.close()