from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import get_db
from app.models.daily_digest import DailyDigest
from app.models.user import User
from app.services.digest_service import generate_daily_digest


router = APIRouter(
    prefix="/api/digest",
    tags=["Digest"],
)


def _get_first_user(db: Session) -> User:
    """Return the Gmail-connected user (last created)."""
    user = db.scalar(select(User).order_by(User.id.desc()))
    if not user:
        user = User(
            email="priyan190406@gmail.com",
            name="Priyan",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        from app.models.user_preference import UserPreference
        pref = UserPreference(
            user_id=user.id,
            language="Tanglish",
            digest_enabled=True,
            digest_time="08:00",
        )
        db.add(pref)
        db.commit()
    return user


@router.post("/generate")
def generate_digest(
    digest_date: date | None = Query(
        default=None,
        description="Date to generate digest for (YYYY-MM-DD). Defaults to today.",
    ),
    db: Session = Depends(get_db),
):
    """Generate (or refresh) the daily digest for today's emails."""
    user = _get_first_user(db)

    try:
        from app.models.email import Email
        from app.models.email_account import EmailAccount
        from app.services.analysis_service import analyze_and_save_email

        # Force re-analysis of recent emails in user's preferred language
        recent_emails = (
            db.query(Email)
            .join(EmailAccount, Email.email_account_id == EmailAccount.id)
            .filter(EmailAccount.user_id == user.id)
            .order_by(Email.received_at.desc())
            .limit(20)
            .all()
        )
        if not recent_emails:
            recent_emails = db.query(Email).order_by(Email.received_at.desc()).limit(20).all()

        for email in recent_emails:
            try:
                analyze_and_save_email(db=db, email_id=email.id, force=True)
            except Exception as e:
                print(f"Refresh briefing re-analysis error for email {email.id}: {e}")

        digest = generate_daily_digest(
            db=db,
            user_id=user.id,
            digest_date=digest_date,
        )

        return {
            "id": digest.id,
            "user_id": digest.user_id,
            "digest_date": digest.digest_date.isoformat(),
            "total_emails": digest.total_emails,
            "important_emails": digest.important_emails,
            "emails": digest.emails,
            "created_at": digest.created_at.isoformat(),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate digest: {exc}",
        )


@router.get("/today")
def get_today_digest(
    db: Session = Depends(get_db),
):
    """Get today's digest if it exists, or generate one."""
    user = _get_first_user(db)

    today = date.today()

    existing = (
        db.query(DailyDigest)
        .filter(
            DailyDigest.user_id == user.id,
            DailyDigest.digest_date == today,
        )
        .first()
    )

    if not existing:
        # Auto-generate if not yet created
        existing = generate_daily_digest(
            db=db,
            user_id=user.id,
            digest_date=today,
        )

    return {
        "id": existing.id,
        "user_id": existing.user_id,
        "digest_date": existing.digest_date.isoformat(),
        "total_emails": existing.total_emails,
        "important_emails": existing.important_emails,
        "emails": existing.emails,
        "created_at": existing.created_at.isoformat(),
    }


@router.get("/briefing")
def get_executive_briefing(
    db: Session = Depends(get_db),
):
    """Return instant AI executive briefing, must-read items, unread stats, and last 20 emails context."""
    from app.models.email import Email
    from app.models.email_account import EmailAccount
    from app.models.user_preference import UserPreference

    user = _get_first_user(db)
    pref = db.query(UserPreference).filter(UserPreference.user_id == user.id).first()
    target_lang = pref.language if pref else "Tanglish"

    # Fetch last 20 emails
    recent_emails = (
        db.query(Email)
        .join(EmailAccount, Email.email_account_id == EmailAccount.id)
        .filter(EmailAccount.user_id == user.id)
        .order_by(Email.received_at.desc())
        .limit(20)
        .all()
    )

    if not recent_emails:
        recent_emails = (
            db.query(Email)
            .order_by(Email.received_at.desc())
            .limit(20)
            .all()
        )

    must_read = []
    unread_emails = []
    overview_list = []

    from app.services.analysis_service import analyze_and_save_email

    unanalyzed_count = 0
    for email in recent_emails:
        analysis = email.analysis
        if not analysis and unanalyzed_count < 3:
            try:
                unanalyzed_count += 1
                analysis = analyze_and_save_email(db=db, email_id=email.id)
                db.refresh(email)
            except Exception as e:
                print(f"Failed analysis for email {email.id}: {e}")

        # Skip promotional / marketing and social emails
        if analysis and analysis.category in ("marketing", "social"):
            continue

        item = {
            "id": email.id,
            "subject": email.subject or "(No Subject)",
            "sender": email.sender or "Unknown",
            "snippet": email.snippet,
            "received_at": email.received_at.isoformat() if email.received_at else None,
            "is_read": email.is_read,
            "importance": analysis.importance if analysis else "medium",
            "summary": analysis.summary if analysis else email.snippet or "",
            "actions": (analysis.actions if analysis else []) or [],
            "deadlines": (analysis.deadlines if analysis else []) or [],
        }

        overview_list.append(item)

        if not email.is_read:
            unread_emails.append(item)

        if analysis and (analysis.importance == "high" or len(analysis.actions or []) > 0):
            must_read.append(item)

    # Build Executive Summary Briefing Narrative
    total_recent = len(recent_emails)
    unread_count = len(unread_emails)
    must_read_count = len(must_read)

    if total_recent == 0:
        if target_lang == "Tanglish":
            briefing_text = "Innum emails sync aagala. Mela irukura 'Sync Gmail' button-a click panni ungal Primary emails-a fetch pannungangal!"
        elif target_lang == "Tamil":
            briefing_text = "இன்னும் மின்னஞ்சல்கள் ஒத்திசைக்கப்படவில்லை. மேலே உள்ள 'Sync Gmail' பொத்தானைக் கிளிக் செய்து மின்னஞ்சல்களைப் பெறவும்!"
        else:
            briefing_text = "No emails synced yet. Click 'Sync Gmail' above to fetch your Gmail Primary emails and AI briefing!"
    elif target_lang == "Tanglish":
        briefing_text = f"Inniku ungaluku total-a {total_recent} emails vandhirukku. Idhula {unread_count} unread emails irukku. Mukkiyama neenga paarkavendiya emails count: {must_read_count}."
    elif target_lang == "Tamil":
        briefing_text = f"இன்று உங்களுக்கு மொத்தம் {total_recent} மின்னஞ்சல்கள் வந்துள்ளன. இதில் {unread_count} படிக்கப்படாதவை. முக்கியமாக நீங்கள் கவனிக்க வேண்டியவை: {must_read_count}."
    else:
        briefing_text = f"You have {total_recent} recent emails. {unread_count} are unread, and {must_read_count} require your immediate attention."

    return {
        "user_language": target_lang,
        "total_recent": total_recent,
        "unread_count": unread_count,
        "must_read_count": must_read_count,
        "executive_briefing": briefing_text,
        "must_read_emails": must_read,
        "unread_emails": unread_emails,
        "last_20_emails": overview_list,
    }


@router.get("/{digest_date}")
def get_digest_by_date(
    digest_date: date,
    db: Session = Depends(get_db),
):
    """Get a digest for a specific date (YYYY-MM-DD)."""
    user = _get_first_user(db)

    digest = (
        db.query(DailyDigest)
        .filter(
            DailyDigest.user_id == user.id,
            DailyDigest.digest_date == digest_date,
        )
        .first()
    )

    if not digest:
        raise HTTPException(
            status_code=404,
            detail=f"No digest found for {digest_date}.",
        )

    return {
        "id": digest.id,
        "user_id": digest.user_id,
        "digest_date": digest.digest_date.isoformat(),
        "total_emails": digest.total_emails,
        "important_emails": digest.important_emails,
        "emails": digest.emails,
        "created_at": digest.created_at.isoformat(),
    }