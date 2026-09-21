from datetime import date

from app.core.database import SessionLocal
from app.services.digest_service import generate_daily_digest


def run_daily_digest(
    user_id: int,
    digest_date: date | None = None,
):
    db = SessionLocal()

    try:

        digest = generate_daily_digest(
            db=db,
            user_id=user_id,
            digest_date=digest_date,
        )

        print(
            f"Daily digest generated for user {user_id}"
        )

        print(
            f"Total emails: {digest.total_emails}"
        )

        print(
            f"Important emails: {digest.important_emails}"
        )

        return digest

    finally:
        db.close()