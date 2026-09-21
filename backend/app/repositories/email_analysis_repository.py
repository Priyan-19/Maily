from sqlalchemy.orm import Session

from app.models.email_analysis import EmailAnalysis
from app.schemas.analysis import EmailAnalysis as EmailAnalysisSchema


def get_analysis_by_email_id(
    db: Session,
    email_id: int,
) -> EmailAnalysis | None:

    return (
        db.query(EmailAnalysis)
        .filter(EmailAnalysis.email_id == email_id)
        .first()
    )


def create_analysis(
    db: Session,
    email_id: int,
    analysis: EmailAnalysisSchema,
) -> EmailAnalysis:

    db_analysis = EmailAnalysis(
        email_id=email_id,
        summary=analysis.summary,
        language=analysis.language,
        category=analysis.category,
        importance=analysis.importance,
        actions=analysis.actions,
        deadlines=analysis.deadlines,
    )

    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    return db_analysis


def save_analysis(
    db: Session,
    email_id: int,
    analysis: EmailAnalysisSchema,
) -> EmailAnalysis:

    existing = get_analysis_by_email_id(
        db=db,
        email_id=email_id,
    )

    if existing:
        existing.summary = analysis.summary
        existing.language = analysis.language
        existing.category = analysis.category
        existing.importance = analysis.importance
        existing.actions = analysis.actions
        existing.deadlines = analysis.deadlines

        db.commit()
        db.refresh(existing)

        return existing

    return create_analysis(
        db=db,
        email_id=email_id,
        analysis=analysis,
    )