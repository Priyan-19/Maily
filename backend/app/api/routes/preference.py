from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db, SessionLocal
from app.models.user import User
from app.models.user_preference import UserPreference
from app.schemas.preference import UserPreferenceResponse, UserPreferenceUpdate

router = APIRouter(
    prefix="/api/settings",
    tags=["Settings"],
)


def _get_first_user(db: Session) -> User:
    user = db.scalar(select(User).order_by(User.id.desc()))
    if not user:
        raise HTTPException(
            status_code=404,
            detail="No user found. Please connect a Gmail account first.",
        )
    return user


def _reanalyze_recent_emails_in_background(user_id: int, target_language: str):
    db = SessionLocal()
    try:
        from app.models.email import Email
        from app.models.email_account import EmailAccount
        from app.services.analysis_service import analyze_and_save_email

        recent_emails = (
            db.query(Email)
            .join(EmailAccount, Email.email_account_id == EmailAccount.id)
            .filter(EmailAccount.user_id == user_id)
            .order_by(Email.received_at.desc())
            .limit(20)
            .all()
        )
        if not recent_emails:
            recent_emails = db.query(Email).order_by(Email.received_at.desc()).limit(20).all()

        for email in recent_emails:
            try:
                analyze_and_save_email(db=db, email_id=email.id, force=True)
            except Exception as exc:
                print(f"Background re-analysis error for email {email.id}: {exc}")
    finally:
        db.close()


@router.get("", response_model=UserPreferenceResponse)
def get_user_preferences(db: Session = Depends(get_db)):
    user = _get_first_user(db)

    pref = (
        db.query(UserPreference)
        .filter(UserPreference.user_id == user.id)
        .first()
    )

    if not pref:
        pref = UserPreference(
            user_id=user.id,
            language="Tanglish",
            digest_enabled=True,
            digest_time="08:00",
        )
        db.add(pref)
        db.commit()
        db.refresh(pref)

    return pref


@router.put("", response_model=UserPreferenceResponse)
def update_user_preferences(
    data: UserPreferenceUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    user = _get_first_user(db)

    pref = (
        db.query(UserPreference)
        .filter(UserPreference.user_id == user.id)
        .first()
    )

    if not pref:
        pref = UserPreference(
            user_id=user.id,
            language="Tanglish",
            digest_enabled=True,
            digest_time="08:00",
        )
        db.add(pref)

    lang_changed = False
    if data.language is not None and data.language != pref.language:
        pref.language = data.language
        lang_changed = True
    if data.digest_enabled is not None:
        pref.digest_enabled = data.digest_enabled
    if data.digest_time is not None:
        pref.digest_time = data.digest_time

    db.commit()
    db.refresh(pref)

    if lang_changed:
        background_tasks.add_task(_reanalyze_recent_emails_in_background, user.id, pref.language)

    return pref
