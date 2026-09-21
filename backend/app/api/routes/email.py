from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.email import Email
from app.models.email_account import EmailAccount

router = APIRouter(
    prefix="/api/emails",
    tags=["Emails"],
)


@router.get("")
def get_emails(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    emails = (
        db.query(Email)
        .join(Email.email_account)
        .order_by(Email.received_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    result = []

    for email in emails:
        analysis = email.analysis

        result.append(
            {
                "id": email.id,
                "gmail_message_id": email.gmail_message_id,
                "thread_id": email.thread_id,
                "sender": email.sender,
                "recipient": email.recipient,
                "subject": email.subject,
                "snippet": email.snippet,
                "body": email.body,
                "received_at": email.received_at,
                "is_read": email.is_read,
                "labels": [],
                "analysis": (
                    {
                        "id": analysis.id,
                        "summary": analysis.summary,
                        "language": analysis.language,
                        "category": analysis.category,
                        "importance": analysis.importance,
                        "actions": analysis.actions or [],
                        "deadlines": analysis.deadlines or [],
                    }
                    if analysis
                    else None
                ),
            }
        )

    return {
        "emails": result,
        "total": len(result),
        "limit": limit,
        "offset": offset,
    }


@router.post("/sync")
def sync_emails(
    db: Session = Depends(get_db),
):
    from app.models.email_account import EmailAccount
    from app.services.email_service import sync_gmail_emails
    from google.oauth2.credentials import Credentials

    account = (
        db.query(EmailAccount)
        .order_by(EmailAccount.id.desc())
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=401,
            detail="No Gmail account connected. Click 'Connect Gmail' to authenticate with Google OAuth.",
        )

    from app.core.config import settings

    credentials = Credentials(
        token=account.access_token,
        refresh_token=account.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        scopes=settings.scopes,
    )

    try:
        emails, next_page_token = sync_gmail_emails(
            db=db,
            credentials=credentials,
            email_account_id=account.id,
            max_results=50,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail=f"Gmail sync error: {exc}. Click 'Connect Gmail' to re-authenticate.",
        )

    return {
        "message": "Email sync completed.",
        "synced": len(emails),
        "next_page_token": next_page_token,
    }


@router.get("/{email_id}")
def get_email_by_id(
    email_id: int,
    db: Session = Depends(get_db),
):
    email = db.query(Email).filter(Email.id == email_id).first()

    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    analysis = email.analysis

    return {
        "id": email.id,
        "gmail_message_id": email.gmail_message_id,
        "thread_id": email.thread_id,
        "sender": email.sender,
        "recipient": email.recipient,
        "subject": email.subject,
        "snippet": email.snippet,
        "body": email.body,
        "received_at": email.received_at,
        "is_read": email.is_read,
        "analysis": (
            {
                "id": analysis.id,
                "summary": analysis.summary,
                "language": analysis.language,
                "category": analysis.category,
                "importance": analysis.importance,
                "actions": analysis.actions or [],
                "deadlines": analysis.deadlines or [],
            }
            if analysis
            else None
        ),
    }


@router.post("/{email_id}/suggest-reply")
def suggest_email_reply(
    email_id: int,
    instructions: str = "",
    db: Session = Depends(get_db),
):
    email = db.query(Email).filter(Email.id == email_id).first()

    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    from app.ai.analyzers.email_analyzer import generate_reply
    from app.models.user_preference import UserPreference

    target_language = "English"
    if email.email_account:
        pref = (
            db.query(UserPreference)
            .filter(UserPreference.user_id == email.email_account.user_id)
            .first()
        )
        if pref and pref.language:
            target_language = pref.language

    instructions_with_lang = f"Language: {target_language}. {instructions}".strip()

    reply_result = generate_reply(
        subject=email.subject,
        sender=email.sender,
        body=email.body,
        instructions=instructions_with_lang,
    )

    return {
        "email_id": email.id,
        "suggested_reply": reply_result.reply,
        "language": target_language,
    }


@router.post("/{email_id}/create-draft")
def create_gmail_draft(
    email_id: int,
    reply_body: str,
    db: Session = Depends(get_db),
):
    email = db.query(Email).filter(Email.id == email_id).first()

    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    account = email.email_account
    if not account:
        raise HTTPException(status_code=400, detail="No email account connected for this email")

    from google.oauth2.credentials import Credentials
    from app.integrations.gmail.service import create_draft_reply

    credentials = Credentials(
        token=account.access_token,
        refresh_token=account.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/gmail.compose"],
    )

    try:
        draft = create_draft_reply(
            credentials=credentials,
            thread_id=email.thread_id,
            to_email=email.sender,
            subject=email.subject,
            body_text=reply_body,
        )

        return {
            "message": "Gmail draft created successfully!",
            "draft_id": draft.get("id"),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to create draft: {exc}")


@router.delete("/clear-all")
def clear_all_emails(
    db: Session = Depends(get_db),
):
    from app.models.daily_digest import DailyDigest
    from app.models.email_analysis import EmailAnalysis

    db.query(DailyDigest).delete()
    db.query(EmailAnalysis).delete()
    db.query(Email).delete()
    db.commit()

    return {"message": "All stored emails and analysis data deleted successfully."}