from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class EmailAccount(Base):
    __tablename__ = "email_accounts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    provider: Mapped[str] = mapped_column(
        String(50),
        default="google",
        nullable=False,
    )

    email_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    access_token: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    refresh_token: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    token_expiry: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="email_accounts",
    )

    emails = relationship(
        "Email",
        back_populates="email_account",
        cascade="all, delete-orphan",
    )