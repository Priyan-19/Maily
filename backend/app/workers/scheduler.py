from apscheduler.schedulers.background import BackgroundScheduler

from app.core.database import SessionLocal
from app.models.user import User
from app.workers.daily_digest import run_daily_digest


scheduler = BackgroundScheduler()


def _get_active_user_id() -> int:
    """Return the latest user_id (the real Gmail-connected user)."""
    db = SessionLocal()
    try:
        user = db.query(User).order_by(User.id.desc()).first()
        return user.id if user else 1
    finally:
        db.close()


def start_scheduler():
    try:
        user_id = _get_active_user_id()

        scheduler.add_job(
            run_daily_digest,
            "cron",
            hour=8,
            minute=0,
            args=[user_id],
            id="daily_digest",
            replace_existing=True,
        )

        scheduler.start()
        print("Maily scheduler started.")
    except Exception as exc:
        print(f"Maily scheduler deferred on startup: {exc}")


def stop_scheduler():

    if scheduler.running:
        scheduler.shutdown()