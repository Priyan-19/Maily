from sqlalchemy.orm import Session

from app.ai.analyzers.email_analyzer import analyze_email
from app.models.email_analysis import EmailAnalysis
from app.repositories.email_analysis_repository import save_analysis


def analyze_and_save_email(
    db: Session,
    email_id: int,
    force: bool = False,
) -> EmailAnalysis:

    from app.models.email import Email

    email = (
        db.query(Email)
        .filter(Email.id == email_id)
        .first()
    )

    if not email:
        raise ValueError("Email not found")

    target_language = "English"

    if email.email_account:
        from app.models.user_preference import UserPreference

        pref = (
            db.query(UserPreference)
            .filter(UserPreference.user_id == email.email_account.user_id)
            .first()
        )
        if pref and pref.language:
            target_language = pref.language

    # Return existing analysis if language matches and not forced
    if email.analysis and not force:
        existing_lang = (email.analysis.language or "").strip().lower()
        if existing_lang == target_language.strip().lower():
            return email.analysis

    analysis = analyze_email(
        subject=email.subject,
        sender=email.sender,
        body=email.body,
        target_language=target_language,
    )

    return save_analysis(
        db=db,
        email_id=email.id,
        analysis=analysis,
    )