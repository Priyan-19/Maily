from app.core.database import SessionLocal
from app.models.email import Email
from app.services.analysis_service import analyze_and_save_email


def run_email_analysis(
    email_id: int,
):
    db = SessionLocal()

    try:

        email = (
            db.query(Email)
            .filter(Email.id == email_id)
            .first()
        )

        if not email:
            raise ValueError(
                "Email not found"
            )

        analysis = analyze_and_save_email(
            db=db,
            email_id=email_id,
        )

        print(
            f"AI analysis completed for email {email_id}"
        )

        return analysis

    finally:
        db.close()