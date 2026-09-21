from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class EmailAnalysis(Base):
    __tablename__ = "email_analyses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    email_id: Mapped[int] = mapped_column(
        ForeignKey("emails.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    language: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="unknown",
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="other",
    )

    importance: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="low",
    )

    actions: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    deadlines: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    email = relationship(
        "Email",
        back_populates="analysis",
    )