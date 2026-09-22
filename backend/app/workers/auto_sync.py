from app.core.database import SessionLocal
from app.models.email_account import EmailAccount
from app.services.email_service import sync_gmail_emails
from app.services.analysis_service import analyze_and_save_email
from google.oauth2.credentials import Credentials
from app.core.config import settings


def run_auto_sync():
    """Background worker to poll connected Gmail accounts every 3 minutes."""
    db = SessionLocal()
    try:
        accounts = db.query(EmailAccount).all()
        for account in accounts:
            try:
                credentials = Credentials(
                    token=account.access_token,
                    refresh_token=account.refresh_token,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=settings.google_client_id,
                    client_secret=settings.google_client_secret,
                    scopes=settings.scopes,
                )
                saved_emails, _ = sync_gmail_emails(
                    db=db,
                    credentials=credentials,
                    email_account_id=account.id,
                    max_results=10,
                )
                # Auto-analyze up to 5 unanalyzed emails
                for email in saved_emails[:5]:
                    if not email.analysis:
                        try:
                            analyze_and_save_email(db=db, email_id=email.id)
                        except Exception as e:
                            print(f"Auto-sync analysis error for email {email.id}: {e}")
                if len(saved_emails) > 0:
                    print(f"Auto-sync: fetched {len(saved_emails)} new emails for {account.email}")
            except Exception as e:
                print(f"Auto-sync skipped for account {account.id}: {e}")
    finally:
        db.close()
