from datetime import date, datetime, time, timezone, timedelta

from sqlalchemy.orm import Session

from app.models.daily_digest import DailyDigest
from app.models.email import Email

IST = timezone(timedelta(hours=5, minutes=30))


def generate_daily_digest(
    db: Session,
    user_id: int,
    digest_date: date | None = None,
) -> DailyDigest:

    if digest_date is None:
        digest_date = datetime.now(IST).date()

    # Fetch emails around the date range
    all_user_emails = (
        db.query(Email)
        .join(Email.email_account)
        .filter(Email.email_account.has(user_id=user_id))
        .filter(Email.received_at.isnot(None))
        .order_by(Email.received_at.desc())
        .all()
    )

    # Filter emails for digest_date matching year, month, day in IST (Indian Standard Time)
    emails = []
    for email in all_user_emails:
        if email.received_at:
            # Convert timestamp to IST
            if email.received_at.tzinfo is None:
                received_ist = email.received_at.replace(tzinfo=timezone.utc).astimezone(IST)
            else:
                received_ist = email.received_at.astimezone(IST)

            if received_ist.date() == digest_date:
                emails.append(email)

    digest_emails = []

    analyzed_count = 0
    for email in emails:
        # If email isn't analyzed yet, auto-analyze up to 3 per request
        if not email.analysis and analyzed_count < 3:
            try:
                analyzed_count += 1
                from app.services.analysis_service import analyze_and_save_email
                analyze_and_save_email(db=db, email_id=email.id)
                db.refresh(email)
            except Exception as e:
                print(f"Failed auto-analysis for email {email.id}: {e}")

        analysis = email.analysis

        digest_emails.append(
            {
                "email_id": email.id,
                "subject": email.subject or "(No Subject)",
                "sender": email.sender or "Unknown",
                "summary": analysis.summary if analysis else email.snippet or "",
                "category": analysis.category if analysis else "General",
                "importance": analysis.importance if analysis else "medium",
                "actions": (analysis.actions if analysis else []) or [],
                "deadlines": (analysis.deadlines if analysis else []) or [],
            }
        )

    important_emails = [
        email
        for email in digest_emails
        if email["importance"] == "high"
    ]

    existing = (
        db.query(DailyDigest)
        .filter(
            DailyDigest.user_id == user_id,
            DailyDigest.digest_date == digest_date,
        )
        .first()
    )

    if existing:

        existing.total_emails = len(digest_emails)

        existing.important_emails = len(
            important_emails
        )

        existing.emails = digest_emails

        db.commit()
        db.refresh(existing)

        return existing

    digest = DailyDigest(
        user_id=user_id,
        digest_date=digest_date,
        total_emails=len(digest_emails),
        important_emails=len(important_emails),
        emails=digest_emails,
    )

    db.add(digest)
    db.commit()
    db.refresh(digest)

    return digest