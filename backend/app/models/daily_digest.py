from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DailyDigest(Base):
    __tablename__ = "daily_digests"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    digest_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    total_emails: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    important_emails: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    emails: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="daily_digests",
    )