from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Email(Base):
    __tablename__ = "emails"

    __table_args__ = (
        UniqueConstraint(
            "email_account_id",
            "gmail_message_id",
            name="uq_email_account_gmail_message",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    email_account_id: Mapped[int] = mapped_column(
        ForeignKey("email_accounts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    gmail_message_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    thread_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    sender: Mapped[str] = mapped_column(
        String(500),
        default="",
    )

    recipient: Mapped[str] = mapped_column(
        String(500),
        default="",
    )

    subject: Mapped[str] = mapped_column(
        String(1000),
        default="",
    )

    snippet: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    body: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    received_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    email_account = relationship(
        "EmailAccount",
        back_populates="emails",
    )

    analysis = relationship(
        "EmailAnalysis",
        back_populates="email",
        uselist=False,
        cascade="all, delete-orphan",
    )