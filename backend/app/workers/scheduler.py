from apscheduler.schedulers.background import BackgroundScheduler

from app.core.database import SessionLocal
from app.models.user import User
from app.workers.daily_digest import run_daily_digest
from app.workers.auto_sync import run_auto_sync


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

        # Automatic Gmail Polling every 3 minutes
        scheduler.add_job(
            run_auto_sync,
            "interval",
            minutes=3,
            id="auto_sync",
            replace_existing=True,
        )

        # Daily Digest generation at 8:00 AM
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
        print("Maily scheduler started (Auto-Sync: 3 mins, Daily Digest: 8 AM).")
    except Exception as exc:
        print(f"Maily scheduler deferred on startup: {exc}")


def stop_scheduler():

    if scheduler.running:
        scheduler.shutdown()